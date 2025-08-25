from fastapi import Depends

from app.core.repo.optimizer_info import OptimizerInfoRepository, get_optimizer_info_repository
from app.schemas.requests.info import ReqOptimizerInfoForm
from app.schemas.services.optimizer_info import OptimizerInfo as OptimizerInfoSchema
from app.schemas.responses.info import RespOptimizerInfoPage


class OptimizerInfoService:
    # crud 중 r 만 구현, 추후 필요시 추가
    def __init__(self, optimizer_info_repo: OptimizerInfoRepository):
        self.optimizer_info_repo = optimizer_info_repo

    def get_optimizer_info_list(self, form: ReqOptimizerInfoForm) -> RespOptimizerInfoPage:
        optimizer_info_list = self.optimizer_info_repo.get_optimizer_info_list(form)
        total_count = self.optimizer_info_repo.get_optimizer_info_count(form)
        return RespOptimizerInfoPage(
            items=optimizer_info_list,
            total_count=total_count,
            page_size=form.page_size,
            current_page=form.page_num,
            url_params=form.model_dump(exclude_none=True),
        )

    def get_optimizer_info_by_id(self, id: int) -> OptimizerInfoSchema:
        return self.optimizer_info_repo.get_optimizer_info_by_id(id)


def get_optimizer_info_service(optimizer_info_repo: OptimizerInfoRepository = Depends(get_optimizer_info_repository)):
    return OptimizerInfoService(optimizer_info_repo)
