from pydantic import BaseModel, ConfigDict, computed_field, Field

from app.utils import divide_with_ceil


class RespPagination(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="allow", populate_by_name=True)
    current_page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1)
    total_count: int = 0
    items: list = Field(default_factory=list)

    @computed_field
    @property
    def total_page(self) -> int:
        return divide_with_ceil(self.total_count, self.page_size)

    @property
    def next_page_num(self) -> int | None:
        return self.current_page + 1 if self.current_page < self.total_page else None

    @property
    def prev_page_num(self) -> int | None:
        return self.current_page - 1 if self.current_page > 1 else None


class RespBase(BaseModel):
    code: int
    message: str
    data: RespPagination | BaseModel | None = None
