from __future__ import annotations

import asyncio

from ..message_bus import MessageBus


def test_message_bus_sync_handler_called() -> None:
    bus = MessageBus()
    called = {}

    def handler(msg: dict[str, int]) -> None:
        called["val"] = msg.get("x")

    bus.subscribe("topic1", handler)
    bus.publish("topic1", {"x": 1})
    assert called.get("val") == 1


def test_message_bus_async_handler_called() -> None:
    bus = MessageBus()
    called = {}

    async def async_handler(msg: dict[str, int]) -> None:
        await asyncio.sleep(0)
        called["v"] = msg.get("y")

    bus.subscribe("topic2", async_handler)
    bus.publish("topic2", {"y": 2})

    # give event loop a moment to run created task
    asyncio.run(asyncio.sleep(0.01))
    assert called.get("v") == 2
