from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.manager import manager


router = APIRouter(
    tags=["WebSocket"]
)


@router.websocket(
    "/ws/tracking/{delivery_id}"
)
async def tracking_socket(
    websocket: WebSocket,
    delivery_id: int
):

    await manager.connect(
        delivery_id,
        websocket
    )

    try:

        while True:

            data = await websocket.receive_json()


            await manager.broadcast(
                delivery_id,
                data
            )


    except WebSocketDisconnect:

        manager.disconnect(
            delivery_id,
            websocket
        )