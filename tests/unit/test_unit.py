from metrics_collector_kafka_pgsql import producer

from tests.fixtures.test_fixtures import EXAMPLE_METRICS_DICT, replace_psutil  # noqa: F401


def test_metrics_collection(replace_psutil):  # noqa: F811
    metrics = producer.collect_metrics('localhost', ['cpu', 'memory', 'disk'])['metrics']
    assert metrics == EXAMPLE_METRICS_DICT
