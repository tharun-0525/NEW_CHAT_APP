from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models import User
from app.services.user_services import getUsers
from app.api.routes_auth import get_current_user
from app.schema.response import ResponseModel
from app.schema.user import UserFetch

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/")
async def get_user(limit: int = 2,after_id:int = 0,db: AsyncSession = Depends(get_db)):
    user = await getUsers(db,limit,after_id)
    if not user:
        data = {"error": "User not found"}
        return ResponseModel(status="failed", data=data)
    data= [{"id": u.id, "username": u.username, "email": u.email} for u in user]
    return ResponseModel(status="success", data=data)

@router.get("/me")
async def read_current_user(current_user: User = Depends(get_current_user)):
    user = UserFetch(id=current_user.id, username=current_user.username, email=current_user.email, name=current_user.name,
                    bio=current_user.bio, profile_image=current_user.profile_image
                    )
    return current_user
