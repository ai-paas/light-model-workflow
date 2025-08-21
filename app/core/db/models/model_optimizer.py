from sqlalchemy import ForeignKey
from sqlalchemy.orm import MappedColumn, mapped_column

from app.core.db.models.base import IDwithTimestamp


class ModelOptimizer(IDwithTimestamp):
    __tablename__ = "model_optimizer"

    model_id: MappedColumn[int] = mapped_column(ForeignKey("model_info.id"), nullable=False, cascade="all, delete-orphan")
    optimizer_id: MappedColumn[int] = mapped_column(ForeignKey("optimizer_info.id"), nullable=False, cascade="all, delete-orphan")
