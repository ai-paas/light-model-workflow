from sqlalchemy import select

from app.core.db.models.model_task import ModelTask
from app.core.db.session import SessionLocal
from app.core.db.connect import SessionDepends
from app.schemas.requests.task import PatchTaskForm, ReqModelTaskForm
from app.schemas.services.model_task import ModelTaskSchema
from app.utils.uuid import str_to_uuid4


class ModelTaskRepository:
    def __init__(self, db: SessionLocal):
        self.db = db

    def create_model_task(self, model_task: ModelTask):
        """
        Create model task

        - 모델 저장 요청시 생성

        Args:
            model_task: ModelTask
        Returns:
            ModelTask
        """
        self.db.add(model_task)
        self.db.commit()
        self.db.refresh(model_task)
        return model_task

    def insert_model_task(self, model_task_schema: ModelTaskSchema) -> ModelTaskSchema:
        """
        Create model task

        - 모델 저장 요청시 생성

        Args:
            model_task: ModelTask
        Returns:
            ModelTask
        """
        model_task = ModelTask.from_schema(model_task_schema)
        self.db.add(model_task)
        self.db.commit()
        self.db.refresh(model_task)
        return model_task.to_schema()

    def get_task_by_uuid(self, task_uuid: str) -> ModelTaskSchema:
        """
        task uuid로 조회
        """
        uuid = str_to_uuid4(task_uuid)
        statement = select(ModelTask).where(ModelTask.task_uuid == uuid).limit(1)
        result = self.db.execute(statement).scalar_one_or_none()
        return result.to_schema() if result else None

    def get_tasks(self, form: ReqModelTaskForm) -> list[ModelTaskSchema]:
        """
        최적화/경량화 작업 요청 기록
        """
        statement = select(ModelTask)
        statement = statement.where(ModelTask.model_name.ilike(f"%{form.model_name_query}%")) if form.model_name_query else statement
        statement = statement.where(ModelTask.task_type.ilike(f"%{form.optimize_name_query}%")) if form.optimize_name_query else statement
        statement = statement.where(ModelTask.progress_status.ilike(f"%{form.task_status}%")) if form.task_status else statement
        statement = statement.offset(form.page_num * form.page_size).limit(form.page_size)
        result = self.db.execute(statement).scalars().all()

        return [model_task.to_schema() for model_task in result]

    def patch_task_status(self, task_uuid: str, patch_task_form: PatchTaskForm):
        """
        최적화/경량화 작업 요청 상태 수정
        """
        uuid = str_to_uuid4(task_uuid)
        statement = select(ModelTask).where(ModelTask.task_uuid == uuid).limit(1)
        result = self.db.execute(statement).scalar_one_or_none()
        if result:
            result.progress_status = patch_task_form.progress_status
            result.model_path_output = patch_task_form.path_output_model
            self.db.commit()
            self.db.refresh(result)
        return result.to_schema() if result else None


def get_model_task_repository(db: SessionLocal = SessionDepends):
    return ModelTaskRepository(db)
