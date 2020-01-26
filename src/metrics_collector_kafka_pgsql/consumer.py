"""
Module for move data from kafka to pgsql.
"""
import logging
import sys

from psycopg2 import Error
from psycopg2.extras import RealDictCursor

from .connections import KafkaConnection, PostgreSQLConnection

logger = logging.getLogger('metrics_collector_kafka_pgsql.consumer')


class MetricsConsumer:
    def __init__(self, config):
        self.kafka_conn = KafkaConnection(config)
        self.consumer = self.kafka_conn.get_consumer()

        self.postgres_conn = PostgreSQLConnection(config).db_conn
        self.postgres_cursor = self.postgres_conn.cursor(cursor_factory=RealDictCursor)

    def __del__(self):
        self.postgres_cursor.close()
        self.postgres_conn.close()

    def move_batch(self):
        raw_msgs = self.consumer.poll(timeout_ms=1000)
        for _tp, msgs in raw_msgs.items():
            for msg in msgs:
                message = str(msg.value, 'utf-8')
                try:
                    self.postgres_cursor.execute("select * from insert_metrics(%s::json)", (message,))
                    self.postgres_conn.commit()
                except Error as exception:
                    logger.error("Error inserting: {} \n{}".format(msg.value, exception))
                    sys.exit(1)

                print("Inserted: {}".format(msg.value))
                self.consumer.commit()

    def start_loop(self):
        while True:
            self.move_batch()
