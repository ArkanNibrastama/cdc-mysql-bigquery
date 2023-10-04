import json
from kafka import KafkaConsumer
from sendToBQ import BigQuery
from datetime import datetime

# initialize BQ connection
bq_table_name = 'expedition.order'
bq = BigQuery(table_name=bq_table_name)

# initialize consumer
topicName = 'source.expedition.order'
bootstrap_servers = ['localhost:29092']
consumer = KafkaConsumer (
                topicName , 
                auto_offset_reset='earliest', 
                bootstrap_servers = bootstrap_servers, 
                group_id='order-transactions'
            )

# read the topic message (data change)
print('reading the messages ...')
for m in consumer:

    # print(json.loads(m.value))
    if len(m) > 0:

        print('data enter...')
        data_changes = json.loads(m.value)
        utc_now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        # check if the data is available
        isAvailable = bq.isAvailable(data_changes['order_id'], bq_table_name)
        if isAvailable:
            # update the latest data
            bq.updateLastRecord(data_changes['order_id'], utc_now, bq_table_name)

        # insert the new data
        data = {
            'order_id': data_changes['order_id'],
            'user_id': data_changes['user_id'],
            'seller_id': data_changes['seller_id'],
            'product_id': data_changes['product_id'],
            'origin_office' : data_changes['origin_office'],
            'destination_office' : data_changes['destination_office'],
            'order_status': data_changes['order_status'],
            'date_now': utc_now
        }
        bq.insertData(data, bq_table_name)

        print('send to BQ!')