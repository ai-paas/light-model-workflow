from pydantic import BaseModel


class RespPagination(BaseModel):
    page_num: int
    page_size: int
    total_page: int
    total_count: int
    items: list[BaseModel]


class RespBaseItem(BaseModel):
    items: list[BaseModel]
    pagination: RespPagination


class RespBase(BaseModel):
    code: int
    message: str
    data: RespPagination | RespBaseItem | None = None

