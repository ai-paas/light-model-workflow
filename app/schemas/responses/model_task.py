from urllib.parse import urlencode

from pydantic import ConfigDict, Field
from pydantic.fields import computed_field

from app.schemas.responses.base import RespPagination
from app.schemas.services.model_task import ModelTaskSchema


class RespModelTaskPage(RespPagination):
    model_config = ConfigDict(from_attributes=True, extra="allow", populate_by_name=True)
    items: list[ModelTaskSchema]
    url_params: dict[str, str | int | None] = Field(default_factory=dict, exclude=True)

    @computed_field
    @property
    def next_page(self) -> str | None:
        if self.next_page_num:
            url_params = self.url_params
            url_params["page_num"] = str(self.next_page_num)
            url_params_str = ("?" + urlencode(url_params)) if url_params else ""
            return f"/api/v1/tasks{url_params_str}"
        return None

    @computed_field
    @property
    def prev_page(self) -> str | None:
        if self.prev_page_num:
            url_params = self.url_params
            url_params["page_num"] = str(self.prev_page_num)
            url_params_str = ("?" + urlencode(url_params)) if url_params else ""
            return f"/api/v1/tasks{url_params_str}"
        return None
