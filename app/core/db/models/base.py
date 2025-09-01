import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, MappedColumn, mapped_column


class Base(DeclarativeBase):
    """
    Base datebase model
    """
    pk: MappedColumn[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )


class IntegerPrimaryKey(DeclarativeBase):
    """
    Integer PK model
    """
    __abstract__ = True
    id: MappedColumn[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )


class FullTimestamp(DeclarativeBase):
    """
    Timestamped model

    - created_at: 생성일시
    - updated_at: 수정일시
    - deleted_at: 삭제일시
    """
    __abstract__ = True
    created_at: MappedColumn[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )
    updated_at: MappedColumn[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )
    deleted_at: MappedColumn[datetime] = mapped_column(
        DateTime,
        nullable=True,
    )


class IDwithTimestamp(IntegerPrimaryKey, FullTimestamp):
    """
    ID with timestamp
    """
    __abstract__ = True
