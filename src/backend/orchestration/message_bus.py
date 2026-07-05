from __future__ import annotations

import asyncio
from typing import Any, Callable, Dict, List


class MessageBus:
    """Simple in-process pub/sub message bus for progress events.

    The bus is intentionally lightweight and sync/async-friendly. Handlers
    may be sync callables or async callables.
    """

    def __init__(self) -> None:
        self._handlers: Dict[str, List[Callable[[Dict[str, Any]], Any]]] = {}

    def subscribe(self, topic: str, handler: Callable[[Dict[str, Any]], Any]) -> None:
        self._handlers.setdefault(topic, []).append(handler)

    def unsubscribe(self, topic: str, handler: Callable[[Dict[str, Any]], Any]) -> None:
        handlers = self._handlers.get(topic)
        if handlers and handler in handlers:
            handlers.remove(handler)

    def publish(self, topic: str, message: Dict[str, Any]) -> None:
        handlers = list(self._handlers.get(topic, []))
        for h in handlers:
            result = h(message)
            if asyncio.iscoroutine(result):
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = None
                if loop is None:
                    asyncio.run(result)
                else:
                    asyncio.create_task(result)
