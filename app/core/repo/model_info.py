from sqlalchemy import select

from app.core.db.session import SessionLocal
from app.core.db.connect import SessionDepends
from app.core.db.models.model_info import ModelInfo
from app.schemas.requests.info import ReqModelInfoForm
from app.schemas.services.model_info import ModelInfo as ModelInfoSchema


class ModelInfoRepository:
    """
    db에 저장된 모델 정보 조회
    입력 및 편집 기능은 추후 구현
    """
    def __init__(self, db: SessionLocal):
        self.db = db

    def get_model_info_list(self, form: ReqModelInfoForm) -> list[ModelInfoSchema]:
        statement = select(ModelInfo)
        statement = statement.where(ModelInfo.model_name.ilike(f"%{form.name}%")) if form.name else statement
        statement = statement.offset(form.offset).limit(form.limit)
        result = self.db.execute(statement).scalars().all()
        return [model_info.to_schema() for model_info in result]
    
    def get_model_info_by_id(self, id: int) -> ModelInfoSchema:
        statement = select(ModelInfo).where(ModelInfo.id == id).limit(1)
        result = self.db.execute(statement).scalar_one_or_none()
        return result.to_schema() if result else None


def get_model_info_repository(db: SessionLocal = SessionDepends):
    return ModelInfoRepository(db)
