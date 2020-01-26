from configparser import ConfigParser

from metrics_collector_kafka_pgsql import connections, consumer, producer

from psycopg2.extras import RealDictCursor

from tests.fixtures.test_fixtures import EXAMPLE_METRICS_DICT, replace_psutil  # noqa: F401


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


def test_overall_process(replace_psutil):  # noqa: F811
    pgsql = connections.PostgreSQLConnection(init_config()).db_conn
    pgsql_cur = pgsql.cursor(cursor_factory=RealDictCursor)
    pgsql_cur.execute("truncate metrics_table;")
    pgsql.commit()

    metrics_producer = producer.MetricsProducer(init_config())
    metrics_producer.send_metrics()

    metrics_consumer = consumer.MetricsConsumer(init_config())
    for _ in range(2):
        metrics_consumer.move_batch()

    pgsql_cur.execute("select metrics_json from metrics_table;")
    metrics_dict = pgsql_cur.fetchone()["metrics_json"]
    pgsql.commit()

    assert metrics_dict["metrics"] == EXAMPLE_METRICS_DICT
