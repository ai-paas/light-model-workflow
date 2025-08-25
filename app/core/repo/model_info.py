from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from app.core.db.session import SessionLocal
from app.core.db.connect import SessionDepends
from app.core.db.models.model_info import ModelInfo
from app.core.db.models.model_optimizer import ModelOptimizer
from app.schemas.requests.info import ReqModelInfoForm
from app.schemas.services.model_info import ModelInfo as ModelInfoSchema


class ModelInfoRepository:
    """
    db에 저장된 모델 정보 조회

    입력 및 편집 기능은 추후 구현
    """
    def __init__(self, db: SessionLocal):
        self.db = db

    def __apply_sort_and_paginate(self, statement: select, form: ReqModelInfoForm) -> select:
        """
        정렬 및 페이지네이션 적용
        - 기본 정렬 조건: id 내림차순
        """
        statement = statement.order_by(ModelInfo.id.desc())
        statement = statement.offset(form.offset).limit(form.limit)
        return statement

    def __apply_filter(self, statement: select, form: ReqModelInfoForm) -> select:
        """
        필터 적용
        - 모델 이름 필터
        """
        statement = statement.where(ModelInfo.model_name.ilike(f"%{form.name}%")) if form.name else statement
        return statement

    def __apply_subquery(self, statement: select, form: ReqModelInfoForm) -> select:
        """
        서브쿼리 적용
        - 최적화 도구 id 필터
        """
        if form.optimizer_id:
            subquery = select(ModelOptimizer.model_id).where(ModelOptimizer.optimizer_id == form.optimizer_id)
            statement = statement.where(ModelInfo.id.in_(subquery))
        return statement

    def get_model_info_list(self, form: ReqModelInfoForm) -> list[ModelInfoSchema]:
        """
        모델 정보 목록 조회
        """
        statement = select(ModelInfo)
        statement = self.__apply_subquery(statement, form)
        statement = self.__apply_filter(statement, form)
        statement = self.__apply_sort_and_paginate(statement, form)
        result = self.db.execute(statement).scalars().all()
        return [model_info.to_schema() for model_info in result]

    def get_model_info_count(self, form: ReqModelInfoForm) -> int:
        """
        모델 정보 개수 조회
        """
        statement = select(func.count(ModelInfo.id))
        statement = self.__apply_subquery(statement, form)
        statement = self.__apply_filter(statement, form)
        return self.db.execute(statement).scalar_one_or_none()

    def get_model_info_by_id(self, id: int) -> ModelInfoSchema:
        """
        모델 정보 상세 조회
        """
        statement = select(ModelInfo).where(ModelInfo.id == id).limit(1)
        result = self.db.execute(statement).scalar_one_or_none()
        return result.to_schema() if result else None


def get_model_info_repository(db: SessionLocal = SessionDepends):
    return ModelInfoRepository(db)
