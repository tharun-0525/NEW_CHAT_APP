from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, Group_Mem, Group
from sqlalchemy.future import select
from app.core.security import verify_password, hash_password, create_access_token


async def createUser(
    db: AsyncSession, name: str, email: str, username: str, password: str
):
    db_user = User(
        name=name,
        username=username,
        email=email,
        hashed_password=hash_password(password),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def getUserByUsername(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def getUserById(db: AsyncSession, user_id: str):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def getUsers(db: AsyncSession, limit: int, offset: int):
    result = await db.execute(select(User).limit(limit))
    if offset:
        result = await db.execute(select(User).where(User.id > offset).limit(limit))
    return result.scalars().all()

async def login_user(username: str, password: str, db: AsyncSession):
    user = await getUserByUsername(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None

    token = create_access_token({"user_id": user.id})
    return token

async def usersOfGroup(group_id: int, db: AsyncSession):
    users = await db.execute(
        select(User).where(
            User.id.in_(
                select(Group_Mem.user_id).where(
                    Group_Mem.g_id==group_id
                )
            )
        )
    )
    return users.scalars().all()

async def searchByUsername(
        username: str,
        db: AsyncSession,
        limit: int,
        offset: int,
):
    result = await db.execute(select(User).where(
                                User.username.like(f'{username}%')).limit(limit).offset(offset)
                            )
    return result.scalars().all()