from __future__ import annotations

import logging
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable

from confluent_kafka import Message as ConfluentMessage
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .kafka_adapter import KafkaAdapter, KafkaRole
from .topic import Topic, TopicDir
from .utils import CitizenKError, annotate_function, function_arguments

if TYPE_CHECKING:
    from .citizenk import CitizenK

logger = logging.getLogger(__name__)


@dataclass
class KafkaEvent:
    key: str | bytes
    value: BaseModel
    topic: Topic
    partition: int
    offset: int
    timestamp: int
    headers: list[tuple[str, Any]]


DEFAULT_BATCH_TIMEOUT_SECONDS = 10.0


class Agent:
    def __init__(
        self,
        app: CitizenK,
        name: str,
        coroutine: Callable,
        topics: list[Topic],
        batch_size: int = 1,
        batch_timeout: int = DEFAULT_BATCH_TIMEOUT_SECONDS,
    ):
        self.app = app
        self.name = name

        if len(topics) == 0:
            raise CitizenKError("It doesn't make sense to have agents without topics")

        for topic in topics:
            if topic.topic_dir == TopicDir.OUTPUT:
                raise CitizenKError("Trying to consume from an output topic")
        self.topics = topics
        self.topic_names = [t.name for t in self.topics]

        if batch_size <= 0:
            raise CitizenKError("Batch size must be greater than zero")
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout

        arguments = function_arguments(coroutine)
        if "values" in arguments:
            self.return_type = "values"
        elif "events" in arguments:
            self.return_type = "events"
        else:
            raise CitizenKError("Agents can only accept values and events")
        self.inject_self = "self" in arguments
        self.coroutine = coroutine

        self.batch_queue = deque()
        self.last_offsets = defaultdict(int)
        self.last_processing_time = time.time()
        self.cycles = 0
        self.messages_processed = 0
        if self.app.auto_generate_apis:
            self._generate_apis()

    def info(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "cycles": self.cycles,
            "messages_processed": self.messages_processed,
            "messages_in_buffer": len(self.batch_queue),
        }

    def startup(self):
        for topic in self.topics:
            for partition in range(topic.partition_count):
                key = (topic.name, partition)
                self.last_offsets[key] = -1

    def _add_to_queue(self, events: list[KafkaEvent]):
        for event in events:
            if event.topic.name in self.topic_names:
                self.batch_queue.append(event)

    def _get_batch_from_queue(self):
        if len(self.batch_queue) >= self.batch_size:
            count = self.batch_size
        elif time.time() - self.last_processing_time > self.batch_timeout:
            count = len(self.batch_queue)
        else:
            return None
        return [self.batch_queue.popleft() for _ in range(count)]

    def _update_last_offsets(self, events: list[KafkaEvent]):
        for event in events:
            key = (event.topic.name, event.partition)
            last_offset = self.last_offsets[key]
            if event.offset > last_offset:
                self.last_offsets[key] = event.offset

    def _generate_apis(self):
        for topic in self.topics:

            async def endpoint(values: int):
                if self.return_type == "values":
                    result = await self.coroutine(values=values)
                else:
                    events = [
                        KafkaEvent(
                            value=v,
                            topic=topic,
                            key="bla",
                            offset=-1,
                            partition=-1,
                            timestamp=-1,
                            headers=[],
                        )
                        for v in values
                    ]
                    result = await self.coroutine(events=events)
                return result

            annotate_function(
                endpoint,
                name=f"send_to_agent_{self.name}_from_{topic.name}",
                doc=f"This endpoint sends value to agent {self.name} from topic {topic.name}",
                argument_types={"values": list[topic.value_type]},
            )

            self.app.add_api_route(
                path=f"{self.app.api_router_prefix}/agent/{self.name}/{topic.name}",
                response_class=JSONResponse,
                methods=["POST"],
                endpoint=endpoint,
            )

    @staticmethod
    def validate_messages(
        msgs: list[ConfluentMessage], topics: dict[str, Topic]
    ) -> list[KafkaEvent]:
        """Validate the incoming Kafka messages"""
        events = []
        for msg in msgs:
            topic_name = msg.topic()
            topic = topics[topic_name]
            value = topic.deserialize(msg.key(), msg.value())
            events.append(
                KafkaEvent(
                    key=msg.key(),
                    value=value,
                    topic=topic,
                    partition=msg.partition(),
                    offset=msg.offset(),
                    timestamp=msg.timestamp()[1],
                    headers=msg.headers(),
                )
            )
        return events

    async def process(self, events: list[KafkaEvent]):
        self._add_to_queue(events)
        results = []
        while True:
            events_batch = self._get_batch_from_queue()
            if not events_batch:
                return results
            self.cycles += 1
            if self.return_type == "events":
                argument = events_batch
            else:
                argument = [e.value for e in events_batch]
            self.messages_processed += len(events_batch)
            arguments = {self.return_type: argument}
            if self.inject_self:
                arguments["self"] = self
            result = await self.coroutine(**arguments)
            self._update_last_offsets(events_batch)
            self.last_processing_time = time.time()
            results.append(result)

    def __str__(self) -> str:
        return self.name


