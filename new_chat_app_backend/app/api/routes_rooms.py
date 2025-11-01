from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.user_services import getUsers, getUserById
from app.api.routes_auth import get_current_user
from app.schema.response import ResponseModel
from app.schema.groups import GroupFetch
from app.services.group_services import getGroups, createGroup, updateGroup

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/", response_model=ResponseModel)
async def groups(
    limit: int = 110, offset: int = 0, db: AsyncSession = Depends(get_db)
):
    rooms = await getGroups(db, limit, offset)
    if not rooms:
        return {"status": "success"}
    data = [
        GroupFetch(
            id=room.id,
            name=room.name,
            description=room.description,
            profile_image=room.profile_image,
        )
        for room in rooms
    ]
    return {"status": "success", "data": data}