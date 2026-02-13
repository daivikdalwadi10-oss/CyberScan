import uuid
from typing import Optional

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..auth.jwt import decode_token
from ..database import get_db
from ..models.enterprise_models import User
from ..realtime.alert_stream import alert_manager

router = APIRouter()


async def _get_token(websocket: WebSocket) -> Optional[str]:
    token = websocket.query_params.get("token")
    if token:
        return token

    auth_header = websocket.headers.get("authorization")
    if auth_header and auth_header.lower().startswith("bearer "):
        return auth_header.split(" ", 1)[1]

    return None


@router.websocket("/ws/alerts")
async def alerts_socket(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db)
):
    token = await _get_token(websocket)
    if not token:
        await websocket.close(code=1008)
        return

    try:
        payload = decode_token(token)
    except ValueError:
        await websocket.close(code=1008)
        return

    if payload.get("type") != "access":
        await websocket.close(code=1008)
        return

    user_id = payload.get("sub")
    if not user_id:
        await websocket.close(code=1008)
        return

    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        await websocket.close(code=1008)
        return

    result = await db.execute(
        select(User).options(selectinload(User.roles)).where(User.id == user_uuid)
    )
    user = result.scalar_one_or_none()
    if not user or not bool(user.is_active) or bool(user.is_locked):
        await websocket.close(code=1008)
        return

    roles = [role.role_type.value for role in user.roles]
    await alert_manager.connect(websocket, str(user.id), roles)
    await websocket.send_json({"type": "connected", "user_id": str(user.id), "roles": roles})

    try:
        while True:
            message = await websocket.receive_json()
            msg_type = message.get("type")
            if msg_type == "ping":
                await websocket.send_json({"type": "pong"})
            elif msg_type == "ack":
                alert_id = message.get("alert_id")
                await websocket.send_json({"type": "ack_received", "alert_id": alert_id})
            else:
                await websocket.send_json({"type": "unsupported", "message": "Unknown message type"})
    except WebSocketDisconnect:
        await alert_manager.disconnect(websocket)
    except Exception:
        await alert_manager.disconnect(websocket)
        await websocket.close(code=1011)