class WebSocketAgent(Agent):
    def __init__(
        self,
        app: CitizenK,
        name: str,
        coroutine: Callable,
        topics: list[Topic],
        batch_size: int = 1,
        batch_timeout: int = DEFAULT_BATCH_TIMEOUT_SECONDS,
        websocket_route: str | None = None,
    ):
        Agent.__init__(
            self,
            app=app,
            name=name,
            coroutine=coroutine,
            topics=topics,
            batch_size=batch_size,
            batch_timeout=batch_timeout,
        )
        self.websocket_route = websocket_route
        if websocket_route:
            self._add_websocket_route()
        self.active_websocket_connections: list[WebSocket] = []
        self.consumer = None

    def _add_websocket_route(self):
        """Add FastAPI websocket route"""

        @self.app.websocket(self.websocket_route)
        async def w(websocket: WebSocket):
            await websocket.accept()
            self.active_websocket_connections.append(websocket)
            self._handle_consumer()
            try:
                while True:
                    # At the moment there is only support Kafka server --> Websocket client
                    # For clinet --> Kafka use REST API
                    data = await websocket.receive_text()
                    logger.info("Received data from we socket %s: ignoring", data)
            except WebSocketDisconnect:
                self.active_websocket_connections.remove(websocket)
                self._handle_consumer()

    def info(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "cycles": self.cycles,
            "messages_processed": self.messages_processed,
            "messages_in_buffer": len(self.batch_queue),
            "connections": len(self.active_websocket_connections),
        }

    def _handle_consumer(self):
        if len(self.active_websocket_connections) > 0 and self.consumer is None:
            # Start consumer once there is at least one connection
            # No consumer group, by default consumes from all partitions latest
            # TODO: support initial offset = latest - timedelta
            self.consumer = KafkaAdapter(self.app.kafka_config, KafkaRole.CONSUMER)
            self.consumer.start_consumer(topics=self.topic_names)
            logger.debug("Started agent %s consumer", self.name)
        if len(self.active_websocket_connections) == 0 and self.consumer is not None:
            # Close consumer if there are no live connections...
            self.consumer.close()
            self.consumer = None
            logger.debug("Closed agent %s consumer", self.name)

    async def consume(self):
        if self.consumer is not None:
            msgs = self.consumer.consume(num_messages=self.batch_size, timeout=0.1)
            if len(msgs) > 0:
                logger.debug("Agent %s consumed %s messages", self.name, len(msgs))
                events = Agent.validate_messages(msgs, {t.name: t for t in self.topics})
                await self.process(events)
                return True
        return False

    async def close(self):
        if self.consumer is not None:
            self.consumer.close()
            self.consumer = None
        for connection in self.active_websocket_connections:
            await connection.close()

    def _generate_apis(self):
        for topic in self.topics:

            async def endpoint(values: int):
                result = await self.coroutine(values=values)
                await self._websocket_broadcast_result(result)
                return result

            annotate_function(
                endpoint,
                name=f"send_to_websocket_agent_{self.name}_from_{topic.name}",
                doc=f"This endpoint sends value to agent {self.name} from topic {topic.name}",
                argument_types={"values": list[topic.value_type]},
            )

            self.app.add_api_route(
                path=f"{self.app.api_router_prefix}/agent/{self.name}/{topic.name}",
                response_class=JSONResponse,
                methods=["POST"],
                endpoint=endpoint,
            )

    async def _websocket_broadcast_result(self, result: str):
        """Broadcast the agent result to all clients"""
        if result is None:
            return
        # Todo, consider using websocket.broadcast
        for connection in list(self.active_websocket_connections):
            try:
                await connection.send_text(result)
            except WebSocketDisconnect:
                logger.info("Websocket connection disconnected")
                self.active_websocket_connections.remove(connection)

    async def process(self, events: list[KafkaEvent]):
        """Process incoming events"""
        results = await Agent.process(self, events)
        for result in results:
            await self._websocket_broadcast_result(result)
        return results

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
