import asyncio
import logging
from dataclasses import dataclass
from typing import Iterable

from fastapi import WebSocket

logger = logging.getLogger("alerts")


@dataclass
class AlertConnection:
    websocket: WebSocket
    user_id: str
    roles: list[str]


class AlertConnectionManager:
    def __init__(self) -> None:
        self._connections: list[AlertConnection] = []
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, user_id: str, roles: list[str]) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections.append(AlertConnection(websocket=websocket, user_id=user_id, roles=roles))
        logger.info('{"event":"ws_connect","user_id":"%s"}' % user_id)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self._connections = [conn for conn in self._connections if conn.websocket != websocket]
        logger.info("{\"event\":\"ws_disconnect\"}")

    async def broadcast(self, message: dict, roles: Iterable[str] | None = None) -> None:
        targets = await self._get_targets(roles)
        for conn in targets:
            await self._safe_send(conn.websocket, message)

    async def _get_targets(self, roles: Iterable[str] | None) -> list[AlertConnection]:
        async with self._lock:
            connections = list(self._connections)
        if not roles:
            return connections
        role_set = set(roles)
        return [conn for conn in connections if role_set.intersection(conn.roles)]

    async def _safe_send(self, websocket: WebSocket, message: dict) -> None:
        try:
            await websocket.send_json(message)
        except Exception:
            logger.exception("{\"event\":\"ws_send_error\"}")
            await self.disconnect(websocket)


alert_manager = AlertConnectionManager()


async def broadcast_alert_created(payload: dict, roles: Iterable[str] | None = None) -> None:
    await alert_manager.broadcast({"type": "alert_created", "payload": payload}, roles)


async def broadcast_alert_updated(payload: dict, roles: Iterable[str] | None = None) -> None:
    await alert_manager.broadcast({"type": "alert_updated", "payload": payload}, roles)
