from fastapi import Depends

from app.core.repo.model_task import ModelTaskRepository, get_model_task_repository
from app.schemas.requests.task import PatchTaskForm, ReqModelTaskForm
from app.schemas.services.model_task import ModelTaskSchema


class ModelTaskService:
    def __init__(self, model_task_repo: ModelTaskRepository):
        self.model_task_repo = model_task_repo

    def get_task_by_uuid(self, task_uuid: str) -> ModelTaskSchema:
        return self.model_task_repo.get_task_by_uuid(task_uuid)

    def get_tasks(self, form: ReqModelTaskForm) -> list[ModelTaskSchema]:
        return self.model_task_repo.get_tasks(form)

    def patch_task(self, task_uuid: str, patch_task_form: PatchTaskForm):
        return self.model_task_repo.patch_task(task_uuid, patch_task_form)

def get_model_task_service(model_task_repo: ModelTaskRepository = Depends(get_model_task_repository)):
    return ModelTaskService(model_task_repo)
