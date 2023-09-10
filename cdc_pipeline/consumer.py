from kafka import KafkaConsumer

topicName = 'data_change'
server = ['localhost:29092']

consumer = KafkaConsumer(topicName, auto_offset_reset='earliest', bootstrap_servers=server, consumer_timeout_ms=10000)

for m in consumer:

    print(f'Topic name = {m.topic}, message = {m.value}')