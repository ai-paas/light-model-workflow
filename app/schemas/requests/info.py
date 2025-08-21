from app.schemas.requests.base import PageReq


class ReqModelInfoForm(PageReq):
    name: str | None = None
    optimizer_id: int | None = None


class ReqOptimizerInfoForm(PageReq):
    name: str | None = None
    model_id: str | None = None
