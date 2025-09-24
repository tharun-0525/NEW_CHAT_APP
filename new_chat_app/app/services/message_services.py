from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models import Message
from sqlalchemy.future import select
from sqlalchemy import or_, and_

async def send_message( content:str, sender_id: int, receiver_id: int, db: AsyncSession):
    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    return new_message

async def fetch_messages(user_id: int, with_user: int, limit: int,db: AsyncSession):
    result = await db.execute(
        select(Message).where(
            or_(and_((Message.sender_id == user_id),(Message.receiver_id == with_user)), 
                and_((Message.sender_id == with_user),(Message.receiver_id == user_id))
            )
        ).order_by(Message.id).limit(limit)
    )
    return result.scalars().all()