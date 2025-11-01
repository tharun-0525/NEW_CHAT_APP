# app/messages/ws.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import json
from app.services.message_services import send_message
from app.db.session import get_db
from app.core.security import verify_token  # your JWT check
from app.core.connection_manager import manager  # your ConnectionManager
from app.schema.message import MessageOut
from app.schema.response import ResponseModel
import asyncio

router = APIRouter()
asyncio.create_task(manager._heartbeat())

@router.websocket("/send")
async def websocket_endpoint(
    websocket: WebSocket, token: str
):
    async for db in get_db():
        user = verify_token(token)
        user_id = user["user_id"]
        await manager.connect(user_id, websocket)

        try:
            while True:

                data = await websocket.receive_text()

                message_data = json.loads(data)
                sender_id = message_data["sender_id"]
                group_id = message_data["group_id"]
                content = message_data["content"]

                if not all([sender_id, group_id, content]):
                    await websocket.send_json(
                        {"status":"failed","message": "Missing sender_id, group_id, or content"}
                    )
                    continue

                msg = await send_message(
                    content=content,
                    sender_id=int(sender_id),
                    group_id=int(group_id),
                    db=db,
                )

                payload = MessageOut(
                    content=msg.content,
                    id=msg.id,
                    group_id=msg.group_id,
                    sender_id=msg.sender_id,
                    timestamp=msg.timestamp.isoformat() if msg.timestamp else None,
                ).model_dump()

                await manager.send_message(payload, sender_id, group_id)

        except WebSocketDisconnect:
            manager.disconnect(user_id, websocket)

@router.get("/", response_model=ResponseModel)
async def test_endpoint():
    return {"message": "WebSocket endpoint is running!"}
