from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models import Message
from sqlalchemy.future import select
from sqlalchemy import or_, and_


async def send_message(
    content: str, sender_id: int, g_id: int, db: AsyncSession
):
    new_message = Message(sender_id=sender_id, g_id=g_id, content=content)
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    return new_message


async def fetch_messages(
    g_id: int, limit: int, after_id: int, db: AsyncSession
):
    result = await db.execute(
        select(Message)
        .where(
            Message.g_id == g_id
        )
        .order_by(Message.timestamp.desc())
        .offset(after_id)
        .limit(limit)
    )
    data = result.scalars().all()

    return data
