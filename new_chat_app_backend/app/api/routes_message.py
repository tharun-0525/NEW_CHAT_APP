from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.routes_auth import get_current_user
from app.schema.message import MessageFetch
from app.services.message_services import fetch_messages
from fastapi import Query
from app.schema.response import ResponseModel
from app.services.group_services import isMember
from fastapi import HTTPException

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/{group_id}", response_model=ResponseModel)
async def get_messages(
    group_id: int,
    limit: int = Query(100, le=100),
    after_id: int = Query(0, ge=0),
    user: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if isMember(user.id, group_id) == False:
        raise HTTPException(status_code=403, detail="You are not a member of this group")
    
    messages = await fetch_messages(group_id, limit, after_id, db)
    msg = [
        MessageFetch(
            id=message.id,
            sender_id=message.sender_id,
            content=message.content,
            timestamp=message.timestamp,
        )
        for message in messages
    ]

    return {"status":"success", "data":msg}
