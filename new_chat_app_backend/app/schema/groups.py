from typing import List, Optional
from pydantic import BaseModel, constr

class GroupCreate(BaseModel):
    name: constr(min_length=1, max_length=100)
    description: Optional[str] = None
    profile_image: Optional[str] = None
    members: List[int]

class GroupFetch(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    profile_image: Optional[str] = None

    class Config:
        orm_mode = True

class GroupUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=100)] = None
    description: Optional[str] = None
    profile_image: Optional[str] = None