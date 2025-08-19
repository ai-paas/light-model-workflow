from pydantic import BaseModel


class ModelTaskSchema(BaseModel):
    model_name: str
    optimize_name: str
    progress_status: bool
    model_path_output: str
    kubeflow_experiment_id: str
    task_uuid: str
    task_type: str
