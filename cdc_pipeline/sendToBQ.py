from google.cloud import bigquery
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credentials.json'

class BigQuery():

    def __init__(self) -> None:
        self.client = bigquery.Client()

    def isAvailable(self, order_id:int, table_name:str) -> bool:

        query = f'''
            SELECT order_id
            FROM `{table_name}`
            WHERE order_id = {order_id}
            LIMIT 1;
        '''
        query_job = self.client.query(query=query)
        result = query_job.result()
        total_row = result.total_rows

        if total_row == 0:
            return False
        else:
            return True

    def updateLastRecord(self, order_id:int, date_now:str, table_name:str) -> None:

        query = f'''
            UPDATE `{table_name}` 
            SET end_date='{date_now}' 
            WHERE order_id={order_id}
            AND end_date IS NULL; 
        '''

        query_job = self.client.query(query=query)
        query_job.result()
        print("data has been updated!")

    def insertData(self, data:list, table_name:str) -> None:
        
        query = f'''
            INSERT INTO `{table_name}` VALUES (
                {data['order_id']}, 
                {data['user_id']}, 
                {data['seller_id']}, 
                {data['product_id']}, 
                '{data['order_status']}', 
                '{data['date_now']}', 
                NULL
            );
        '''
        query_job = self.client.query(query=query)
        query_job.result()
        print("data has been loaded!")
