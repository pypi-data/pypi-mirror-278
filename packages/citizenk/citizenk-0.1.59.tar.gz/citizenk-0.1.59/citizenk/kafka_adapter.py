import json
import logging
import os
import subprocess
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from time import time
from typing import Any, Optional, Tuple, Union

import certifi
from confluent_kafka import (
    Consumer,
    ConsumerGroupTopicPartitions,
    KafkaError,
    KafkaException,
    Message,
    Producer,
    TopicPartition,
)
from confluent_kafka.admin import AdminClient

from .murmur2 import murmur2_partition

logger = logging.getLogger(__name__)


class KafkaRole(Enum):
    ADMIN = 1
    CONSUMER = 2
    PRODUCER = 3


@dataclass
class KafkaConfig:
    """Kafka connection details"""

    bootstrap_servers: str
    tls: bool = True
    sasl_mechanism: str = "PLAIN"
    sasl_username: Optional[str] = None
    sasl_password: Optional[str] = None
    extra_config: Optional[dict[str, str]] = None


def ttl_cache(ttl: int):
    def wrapper(func):
        @wraps(func)
        def _decorator(self, *args, **kwargs):
            if len(args) > 0:
                raise ValueError("Expected only kwargs arguments")
            now = time()

            # Empty old cache items
            for key in list(self.calls_cache.keys()):
                if now > self.calls_cache[key]["cached_expires_at"]:
                    del self.calls_cache[key]

            # Find cache key
            cache_key = [func.__name__]
            for value in kwargs.values():
                cache_key.append(value)
            cache_key = tuple(cache_key)
            cached = None
            if cache_key in self.calls_cache:
                return self.calls_cache[cache_key]["cached"]

            # Key not found, calculate it and update cache
            cached = func(self, *args, **kwargs)
            self.calls_cache[cache_key] = {
                "cached_expires_at": now + ttl,
                "cached": cached,
            }
            return cached

        return _decorator

    return wrapper


