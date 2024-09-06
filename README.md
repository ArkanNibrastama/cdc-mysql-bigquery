# Change Data Capture from RDBMS (MySQL) to Data Warehouse (BigQuery)

## Intro
In the highly competitive logistics and expedition industry, businesses must continuously optimize their operations to stay ahead. For an expedition company, this means efficiently managing warehouse capacities, employee allocations, and processing times. The challenge lies in accurately tracking the time span of each business process and identifying areas that need improvement. The "CDC and SCD Approach to Enhancing Expedition Operations" project addresses this challenge by implementing a data pipeline that leverages Change Data Capture (CDC) and Slowly Changing Dimension (SCD) type 2. This approach allows the company to monitor changes in key processes and make data-driven decisions to optimize operations, such as adjusting warehouse capacities or reallocating employees to high-demand locations.

## Goals
The primary goals of the CDC and SCD project include:

1. <b>Real-Time Data Tracking:</b> Implement CDC to monitor and capture real-time changes in order statuses (e.g., processing, shipping, arrived) and stream this data into BigQuery via Kafka. This enables the company to maintain an up-to-date view of business operations across all locations.

2. <b>Historical Data Management:</b> Use SCD type 2 to track and store the history of changes in key business processes. By updating the end_date field in the data warehouse before inserting new records, the company can maintain a comprehensive history of each process, allowing for more accurate analysis and decision-making.

3. <b>Operational Optimization:</b> Utilize the insights gained from real-time and historical data to identify and optimize underperforming warehouses or offices. The goal is to enhance overall business efficiency, reduce operational bottlenecks, and improve service delivery times.

## Solution
![img](src/data_architecture.png)


## How to build
- Clone the project 

    ```bash
    git clone https://github.com/ArkanNibrastama/cdc-mysql-bigquery.git
    ```
- Install all the dependencies

    ```bash
    pip install -r requirements.txt
    ```
- Build all the containers

    ```bash
    docker-compose up -d
    ```
- Create database on mysql container, you can   use universal database tool like DBeaver to create database, or you can go to mysql container > terminal then type

    ```bash
    mysql -u root -p 123
    ```
    then 

    ```bash
    CREATE DATABASE expedition;
    ```

- Run the API
    ```bash
    uvicorn orderAPI:api --reload
    ```

- Make a Debezium connector

    ```json
    {
        "name": "expedition-order-connector",  
        "config": {  
            "connector.class": "io.debezium.connector.mysql.MySqlConnector",
            "tasks.max": "1",  
            "database.hostname": "mysql",  
            "database.port": "3306",
            "database.user": "root",
            "database.password": "123",
            "database.server.id": "184054",
            "topic.prefix": "source",  
            "database.include.list": "expedition",  
            "schema.history.internal.kafka.bootstrap.servers": "kafka:9092",  
            "schema.history.internal.kafka.topic": "schemahistory.expedition",
            "transforms" : "unwrap",
            "transforms.unwrap.type" : "io.debezium.transforms.ExtractNewRecordState",
            "key.converter.schemas.enable": "false",
            "value.converter.schemas.enable": "false",
            "value.converter": "org.apache.kafka.connect.json.JsonConverter",
            "key.converter": "org.apache.kafka.connect.json.JsonConverter"
        }
    }
    ```
    make an API request (POST) and fill the header with JSON configuration below.

- Check the topics
    ```bash
    python topics.py
    ```
    if there is no source.expedition.order topic, try to create new data on the API then try to run this code again.

- Send data into BigQuery by run consumer.py, before that make sure to add the service account json file and create expedition dataset on BigQuery
    ```bash
    python consumer.py
    ```

## Conclusion
The implementation of the CDC and SCD approach has had a significant impact on the expedition company's operations. By enabling real-time tracking and comprehensive historical analysis, the company has been able to identify inefficiencies in their processes and make informed decisions to <b>optimize warehouse capacities and employee allocations</b>. As a result, <b>the company can optimize approximately 30% of the delivery process</b>, leading to increased customer satisfaction and a stronger competitive position in the market.

## Full explanation
To make better understand of this repository, you can check my Medium post about this project [CDC and SCD Approach to Enhancing Expedition Operations](https://medium.com/@arkan6040nibrastama/cdc-and-scd-approach-to-enhancing-expedition-operations-3a75256c2b74).