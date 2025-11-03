from fastapi import WebSocket
from typing import Dict, List
import json
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.group_services import getGroups
from app.db.session import get_db
from fastapi import Depends

class ConnectionManager:
    def __init__(self):
        self.room_connections: Dict[int, set[int]] = {}
        self.active_connections: Dict[int, set[WebSocket]] = {}
    
    async def connect(self, user_id: int, websocket: WebSocket, db: AsyncSession):
        await websocket.accept()
        
        self.active_connections.setdefault(user_id, set()).add(websocket)
        
        groups = await getGroups(user_id, db)
        for group in groups:
            group_id = group.id
            self.room_connections.setdefault(group_id, set()).add(user_id)

    def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
                for _, users in self.room_connections.items():
                    if user_id in users:
                        users.remove(user_id)

    async def send_message(self, message: dict, user_id: int, group_id: int):
        if self.room_connections[group_id]:
            dead_sockets = set()
            for uid in self.room_connections[group_id]:
                for ws in self.active_connections[uid]:
                    try:
                        await ws.send_json(message)
                    except Exception:
                        dead_sockets.add(ws)

            for ws in dead_sockets:
                self.disconnect(user_id, ws)

    def connected_list(self) -> List[int]:
        return self.active_connections

    async def _heartbeat(self):
        while True:
            for user_id, websockets in self.active_connections.items():
                dead_sockets = set()
                for ws in websockets:
                    try:
                        await ws.send_json({"status": "success", "message": "ping"})
                    except Exception:
                        dead_sockets.add(ws)

                for ws in dead_sockets:
                    self.disconnect(user_id, ws)
            await asyncio.sleep(30)


manager = ConnectionManager()
