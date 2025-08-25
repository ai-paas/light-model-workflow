from sqlalchemy import select, func

from app.core.db.session import SessionLocal
from app.core.db.connect import SessionDepends
from app.core.db.models.model_optimizer import ModelOptimizer
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

    def __apply_sort_and_paginate(self, statement: select, form: ReqOptimizerInfoForm) -> select:
        """
        정렬 및 페이지네이션 적용
        - 기본 정렬 조건: id 내림차순
        """
        statement = statement.order_by(OptimizerInfo.id.desc())
        statement = statement.offset(form.offset).limit(form.limit)
        return statement

    def __apply_filter(self, statement: select, form: ReqOptimizerInfoForm) -> select:
        """
        필터 적용
        - 최적화 도구 이름 필터
        """
        statement = statement.where(OptimizerInfo.optimizer_name.ilike(f"%{form.name}%")) if form.name else statement
        return statement

    def __apply_subquery(self, statement: select, form: ReqOptimizerInfoForm) -> select:
        """
        서브쿼리 적용
        - 모델 id 필터
        """
        if form.model_id:
            subquery = select(ModelOptimizer.optimizer_id).where(ModelOptimizer.model_id == form.model_id)
            statement = statement.where(OptimizerInfo.id.in_(subquery))
        return statement

    def get_optimizer_info_list(self, form: ReqOptimizerInfoForm) -> list[OptimizerInfoSchema]:
        """
        최적화 정보 목록 조회
        """
        statement = select(OptimizerInfo)
        statement = self.__apply_subquery(statement, form)
        statement = self.__apply_filter(statement, form)
        statement = self.__apply_sort_and_paginate(statement, form)
        result = self.db.execute(statement).scalars().all()
        return [optimizer_info.to_schema() for optimizer_info in result]

    def get_optimizer_info_by_id(self, id: int) -> OptimizerInfoSchema:
        """
        최적화 정보 상세 조회
        """
        statement = select(OptimizerInfo).where(OptimizerInfo.id == id).limit(1)
        result = self.db.execute(statement).scalar_one_or_none()
        return result.to_schema() if result else None

    def get_optimizer_info_count(self, form: ReqOptimizerInfoForm) -> int:
        """
        최적화 정보 개수 조회
        """
        statement = select(func.count(OptimizerInfo.id))
        statement = self.__apply_subquery(statement, form)
        statement = self.__apply_filter(statement, form)
        return self.db.execute(statement).scalar_one_or_none()


def get_optimizer_info_repository(db: SessionLocal = SessionDepends):
    return OptimizerInfoRepository(db)
