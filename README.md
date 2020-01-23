# metrics-collector-kafka-pgsql

# Description
Service to collect computer metrics and send it via kafka to postgresql.

Consists of two components:
* producer, that collects metrics and sends it to kafka
* consumer, that receives data from kafka and sends it to postgresql 

# Usage
python metrics-collector.py [-h] [-c CONFIG] {producer,consumer}

# Installing

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