# Change Data Capture from RDBMS (MySQL) to Data Warehouse (BigQuery)

```bash
docker run -d --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123 -e MYSQL_USER=mysqluser -e MYSQL_PASSWORD=user123 debezium/example-mysql:2.3
```