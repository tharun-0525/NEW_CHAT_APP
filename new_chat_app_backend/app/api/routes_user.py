from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.user_services import getUsers, getUserById
from app.api.routes_auth import get_current_user
from app.schema.response import ResponseModel
from app.schema.user import UserFetch

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", response_model=ResponseModel)
async def get_user(
    limit: int = 2, offset: int = 0, db: AsyncSession = Depends(get_db)
):
    user = await getUsers(db, limit, offset)
    if not user:
        return {"status": "failed", "message": "Users not found"}
    print("Fetched Users:", user)
    data = [
        UserFetch(
            id=u.id,
            username=u.username,
            email=u.email,
            name=u.name,
            bio=u.bio,
            profile_image=u.profile_image)
        for u in user
    ]
    return {"status": "success", "data": data}


@router.get("/me", response_model=ResponseModel)
async def read_current_user(
    current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    user = await getUserById(db, user_id=current_user)
    if not user:
        data = {"error": "User not found"}
        return ResponseModel(status="failed", data=data)
    data = UserFetch(
        id=user.id,
        username=user.username,
        email=user.email,
        name=user.name,
        bio=user.bio,
        profile_image=user.profile_image,
    )
    return {"status": "success", "data": data}
