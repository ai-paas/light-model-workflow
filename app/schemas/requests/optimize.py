from pydantic import BaseModel
from typing import Any

class ReqOptimizeBodyBase(BaseModel):
    """
    최적화 요청 기본 폼
    """
    # 모델이 저장된 mlflow의 run id
    saved_model_run_id: str

    # model 이 저장된 경로 ex) models/bert-base-uncased-model
    saved_model_path: str  # 삭제 고려


class ReqOptimizeWithNameAndArgsBody(ReqOptimizeBodyBase):
    """
    모델 이름 추가
    """
    model_name: str
    args: dict[str, Any]
