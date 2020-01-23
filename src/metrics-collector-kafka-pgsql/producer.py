"""Module for metrics producer.

Make json with metrics and sends it to kafka.

"""
import json
import logging
from configparser import ConfigParser
from datetime import datetime, timezone
from platform import node
from time import sleep

import psutil

from .connections import KafkaConnection

NETWORK_STAT_COLLECT_TIMEOUT = 0.2

logger = logging.getLogger('metrics-collector-kafka-pgsql.producer')


class MetricsProducer:
    """
    Collects OS metrics and sends them to kafka
    """

    def __init__(self, config_path):
        config = ConfigParser()
        config.read(config_path)

        self.metrics_interval = int(config.get('metrics', 'metrics_interval', fallback='5'))
        self.metrics_list = list(
            map(str.lower,
                map(str.strip,
                    config.get('metrics', 'metrics_list', fallback='cpu,memory').split(','))))
        logger.info(f'Metrics list: {self.metrics_list}')

        self.hostname = node()

        self.kafka_connection = KafkaConnection(config_path)

        self.producer = self.kafka_connection.get_producer()

    def collect_metrics(self):
        result = {'host': self.hostname,
                  'timestamp': datetime.now(timezone.utc).isoformat()}
        metrics = {}
        for key in self.metrics_list:
            if key == 'cpu':
                metrics['cpu_load'] = psutil.cpu_percent(interval=0.1)  # CPU load in percent
            elif key == 'memory':
                memory_usage = psutil.virtual_memory()
                metrics['memory_usage'] = round((memory_usage.used / memory_usage.total) * 100, 1)  # Used memory in percent
            elif key == 'network':
                network_usage_1 = psutil.net_io_counters()
                sleep(NETWORK_STAT_COLLECT_TIMEOUT)
                network_usage_2 = psutil.net_io_counters()
                # Network usage speed,  Kb/sec
                network_metrics = {
                    'network_sending': round((network_usage_2.bytes_sent - network_usage_1.bytes_sent) * (1 / NETWORK_STAT_COLLECT_TIMEOUT) / 1024, 1),
                    'network_receiving': round((network_usage_2.bytes_recv - network_usage_1.bytes_recv) * (1 / NETWORK_STAT_COLLECT_TIMEOUT) / 1024, 1)
                }
                metrics['network'] = network_metrics
            elif key == 'disk':
                disk_usage = psutil.disk_usage('/')
                metrics['disk_usage'] = round((disk_usage.used / disk_usage.total) * 100, 1)  # Used disk on root partition in percent
        result['metrics'] = metrics
        return result

    def send_metrics(self):
        message = json.dumps(self.collect_metrics(), ensure_ascii=True)
        logger.info(f'Sending message: {message}')
        self.producer.send(self.kafka_connection.kafka_topic, message.encode("utf-8"))
        self.producer.flush()

    def sleep(self):
        logger.info(f'Sleeping for {self.metrics_interval} seconds')
        sleep(self.metrics_interval)

    def start_loop(self):
        while True:
            self.send_metrics()
            self.sleep()
