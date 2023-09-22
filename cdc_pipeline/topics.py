# list all kafka topics
from kafka import KafkaConsumer
bootstrap_servers = ['localhost:29092']
consumer = KafkaConsumer( bootstrap_servers=bootstrap_servers)
consumer.topics()