from collections import namedtuple

from metrics_collector_kafka_pgsql import producer

import psutil


def test_metrics_collection(monkeypatch):
    def mock_cpu_percent(*args, **kwargs):
        return 146.0

    def mock_virtual_memory(*args, **kwargs):
        svmem = namedtuple('svmem',
                           ['total', 'available', 'percent', 'used', 'free', 'active', 'inactive', 'buffers', 'cached', 'shared', 'slab'])
        return svmem(42, 2, 86, 0, 0, 0, 0, 0, 0, 0, 0)

    def mock_disk_usage(*args, **kwargs):
        sdiskusage = namedtuple('sdiskusage', ['total', 'used', 'free', 'percent'])
        return sdiskusage(84, 4, 0, 77)

    monkeypatch.setattr(psutil, "cpu_percent", mock_cpu_percent)
    monkeypatch.setattr(psutil, "virtual_memory", mock_virtual_memory)
    monkeypatch.setattr(psutil, "disk_usage", mock_disk_usage)

    metrics = producer.collect_metrics('localhost', ['cpu', 'memory', 'disk'])['metrics']
    assert metrics == {'cpu_load': 146,
                       'memory_usage': 86,
                       'disk_usage': 77
                       }
