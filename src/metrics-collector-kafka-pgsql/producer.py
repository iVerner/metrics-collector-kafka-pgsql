"""Module for metrics producer.

Make json with metrics and sends it to kafka.

"""
# Standard library imports
import logging
import json
from time import sleep
from datetime import datetime
from configparser import ConfigParser

# Third party imports
# import psutil

# Local application imports
from connections import KafkaConnection


class MetricsCollector:
    """
    Collects OS metrics and sends them to kafka
    """

    def __init__(self, config_path='config.ini'):
        self.log = logging.getLogger('metrics_producer')
        self.log.addHandler(logging.StreamHandler())
        self.log.setLevel('INFO')

        config = ConfigParser()
        config.read(config_path)

        self.metrics_interval = int(config.get('metrics', 'metrics_interval', fallback='5'))
        self.metrics_list = list(
            map(str.lower,
                map(str.strip,
                    config.get('metrics', 'metrics_list', fallback='cpu,memory').split(','))))
        self.log.info(f'Metrics list: {self.metrics_list}')

        self.kafka_connection = KafkaConnection(config_path)

        self.producer = self.kafka_connection.get_producer()

    def collect_metrics(self):
        result = {}
        result['host'] = 'be-be-be'
        result['timestamp'] = datetime.now().isoformat()
        metrics = {}
        for key in self.metrics_list:
            if key == 'cpu':
                metrics['cpu'] = 1
            if key == 'memory':
                metrics['memory'] = '32Gb'
            if key == 'network':
                metrics['network'] = '10G'
            if key == 'disk':
                metrics['disk'] = '0.5Tb'
        result['metrics'] = metrics
        return result

    def send_metrics(self):
        message = json.dumps(self.collect_metrics(), ensure_ascii=True)
        self.log.info(f'Sending message: {message}')
        self.producer.send(self.kafka_topic, message.encode("utf-8"))
        self.producer.flush()

    def sleep(self):
        self.log.info(f'Sleeping for {self.metrics_interval} seconds')
        sleep(self.metrics_interval)

    def start_loop(self):
        while True:
            self.send_metrics()
            self.sleep()


def main():
    collector = MetricsCollector('../../config.ini')
    collector.start_loop()


if __name__ == '__main__':
    main()
