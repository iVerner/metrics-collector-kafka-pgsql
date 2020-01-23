"""Module for move data from kafka to pgsql.

"""
# Standard library imports
import logging

# Third party imports
from psycopg2.extras import RealDictCursor

# Local application imports
from connections import KafkaConnection, PostgreSQLConnection


class DatabaseFiller:
    def __init__(self, config_path='config.ini'):
        self.kafka_conn = KafkaConnection(config_path)
        self.consumer = self.kafka_conn.get_consumer()

        print(self.consumer.subscription())

        self.postgres_conn = PostgreSQLConnection(config_path).db_conn

    def start_loop(self):
        cursor = self.postgres_conn.cursor(cursor_factory=RealDictCursor)
        while True:
            raw_msgs = self.consumer.poll(timeout_ms=1000)
            for tp, msgs in raw_msgs.items():
                for msg in msgs:
                    message = str(msg.value, 'utf-8')
                    try:
                        cursor.execute(f"select * from insert_metrics(%s::json)", (message,))
                    except Exception as e:
                        print("Error inserting: {} \n{}".format(msg.value, e))

                    _ = cursor.fetchone()

                    print("Inserted: {}".format(msg.value))
                    self.consumer.commit()


def main():
    filler = DatabaseFiller('config.ini')
    filler.start_loop()


if __name__ == '__main__':
    main()