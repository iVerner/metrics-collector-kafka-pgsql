"""Module for metrics producer.

Make json with metrics and sends it to kafka.

"""
import json
import logging
from datetime import datetime, timezone
from platform import node
from time import sleep

import psutil

from .connections import KafkaConnection

NETWORK_STAT_COLLECT_TIMEOUT = 0.2

logger = logging.getLogger('metrics_collector_kafka_pgsql.producer')


def collect_metrics(hostname, metrics_list):
    result = {'host': hostname,
              'timestamp': datetime.now(timezone.utc).isoformat()}
    metrics = {}
    for key in metrics_list:
        if key == 'cpu':
            # CPU load in percent
            metrics['cpu_load'] = psutil.cpu_percent(interval=0.2)
        elif key == 'memory':
            # Used memory in percent
            memory_usage = psutil.virtual_memory()
            metrics['memory_usage'] = memory_usage.percent
        elif key == 'network':
            # Network usage speed,  Kb/sec
            counters_1 = psutil.net_io_counters()
            sleep(NETWORK_STAT_COLLECT_TIMEOUT)
            counters_2 = psutil.net_io_counters()
            network_metrics = {
                'network_sending': round(
                    (counters_2.bytes_sent - counters_1.bytes_sent) * (1 / NETWORK_STAT_COLLECT_TIMEOUT) / 1024, 1),
                'network_receiving': round(
                    (counters_2.bytes_recv - counters_1.bytes_recv) * (1 / NETWORK_STAT_COLLECT_TIMEOUT) / 1024, 1)
            }
            metrics['network'] = network_metrics
        elif key == 'disk':
            # Used disk on root partition in percent
            disk_usage = psutil.disk_usage('/')
            metrics['disk_usage'] = disk_usage.percent
    result['metrics'] = metrics
    return result


class MetricsProducer:
    """
    Collects OS metrics and sends them to kafka
    """

    def __init__(self, config):
        self.metrics_interval = int(config.get('metrics', 'metrics_interval', fallback='5'))
        self.metrics_list = list(
            map(str.lower,
                map(str.strip,
                    config.get('metrics', 'metrics_list', fallback='cpu,memory').split(','))))
        logger.info(f'Metrics list: {self.metrics_list}')

        self.hostname = node()

        self.kafka_connection = KafkaConnection(config)

        self.producer = self.kafka_connection.get_producer()

    def send_metrics(self):
        message = json.dumps(collect_metrics(self.hostname, self.metrics_list), ensure_ascii=True)
        logger.info(f'Sending message: {message}')
        self.producer.send(self.kafka_connection.kafka_topic, message.encode("utf-8"))
        self.producer.flush()

    def sleep(self):
        logger.debug(f'Sleeping for {self.metrics_interval} seconds')
        sleep(self.metrics_interval)

    def start_loop(self):
        while True:
            self.send_metrics()
            self.sleep()
