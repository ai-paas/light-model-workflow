from fastapi import Depends

from app.core.repo.optimizer_info import OptimizerInfoRepository, get_optimizer_info_repository
from app.schemas.requests.info import ReqOptimizerInfoForm
from app.schemas.services.optimizer_info import OptimizerInfo as OptimizerInfoSchema


class OptimizerInfoService:
    def __init__(self, optimizer_info_repo: OptimizerInfoRepository):
        self.optimizer_info_repo = optimizer_info_repo

    def get_optimizer_info_list(self, form: ReqOptimizerInfoForm) -> list[OptimizerInfoSchema]:
        return self.optimizer_info_repo.get_optimizer_info_list(form)

    def get_optimizer_info_by_id(self, id: int) -> OptimizerInfoSchema:
        return self.optimizer_info_repo.get_optimizer_info_by_id(id)


def get_optimizer_info_service(optimizer_info_repo: OptimizerInfoRepository = Depends(get_optimizer_info_repository)):
    return OptimizerInfoService(optimizer_info_repo)
