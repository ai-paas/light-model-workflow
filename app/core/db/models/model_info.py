from sqlalchemy import String
from sqlalchemy.orm import MappedColumn, mapped_column

from app.core.db.models.base import IDwithTimestamp
from app.schemas.services.model_info import ModelInfo as ModelInfoSchema


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

    def to_schema(self) -> ModelInfoSchema:
        return ModelInfoSchema(
            id=self.id,
            model_name=self.model_name,
            model_task=self.model_task,
            run_id=self.run_id,
            path=self.path,
        )

    @classmethod
    def from_schema(cls, schema: ModelInfoSchema) -> "ModelInfo":
        return cls(
            id=schema.id,
            model_name=schema.model_name,
            model_task=schema.model_task,
            run_id=schema.run_id,
            path=schema.path,
        )
