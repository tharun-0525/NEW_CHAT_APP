from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models import User
from app.services.user_services import getUsers, getUserById
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
    print("Fetched Users:", user)
    data= [{"id": u.id, "username": u.username, "email": u.email, "name": u.name, "bio": u.bio, "profile_image": u.profile_image} for u in user]
    #data= [UserFetch(id= u.id, username= u.username, email=u.email, name=u.name, bio=u.bio, profile_image=u.profile_image) for u in user]
    return ResponseModel(status="success", data=data)

@router.get("/me")
async def read_current_user(current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user= await getUserById(db, user_id=current_user)
    if not user:
        data = {"error": "User not found"}
        return ResponseModel(status="failed", data=data)
    data= UserFetch(id=user.id, username=user.username, email=user.email, name=user.name, bio=user.bio, profile_image=user.profile_image)
    return ResponseModel(status="success", data=[data])
