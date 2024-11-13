from enum import Enum


class ModelLiteMapper(Enum):
    """
    경량화 / 최적화 이미지 매핑
    """

    # Bert
    BERT_TRT = "aipaas-harbor.surromind.ai/trt-workflow/bert_trt_test:v0.5"
    BERT_OPENVINO = "aipaas-harbor.surromind.ai/openvino-workflow/bert_openvino_test:v0.1"

    # Owlv2
    OWLV2_PTQ = "aipaas-harbor.surromind.ai/ptq-workflow/owl_v2_ptq_test:v0.5"



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