import asyncio
import logging
from collections import defaultdict
from typing import Dict, List, Callable, Awaitable, Optional
from cerebellum.cognition.runtime.types import Message

logger = logging.getLogger("cerebellum.runtime.event_bus")

Handler = Callable[[Message], Awaitable[None]]

class MessageBus:
    """
    Bus de mensajes asíncrono que desacopla la publicación de la entrega.
    """
    def __init__(self):
        self._subscribers: Dict[str, List[Handler]] = defaultdict(list)
        self._queue: asyncio.Queue[Message] = asyncio.Queue()

    def subscribe(self, topic: str, handler: Handler) -> None:
        """Suscribe un handler a un tópico específico."""
        self._subscribers[topic].append(handler)
        logger.debug(f"Subscribed handler to topic: {topic}")

    async def publish(self, message: Message) -> None:
        """Encola un mensaje para ser procesado."""
        await self._queue.put(message)
        logger.debug(f"Message published to queue: {message.topic} (from {message.sender})")

    async def next_message(self, timeout_s: float) -> Optional[Message]:
        """Obtiene el próximo mensaje de la cola con un timeout."""
        try:
            return await asyncio.wait_for(self._queue.get(), timeout=timeout_s)
        except (asyncio.TimeoutError, TimeoutError):
            return None

    async def deliver(self, message: Message) -> None:
        """Entrega un mensaje a todos sus suscriptores registrados."""
        # Se entrega a los suscriptores del tópico específico y también a los de 'broadcast' o '*'
        handlers = self._subscribers.get(message.topic, []) + self._subscribers.get("*", [])
        
        if not handlers:
            logger.debug(f"No handlers found for topic: {message.topic}")
            return

        tasks = [handler(message) for handler in handlers]
        await asyncio.gather(*tasks)
        self._queue.task_done()