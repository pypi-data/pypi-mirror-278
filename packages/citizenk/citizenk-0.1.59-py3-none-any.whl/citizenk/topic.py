from __future__ import annotations

import json
import logging
import time
from collections import defaultdict
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable

from confluent_kafka import TopicPartition
from confluent_kafka.schema_registry import Schema, SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer, AvroSerializer
from confluent_kafka.serialization import (
    MessageField,
    SerializationContext,
    SerializationError,
)
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError

from .utils import CitizenKError, annotate_function

if TYPE_CHECKING:
    from .citizenk import CitizenK

logger = logging.getLogger(__name__)


class JSONSchema(BaseModel):
    model_config = {
        # This allows adding new optional properites to the schema
        "json_schema_extra": {"additionalProperties": False}
    }


class TopicDir(Enum):
    INPUT = 1
    OUTPUT = 2
    BIDIR = 3


class SchemaType(Enum):
    JSON = 1
    AVRO = 2
    PROTOBUF = 3


class Topic:
    MAX_KEYS_IN_STAT = 10

    def __init__(
        self,
        app: CitizenK,
        name: str,
        value_type: BaseModel,
        topic_dir: TopicDir = TopicDir.INPUT,
        schema_type: SchemaType = SchemaType.JSON,
        subject_name: str | None = None,
        partitioner: Callable[[str | bytes]] = None,
    ):
        self.app = app
        self.name = name
        self.value_type = value_type
        self.topic_dir = topic_dir

        # Schema stuff
        self.schema_type = schema_type
        self.subject_name = f"{name}-value" if subject_name is None else subject_name
        self.schema_id = None

        # Partitioner
        self.partitioner = partitioner
        self.partition_count = None
        if self.app.auto_generate_apis:
            self._generate_apis()

        # Offsets last committed
        self.last_committed_offset = defaultdict(int)

        # Register topic schema
        self.serializer = None
        self.serializer_context = None
        self.deserializer = None
        self._manage_schema()

        # Stats
        self.replica_count = None
        self.messages_sent = 0
        self.messages_received = 0
        self.validation_errors = 0
        self.last_message_sent = None
        self.last_message_received = None
        self.sent_keys_sample = defaultdict(int)
        self.receive_keys_sample = defaultdict(int)

    def startup(self, confluent_topic):
        self.partition_count = len(confluent_topic.partitions)
        self.replica_count = len(confluent_topic.partitions[0].replicas)
        for partition in range(self.partition_count):
            self.last_committed_offset[partition] = -1

    def info(self, lags: dict[str, int] = {}, assignments: dict[str, list[int]] = {}):
        topic_info = {
            "name": self.name,
            "dir": self.topic_dir.name,
            "value": self.value_type.__name__,
            "subject": self.subject_name,
            "schema_type": self.schema_type.name,
            "partitions": self.partition_count,
            "replicas": self.replica_count,
            "sent": self.messages_sent,
            "received": self.messages_received,
            "sent_keys_sample": {
                k: round(time.time() - v) for k, v in self.sent_keys_sample.items()
            },
            "receive_keys_sample": {
                k: round(time.time() - v) for k, v in self.receive_keys_sample.items()
            },
            "validation_errors": self.validation_errors,
        }
        if self.name in lags:
            topic_info["lag"] = lags[self.name]
        if self.name in assignments:
            topic_info["assignments"] = assignments[self.name]
        return topic_info

    def _generate_apis(self):
        if self.topic_dir in [TopicDir.OUTPUT, TopicDir.BIDIR]:

            def f(value: int, key: str = "", count: int = 1, partition: int = -1):
                for n in range(count):
                    if key == "":
                        self.send(value, str(n), partition)
                    else:
                        self.send(value, key, partition)
                return value

            annotate_function(
                f,
                name=f"send_to_topic_{self.name}",
                doc=f"This endpoint sends value to topic {self.name}",
                argument_types={"value": self.value_type},
            )
            self.app.add_api_route(
                path=f"{self.app.api_router_prefix}/topic/{self.name}",
                response_class=JSONResponse,
                methods=["POST"],
                endpoint=f,
            )

        if self.topic_dir in [TopicDir.INPUT, TopicDir.BIDIR]:

            def g():
                if self.last_message_received is None:
                    return []
                else:
                    return [self.last_message_received]

            annotate_function(
                g,
                name=f"get_last_topic_{self.name}_message",
                doc=f"This endpoint returns the last message received from topic {self.name}",
                argument_types={},
            )
            self.app.add_api_route(
                path=f"{self.app.api_router_prefix}/topic/{self.name}",
                response_class=JSONResponse,
                response_model=list[self.value_type],
                methods=["GET"],
                endpoint=g,
            )

    def send(
        self,
        value: dict[Any, Any] | BaseModel,
        key: str | bytes = None,
        partition: int = -1,
    ):
        if self.app.is_sink():
            raise CitizenKError("Trying to produce in a sink app")
        if self.topic_dir == TopicDir.INPUT:
            raise CitizenKError("Trying to produce to an input topic")
        value = self.serialize(value)
        if value is None:
            return False
        if not isinstance(key, (str, bytes)):
            raise CitizenKError("Key should be a either a str or bytes", key)
        if self.partitioner is not None and partition == -1:
            partition = self.partitioner(key)

        # Update keys stats
        self.sent_keys_sample[key] = time.time()
        if len(self.sent_keys_sample) > self.MAX_KEYS_IN_STAT:
            oldest_key = min(self.sent_keys_sample, key=self.sent_keys_sample.get)
            del self.sent_keys_sample[oldest_key]

        # TODO: Add schema to headers
        self.app.producer.produce(
            topic=self.name, value=value, key=key, partition=partition
        )
        return True

    def _manage_schema(self):
        """Handle schema registry registration and validation"""
        # https://yokota.blog/2021/03/29/understanding-json-schema-compatibility/
        if self.app.schema_registry_url is not None:
            # Schema registration
            schema_registry_conf = {"url": self.app.schema_registry_url}
            schema_registry_client = SchemaRegistryClient(schema_registry_conf)
            if self.schema_type == SchemaType.AVRO:
                schema_str = json.dumps(self.value_type.avro_schema())
                self.serializer_context = SerializationContext(
                    self.name, MessageField.VALUE
                )
            elif self.schema_type == SchemaType.JSON:
                schema_str = self.value_type.schema_json()
            else:
                raise CitizenKError("Unsupported schema type")
            logger.debug(schema_str)
            schema = Schema(
                schema_str=schema_str,
                schema_type=self.schema_type.name,
            )
            # Schema registration for Output and Bidir topics
            if self.topic_dir != TopicDir.INPUT:
                if self.schema_type == SchemaType.AVRO:
                    self.serializer = AvroSerializer(schema_registry_client, schema_str)

                schema_id = schema_registry_client.register_schema(
                    subject_name=self.subject_name, schema=schema
                )
                logger.info("Schema id registered for %s is %s", self.name, schema_id)
                self.schema_id = schema_id
            # Schema validation for Input and Bidir topics
            if self.topic_dir != TopicDir.OUTPUT:
                if self.schema_type == SchemaType.AVRO:
                    self.deserializer = AvroDeserializer(
                        schema_registry_client, schema_str
                    )

                if not schema_registry_client.test_compatibility(
                    subject_name=self.subject_name, schema=schema
                ):
                    logger.error(
                        "Schema for %s is not compatible with the latest schema registry",
                        self.name,
                    )
                else:
                    logger.info(
                        "Schema for %s is compatible with the latest schema registry",
                        self.name,
                    )
        elif self.schema_type == SchemaType.AVRO:
            raise CitizenKError("AVRO Schema requires a schema registry")

    def serialize(self, value: dict[Any, Any] | BaseModel) -> bytes:
        if isinstance(value, dict):
            try:
                value = self.value_type(**value)
            except ValidationError as exp:
                logger.error("Error while validating send value %s", exp.json())
                return None
        if not isinstance(value, BaseModel):
            raise CitizenKError("Value should be a pydantic model", value)

        self.messages_sent += 1
        self.last_message_sent = value

        if self.schema_type == SchemaType.JSON:
            return value.model_dump_json()
        elif self.schema_type == SchemaType.AVRO:
            try:
                return self.serializer(value.model_dump(), self.serializer_context)
            except SerializationError:
                logger.error("Failed to serialise value %s", value)
                return None
        else:
            raise CitizenKError("No available serializer")

    def deserialize(self, key: str | bytes, value: bytes) -> BaseModel:
        # convert bytes to dict
        if self.schema_type == SchemaType.JSON:
            try:
                value = json.loads(value)
            except json.decoder.JSONDecodeError as exp:
                self.validation_errors += 1
                logger.error("JSON decode error %s", exp)
                return None
        elif self.schema_type == SchemaType.AVRO:
            try:
                value = self.deserializer(value, self.serializer_context)
            except SerializationError as exp:
                self.validation_errors += 1
                logger.error("Failed to deserialise AVRO value %s", exp.json())
                return None
        else:
            raise CitizenKError("No available serializer")

        # convert dict to pydantic model
        try:
            value = self.value_type(**value)
        except ValidationError as exp:
            self.validation_errors += 1
            logger.error("Error while validating received value %s", exp.json())
            return None

        # Update keys stats
        self.receive_keys_sample[key] = time.time()
        if len(self.receive_keys_sample) > self.MAX_KEYS_IN_STAT:
            oldest_key = min(self.receive_keys_sample, key=self.receive_keys_sample.get)
            del self.receive_keys_sample[oldest_key]

        self.messages_received += 1
        self.last_message_received = value
        return value

    def offsets_to_commit(self, agents_offsets: list[dict[tuple[str, int], int]]):
        partition_offsets = defaultdict(list)

        # Collect processed offsets from all agents
        for agent_offsets in agents_offsets:
            for key, offset in agent_offsets.items():
                topic = key[0]
                if topic != self.name:
                    continue
                partition = key[1]
                partition_offsets[partition].append(offset)

        # Check if processed offsets is higher from last committed offset
        commit_offsets = []
        for partition, offsets in partition_offsets.items():
            last_offset = self.last_committed_offset[partition]
            min_offset_to_commit = min(offsets)
            if min_offset_to_commit > last_offset:
                commit_offsets.append(
                    TopicPartition(
                        topic=self.name,
                        partition=partition,
                        offset=min_offset_to_commit,
                    )
                )
                self.last_committed_offset[partition] = min_offset_to_commit
        return commit_offsets

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
