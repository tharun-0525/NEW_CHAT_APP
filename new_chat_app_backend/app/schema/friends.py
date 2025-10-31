from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel


class FriendRequestCreate(BaseModel):
    requester_id: int
    addressee_id: int
    status: str


class FriendRequestFetch(BaseModel):
    id: int
    requester_id: int
    addressee_id: int
    status: str

    class Config:
        orm_mode = True
