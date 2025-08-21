from pydantic import BaseModel


class PageReq(BaseModel):
    page_num: int = 1
    page_size: int = 10
    # 추후 sort 고려

    @property
    def limit(self):
        return self.page_size

    @property
    def offset(self):
        return (self.page_num - 1) * self.page_size
