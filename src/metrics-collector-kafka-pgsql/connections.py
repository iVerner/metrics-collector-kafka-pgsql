"""Module for connections to kafka and pgsql.

Make connections using config file.

"""
# Standard library imports
import logging
from configparser import ConfigParser

# Third party imports
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable
import psycopg2


class KafkaConnection:
    def __init__(self, config_path='config.ini'):
        self.log = logging.getLogger('kafka_connection')
        self.log.addHandler(logging.StreamHandler())
        self.log.setLevel('INFO')

        config = ConfigParser()
        config.read(config_path)

        self.kafka_host = config.get('kafka', 'host', fallback='localhost')
        self.kafka_port = int(config.get('kafka', 'port', fallback='9092'))
        self.kafka_topic = config.get('kafka', 'topic', fallback='metrics_topic')

        self.bootstrap_server = f'{self.kafka_host}:{self.kafka_port}'

        self.ssl_cafile = config.get('kafka', 'ssl_cafile', fallback='ca.pem')
        self.ssl_certfile = config.get('kafka', 'ssl_certfile', fallback='service.cert')
        self.ssl_keyfile = config.get('kafka', 'ssl_keyfile', fallback='service.key')

        self.client_id = config.get('kafka', 'client_id', fallback='metrics-collector-kafka-pgsql-client')
        self.group_id = config.get('kafka', 'group_id', fallback='metrics-collector-group')

    def get_producer(self):
        self.log.info(f'Connecting to Kafka server {self.bootstrap_server}...')
        try:
            producer = KafkaProducer(bootstrap_servers=self.bootstrap_server,
                                     security_protocol="SSL",
                                     ssl_cafile=self.ssl_cafile,
                                     ssl_certfile=self.ssl_certfile,
                                     ssl_keyfile=self.ssl_keyfile)
            pass
        except NoBrokersAvailable as e:
            self.log.error(f'Error connecting to Kafka server {self.bootstrap_server}.')
            raise e

        return producer

    def get_consumer(self):
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
        return consumer


class PostgreSQLConnection:
    def __init__(self, config_path='config.ini'):
        self.log = logging.getLogger('postgresql_connection')
        self.log.addHandler(logging.StreamHandler())
        self.log.setLevel('INFO')

        config = ConfigParser()
        config.read(config_path)

        self.host = config.get('postgresql', 'host', fallback='localhost')
        self.port = int(config.get('postgresql', 'port', fallback='5432'))

        self.user = config.get('postgresql', 'user', fallback='')
        self.password = config.get('postgresql', 'password', fallback='')

        self.database = config.get('postgresql', 'database', fallback='')

        self.uri = f'postgres://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?sslmode=require'

        self.db_conn = psycopg2.connect(self.uri)

    def get_connection(self):
        return self.db_conn
