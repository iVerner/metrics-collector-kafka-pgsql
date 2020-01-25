"""Main package module."""

import argparse
import logging
import sys
from configparser import ConfigParser

from .consumer import MetricsConsumer
from .producer import MetricsProducer


def main():
    """
    Main function
    """
    logger = logging.getLogger('metrics_collector_kafka_pgsql')
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("start_mode", help="Mode: producer/consumer", type=str, choices=['producer', 'consumer'])
    parser.add_argument("-c", "--config", help="Path to config file", type=str, default='config.ini')

    args = parser.parse_args()

    config = ConfigParser()
    try:
        with open(args.config) as config_file:
            config.read_file(config_file)
    except FileNotFoundError:
        logger.error(f'Config file "{args.config}" not found. Exiting.')
        sys.exit(1)

    if args.start_mode == 'producer':
        logger.info('Starting Metrics producer')
        worker = MetricsProducer(config)
    elif args.start_mode == 'consumer':
        logger.info('Starting Metrics consumer')
        worker = MetricsConsumer(config)
    else:
        logger.error(f'Unknown command {args.start_mode}. Exiting.')
        sys.exit(1)

    worker.start_loop()


if __name__ == '__main__':
    main()
