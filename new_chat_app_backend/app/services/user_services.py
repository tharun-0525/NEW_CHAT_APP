from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from sqlalchemy.future import select
from app.core.security import verify_password, hash_password, create_access_token

async def createUser(db: AsyncSession, name: str, email: str, username: str, password: str):
    db_user = User(name=name, username=username, email=email, hashed_password=hash_password(password))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def getUserByUsername(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def getUsers(db: AsyncSession,limit: int,after_id: int):
    result = await db.execute(select(User.username, User.id, User.email).limit(limit))
    if after_id:
        result = await db.execute(select(User.username, User.id, User.email).where(User.id > after_id).limit(limit))
    return result.fetchall()

async def login_user(username: str, password: str, db: AsyncSession):
    user = await getUserByUsername(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return {"error": "Invalid username or password"}

    token = create_access_token({"user_id":user.id}) 
    return token
