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


@router.post("/{model_name}/optimizers/{optimize_name}")
async def lite_model(
    *,
    db: Session = SessionDepends,
    model_name: SupportModel,
    optimize_name: SupportOptimize,
    request: Request,
    model_service: ModelService = Depends(get_model_service),
):
    optimize_form = await request.json()
    model_value = model_name.value
    optimize_value = optimize_name.value

    try:  # Bert
        if model_value == SupportModel.Bert.value:
            if optimize_value == SupportOptimize.TENSORRT.value:
                form = ReqBertTRTForm(**optimize_form)
                result = model_service.bert_trt(
                    db=db,
                    model_name=model_value,
                    optimize_name=optimize_value,
                    optimize_form=form,
                )
            elif optimize_value == SupportOptimize.OPENVINO.value:
                form = ReqBertOpenvinoForm(**optimize_form)
                result = model_service.bert_openvino(
                    db=db,
                    model_name=model_value,
                    optimize_name=optimize_value,
                    optimize_form=form,
                )
            else:
                raise HTTPException(status_code=400, detail="Invalid form data")

        # OwlV2
        elif model_value == SupportModel.OwlV2.value:
            if optimize_value == SupportOptimize.PTQ.value:
                form = ReqOwlV2PTQForm(**optimize_form)
                result = model_service.owlv2_ptq(
                    db=db,
                    model_name=model_value,
                    optimize_name=optimize_value,
                    optimize_form=form,
                )
            else:
                raise HTTPException(status_code=400, detail="Invalid form data")

        else:
            raise HTTPException(status_code=400, detail="Invalid form data")
    except ValidationError as e:
        # Pydantic ValidationError 처리
        raise HTTPException(status_code=422, detail=e.errors())
    except HTTPException as e:
        # 이미 발생한 HTTPException은 다시 raise
        raise e
    except Exception as e:
        # 그 외의 모든 예외 처리
        raise HTTPException(status_code=500, detail=str(e))
    return result
