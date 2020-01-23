"""Module for move data from kafka to pgsql.

"""
import logging

from psycopg2.extras import RealDictCursor

from .connections import KafkaConnection, PostgreSQLConnection

logger = logging.getLogger('metrics-collector-kafka-pgsql.consumer')


class MetricsConsumer:
    def __init__(self, config_path):
        self.kafka_conn = KafkaConnection(config_path)
        self.consumer = self.kafka_conn.get_consumer()

        self.postgres_conn = PostgreSQLConnection(config_path).db_conn

    def start_loop(self):
        cursor = self.postgres_conn.cursor(cursor_factory=RealDictCursor)
        while True:
            raw_msgs = self.consumer.poll(timeout_ms=1000)
            for _tp, msgs in raw_msgs.items():
                for msg in msgs:
                    message = str(msg.value, 'utf-8')
                    try:
                        cursor.execute("select * from insert_metrics(%s::json)", (message,))
                    except Exception as exception:
                        logger.error("Error inserting: {} \n{}".format(msg.value, exception))

                    _ = cursor.fetchone()

                    print("Inserted: {}".format(msg.value))
                    self.consumer.commit()
