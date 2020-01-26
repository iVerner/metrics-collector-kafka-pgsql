from metrics_collector_kafka_pgsql import producer


def test_metrics_collection():
    metrics_json = producer.collect_metrics("localhost", ["cpu"])
    assert ("host" in metrics_json) and ("cpu" in metrics_json["metrics"])
