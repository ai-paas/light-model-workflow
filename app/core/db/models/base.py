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


class IDwithTimestamp(IntegerPrimaryKey):
    """
    ID with timestamp
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
