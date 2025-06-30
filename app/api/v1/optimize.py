from fastapi import APIRouter, Depends, Body
from typing import Any

from app.schemas.requests.optimize import ReqOptimizeWithNameAndArgsBody
from app.services.optimize import OptimizeService, get_optimize_service

router = APIRouter()

"""
모델 이름을 입력받고 해당 모델을 경량화/최적화 후 mlflow에 저장하는 라우터
"""


@router.post("/optimize/{optimizer_id}")
async def optimize(
    optimizer_id: int,
    *,
    optimize_form: ReqOptimizeWithNameAndArgsBody = Body(...),
    optimize_service: OptimizeService = Depends(get_optimize_service),
):
    result = None
    # hardcoded before refactor and apply db
    if optimizer_id == 1: # 1: tensorrt
        result = optimize_service.tensorrt(optimize_form)
    elif optimizer_id == 2: # 2: openvino
        result = optimize_service.openvino(optimize_form)
    # pruning, npu, tpu, quantization, etc.
    return result
