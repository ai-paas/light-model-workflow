from pydantic import BaseModel
from typing import List, Any

from app.config.enums import ModelLiteMapper, SupportModel, SupportOptimize

"""
Service layer에서 사용되는 type
"""


class OptimizationTaskInfo(BaseModel):
    """
    최적화 / 경량화 작업시 필요한 공통 정보
    """
    model_name: str
    optimize_name: str
    docker_image_path: ModelLiteMapper
    command: List[str]
    args: List[Any]


class OptimizationSetUp(BaseModel):
    """
    최적화 / 경량화 작업시 필요한 공통 정보
    """
    model_name: str
    optimize_name: str
    docker_image_path: str
    command: list[str]
    args: list[Any]
    env: dict[str, str]
    accelerator_type: str
