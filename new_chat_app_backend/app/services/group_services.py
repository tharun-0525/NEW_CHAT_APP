from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models import Message, Group_Mem, Group, GroupModelEnum
from sqlalchemy.future import select
from sqlalchemy import or_, and_

async def getGroups(
    user_id: int, limit: int, offset: int, db: AsyncSession
):
    result = await db.execute(
        select(Group.id, Group.name, Group.description, Group.profile_image)
        .where(
            Group.id.in_(
                select(Group_Mem.group_id).where(Group_Mem.user_id == user_id)
            )
        )
        .distinct()
        .offset(offset)
        .limit(limit)
    )
    data = result.scalars().all()
    return data

async def createGroup(
    name: str, description: str, profile_image: str, members: list[int], db: AsyncSession
):
    model = GroupModelEnum.PRIVATE if len(members)==2 else GroupModelEnum.ROOM
    new_group = Group(name=name, 
                    description=description, 
                    profile_image=profile_image, 
                    created_by=members[0], 
                    model = model
                    )
    db.add(new_group)
    await db.commit()
    await db.refresh(new_group)

    for member_id in members:
        group_mem = Group_Mem(group_id=new_group.id, user_id=member_id)
        db.add(group_mem)

    await db.commit()
    return new_group

async def updateGroup(
    group_id: int, name: str, description: str, profile_image: str, db: AsyncSession
):
    result = await db.execute(select(Group).where(Group.id == group_id))
    group = result.scalar_one_or_none()
    if not group:
        return None

    group.name = name
    group.description = description
    group.profile_image = profile_image

    db.add(group)
    await db.commit()
    await db.refresh(group)
    return group

async def isMember(
    user_id: int, group_id: int, db: AsyncSession
):
    result = await db.execute(
        select(Group_Mem).where(
            and_(
                Group_Mem.user_id == user_id,
                Group_Mem.group_id == group_id
            )
        )
    )
    membership = result.scalar_one_or_none()
    return membership is not None