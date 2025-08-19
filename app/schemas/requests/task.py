from pydantic import BaseModel


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

    page_num: int = 0
    page_size: int = 10
    model_name_query: str | None = None
    optimize_name_query: str | None = None
    task_status: str | None = None
