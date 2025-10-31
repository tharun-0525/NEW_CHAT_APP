import pydantic
from typing import Optional


class ResponseModel(pydantic.BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[list] = None
