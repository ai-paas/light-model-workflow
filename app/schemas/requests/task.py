from pydantic import BaseModel

from app.schemas.requests.base import PageReq

class PatchTaskForm(BaseModel):
    """
    Task 수정시 사용되는 Form
    """

    # pipeline 상태
    progress_status: bool

    # 경량화 모델 저장 경로
    path_output_model: str


class ReqModelTaskForm(BaseModel):
    """
    모델 최적화 작업 조회 시 사용되는 Form
    """

    model_name_query: str | None = None
    optimizer_name_query: str | None = None
    task_status: str | None = None


class ReqModelTaskPageForm(PageReq, ReqModelTaskForm):
    """
    페이지네이션 적용된 모델 최적화 작업 조회 시 사용되는 Form
    """
    ...
