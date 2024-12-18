from enum import Enum
from app.core.settings import get_settings

SETTINGS = get_settings()


class ModelLiteMapper(Enum):
    """
    경량화 / 최적화 이미지 매핑
    """

    # Bert
    BERT_TRT = SETTINGS.BERT_TRT
    BERT_OPENVINO = SETTINGS.BERT_OPENVINO

    # Owlv2
    OWLV2_PTQ = SETTINGS.OWLV2_PTQ


class SupportModel(Enum):
    """
    지원하는 모델
    """

    Bert = "bert"
    OwlV2 = "owlv2"


class SupportOptimize(Enum):
    """
    지원하는 최적화 / 경량화
    """

    PTQ = "ptq"
    TENSORRT = "tensorrt"
    OPENVINO = "openvino"