class KafkaAdapter:
    """Kafka adapter Using confluent API"""

    def __init__(
        self,
        config: KafkaConfig,
        role: KafkaRole = KafkaRole.ADMIN,
        consumer_group_name: Optional[str] = None,
        consumer_group_init_offset: Optional[str] = "latest",
        consumer_group_auto_commit: Optional[bool] = True,
        extra_config: Optional[dict[str, str]] = None,
    ):
        self.role = role
        self.consumer_group_name = consumer_group_name
        self.consumer_group_auto_commit = consumer_group_auto_commit
        self.consumer_started = False
        self.consumer_topics = {}
        self.assigned_partitions = defaultdict(set)
        self.kafka_error = None
        self.last_stats = {}
        self.topic_stats = defaultdict(int)
        self.total_bytes_in = 0
        self.total_bytes_out = 0

        # used by ttl_cache
        self.calls_cache = {}

        self.sasl_username = config.sasl_username
        self.sasl_password = config.sasl_password
        self.sasl_mechanism = config.sasl_mechanism.upper()
        if self.sasl_mechanism == "PLAIN":
            self.config = {"security.protocol": "SSL" if config.tls else "PLAINTEXT"}
        elif self.sasl_mechanism in ["SCRAM-SHA-512", "SCRAM-SHA-256"]:
            if config.sasl_username is None or config.sasl_password is None:
                raise ValueError("Expected valid sasl_username and sasl_password")

            self.config = {
                "sasl.mechanism": self.sasl_mechanism,
                "security.protocol": "SASL_SSL" if config.tls else "SASL_PLAINTEXT",
                "ssl.ca.location": certifi.where(),
                "sasl.username": config.sasl_username,
                "sasl.password": config.sasl_password,
            }
        else:
            raise ValueError("Unsupported sasl_mechanism")
        self.config["bootstrap.servers"] = config.bootstrap_servers
        # self.config["statistics.interval.ms"] = 15 * 60 * 1000
        self.config["error_cb"] = self._on_kafka_error
        self.config["stats_cb"] = self._on_kafka_stats

        # Add additional config
        if config.extra_config is not None:
            self.config.update(config.extra_config)
        if extra_config is not None:
            self.config.update(extra_config)
        self.admin_config = self.config.copy()
        self.admin = AdminClient(self.admin_config)

        if self.role == KafkaRole.CONSUMER:
            self.config["auto.offset.reset"] = consumer_group_init_offset
            self.config["on_commit"] = self._on_kafka_commit
            if self.consumer_group_name is not None:
                self.config["group.id"] = self.consumer_group_name
                self.config["enable.auto.commit"] = consumer_group_auto_commit
            else:
                logger.info("Starting consumer without a consumer group")
                self.config["enable.auto.commit"] = False
                self.config["group.id"] = "dummy_shouldnt_be_used"
            self.connection = Consumer(self.config, logger=logger)
        elif self.role == KafkaRole.PRODUCER:
            self.config["partitioner"] = "murmur2"
            self.connection = Producer(self.config, logger=logger)
        else:
            self.connection = self.admin
        try:
            metadata = self.connection.list_topics(timeout=15)
        except KafkaException as exp:
            self._on_kafka_error(exp.args[0])
            raise
        logger.debug("Connected to %s cluster %s", self.role.name, metadata.cluster_id)

    @ttl_cache(60)
    def get_all_broker_groups(self) -> list[str]:
        try:
            future = self.admin.list_consumer_groups(request_timeout=15)
            groups = future.result()
        except KafkaException as exp:
            logger.error("Failed to get consumer groups")
            self._on_kafka_error(exp.args[0])
            return []
        return [g.group_id for g in groups.valid]

    @ttl_cache(60)
    def get_group_members(self) -> dict[Tuple, str]:
        if self.consumer_group_name is None:
            logger.error("Request group members for empty group")
            return {}
        groups = [self.consumer_group_name]
        members = {}
        try:
            future_map = self.admin.describe_consumer_groups(groups, request_timeout=15)
        except KafkaException as exp:
            logger.error("Failed to get group members")
            self._on_kafka_error(exp.args[0])
            return {}

        if len(future_map) == 0:
            logger.info("Weird, didn't get any members for groups %s", groups)
        for future in future_map.values():
            try:
                g = future.result()
                for member in g.members:
                    if member.assignment:
                        host = member.host.split("/")[1]
                        for t in member.assignment.topic_partitions:
                            members[(t.topic, t.partition)] = host
            except KafkaException:
                logger.error("Error while describing group")
        logger.info("Found members %s", members)
        return members

    def get_partition_id(self, topic: str, key: Union[str, bytes]) -> int:
        if isinstance(key, str):
            key = key.encode()
        num_partitions = self.get_partition_count(topic=topic)
        if num_partitions == 0:
            return None
        return murmur2_partition(key, num_partitions)

    @ttl_cache(300)
    def get_partition_count(self, topic: str) -> int:
        """Get list of all topics in the broker"""
        try:
            topics = self.connection.list_topics(topic, timeout=15).topics
        except KafkaException as exp:
            logger.error("Failed to list topic %s", topic)
            self._on_kafka_error(exp.args[0])
            return 0

        if len(topics) == 0:
            return 0
        else:
            return len(topics[topic].partitions)

    @ttl_cache(300)
    def get_all_broker_topics(self) -> dict[str, Any]:
        """Get list of all topics in the broker"""
        try:
            topics = self.connection.list_topics(timeout=15).topics
        except KafkaException as exp:
            logger.error("Failed to list topics")
            self._on_kafka_error(exp.args[0])
            return {}

        return {
            topic_name: topic
            for topic_name, topic in topics.items()
            if not topic_name.startswith("__")
        }

    @ttl_cache(300)
    def get_all_broker_partitions(self) -> list[TopicPartition]:
        """Get list of all partiotions in the broker"""
        topics = self.get_all_broker_topics()
        return [
            TopicPartition(topic_name, p)
            for topic_name, topic in topics.items()
            for p in topic.partitions
        ]

    def get_partitions_with_offsets(
        self,
        topics: list[str],
        strategy: str = "latest",
        x: int = 0,
        epoch: int = 0,
        partition_filter: list[int] = [],
    ) -> list[TopicPartition]:
        """
        Get a list of partitions in the broker for the given topics
        And set offsets based on the specified strategy:
            p = num partitions
            latest-x/p
            earielst+x/p
            x
            time
        """
        filtered_partitions = []
        for topic in topics:
            # Get the topic's partitions
            try:
                metadata = self.connection.list_topics(topic, timeout=15)
            except KafkaException as exp:
                logger.error("Failed to list topic %s", topic)
                self._on_kafka_error(exp.args[0])
                continue

            if metadata.topics[topic].error is not None:
                self._on_kafka_error(metadata.topics[topic].error)
                continue

            # Construct TopicPartition list of partitions to query
            if len(partition_filter) == 0:
                partitions = [
                    TopicPartition(topic, p) for p in metadata.topics[topic].partitions
                ]
            else:
                partitions = [
                    TopicPartition(topic, p)
                    for p in metadata.topics[topic].partitions
                    if p in partition_filter
                ]
            filtered_partitions += partitions

        # for time strategy lookup offset for time
        if epoch > 0:
            epoch = int(epoch)
            for p in filtered_partitions:
                p.offset = epoch
            try:
                return self.connection.offsets_for_times(
                    filtered_partitions, timeout=15
                )
            except KafkaException as exp:
                logger.error(
                    "Failed to get offsets for times of %s", filtered_partitions
                )
                self._on_kafka_error(exp.args[0])
                return []

        else:
            for p in filtered_partitions:
                try:
                    (lo, hi) = self.connection.get_watermark_offsets(
                        p, timeout=15, cached=False
                    )
                except KafkaException as exp:
                    logger.error("Failed to get watermark offsets of %s", p)
                    self._on_kafka_error(exp.args[0])
                    continue

                if strategy == "latest":
                    p.offset = hi - x
                elif strategy == "earliest":
                    p.offset = lo + x
                elif strategy == "specific":
                    p.offset = x
                else:
                    raise ValueError("Unsupported offset strategy")

                if p.offset < lo:
                    p.offset = lo
                if p.offset > hi:
                    p.offset = hi
            return filtered_partitions

    def get_own_group_topics(self) -> list[str]:
        """Get a list of all the topics in the consumer group"""
        if self.role != KafkaRole.CONSUMER or self.consumer_group_name is None:
            return []

        group_topics = set()
        partitions = self.get_all_broker_partitions()
        # Find which topic has stored offset for the group
        try:
            committed = self.connection.committed(partitions, timeout=15)
        except KafkaException as exp:
            logger.error(
                "Failed to get group committed offsets %s %s",
                self.consumer_group_name,
                exp,
            )
            self._on_kafka_error(exp.args[0])
            return []

        for p in committed:
            if p.offset > 0:
                group_topics.add(p.topic)
        return list(group_topics)

    def get_group_lag(self) -> dict[str, int]:
        """Get the total lag of the group for each topic"""
        group_topics = defaultdict(int)
        if self.role != KafkaRole.CONSUMER or self.consumer_group_name is None:
            return group_topics

        partitions = self.get_all_broker_partitions()
        try:
            committed = self.connection.committed(partitions, timeout=15)
            for p in committed:
                if p.offset >= 0:
                    (_, hi) = self.connection.get_watermark_offsets(
                        p, timeout=15, cached=True
                    )
                    if hi <= 0:
                        continue
                    topic = p.topic
                    lag = hi - p.offset
                    group_topics[topic] += lag
            logger.debug(
                "Topics Lag for %s group are %s", self.consumer_group_name, group_topics
            )
        except KafkaException as exp:
            logger.error(
                "Failed to get group committed offsets %s %s",
                self.consumer_group_name,
                exp,
            )
            self._on_kafka_error(exp.args[0])
            return group_topics

        return group_topics

    def delete_groups(self, groups: list[str]) -> int:
        """Delete the given consumer groups"""
        if len(groups) == 0:
            return 0

        broker_groups = self.get_all_broker_groups()
        groups_to_delete = []
        for group in groups:
            if group in broker_groups:
                groups_to_delete.append(group)

        if len(groups_to_delete) == 0:
            logger.info("Can't delete consumer groups %s : not in broker", groups)
            return 0

        future_map = self.admin.delete_consumer_groups(
            groups_to_delete, request_timeout=15
        )
        count = 0
        for group_id, future in future_map.items():
            try:
                future.result()
                logger.debug("Deleted consumer groups %s", group_id)
                count += 1
            except KafkaException as ex:
                logger.error("Failed to delete consumer groups %s %s", group_id, ex)
        return count

    def delete_offset_for_group_api(
        self, group: str, topic: Optional[str] = None
    ) -> int:
        """Delete the offset of the given topic from  (Not working) !!"""
        if topic is None:
            return 0
        topics = self.admin.list_topics(topic, timeout=15).topics
        if len(topics) == 0:
            logger.error("Can't find topic %s in broker", topic)
            return 0
        group_request = [
            ConsumerGroupTopicPartitions(
                group, [TopicPartition(topic, p, 0) for p in topics[topic].partitions]
            )
        ]
        future_map = self.admin.alter_consumer_group_offsets(
            group_request, request_timeout=15
        )
        count = 0
        for future in future_map.values():
            try:
                future.result()
                logger.debug("Deleted offset of topic %s group %s", topic, group)
                count += 1
            except KafkaException as ex:
                logger.error(
                    "Failed to delete offset of topic %s from consumer groups %s %s",
                    group,
                    topic,
                    ex,
                )
        return count

    def reset_offset_for_group(self, group: str, topic: Optional[str] = None) -> int:
        """
        Resets the offset of a topic for the group to latest.
        """
        params = {"--reset-offsets": "", "--to-latest": ""}
        if topic is None:
            params["--all-topics"] = ""
        else:
            params["--topic"] = topic

        error_code = self.group_ops(group, params)
        if error_code != 0:
            logger.error(
                "Failed to reset offsets for group using kafka CLI %s", error_code
            )
        else:
            logger.debug(
                "Successfully reset offsets for group %s topic %s", group, topic
            )
        return error_code

    def delete_offset_for_group(self, group: str, topic: Optional[str] = None) -> int:
        """
        Deletes the offset of a topic for the group.
        """
        # When we stop consuming a topic, we want to delete the offsets of the consumer group
        # So that when we consume the same topic back, we will start from latest and not the stored
        # offset. I coulnd't find a way to delete the offsets using the API, so I had to use the
        # Standard kafka cli for this
        # kafka-consumer-groups.sh --bootstrap-server 'localhost:9092' --group replicator --command-config local.config --topic globalvia.ap53.dev.camera.video.ocr - 1  --delete-offsets
        params = {"--delete-offsets": ""}
        if topic is None:
            params["--all-topics"] = ""
        else:
            params["--topic"] = topic

        error_code = self.group_ops(group, params)
        if error_code != 0:
            logger.error(
                "Failed to delete offsets for group using kafka CLI %s", error_code
            )
        else:
            logger.debug(
                "Successfully deleted offsets for group %s topic %s", group, topic
            )
        return error_code

    def group_ops(self, group: str, ops_params: dict[str, str]) -> int:
        """
        Perform the given ops on the group

        Which op:
        --describe
        --delete to delete the group
        --delete-offsets to delete offsets for a topic / all topics
        --reset-offsets to reset offsets for a topic / all topics

        Which topic:
        --topic <name>
        --all-topics

        Which offset
        --to-earliest
        --to-latest
        --to-offset
        --shift-by
        --to-datetime
        """
        temp_config_filename = tempfile.NamedTemporaryFile(
            suffix=".config", delete=False
        ).name

        config_string = "\n".join([f"{k}={v}" for k, v in self.config.items()])
        if self.sasl_mechanism == "PLAIN":
            config_string += "\nsasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule"
            config_string += f' required username="{self.sasl_username}" password="{self.sasl_password}";'
        elif self.sasl_mechanism in ["SCRAM-SHA-512", "SCRAM-SHA-256"]:
            config_string += "\nsasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule"
            config_string += f' required username="{self.sasl_username}" password="{self.sasl_password}";'

        # This will also add some unknown configs like group.id, auto.offset.reset etc..
        with open(temp_config_filename, "w") as f:
            f.write(config_string)

        command = "kafka-consumer-groups.sh"
        params = {
            "--bootstrap-server": self.config["bootstrap.servers"],
            "--command-config": temp_config_filename,
            "--group": group,
            "--execute": "",
        }
        params.update(ops_params)
        command_with_params = command + "".join(
            [f" {k} {v}" for k, v in params.items()]
        )
        error_code = subprocess.call(
            command_with_params,
            shell=True,
            stderr=sys.stderr,
            stdout=sys.stdout,
            timeout=15,
        )
        os.remove(temp_config_filename)
        return error_code

    def delete_old_offsets_for_group(self) -> int:
        if self.role != KafkaRole.CONSUMER:
            return 0
        if not self.consumer_started:
            return 0
        if self.consumer_group_name is None:
            return 0
        # Check if the consumer group has unwanted topics if so, delete them
        count = 0
        group_topics = self.get_own_group_topics()
        for t in group_topics:
            if t not in self.consumer_topics:
                logger.info("topic %s is no longer consumed, deleting offsets", t)
                self.delete_offset_for_group(self.consumer_group_name, t)
                count += 1
        return count

    def start_consumer(
        self,
        topics: list[str],
        count: int = 0,
        strategy: str = "latest",
        epoch: int = 0,
        partition_filter: list[int] = [],
    ):
        """Start the consumer with the given topics. offset = latest-n"""
        self.stop_consumer()

        if self.consumer_group_name is not None:
            # Subscribe to desired source topics
            logger.debug("Subscribing to %s", topics)
            if len(topics) > 0:
                self.connection.subscribe(
                    topics,
                    on_assign=self._on_kafka_assign,
                    on_revoke=self._on_kafka_revoke,
                    on_lost=self._on_kafka_lost,
                )
        else:
            # Assign partitions to consumer
            logger.debug("Subscribing to %s without a consumer group", topics)
            source_partitions = self.get_partitions_with_offsets(
                topics=topics,
                x=count,
                strategy=strategy,
                epoch=epoch,
                partition_filter=partition_filter,
            )
            if len(source_partitions) == 0:
                logger.error("Couldn't find any partitions to assign to")
            else:
                self.connection.assign(source_partitions)
        self.consumer_topics = topics
        self.consumer_started = True
        logger.debug("Finished setting up consumer, and starting consuming")

    @staticmethod
    def stringify_key(key):
        if key is None or isinstance(key, str):
            return key
        elif isinstance(key, bytes):
            return key.decode()
        else:
            logger.error("Unexpected key type %s", type(key))
            return str(key)

    @staticmethod
    def messages_to_dict(messages: list[Message]) -> list[dict[str, Any]]:
        try:
            return [
                {
                    "topic": m.topic(),
                    "key": KafkaAdapter.stringify_key(m.key()),
                    "value": json.loads(m.value()),
                    "partition": m.partition(),
                    "offset": m.offset(),
                    "timestamp": m.timestamp()[1],
                }
                for m in messages
            ]
        except json.decoder.JSONDecodeError as exp:
            logger.debug("JSON Decode error %s", exp)
            return []

    def consume(self, num_messages: int = 1, timeout: float = 1.0) -> list[Message]:
        """Consume records from the topics"""
        confluent_msgs = self.connection.consume(num_messages, timeout)
        msgs = []
        for msg in confluent_msgs:
            error = msg.error()
            if error is None:
                msgs.append(msg)
                self.topic_stats[msg.topic()] += 1
                self.total_bytes_in += len(msg)
            else:
                self._on_kafka_error(error)
        logger.debug("Consumed %s Kafka messages", len(msgs))
        return msgs

    def commit(self, msgs: list[Message]):
        if self.consumer_group_name is None:
            return
        if self.consumer_group_auto_commit:
            return
        self.connection.commit(msgs)

    def produce(
        self,
        topic: str,
        value: Any,
        key: Optional[Any] = None,
        partition: int = -1,
        headers: Optional[dict[str, bytes]] = None,
    ):
        if not isinstance(key, bytes):
            key = str(key).encode()
            self.total_bytes_out += len(key)
        """Produce a message to the given topic"""
        self.topic_stats[topic] += 1
        self.total_bytes_out += len(value)
        self.connection.produce(
            topic, value=value, key=key, partition=partition, headers=headers
        )

    def _on_kafka_commit(self, err: KafkaError, partitions: list[TopicPartition]):
        logger.debug(
            "Kafka committed err=%s num partitions=%s",
            err,
            len([p for p in partitions if p.offset > 0]),
        )

    def _on_kafka_stats(self, json_str: str):
        logger.info(
            "Kafka stats updated for role %s group %s",
            self.role,
            self.consumer_group_name,
        )
        self.last_stats = json.loads(json_str)

    def _on_kafka_error(self, err: KafkaError):
        self.kafka_error = err
        logger.error("Kafka error %s", err)

    def _on_kafka_assign(self, consumer, partitions: list[TopicPartition]):
        logger.info("Group rebalancing. Partitions assigned %s", partitions)
        for p in partitions:
            self.assigned_partitions[p.topic].add(p.partition)

    def _on_kafka_revoke(self, consumer, partitions: list[TopicPartition]):
        logger.info("Group rebalancing. Partition revoked %s", partitions)
        for p in partitions:
            self.assigned_partitions[p.topic].discard(p.partition)

    def _on_kafka_lost(self, consumer, partitions: list[TopicPartition]):
        logger.info("Group rebalancing. Partitions lost %s", partitions)
        for p in partitions:
            self.assigned_partitions[p.topic].discard(p.partition)

    def is_assigned(self, topic):
        return len(self.assigned_partitions[topic]) > 0

    def get_topic_stats(self) -> dict[str, int]:
        result = self.topic_stats
        self.topic_stats = defaultdict(int)
        return result

    def get_total_bytes(self) -> tuple[int, int]:
        result = (self.total_bytes_in, self.total_bytes_out)
        self.total_bytes_in = 0
        self.total_bytes_out = 0
        return result

    def messages_in_queue(self) -> int:
        if self.role != KafkaRole.PRODUCER:
            return 0
        return len(self.connection)

    def poll(self):
        """Poll the broker"""
        self.connection.poll(0)

    def stop_consumer(self):
        """Stop the consumer"""
        if self.role != KafkaRole.CONSUMER:
            return
        if not self.consumer_started:
            return
        if self.consumer_group_name is None:
            logger.debug("Unassign from all partitions")
            self.connection.unassign()
        else:
            logger.debug("Unsubscribe from all partitions")
            self.connection.unsubscribe()

    def stop_producer(self):
        """Stop the producer"""
        if self.role != KafkaRole.PRODUCER:
            return
        self.connection.flush(timeout=15)
        logger.debug("Flushed producer queue")

    def close(self):
        """Close the connection"""
        self.stop_consumer()
        self.stop_producer()
        if self.role == KafkaRole.CONSUMER:
            self.connection.close()
