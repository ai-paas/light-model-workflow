from pydantic import BaseModel, ConfigDict


class OptimizerInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="allow", populate_by_name=True)
    id: int
    optimizer_name: str
    accelerator: str
    argument: dict
