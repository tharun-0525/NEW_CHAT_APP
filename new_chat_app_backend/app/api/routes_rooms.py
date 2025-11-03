from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.routes_auth import get_current_user
from app.schema.response import ResponseModel
from app.schema.groups import GroupFetch, GroupCreate, GroupUpdate
from app.services.group_services import getGroups, createGroup, updateGroup

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/", response_model=ResponseModel)
async def groups(
    user_id: int = Depends(get_current_user),
    limit: int = 110, 
    offset: int = 0, db: AsyncSession = Depends(get_db)
):

    rooms = await getGroups(user_id=user_id, db=db,limit=limit, offset=offset)
    print("groups",rooms)
    if not rooms:
        return {"status": "success"}
    data = [
        GroupFetch(
            id=room.id,
            name=room.name,
            description=room.description
        )
        for room in rooms
    ]
    return {"status": "success", "data": data}

@router.post("/", response_model=ResponseModel)
async def create_room( 
    members: List[int],
    name: Optional[str] = None,
    description: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    group= GroupCreate(
        name=name,
        description=description,
        members=members
    )
    new_group = await createGroup(
        group=group,
        db=db
    )
    return {"status": "success", "data": [new_group.id]}

@router.put("/{group_id}", response_model=ResponseModel)
async def update_room( 
    group_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    group = GroupUpdate(
        name=name,
        description=description
    )
    updated_group = await updateGroup(
        group_id=group_id,
    )
    if not updated_group:
        return {"status": "failed", "message": "Group not found"}
    return {"status": "success", "data": [updated_group.id]}