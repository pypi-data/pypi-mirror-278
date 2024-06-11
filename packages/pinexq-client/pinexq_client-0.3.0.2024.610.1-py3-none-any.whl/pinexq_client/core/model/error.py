from pydantic import BaseModel


class ProblemDetails(BaseModel):
    type: str | None = None
    title: str | None = None
    status: int | None = None
    detail: str | None = None
    instance: str | None = None
