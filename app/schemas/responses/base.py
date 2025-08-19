from pydantic import BaseModel, ConfigDict


class RespPagination(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="allow", populate_by_name=True)
    page_num: int
    page_size: int
    total_page: int
    total_count: int
    items: list[BaseModel] | None = None
    # next_page, prev_page


class RespBase(BaseModel):
    code: int
    message: str
    data: RespPagination | BaseModel | None = None
