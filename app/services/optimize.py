from sqlalchemy.orm import Session
from kfp import dsl

from app.config.enums import SupportOptimize
from app.core.db.connect import SessionDepends
from app.core.db.models.model_task import ModelTask
from app.core.settings import get_settings
from app.utils.kfp_client_manager import KFPClientManager
from app.utils.uuid import get_uuid_str
from app.schemas.services.types import OptimizationSetUp
from app.schemas.requests.optimize import ReqOptimizeWithNameAndArgsBody

SETTINGS = get_settings()


def get_optimize_service(db: Session = SessionDepends):
    """
    최적화 서비스 레이어 의존성 주입을 위한 함수
    Args:
        db: 데이터베이스 세션 의존성
    Returns:
        OptimizeService: 최적화 서비스 레이어 인스턴스
    """
    return OptimizeService(db=db)


class OptimizeService:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def run_optimize_task(db: Session, task_info: OptimizationSetUp):
        """
        최적화 작업 실행
        Args:
            db: 데이터베이스 세션
            task_info: 최적화 작업 정보
        Returns:
            task_info: 최적화 작업 정보
        """
        
        @dsl.container_component
        # 사용할 컨테이너 정의 및 설정 추가
        def lite_model_component():
            return dsl.ContainerSpec(
                # 사용할 도커이미지의 주소 및 태그
                image=task_info.docker_image_path,
                # 실행할 커맨드
                command=task_info.command,
                # 필요한 변수들 정의 (string으로 정의)
                args=task_info.args,
            )

        # 파이프라인 정의
        @dsl.pipeline(name=f"{task_info.model_name}_{task_info.optimize_name}")
        def lite_model():
            lite_model_task = lite_model_component()

            if task_info.accelerator_type != "cpu":
                accelerator_type: str = task_info.accelerator_type
                lite_model_task.set_accelerator_limit(1)  # container_spec.resources.accelerator_limit
                lite_model_task.container_spec.resources.accelerator_type = accelerator_type

            # 환경변수 설정
            for key, value in task_info.env.items():
                lite_model_task.set_env_variable(key, value)

        # 정의된 함수로 파이프라인 생성

        kfp_client = KFPClientManager().get_kfp_client()

        run = kfp_client.create_run_from_pipeline_func(
            experiment_name="aipaas-lite-model-workflow",
            pipeline_func=lite_model,
            namespace=SETTINGS.KUBEFLOW_NAMESPACE,
        )

        # return run
        # 이하 리팩토링 필요
        kubeflow_experiment_id = run.run_id
        uuid_str = task_info.env["SERVER_UUID"]

        new_task = ModelTask(
            task_uuid=uuid_str,
            model_name=task_info.model_name,
            task_type=task_info.optimize_name,
            kubeflow_experiment_id=kubeflow_experiment_id,
        )

        db.add(new_task)
        db.commit()

        return {"task_uuid": uuid_str, "kubeflow_experiment_id": kubeflow_experiment_id}

    def pruning(self, optimize_form: ReqOptimizeWithNameAndArgsBody):
        """
        Pruning 경량화 작업
        Args:
            optimize_form: 경량화 폼
        Returns:
            task_info: 경량화 작업 정보
        """
        container_image: str = SETTINGS.PRUNING_IMG # 변경 필요
        
        task_info = OptimizationSetUp(
            model_name=optimize_form.model_name,
            optimize_name=SupportOptimize.PRUNING.value,
            docker_image_path=container_image,
            command=[
                "pipenv",
                "run",
                "python",
                "main.py",
            ],
            args=[f"--{key} {value}" for key, value in optimize_form.args.items()],
            env={
                "AWS_ACCESS_KEY_ID": SETTINGS.AWS_ACCESS_KEY_ID,
                "AWS_SECRET_ACCESS_KEY": SETTINGS.AWS_SECRET_ACCESS_KEY,
                "MLFLOW_TRACKING_URI": SETTINGS.MLFLOW_TRACKING_URL,
                "MLFLOW_S3_ENDPOINT_URL": SETTINGS.MLFLOW_S3_ENDPOINT_URL,
                "MLFLOW_HTTP_REQUEST_TIMEOUT": SETTINGS.MLFLOW_HTTP_REQUEST_TIMEOUT,
                "SERVER_UUID": get_uuid_str(),
                "SERVER_PATH": f"{SETTINGS.SERVER_URL}/api/v1/tasks",
                "RUN_ID": optimize_form.saved_model_run_id,
                "MODEL_PATH": optimize_form.saved_model_path,
                "MODEL_NAME": optimize_form.model_name,
            },
            accelerator_type="cpu",
        )

        result = self.run_optimize_task(self.db, task_info)

        return result

    def tensorrt(self, optimize_form: ReqOptimizeWithNameAndArgsBody):
        """
        TensorRT 최적화 작업
        Args:
            optimize_form: 최적화 폼
        Returns:
            task_info: 최적화 작업 정보
        """

        # 사용할 도커 이미지 경로
        container_image: str = SETTINGS.TENSORRT_IMG # 변경 필요

        # 최적화 작업 정보
        task_info = OptimizationSetUp(
            model_name=optimize_form.model_name,
            optimize_name=SupportOptimize.TENSORRT.value,
            docker_image_path=container_image,
            command=[
                "pipenv",
                "run",
                "python",
                "main.py",
            ],
            args=[f"--{key} {value}" for key, value in optimize_form.args.items()],
            env={
                "AWS_ACCESS_KEY_ID": SETTINGS.AWS_ACCESS_KEY_ID,
                "AWS_SECRET_ACCESS_KEY": SETTINGS.AWS_SECRET_ACCESS_KEY,
                "MLFLOW_TRACKING_URI": SETTINGS.MLFLOW_TRACKING_URL,
                "MLFLOW_S3_ENDPOINT_URL": SETTINGS.MLFLOW_S3_ENDPOINT_URL,
                "MLFLOW_HTTP_REQUEST_TIMEOUT": SETTINGS.MLFLOW_HTTP_REQUEST_TIMEOUT,
                "SERVER_UUID": get_uuid_str(),
                "SERVER_PATH": f"{SETTINGS.SERVER_URL}/api/v1/tasks",
                "RUN_ID": optimize_form.saved_model_run_id,
                "MODEL_PATH": optimize_form.saved_model_path,
                "MODEL_NAME": optimize_form.model_name,
            },
            accelerator_type="nvidia.com/gpu",
        )

        result = self.run_optimize_task(self.db, task_info)

        return result

    def openvino(self, optimize_form: ReqOptimizeWithNameAndArgsBody):
        """
        OpenVINO 최적화 작업
        Args:
            optimize_form: 최적화 폼
        Returns:
            task_info: 최적화 작업 정보
        """

        # 사용할 도커 이미지 경로
        container_image: str = SETTINGS.OPENVINO_IMG # 변경 필요

        # 최적화 작업 정보
        task_info = OptimizationSetUp(
            model_name=optimize_form.model_name,
            optimize_name=SupportOptimize.OPENVINO.value,
            docker_image_path=container_image,
            command=[
                "pipenv",
                "run",
                "python",
                "main.py",
            ],
            args=[f"--{key} {value}" for key, value in optimize_form.args.items()],
            env={
                "AWS_ACCESS_KEY_ID": SETTINGS.AWS_ACCESS_KEY_ID,
                "AWS_SECRET_ACCESS_KEY": SETTINGS.AWS_SECRET_ACCESS_KEY,
                "MLFLOW_TRACKING_URI": SETTINGS.MLFLOW_TRACKING_URL,
                "MLFLOW_S3_ENDPOINT_URL": SETTINGS.MLFLOW_S3_ENDPOINT_URL,
                "MLFLOW_HTTP_REQUEST_TIMEOUT": SETTINGS.MLFLOW_HTTP_REQUEST_TIMEOUT,
                "SERVER_UUID": get_uuid_str(),
                "SERVER_PATH": f"{SETTINGS.SERVER_URL}/api/v1/tasks",
                "RUN_ID": optimize_form.saved_model_run_id,
                "MODEL_PATH": optimize_form.saved_model_path,
                "MODEL_NAME": optimize_form.model_name,
            },
            accelerator_type="cpu",
        )

        result = self.run_optimize_task(self.db, task_info)

        return result

    def sklearn_onnx(self, optimize_form: ReqOptimizeWithNameAndArgsBody):
        """
        sklearn-onnx 최적화 작업
        Args:
            optimize_form: 최적화 폼
        Returns:
            task_info: 최적화 작업 정보
        """

        # 사용할 도커 이미지 경로
        container_image: str = SETTINGS.SKLEARN_ONNX_IMG # 변경 필요

        # 최적화 작업 정보
        task_info = OptimizationSetUp(
            model_name=optimize_form.model_name,
            optimize_name=SupportOptimize.SKLEARN_ONNX.value,
            docker_image_path=container_image,
            command=[
                "pipenv",
                "run",
                "python",
                "main.py",
            ],
            args=[f"--{key} {value}" for key, value in optimize_form.args.items()],
            env={
                "AWS_ACCESS_KEY_ID": SETTINGS.AWS_ACCESS_KEY_ID,
                "AWS_SECRET_ACCESS_KEY": SETTINGS.AWS_SECRET_ACCESS_KEY,
                "MLFLOW_TRACKING_URI": SETTINGS.MLFLOW_TRACKING_URL,
                "MLFLOW_S3_ENDPOINT_URL": SETTINGS.MLFLOW_S3_ENDPOINT_URL,
                "MLFLOW_HTTP_REQUEST_TIMEOUT": SETTINGS.MLFLOW_HTTP_REQUEST_TIMEOUT,
                "SERVER_UUID": get_uuid_str(),
                "SERVER_PATH": f"{SETTINGS.SERVER_URL}/api/v1/tasks",
                "RUN_ID": optimize_form.saved_model_run_id,
                "MODEL_PATH": optimize_form.saved_model_path,
                "MODEL_NAME": optimize_form.model_name,
            },
            accelerator_type="cpu",
        )

        result = self.run_optimize_task(self.db, task_info)

        return result
