"""
Main module
"""
import argparse
import logging
import sys

from .consumer import MetricsConsumer
from .producer import MetricsProducer


def main():
    """
    Main function
    """
    logger = logging.getLogger('metrics-collector-kafka-pgsql')
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

    if args.start_mode == 'producer':
        logger.info('Starting Metrics producer')
        worker = MetricsProducer(args.config)
    elif args.start_mode == 'consumer':
        logger.info('Starting Metrics consumer')
        worker = MetricsConsumer(args.config)
    else:
        logger.error(f'Unknown command {args.start_mode}. Exiting.')
        sys.exit()

    worker.start_loop()


if __name__ == '__main__':
    main()
