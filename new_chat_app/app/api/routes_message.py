from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.routes_auth import get_current_user
from app.db.models import Message, User
from app.schema.message import MessageCreate, MessageOut
from app.services.message_services import send_message, fetch_messages
from fastapi import Query

router = APIRouter()

@router.get("/{with_user}")
async def get_messages(with_user: int,
                       limit: int = Query(100, le=100),
                       user: dict = Depends(get_current_user), 
                       db: AsyncSession = Depends(get_db)):
    messages = await fetch_messages(user["user_id"], with_user, limit,db)
    return messages

@router.post("/send")
async def post_message(text: MessageCreate,db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    message= Message(
        content=text.content,
        sender_id=current_user.id,
        receiver_id=text.receiver_id
    )

    await send_message(message, db)
    return message
