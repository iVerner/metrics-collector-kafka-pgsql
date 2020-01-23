"""
Main module
"""
# Standard library imports
import logging
import argparse

# Third party imports

# Local application imports
from producer import MetricsProducer
from consumer import MetricsConsumer


def main():
    logger = logging.getLogger('metrics-collector-kafka-pgsql')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

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
        quit(1)

    worker.start_loop()


if __name__ == '__main__':
    main()
