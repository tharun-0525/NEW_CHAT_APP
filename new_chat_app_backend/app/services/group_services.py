from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models import Group_Mem, Group, GroupModelEnum
from sqlalchemy.future import select
from sqlalchemy import or_, and_
from app.schema.groups import GroupCreate, GroupUpdate

async def getGroups(
    user_id: int,  db: AsyncSession, limit: int= None, offset: int = None,
):

    result =(
        select(Group)
        .where(
            Group.id.in_(
                select(Group_Mem.g_id).where(Group_Mem.user_id == user_id)
            )
        )
        .distinct()
    )
    if limit is not None and offset is not None:
        result = result.offset(offset).limit(limit)
    result = await db.execute(result)      
    data = result.scalars().all()
    return data

async def createGroup(
    group: GroupCreate, db: AsyncSession
):
    name = group.name
    description = group.description 
    members = group.members
    model = GroupModelEnum.PRIVATE if len(members)==2 else GroupModelEnum.ROOM
    new_group = Group(name=name, 
                    description=description,  
                    created_by=members[0], 
                    model = model
                    )
    db.add(new_group)
    await db.commit()
    await db.refresh(new_group)

    for member_id in members:
        group_mem = Group_Mem(g_id=new_group.id, user_id=member_id)
        db.add(group_mem)

    await db.commit()
    return new_group

async def updateGroup(
    g_id: int, group: GroupUpdate,db: AsyncSession
):
    result = await db.execute(select(Group).where(Group.id == g_id))
    group = result.scalar_one_or_none()
    if not group:
        return None

    group.name = group.name
    group.description = group.description

    db.add(group)
    await db.commit()
    await db.refresh(group)
    return group

async def isMember(
    user_id: int, g_id: int, db: AsyncSession
):
    result = await db.execute(
        select(Group_Mem).where(
            and_(
                Group_Mem.user_id == user_id,
                Group_Mem.g_id == g_id
            )
        )
    )
    membership = result.scalar_one_or_none()
    return membership is not None