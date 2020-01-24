# metrics-collector-kafka-pgsql

# Description
Service to collect computer metrics and send it via kafka to postgresql.

Consists of two components:
* producer, that collects metrics and sends it to kafka
* consumer, that receives data from kafka and sends it to postgresql 

# Installing

Let's asumme you have installed Kafka and PostgreSQL.

1. You have to install dependencies first because metrics-collector-kafka-pgsql package uploaded to test PyPI:
    
    python3 -m pip install kafka-python psycopg2 psutil

2. Install python package metrics-collector-kafka-pgsql:

    python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps metrics-collector-kafka-pgsql
    
3. Create the table "metrics_table" and function "insert_metrics" at PostgreSQL using scripts from directory sql/.
4. Download files ca.pem, service.cert and service.key needed to SSL connection to Kafka
5. Create configuration file

# Usage
python -m metrics-collector-kafka-pgsql [-h] [-c CONFIG] {producer,consumer}

Example: python3 -m metrics-collector-kafka-pgsql consumer -c /path/to/config/file/config.ini

# Configuring

Configuration file format:

## Section [metrics] 
* metrics_list - Set list of metrics to measure. Possible choises - cpu, memory, disk, network

    cpu - CPU overall load in percent
    
    memory - Memory usage in percent
    
    disk - Disk usage in percent
    
    network - sending and receiving speed via all network interfaces in Kb/s 

## Section [kafka]
Common for producer and consumer parameters

* host - kafka cluster network address
* port - port to connect
* topic - kafka topic to use

Producer specific parameters

* ssl_cafile - path to ca.pem
* ssl_certfile - path to service.cert
* ssl_keyfile - path to service.key

Consumer specific parameters

* client_id - Client name
* group_id - Group name

## Section [postgresql]

* host - postgresql network address
* port - port to connect
* user - username
* password - user password
* database -database name