from fastapi import APIRouter, Depends

from app.schemas.requests.info import ReqModelInfoForm, ReqOptimizerInfoForm
from app.services.model import ModelInfoService, get_model_service
from app.services.optimizer import OptimizerInfoService, get_optimizer_info_service
from app.schemas.responses.info import RespModelInfoPage, RespOptimizerInfoPage
from app.schemas.services.model_info import ModelInfo
from app.schemas.services.optimizer_info import OptimizerInfo

router = APIRouter()

@router.get("/model")
def get_model_list(
    form: ReqModelInfoForm = Depends(ReqModelInfoForm),
    model_service: ModelInfoService = Depends(get_model_service)
) -> RespModelInfoPage:
    return model_service.get_model_info_list(form)


@router.get("/model/{model_id}")
def get_model(model_id: int, model_service: ModelInfoService = Depends(get_model_service)) -> ModelInfo:
    return model_service.get_model_info_by_id(model_id)


@router.get("/optimizer")
def get_optimizer_list(
    form: ReqOptimizerInfoForm = Depends(ReqOptimizerInfoForm),
    optimizer_service: OptimizerInfoService = Depends(get_optimizer_info_service)
) -> RespOptimizerInfoPage:
    return optimizer_service.get_optimizer_info_list(form)


@router.get("/optimizer/{optimizer_id}")
def get_optimizer(
    optimizer_id: int, 
    optimizer_service: OptimizerInfoService = Depends(get_optimizer_info_service)
) -> OptimizerInfo:
    return optimizer_service.get_optimizer_info_by_id(optimizer_id)
