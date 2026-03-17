import asyncio
import logging
import uuid
from typing import Dict, List, Optional, Any, Callable, Awaitable
from cerebellum.cognition.runtime.event_bus import MessageBus
from cerebellum.cognition.runtime.types import Message, CognitiveContext, RuntimeConfig

logger = logging.getLogger("cerebellum.runtime.cognitive_runtime")

class CognitiveModule:
    """
    Clase base para todos los módulos que se conectan al runtime.
    """
    def __init__(self, name: str):
        self.name = name
        self.subscriptions: List[str] = [name] # Por defecto se suscribe a su propio nombre
        self._runtime: Optional['CognitiveRuntime'] = None
        self._context: Optional[CognitiveContext] = None

    def _bind_runtime(self, runtime: 'CognitiveRuntime'):
        self._runtime = runtime

    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        """Handler principal de mensajes para el módulo."""
        pass

    async def on_start(self, context: CognitiveContext) -> None:
        """Gancho de inicio del módulo."""
        pass

    async def on_stop(self, context: CognitiveContext) -> None:
        """Gancho de parada del módulo."""
        pass

    async def publish(self, topic: str, payload: Dict[str, Any], correlation_id: Optional[str] = None):
        """Publica un mensaje al bus a través del runtime."""
        if not self._runtime:
            raise RuntimeError(f"Module {self.name} is not bound to a runtime.")
        
        message = Message(
            id=str(uuid.uuid4()),
            sender=self.name,
            receiver="broadcast",
            topic=topic,
            payload=payload,
            correlation_id=correlation_id or (self._context.run_id if self._context else None)
        )
        await self._runtime.publish(message)

class CognitiveRuntime:
    """
    Motor principal que gestiona el ciclo de vida y la coreografía de mensajes.
    Inspirado en el patrón de AgentRuntime solicitado por el USER.
    """
    def __init__(
        self,
        bus: MessageBus,
        config: Optional[RuntimeConfig] = None
    ):
        self._bus = bus
        self._config = config or RuntimeConfig()
        self._modules: Dict[str, CognitiveModule] = {}
        self._context: Optional[CognitiveContext] = None

    @property
    def context(self) -> CognitiveContext:
        if self._context is None:
            raise RuntimeError("Runtime not started. Call start(run_id=...) first.")
        return self._context

    def register(self, module: CognitiveModule) -> None:
        """Registra un módulo cognitivo en el bus."""
        self._modules[module.name] = module
        module._bind_runtime(self)

        async def handler(msg: Message) -> None:
            if self._context:
                # Inyectamos el contexto actual en el módulo antes de procesar
                module._context = self._context
                await module.on_message(msg, self._context)

        # Suscribimos el módulo a todos los tópicos que le interesan
        for topic in module.subscriptions:
            self._bus.subscribe(topic, handler)
            
        logger.info(f"Module registered: {module.name} (Subscriptions: {module.subscriptions})")

    async def publish(self, message: Message) -> None:
        """Publica un mensaje al bus."""
        await self._bus.publish(message)

    async def start(self, run_id: Optional[str] = None, metadata: Optional[dict] = None) -> None:
        """Inicia el runtime y todos sus módulos."""
        rid = run_id or str(uuid.uuid4())
        self._context = CognitiveContext(run_id=rid, metadata=metadata or {})
        logger.info(f"Starting Cognitive Runtime [run_id={rid}]")
        
        for m in self._modules.values():
            await m.on_start(self._context)

    async def stop(self) -> None:
        """Detiene el runtime y todos sus módulos."""
        if self._context is None:
            return
        
        logger.info(f"Stopping Cognitive Runtime [run_id={self._context.run_id}]")
        for m in self._modules.values():
            await m.on_stop(self._context)
        self._context = None

    async def run_until_idle(self) -> int:
        """
        Ciclo principal de consumo: procesa mensajes hasta que el bus quede vacío.
        Devuelve el número de mensajes procesados.
        """
        processed = 0
        idle_grace = self._config.idle_grace_ms / 1000.0

        logger.debug("Runtime entering idle loop...")
        while processed < self._config.max_messages:
            msg = await self._bus.next_message(timeout_s=idle_grace)
            if msg is None:
                break
            processed += 1
            await self._bus.deliver(msg)

        if processed > 0:
            logger.info(f"Cycle completed. Processed {processed} messages.")
        return processed
