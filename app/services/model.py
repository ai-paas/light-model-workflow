from fastapi import Depends

from app.core.repo.model_info import ModelInfoRepository, get_model_info_repository
from app.schemas.requests.info import ReqModelInfoForm
from app.schemas.services.model_info import ModelInfo as ModelInfoSchema
from app.schemas.responses.info import RespModelInfoPage


class ModelInfoService:
    # crud 중 r 만 구현, 추후 필요시 추가
    def __init__(self, model_info_repo: ModelInfoRepository):
        self.model_info_repo = model_info_repo

    def get_model_info_list(self, form: ReqModelInfoForm) -> RespModelInfoPage:
        model_info_list = self.model_info_repo.get_model_info_list(form)
        total_count = self.model_info_repo.get_model_info_count(form)
        return RespModelInfoPage(
            items=model_info_list,
            total_count=total_count,
            page_size=form.page_size,
            current_page=form.page_num,
            url_params=form.model_dump(exclude_none=True),
        )

    def get_model_info_by_id(self, id: int) -> ModelInfoSchema:
        return self.model_info_repo.get_model_info_by_id(id)


def get_model_service(model_info_repo: ModelInfoRepository = Depends(get_model_info_repository)):
    return ModelInfoService(model_info_repo)