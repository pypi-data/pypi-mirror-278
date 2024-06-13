import asyncio
import json
import logging
import os
import signal
import socket
import threading
import time
from datetime import datetime
from enum import Enum
from functools import wraps
from typing import Any, Callable, Dict, Optional, Union

import httpx
from confluent_kafka import KafkaException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .agent import DEFAULT_BATCH_TIMEOUT_SECONDS, Agent, WebSocketAgent
from .kafka_adapter import KafkaAdapter, KafkaConfig, KafkaRole
from .topic import SchemaType, Topic, TopicDir
from .utils import CitizenKError

logger = logging.getLogger(__name__)


class AppType(Enum):
    SOURCE = 1
    SINK = 2
    TRANSFORM = 3


class CitizenK(FastAPI):
    def __init__(
        self,
        kafka_config: KafkaConfig,
        app_name: str,
        app_type: AppType = AppType.SOURCE,
        consumer_group_init_offset: str = "latest",
        consumer_group_auto_commit: bool = True,
        schema_registry_url: Optional[str] = None,
        auto_generate_apis: bool = True,
        max_processing_cycle_ms: int = 5 * 1000,
        api_router_prefix: str = "",
        api_port: Optional[int] = None,
        agents_in_thread: bool = False,
        consumer_extra_config: Optional[dict[str, str]] = None,
        producer_extra_config: Optional[dict[str, str]] = None,
        exit_on_agent_exception: bool = True,
        log_periodic_stats: bool = True,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.app_name = app_name
        self.app_type = app_type
        self.kafka_config = kafka_config
        self.consumer_group_init_offset = consumer_group_init_offset
        self.consumer_group_auto_commit = consumer_group_auto_commit
        self.schema_registry_url = schema_registry_url
        self.auto_generate_apis = auto_generate_apis
        self.max_processing_cycle_ms = max_processing_cycle_ms
        self.api_router_prefix = api_router_prefix
        self.api_port = api_port
        self.consumer_extra_config = consumer_extra_config
        self.producer_extra_config = producer_extra_config
        self.exit_on_agent_exception = exit_on_agent_exception
        self.log_periodic_stats = log_periodic_stats

        self.producer = None
        self.consumer = None
        self._started = datetime.utcnow()

        self.total_batch_size = 0
        self.consumer_topics = set()
        self.topics = {}
        self.agents = {}
        self.websocket_agents = {}
        self.agents_in_thread = agents_in_thread
        self.background_loop = None
        self.background_thread = None
        self.main_consumer_loop_task = None
        self.monitor_loop_task = None
        self.periodic_stats = dict()
        self.init_periodic_stats()

        self.add_event_handler("startup", self.startup)
        self.add_event_handler("shutdown", self.shutdown)
        if auto_generate_apis:
            self._generate_apis()

    def _generate_apis(self):
        @self.get(
            f"{self.api_router_prefix}/stats/producer", response_class=JSONResponse
        )
        def get_producer_stats():
            """Get the producer stats"""
            if self.producer is not None:
                return self.producer.last_stats
            return {}

        @self.get(
            f"{self.api_router_prefix}/stats/consumer", response_class=JSONResponse
        )
        def get_consumer_stats():
            """Get the producer stats"""
            if self.consumer is not None:
                return self.consumer.last_stats
            return {}

        def get_info():
            """Get the service info"""
            hosts = {}
            assignments = {}
            lags = {}
            if self.consumer is not None:
                hosts = self.consumer.get_group_members()
                assignments = self.consumer.assigned_partitions
                lags = self.consumer.get_group_lag()
            return {
                "started": self._started,
                "app": {
                    "name": self.app_name,
                    "title": self.title,
                    "description": self.description,
                    "version": self.version,
                },
                "host": socket.gethostbyname(socket.gethostname()),
                "topics": [t.info(lags, assignments) for t in self.topics.values()],
                "agents": [a.info() for a in self.agents.values()],
                "websocket_agents": [a.info() for a in self.websocket_agents.values()],
                "hosts": {f"{tp[0]}-{tp[1]}": h for tp, h in hosts.items()},
            }

        @self.get(f"{self.api_router_prefix}/info", response_class=JSONResponse)
        def get_service_info():
            return get_info()

        @self.get(f"{self.api_router_prefix}/allinfo", response_class=JSONResponse)
        @self.broadcast_router()
        async def get_all_info(request: Request):
            return get_info()

    def is_sink(self) -> bool:
        return self.app_type == AppType.SINK

    def fast_status(self) -> bool:
        """Return the status without actively checking Kafka connectivity"""

        # Check Kafka consumer error
        if self.consumer is not None:
            if self.consumer.kafka_error is not None:
                return False

        # Check Kafka producer error
        if self.producer is not None:
            if self.producer.kafka_error is not None:
                return False

        # Check background thread status
        if self.background_thread is not None:
            if not self.background_thread.is_alive():
                return False

        # Check consumer task status
        if self.main_consumer_loop_task is not None:
            if self.main_consumer_loop_task.done():
                return False

        # Check consumer task status
        if self.monitor_loop_task is not None:
            if self.monitor_loop_task.done():
                return False

        return True

    def status(self) -> bool:
        """Return the status, plus actively checking Kafka connectivity"""

        if not self.fast_status():
            return False

        if self.consumer is not None:
            # Use list topics to see if the broker is still up
            try:
                self.consumer.get_all_broker_topics()
            except KafkaException:
                logger.error("Failed to get topics from broker")
                return False

        if self.producer is not None:
            # Use list topics to see if the broker is still up
            try:
                self.producer.get_all_broker_topics()
            except KafkaException:
                logger.error("Failed to get topics from broker")
                return False
        return True

    def startup(self):
        """CitizenK startup. Called on FastAPI startup"""
        logger.info("CitizenK starting up...")

        # Find all consumer topics
        for agent in self.agents.values():
            self.consumer_topics.update({t.name for t in agent.topics})
            self.total_batch_size += agent.batch_size

        # Create and start consumer
        if len(self.consumer_topics) > 0:
            if self.app_type == AppType.SOURCE:
                raise CitizenKError("Trying to consume topics in a source app")
            self.consumer = KafkaAdapter(
                config=self.kafka_config,
                role=KafkaRole.CONSUMER,
                consumer_group_name=self.app_name,
                consumer_group_init_offset=self.consumer_group_init_offset,
                consumer_group_auto_commit=self.consumer_group_auto_commit,
                extra_config=self.consumer_extra_config,
            )
            self.consumer.start_consumer(list(self.consumer_topics))

        # Create producer
        if self.app_type in [AppType.SOURCE, AppType.TRANSFORM]:
            self.producer = KafkaAdapter(
                config=self.kafka_config,
                role=KafkaRole.PRODUCER,
                extra_config=self.producer_extra_config,
            )

        # Check that all topics exist in broker
        broker = self.producer if self.consumer is None else self.consumer
        broker_topics = broker.get_all_broker_topics()
        for topic_name, topic in self.topics.items():
            if topic_name not in broker_topics:
                raise CitizenKError(f"Can't find topic {topic_name} in broker")
            # Set num partitions and replicas in topic. Might be useful...
            topic.startup(broker_topics[topic_name])

        for agent in self.agents.values():
            agent.startup()

        # Start Main consumer loop if there is any consumer
        # Normal global consumer (with group)
        # Websocket consumers (no group)
        if self.consumer is not None or len(self.websocket_agents) > 0:

            if self.agents_in_thread:
                # Start in a thread
                self.background_loop = asyncio.new_event_loop()
                self.background_thread = threading.Thread(
                    target=self._background_consumer_thread,
                    args=(self.background_loop,),
                )
                self.background_thread.start()
                self.main_consumer_loop_task = asyncio.run_coroutine_threadsafe(
                    self._main_consumer_loop(), self.background_loop
                )
            else:
                # Start in a task
                self.main_consumer_loop_task = asyncio.create_task(
                    self._main_consumer_loop()
                )
            self.monitor_loop_task = asyncio.create_task(self._monitor_loop())

    async def shutdown(self):
        """CitizenK shutdown called on FastAPI shutown"""
        logger.info("CitizenK shutting down...")
        if self.consumer is not None:
            logger.info("Shutting down consumer...")
            self.consumer.close()
            self.consumer = None
        if self.producer is not None:
            logger.info("Shutting down producer...")
            self.producer.close()
            self.producer = None
        for agent in self.websocket_agents.values():
            logger.info("Shutting down websocket agents...")
            await agent.close()
        if self.main_consumer_loop_task is not None:
            logger.info("Shutting down main consumer loops...")
            self.main_consumer_loop_task.cancel()
        if self.background_loop is not None:
            logger.info("Shutting down background loop...")
            self.background_loop.stop()

    def _background_consumer_thread(self, loop: asyncio.BaseEventLoop):
        logger.info("CitizenK background consumer thread started...")
        asyncio.set_event_loop(loop)
        try:
            loop.run_forever()
        except asyncio.CancelledError as exp:
            logger.error("Background consumer loop cancelled %s", exp)
            return
        logger.error("Background consumer loop stopped")

    async def _monitor_loop(self):
        """Periodic task that checks Kafka status, and kills the process"""
        logger.info("CitizenK main monitor loop started...")
        while True:
            await asyncio.sleep(60)
            # Check status
            start_time = time.time()
            if not self.status():
                await self.shutdown()
                os.kill(os.getpid(), signal.SIGINT)
                await asyncio.sleep(60)
                os.kill(os.getpid(), signal.SIGKILL)
            duration = 1000 * (time.time() - start_time)
            if self.log_periodic_stats:
                logger.info(
                    "CitizenK OK. Check took %s ms. Idle cycles %s/%s time: %s/%s ms",
                    duration,
                    self.periodic_stats["idle_cycles"],
                    self.periodic_stats["total_cycles"],
                    self.periodic_stats["idle_duration"],
                    self.periodic_stats["idle_duration"]
                    + self.periodic_stats["processing_duration"],
                )
            self.init_periodic_stats()

    def _commit_offsets(self):
        agents_offsets = []
        for agent in self.agents.values():
            agents_offsets.append(agent.last_offsets)
        offsets_to_commit = []
        for topic in self.topics.values():
            offsets_to_commit += topic.offsets_to_commit(agents_offsets)
        self.consumer.commit(offsets_to_commit)

    def init_periodic_stats(self):
        self.periodic_stats = {
            "start_time": time.time(),
            "end_time": time.time(),
            "idle_duration": 0,
            "processing_duration": 0,
            "total_cycles": 0,
            "idle_cycles": 0,
        }

    async def _consumer_step(self):
        consumed = False
        start_time = time.time()
        duration = 1000 * (start_time - self.periodic_stats["end_time"])
        self.periodic_stats["idle_duration"] += duration
        self.periodic_stats["total_cycles"] += 1
        # Consume from global consumer
        if self.consumer is not None:
            msgs = self.consumer.consume(
                num_messages=self.total_batch_size, timeout=0.1
            )
            if len(msgs) > 0:
                consumed = True
            else:
                self.periodic_stats["idle_cycles"] += 1

            events = Agent.validate_messages(msgs, self.topics)
            for agent in self.agents.values():
                await agent.process(events)
            if not self.consumer_group_auto_commit:
                self._commit_offsets()

        # Consume from websocket agents consumers (no group)
        for agent in self.websocket_agents.values():
            if await agent.consume():
                consumed = True

        end_time = time.time()
        duration = 1000 * (end_time - start_time)
        self.periodic_stats["processing_duration"] += duration
        self.periodic_stats["end_time"] = end_time

        if duration > self.max_processing_cycle_ms:
            logger.error(
                "Processing cycle took %s ms > %s",
                duration,
                self.max_processing_cycle_ms,
            )
        return consumed

    async def _main_consumer_loop(self):
        """Main Kafka consumer loop which invokes the process agents"""
        logger.debug("CitizenK main processing loop started...")
        while True:
            # Check if consumer was deleted
            if self.consumer is None and len(self.consumer_topics) > 0:
                break

            try:
                consumed = await self._consumer_step()
                # Poll producer
                if self.producer is not None:
                    self.producer.poll()

                if consumed:
                    # Just to give other tasks opportunity to run
                    await asyncio.sleep(0)
                else:
                    # Wait a bit until messages arrive
                    logger.debug("No kafka events, sleeping")
                    await asyncio.sleep(1)

            except Exception as exp:
                logger.exception("Exception in main loop: %s", str(exp))
                if self.exit_on_agent_exception:
                    break
                await asyncio.sleep(3)

    def topic(
        self,
        name: str,
        value_type: BaseModel,
        topic_dir: TopicDir = TopicDir.INPUT,
        schema_type: SchemaType = SchemaType.JSON,
        subject_name: Optional[str] = None,
        partitioner: Callable[[Union[str, bytes]], int] = None,
    ) -> Topic:
        if name in self.topics:
            raise CitizenKError(f"Topic {name} already exists")

        if self.app_type == AppType.SOURCE and topic_dir == TopicDir.INPUT:
            raise CitizenKError("Can't use input topics in a source app")

        if self.app_type == AppType.SINK and topic_dir == TopicDir.OUTPUT:
            raise CitizenKError("Can't use output topics in a sink app")

        t = Topic(
            self,
            name=name,
            value_type=value_type,
            topic_dir=topic_dir,
            schema_type=schema_type,
            subject_name=subject_name,
            partitioner=partitioner,
        )
        self.topics[name] = t
        logger.debug("Adding topic %s", name)
        return t

    def agent(
        self,
        topics: Union[Topic, list[Topic]],
        batch_size: int = 1,
        batch_timeout: int = DEFAULT_BATCH_TIMEOUT_SECONDS,
        websocket_route: Optional[str] = None,
    ) -> Callable:
        """
        decorates a function of this type:
        async def processing_agent(events: list[KafkaEvent])

        Or this type:
        async def processing_agent(values: list[BaseModel])

        Both of these functions consumes from in_topics and produce to out_topics
        """

        if self.app_type == AppType.SOURCE:
            raise CitizenKError("There is no point in creating agents in a source app")

        if isinstance(topics, Topic):
            topics = [topics]

        def decorator(f):
            @wraps(f)
            async def wrapper(*args, **kwargs):
                return await f(*args, **kwargs)

            agent_name = f.__name__
            if websocket_route is None:
                self.agents[agent_name] = Agent(
                    app=self,
                    name=agent_name,
                    coroutine=f,
                    topics=topics,
                    batch_size=batch_size,
                    batch_timeout=batch_timeout,
                )
            else:
                self.websocket_agents[agent_name] = WebSocketAgent(
                    app=self,
                    name=agent_name,
                    coroutine=f,
                    topics=topics,
                    batch_size=batch_size,
                    batch_timeout=batch_timeout,
                    websocket_route=websocket_route,
                )

            logger.debug("Adding agent %s %s", agent_name, topics)
            return wrapper

        return decorator

    def _find_member_host(
        self, topic: Topic, key: str = None, partition_id: int = None
    ):
        if partition_id is None:
            # Get the partition for this key and topic
            if topic.partitioner is not None:
                partition_id = topic.partitioner(key)
            else:
                partition_id = self.consumer.get_partition_id(topic.name, key)
            if partition_id is None:
                raise CitizenKError("Failed to get partition id from key")

        logger.debug(
            "Partition id for topic %s and key %s is %s",
            topic.name,
            key,
            partition_id,
        )

        members = self.consumer.get_group_members()
        host = members.get((topic.name, partition_id), None)
        if host is None:
            raise CitizenKError(
                f"Can't find a host for this request {topic.name}/{partition_id}"
            )
        return host

    async def request(
        self,
        topic: Topic,
        key: str = None,
        partition_id: int = None,
        method: str = "GET",
        path: str = "",
        params: Dict[str, Any] = None,
        data: Any = None,
        timeout: float = 10.0,
    ):
        """Used for exchanging data between workers of the same app
        Calls the given API of the worker (consumer group member) that processes
        the partition_id / key of the topic.
        If the worker is this worker, then it would still call it...
        """
        host = self._find_member_host(topic, str(key), partition_id)
        # Send the request to the host
        port = "" if self.api_port is None else f":{self.api_port}"

        url = f"http://{host}{port}{path}"
        logger.debug("Routing request to %s", url)
        async with httpx.AsyncClient() as client:
            r = await client.request(
                method=method, url=url, params=params, content=data, timeout=timeout
            )
            r.raise_for_status()
            try:
                return r.json()
            except json.JSONDecodeError:
                return r.text

    def topic_router(
        self, topic: Topic, match_info: str, timeout: float = 10.0
    ) -> Callable:
        """
        routes the request to the right worker based on topic, key:
        assumes default partitioner... Used mainly for statefule services where
        Each worker holds some state / key
        """

        def decorator(f):
            @wraps(f)
            async def wrapper(*args, **kwargs):
                if self.consumer is None or self.consumer.consumer_group_name is None:
                    raise CitizenKError(
                        "Topic routing doesn't make sense without a consumer group"
                    )

                if "request" not in kwargs or not isinstance(
                    kwargs["request"], Request
                ):
                    raise CitizenKError(
                        "Topic routing endpoint must include a request object"
                    )

                if match_info is not None and match_info not in kwargs:
                    raise CitizenKError(
                        "Topic routing endpoint must include the match_info key"
                    )

                # Return if reached the final host
                request = kwargs["request"]
                params = dict(request.query_params)
                if "citizenk_stop_propogate" in params:
                    return await f(*args, **kwargs)
                params["citizenk_stop_propogate"] = True

                # Try to convert key to string... to support int as well
                key = str(kwargs[match_info])
                host = self._find_member_host(topic, key, None)

                # Check if this worker is assigned to this partition
                current_host = socket.gethostbyname(socket.gethostname())
                if host == current_host:
                    return await f(*args, **kwargs)

                # Route the request to the host
                url = httpx.URL(str(request.url)).copy_with(host=host)
                # Mainly used for testing purposes
                if self.api_port is not None:
                    url = url.copy_with(port=self.api_port)
                logger.debug("Routing request to %s", url)
                async with httpx.AsyncClient() as client:
                    r = await client.request(
                        method=request.method,
                        url=url,
                        headers=request.headers.raw,
                        params=params,
                        content=await request.body(),
                        timeout=timeout,
                    )
                    r.raise_for_status()
                    try:
                        return r.json()
                    except json.JSONDecodeError:
                        return r.text

            return wrapper

        return decorator

    async def broadcast_request(
        self,
        method: str = "GET",
        path: str = "",
        params: Dict[str, Any] = None,
        data: Any = None,
        timeout: float = 10.0,
    ):
        """Used for exchanging data between workers of the same app
        Calls the given API of the worker (consumer group member) that processes
        the partition_id / key of the topic.
        If the worker is this worker, then it would still call it...
        """
        members = self.consumer.get_group_members()
        hosts = set(members.values())

        # Send the request to the host
        port = "" if self.api_port is None else f":{self.api_port}"

        # Route the request to all hosts
        response = {}
        async with httpx.AsyncClient() as client:
            for host in hosts:
                url = f"http://{host}{port}{path}"
                logger.debug("Broadcast to %s", url)
                # Add leader argument to host leader
                r = await client.request(
                    method=method,
                    url=url,
                    params=params,
                    content=data,
                    timeout=timeout,
                )
                r.raise_for_status()
                response[host] = r.json()
        return response

    def broadcast_router(self, timeout: float = 10.0) -> Callable:
        """
        routes the request to the all the workers and aggregate the JSON response
        """

        def decorator(f):
            @wraps(f)
            async def wrapper(*args, **kwargs):
                if self.consumer is None or self.consumer.consumer_group_name is None:
                    raise CitizenKError(
                        "Broadcast routing doesn't make sense without a consumer group"
                    )

                if "request" not in kwargs or not isinstance(
                    kwargs["request"], Request
                ):
                    raise CitizenKError(
                        "Broadcast routing endpoint must include a request object"
                    )

                if not asyncio.iscoroutinefunction(f):
                    raise CitizenKError("Broadcast endpoint must be async")

                # Return if reached the final host
                request = kwargs["request"]
                params = dict(request.query_params)
                if "citizenk_stop_propogate" in params:
                    if "leader" in f.__annotations__:
                        kwargs["leader"] = False
                    return await f(*args, **kwargs)
                params["citizenk_stop_propogate"] = True
                if "leader" in f.__annotations__:
                    kwargs["leader"] = True

                body = await request.body()
                members = self.consumer.get_group_members()
                hosts = set(members.values())
                current_host = socket.gethostbyname(socket.gethostname())
                if len(hosts) == 0:
                    logger.error("couldn't find any hosts to route the request to")
                    return {}

                # Route the request to all hosts
                response = {}
                async with httpx.AsyncClient() as client:
                    for host in hosts:
                        if host == current_host:
                            logger.debug("%s is host leader", host)
                            response[host] = await f(*args, **kwargs)
                            continue
                        logger.debug("%s is not host leader", host)
                        url = httpx.URL(str(request.url)).copy_with(host=host)
                        # Mainly used for testing purposes
                        if self.api_port is not None:
                            url = url.copy_with(port=self.api_port)
                        logger.debug("Broadcast to %s", url)
                        # Add leader argument to host leader
                        r = await client.request(
                            method=request.method,
                            url=url,
                            headers=request.headers.raw,
                            params=params,
                            content=body,
                            timeout=timeout,
                        )
                        r.raise_for_status()
                        response[host] = r.json()
                return response

            return wrapper

        return decorator
