from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel


class MessageCreate(BaseModel):
    content: str
    receiver_id: int


class MessageFetch(BaseModel):
    id: int
    content: str
    sender_id: int
    receiver_id: int

    model_config = {"from_attributes": True}


class MessageOut(MessageFetch):
    timestamp: Optional[str] = None

    model_config = {"from_attributes": True}
