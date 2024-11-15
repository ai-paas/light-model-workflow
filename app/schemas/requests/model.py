from typing import List

from pydantic import BaseModel


class ReqLiteModelBaseForm(BaseModel):
    """
    모델 생성시 공통적으로 사용되는 Form
    """

    # 모델이 저장된 mlflow의 run id
    saved_model_run_id: str

    # model 이 저장된 경로 ex) models/bert-base-uncased-model
    saved_model_path: str


class ReqOwlV2PTQForm(ReqLiteModelBaseForm):
    """
    owlv2 ptq form
    """

    # quantization 을 적용할 레이어 이름
    quantization_layers: List[str]


class ReqBertTRTForm(ReqLiteModelBaseForm):
    pass


class ReqBertOpenvinoForm(ReqLiteModelBaseForm):
    pass
