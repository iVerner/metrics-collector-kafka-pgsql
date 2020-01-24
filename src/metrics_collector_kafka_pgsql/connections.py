"""Module for connections to kafka and pgsql.

Make connections using config file.

"""
import logging

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

import psycopg2

logger = logging.getLogger('metrics_collector_kafka_pgsql.connections')


class KafkaConnection:
    def __init__(self, config):
        kafka_host = config.get('kafka', 'host', fallback='localhost')
        kafka_port = int(config.get('kafka', 'port', fallback='9092'))
        self.bootstrap_server = f'{kafka_host}:{kafka_port}'

        self.kafka_topic = config.get('kafka', 'topic', fallback='metrics_topic')

        self.ssl_cafile = config.get('kafka', 'ssl_cafile', fallback='ca.pem')
        self.ssl_certfile = config.get('kafka', 'ssl_certfile', fallback='service.cert')
        self.ssl_keyfile = config.get('kafka', 'ssl_keyfile', fallback='service.key')

        self.client_id = config.get('kafka', 'client_id', fallback='metrics_collector_kafka_pgsql-client')
        self.group_id = config.get('kafka', 'group_id', fallback='metrics-collector-group')

    def get_producer(self):
        logger.info(f'Connecting to Kafka server {self.bootstrap_server}...')
        try:
            producer = KafkaProducer(bootstrap_servers=self.bootstrap_server,
                                     security_protocol="SSL",
                                     ssl_cafile=self.ssl_cafile,
                                     ssl_certfile=self.ssl_certfile,
                                     ssl_keyfile=self.ssl_keyfile)
        except NoBrokersAvailable:
            logger.error(f'Error connecting to Kafka server {self.bootstrap_server}.')
            raise

        return producer

    def get_consumer(self):
        logger.info(f'Connecting to Kafka server {self.bootstrap_server}...')
        try:
            consumer = KafkaConsumer(
                self.kafka_topic,
                auto_offset_reset="earliest",
                bootstrap_servers=self.bootstrap_server,
                client_id=self.client_id,
                group_id=self.group_id,
                security_protocol="SSL",
                ssl_cafile=self.ssl_cafile,
                ssl_certfile=self.ssl_certfile,
                ssl_keyfile=self.ssl_keyfile
            )
        except NoBrokersAvailable:
            logger.error(f'Error connecting to Kafka server {self.bootstrap_server}.')
            raise
        return consumer


class PostgreSQLConnection:
    def __init__(self, config):
        self.host = config.get('postgresql', 'host', fallback='localhost')
        self.port = int(config.get('postgresql', 'port', fallback='5432'))

        self.user = config.get('postgresql', 'user', fallback='')
        self.password = config.get('postgresql', 'password', fallback='')

        self.database = config.get('postgresql', 'database', fallback='')

        self.uri = f'postgres://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?sslmode=require'

        try:
            self.db_conn = psycopg2.connect(self.uri)
        except psycopg2.OperationalError:
            logger.error(f'Error connecting to PostgreSQL server {self.host}:{self.port}.')
            raise
