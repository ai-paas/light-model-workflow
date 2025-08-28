from fastapi import APIRouter, Depends

from app.schemas.requests.task import ReqModelTaskPageForm, PatchTaskForm
from app.services.model_task import ModelTaskService, get_model_task_service

router = APIRouter()

"""
모델의 경량화/최적화 작업을 관리하는 라우터 정의
"""


@router.get("")
def get_tasks(
    *,
    form: ReqModelTaskPageForm = Depends(ReqModelTaskPageForm),
    model_task_service: ModelTaskService = Depends(get_model_task_service),
):
    """
    Get all tasks
    
    - 페이지네이션 적용
    """
    tasks = model_task_service.get_tasks(form)
    return tasks


@router.get("/{task_id}")
def get_task(*, task_id: str, model_task_service: ModelTaskService = Depends(get_model_task_service)):
    """
    Get one task by task_id

    - task uuid 를 통해 단일 조회
    """
    task = model_task_service.get_task_by_uuid(task_id)
    return task


@router.patch("/{task_id}")
def patch_task(
    *,
    task_id: str,
    patch_task_form: PatchTaskForm,
    model_task_service: ModelTaskService = Depends(get_model_task_service),
):
    """
    Patch one task by task_id

    - 프로그레스 상태 업데이트
    - 모델 경로 업데이트
    """
    task = model_task_service.patch_task(task_id, patch_task_form)
    return task
