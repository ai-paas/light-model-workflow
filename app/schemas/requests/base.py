from pydantic import BaseModel, Field


class PageReq(BaseModel):
    page_num: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1)
    # 추후 sort 고려

    @property
    def limit(self):
        return self.page_size

    @property
    def offset(self):
        return (self.page_num - 1) * self.page_size
