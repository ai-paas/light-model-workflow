from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.config.enums import SupportOptimize, SupportModel
from app.core.db.connect import SessionDepends
from app.schemas.requests.model import (
    ReqOwlV2PTQForm,
    ReqBertTRTForm,
    ReqBertOpenvinoForm,
)
from app.services.model_service import ModelService, get_model_service

router = APIRouter()

"""
모델 이름을 입력받고 해당 모델을 경량화/최적화 후 mlflow에 저장하는 라우터
"""


@router.post("/bert/optimizers/tensorrt")
async def bert_trt(
    *,
    db: Session = SessionDepends,
    optimize_form: ReqBertTRTForm,
    model_service: ModelService = Depends(get_model_service),
):
    result = model_service.bert_trt(
        db=db,
        model_name=SupportModel.Bert.value,
        optimize_name=SupportOptimize.TENSORRT.value,
        optimize_form=optimize_form,
    )
    return result


@router.post("/bert/optimizers/openvino")
async def bert_openvino(
    *,
    db: Session = SessionDepends,
    optimize_form: ReqBertOpenvinoForm,
    model_service: ModelService = Depends(get_model_service),
):
    result = model_service.bert_openvino(
        db=db,
        model_name=SupportModel.Bert.value,
        optimize_name=SupportOptimize.OPENVINO.value,
        optimize_form=optimize_form,
    )
    return result


@router.post("/owlv2/optimizers/ptq")
async def owlv2_ptq(
    *,
    db: Session = SessionDepends,
    optimize_form: ReqOwlV2PTQForm,
    model_service: ModelService = Depends(get_model_service),
):
    result = model_service.owlv2_ptq(
        db=db,
        model_name=SupportModel.OwlV2.value,
        optimize_name=SupportOptimize.PTQ.value,
        optimize_form=optimize_form,
    )
    return result
