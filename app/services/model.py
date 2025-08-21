from fastapi import Depends

from app.core.repo.model_info import ModelInfoRepository, get_model_info_repository
from app.schemas.requests.info import ReqModelInfoForm
from app.schemas.services.model_info import ModelInfo as ModelInfoSchema


class ModelInfoService:
    def __init__(self, model_info_repo: ModelInfoRepository):
        self.model_info_repo = model_info_repo

    def get_model_info_list(self, form: ReqModelInfoForm) -> list[ModelInfoSchema]:
        return self.model_info_repo.get_model_info_list(form)

    def get_model_info_by_id(self, id: int) -> ModelInfoSchema:
        return self.model_info_repo.get_model_info_by_id(id)


def get_model_service(model_info_repo: ModelInfoRepository = Depends(get_model_info_repository)):
    return ModelInfoService(model_info_repo)