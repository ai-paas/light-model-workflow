from uuid import uuid4

from kfp import dsl
from sqlalchemy.orm import Session


from app.config.enums import ModelLiteMapper, SupportModel, SupportOptimize
from app.core.db.models.model_task import ModelTask
from app.core.settings import get_settings
from app.schemas.requests import model
from app.schemas.requests.model import ReqBertTRTForm
from app.services.types import OptimizationTaskInfo
from app.utils.kfp_client_manager import KFPClientManager

SETTINGS = get_settings()


def get_model_service():
    return ModelService()


class ModelService:
    @staticmethod
    def run_optimize_task(db: Session, task_info: OptimizationTaskInfo):
        docker_image_path = task_info.docker_image_path.value
        # 작업 완료시 server에 요청을 보낼 url
        response_server_url = SETTINGS.SERVER_URL

        uuidV4 = uuid4()
        uuid_str = str(uuidV4)

        @dsl.container_component
        # 사용할 컨테이너 정의 및 설정 추가
        def lite_model_component():
            return dsl.ContainerSpec(
                # 사용할 도커이미지의 주소 및 태그
                image=docker_image_path,
                # 실행할 커맨드
                command=task_info.command,
                # 필요한 변수들 정의 (string으로 정의)
                args=task_info.args
                + [
                    "--model_name",
                    task_info.model_name,
                    "--mlflow_tracking_url",
                    SETTINGS.MLFLOW_TRACKING_URL,
                    "--mlflow_s3_endpoint_url",
                    SETTINGS.MLFLOW_S3_ENDPOINT_URL,
                    "--server_uuid",
                    uuid_str,
                    "--server_path",
                    f"{response_server_url}/api/v1/tasks",
                    "--aws_access_key_id",
                    SETTINGS.AWS_ACCESS_KEY_ID,
                    "--aws_secret_access_key",
                    SETTINGS.AWS_SECRET_ACCESS_KEY,
                ],
            )

        # 파이프라인 정의
        @dsl.pipeline(name=f"{task_info.model_name}_{task_info.optimize_name}")
        def lite_model():
            lite_model_task = lite_model_component()
            # todo : gpu 작업을 구분햐여 해당 작업에만 가속기 설정
            accelerator_type: str = "nvidia.com/gpu"
            lite_model_task.set_accelerator_limit(1)  # container_spec.resources.accelerator_limit
            lite_model_task.container_spec.resources.accelerator_type = accelerator_type

        # 정의된 함수로 파이프라인 생성

        kfp_client = KFPClientManager().get_kfp_client()

        run = kfp_client.create_run_from_pipeline_func(
            experiment_name="aipaas-lite-model-workflow",
            pipeline_func=lite_model,
            namespace=SETTINGS.KUBEFLOW_NAMESPACE,
        )

        kubeflow_experiment_id = run.run_id

        new_task = ModelTask(
            task_uuid=uuid_str,
            model_name=task_info.model_name,
            task_type=task_info.optimize_name,
            kubeflow_experiment_id=kubeflow_experiment_id,
        )

        db.add(new_task)
        db.commit()

        return {"task_uuid": uuid_str, "kubeflow_experiment_id": kubeflow_experiment_id}

    def bert_trt(
        self,
        db: Session,
        model_name: SupportModel,
        optimize_name: SupportOptimize,
        optimize_form: ReqBertTRTForm,
    ) -> dict[str, any]:
        """
        trt를 적용한 모델 경량화
        """

        task_info = OptimizationTaskInfo(
            model_name=model_name,
            optimize_name=optimize_name,
            docker_image_path=ModelLiteMapper.BERT_TRT.value,
            command=[
                "pipenv",
                "run",
                "python",
                "main.py",
            ],
            args=[
                "--model_run_id",
                optimize_form.saved_model_run_id,
                "--model_path",
                optimize_form.saved_model_path,
            ],
        )

        return self.run_optimize_task(db, task_info)

    def bert_openvino(
        self,
        db: Session,
        model_name: SupportModel,
        optimize_name: SupportOptimize,
        optimize_form: model.ReqBertOpenvinoForm,
    ) -> dict[str, any]:
        """
        openvino를 적용한 모델 경량화
        """

        task_info = OptimizationTaskInfo(
            model_name=model_name,
            optimize_name=optimize_name,
            docker_image_path=ModelLiteMapper.BERT_OPENVINO.value,
            command=[
                "pipenv",
                "run",
                "python",
                "main.py",
            ],
            args=[
                "--model_run_id",
                optimize_form.saved_model_run_id,
                "--model_path",
                optimize_form.saved_model_path,
            ],
        )

        return self.run_optimize_task(db, task_info)

    def owlv2_ptq(
        self,
        db: Session,
        model_name: SupportModel,
        optimize_name: SupportOptimize,
        optimize_form: model.ReqOwlV2PTQForm,
    ) -> dict[str, any]:
        """
        ptq를 적용한 모델 경량화
        """

        quantization_layers_str = ",".join(optimize_form.quantization_layers)

        task_info = OptimizationTaskInfo(
            model_name=model_name,
            optimize_name=optimize_name,
            docker_image_path=ModelLiteMapper.OWLV2_PTQ.value,
            command=[
                "pipenv",
                "run",
                "python",
                "main.py",
            ],
            args=[
                "--quantization_layers",
                quantization_layers_str,
                "--model_run_id",
                optimize_form.saved_model_run_id,
                "--model_path",
                optimize_form.saved_model_path,
            ],
        )

        return self.run_optimize_task(db, task_info)

    def detr_resnet50(
        self,
        db: Session,
        model_name: SupportModel,
        optimize_name: SupportOptimize,
        optimize_form: model.ReqDetrResnetForm,
    ) -> dict[str, any]:
        """
        DETR Resnet50 모델에 대한 최적화/경량화
        """

        task_info = OptimizationTaskInfo(
            model_name=model_name,
            optimize_name=optimize_name,
            docker_image_path=ModelLiteMapper.DETR_Resnet50.value,
            command=[
                "pipenv",
                "run",
                "python",
                "main.py",
            ],
            args=[
                "--model_run_id",
                optimize_form.saved_model_run_id,
                "--model_path",
                optimize_form.saved_model_path,
                # 모델 다운로드에 시간이 많이 소요되므로 설정값(기본값 120초) 조정 필요
                "--mlflow_http_request_timeout",
                SETTINGS.MLFLOW_HTTP_REQUEST_TIMEOUT,
            ],
        )

        return self.run_optimize_task(db, task_info)
