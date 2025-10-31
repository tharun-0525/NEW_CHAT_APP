from fastapi import WebSocket
from typing import Dict, List
import json
import asyncio


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, set[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            dead_sockets = set()
            for ws in self.active_connections[user_id]:
                try:
                    await ws.send_json(message)
                except Exception:
                    dead_sockets.add(ws)

            for ws in dead_sockets:
                self.disconnect(user_id, ws)

    def is_connected(self, user_id: int) -> bool:
        return user_id in self.active_connections

    def connected_list(self) -> List[int]:
        return self.active_connections

    async def _heartbeat(self):
        while True:
            print(self.active_connections)
            for user_id, websockets in self.active_connections.items():
                dead_sockets = set()
                for ws in websockets:
                    try:
                        print("Sending heartbeat to user:", user_id)
                        await ws.send_json({"status": "success", "message": "ping"})
                    except Exception:
                        dead_sockets.add(ws)

                for ws in dead_sockets:
                    self.disconnect(user_id, ws)
            await asyncio.sleep(30)


manager = ConnectionManager()
