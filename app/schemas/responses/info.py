from urllib.parse import urlencode

from pydantic import ConfigDict, computed_field, Field

from app.schemas.services.model_info import ModelInfo
from app.schemas.services.optimizer_info import OptimizerInfo
from app.schemas.responses.base import RespPagination


class RespModelInfoPage(RespPagination):
    model_config = ConfigDict(from_attributes=True, extra="allow", populate_by_name=True)
    items: list[ModelInfo]
    url_params: dict[str, str | int | None] = Field(default_factory=dict, exclude=True)

    @computed_field
    @property
    def next_page(self) -> str | None:
        """
        다음 페이지 링크 생성
        url_params 입력 필요
        """
        if self.next_page_num:
            url_params = self.url_params
            url_params["page_num"] = str(self.next_page_num)
            return f"/api/v1/info/model?{urlencode(url_params)}"
        return None

    @computed_field
    @property
    def prev_page(self) -> str | None:
        if self.prev_page_num:
            url_params = self.url_params
            url_params["page_num"] = str(self.prev_page_num)
            return f"/api/v1/info/model?{urlencode(url_params)}"
        return None


class RespOptimizerInfoPage(RespPagination):
    model_config = ConfigDict(from_attributes=True, extra="allow", populate_by_name=True)
    items: list[OptimizerInfo]
    url_params: dict[str, str | int | None] = Field(default_factory=dict, exclude=True)

    @computed_field
    @property
    def next_page(self) -> str | None:
        if self.next_page_num:
            url_params = self.url_params
            url_params["page_num"] = str(self.next_page_num)
            return f"/api/v1/info/optimizer?{urlencode(url_params)}"
        return None

    @computed_field
    @property
    def prev_page(self) -> str | None:
        if self.prev_page_num:
            url_params = self.url_params
            url_params["page_num"] = str(self.prev_page_num)
            return f"/api/v1/info/optimizer?{urlencode(url_params)}"
        return None
