from metrics_collector_kafka_pgsql import producer


def test_metrics_collection():
    metrics_dict = producer.collect_metrics("localhost", ["cpu"])
    assert ("host" in metrics_dict.keys()) and (
            "cpu_load" in metrics_dict["metrics"].keys()) and not (
            "memory_usage" in metrics_dict["metrics"].keys())
