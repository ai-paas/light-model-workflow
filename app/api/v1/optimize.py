from fastapi import APIRouter, Depends, Body

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
) -> dict:
    result = optimize_service.optimize(optimizer_id, optimize_form)
    return result
