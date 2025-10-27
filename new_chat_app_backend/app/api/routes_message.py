from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.routes_auth import get_current_user
from app.schema.message import MessageCreate, MessageFetch
from app.services.message_services import send_message, fetch_messages
from fastapi import Query
from app.schema.response import ResponseModel

router = APIRouter()

@router.get("/{with_user}")
async def get_messages(with_user: int,
                    limit: int = Query(100, le=100),
                    after_id: int = Query(0, ge=0),
                    user: int = Depends(get_current_user), 
                    db: AsyncSession = Depends(get_db)):
    messages = await fetch_messages(user, with_user, limit, after_id, db)
    msg= [MessageFetch(id= message.id, sender_id= message.sender_id, receiver_id= message.receiver_id, content= message.content, timestamp= message.timestamp) for message in messages]
    
    return ResponseModel(status="success", data=msg)

@router.post("/send")
async def post_message(text: MessageCreate,db: AsyncSession = Depends(get_db),current_user: int = Depends(get_current_user)):

    await send_message(content=text.content,receiver_id=text.receiver_id,sender_id=current_user, db=db)
    
    return ResponseModel(status="success")
