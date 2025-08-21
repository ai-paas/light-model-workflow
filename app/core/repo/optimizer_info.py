from sqlalchemy import select

from app.core.db.session import SessionLocal
from app.core.db.connect import SessionDepends
from app.core.db.models.optimizer_info import OptimizerInfo
from app.schemas.requests.info import ReqOptimizerInfoForm
from app.schemas.services.optimizer_info import OptimizerInfo as OptimizerInfoSchema


class OptimizerInfoRepository:
    """
    db에 저장된 최적화 정보 조회
    입력 및 편집 기능은 추후 구현
    """
    def __init__(self, db: SessionLocal):
        self.db = db

    def get_optimizer_info_list(self, form: ReqOptimizerInfoForm) -> list[OptimizerInfoSchema]:
        statement = select(OptimizerInfo)
        statement = statement.where(OptimizerInfo.optimizer_name.ilike(f"%{form.name}%")) if form.name else statement
        statement = statement.offset(form.offset).limit(form.limit)
        result = self.db.execute(statement).scalars().all()
        return [optimizer_info.to_schema() for optimizer_info in result]

    def get_optimizer_info_by_id(self, id: int) -> OptimizerInfoSchema:
        statement = select(OptimizerInfo).where(OptimizerInfo.id == id).limit(1)
        result = self.db.execute(statement).scalar_one_or_none()
        return result.to_schema() if result else None


def get_optimizer_info_repository(db: SessionLocal = SessionDepends):
    return OptimizerInfoRepository(db)