from typing import List, Annotated, Optional
from pydantic import BaseModel, Field

class GroupCreate(BaseModel):
    name: Optional[Annotated[str, Field(min_length=1, max_length=100)]] = None 
    description: Optional[str] = None
    members: List[int] = Field(min_items=2)

class GroupFetch(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True

class GroupUpdate(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)] = None
    description: Optional[str] = None
