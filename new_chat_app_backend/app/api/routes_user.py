from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models import User
from app.services.user_services import getUsers
from app.api.routes_auth import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/")
async def get_user(limit: int = 2,after_id:int = 0,db: AsyncSession = Depends(get_db)):
    user = await getUsers(db,limit,after_id)
    if not user:
        return {"error": "User not found"}
    return [{"id": u.id, "username": u.username, "email": u.email} for u in user]

@router.get("/me")
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
