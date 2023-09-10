from kafka import KafkaProducer
from json import dumps

topic = 'data_change'

server = ['localhost:29092']

producer = KafkaProducer(value_serializer=lambda m: dumps(m).encode('utf-8'), bootstrap_servers = server)

producer.send(topic=topic, value={'name':'arkan'})

print("Message sent")