"""
테이블 생성
"""

from sqlalchemy import create_engine

from app.core.settings import get_settings
from app.core.db.models import Base, IntegerPrimaryKey


def create_table():
    """
    두가지 베이스 모델 기반 테이블 생성
    """
    try:
        settings = get_settings()
        engine = create_engine(settings.get_db_uri, echo=True)

        Base.metadata.create_all(engine)
        IntegerPrimaryKey.metadata.create_all(engine)
    except Exception as e:
        print(e)
        raise e


if __name__ == "__main__":
    print("테이블 생성 시작")
    create_table()
