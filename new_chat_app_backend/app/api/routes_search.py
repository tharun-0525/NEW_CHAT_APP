from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.user_services import searchByUsername
from app.services.group_services import searchByGroupname
from app.api.routes_auth import get_current_user
from app.schema.response import ResponseModel
from app.schema.user import UserFetch
from app.schema.groups import GroupFetch

router= APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/users",response_model=ResponseModel)
async def usersearch(
    username: str,
    db: AsyncSession = Depends(get_db),
    limit: int = 10,
    offset: int = 0
):
    users = await searchByUsername(username, db, limit, offset)
    data = [
        UserFetch(
            id=u.id,
            username=u.username,
            email=u.email,
            name=u.name,
            bio=u.bio,
            profile_image=u.profile_image)
        for u in users
    ]
    return {"status": "success", "data": data}

@router.get("/groups",response_model=ResponseModel)
async def usersearch(
    groupname: str,
    db: AsyncSession = Depends(get_db),
    limit: int = 10,
    offset: int = 0
):
    groups = await searchByGroupname(groupname, db, limit, offset)
    data = [
        GroupFetch(
            id=g.id,
            name=g.name,
            description=g.description
            )
        for g in groups
    ]
    return {"status": "success", "data": data}

