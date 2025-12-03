from pydantic import BaseModel, ConfigDict


class ModelInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="allow", populate_by_name=True)
    id: int
    model_name: str
    model_task: str
    run_id: str
    path: str
