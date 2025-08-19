from sqlalchemy import String
from sqlalchemy.orm import MappedColumn, mapped_column

from app.core.db.models.base import IDwithTimestamp


class ModelInfo(IDwithTimestamp):
    __tablename__ = "model_info"

    # 모델 이름
    model_name: MappedColumn[str] = mapped_column(String, nullable=False)
    # 모델이 수행하는 작업
    model_task: MappedColumn[str] = mapped_column(String, nullable=False)
    # 모델 경로
    run_id: MappedColumn[str] = mapped_column(String, nullable=False)
    # 모델 설명
    path: MappedColumn[str] = mapped_column(String, nullable=False)
