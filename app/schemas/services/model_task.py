from pydantic import BaseModel


class ModelTaskSchema(BaseModel):
    model_name: str
    progress_status: bool = False
    model_path_output: str | None = None
    kubeflow_experiment_id: str
    task_uuid: str
    task_type: str
