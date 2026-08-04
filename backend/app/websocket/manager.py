from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}


    async def connect(
        self,
        delivery_id: int,
        websocket: WebSocket
    ):

        await websocket.accept()

        if delivery_id not in self.active_connections:
            self.active_connections[delivery_id] = []

        self.active_connections[delivery_id].append(
            websocket
        )


    def disconnect(
        self,
        delivery_id: int,
        websocket: WebSocket
    ):

        if delivery_id in self.active_connections:

            if websocket in self.active_connections[delivery_id]:

                self.active_connections[delivery_id].remove(
                    websocket
                )


            if len(self.active_connections[delivery_id]) == 0:

                del self.active_connections[delivery_id]



    async def broadcast(
        self,
        delivery_id: int,
        message: dict
    ):

        if delivery_id in self.active_connections:

            for connection in self.active_connections[delivery_id]:

                await connection.send_json(
                    message
                )


manager = ConnectionManager()