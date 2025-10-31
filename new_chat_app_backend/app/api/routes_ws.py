# app/messages/ws.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import json
from app.services.message_services import send_message
from app.db.session import get_db
from app.core.security import verify_token  # your JWT check
from app.core.connection_manager import manager  # your ConnectionManager
from app.schema.message import MessageOut
import asyncio

router = APIRouter()


@router.websocket("/send")
async def websocket_endpoint(
    websocket: WebSocket, user_id: int, token: str, db: AsyncSession = Depends(get_db)
):

    sender_id = verify_token(token)
    await manager.connect(sender_id["user_id"], websocket)

    try:
        while True:

            data = await websocket.receive_text()

            message_data = json.loads(data)
            sender_id = message_data["sender_id"]
            receiver_id = message_data["receiver_id"]
            content = message_data["content"]

            msg = await send_message(
                content=content,
                sender_id=int(sender_id),
                receiver_id=int(receiver_id),
                db=db,
            )
            payload = MessageOut(
                content=msg.content,
                id=msg.id,
                receiver_id=msg.receiver_id,
                sender_id=msg.sender_id,
                timestamp=msg.timestamp.isoformat() if msg.timestamp else None,
            ).dict()

            print(manager.connected_list())

            if manager.is_connected(msg.sender_id):
                print("sent to user itself")
                await manager.send_personal_message(payload, msg.sender_id)

            if manager.is_connected(msg.receiver_id):
                print("sent to intended")
                await manager.send_personal_message(payload, msg.receiver_id)

    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)


@router.get("/")
async def test_endpoint():
    return {"message": "WebSocket endpoint is running!"}
