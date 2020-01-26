from configparser import ConfigParser

from metrics_collector_kafka_pgsql import connections


def init_config():
    config = ConfigParser()
    config.read("tests/test_config.ini")
    return config


def test_kafka_producer_connection():
    connections.KafkaConnection(init_config()).get_producer()


def test_kafka_consumer_connection():
    connections.KafkaConnection(init_config()).get_consumer()


def test_postgresql_connection():
    connections.PostgreSQLConnection(init_config())
