"""
    This module give the dynamodb client operation
"""
import uuid
import boto3

#pylint: disable=W0703
class DynamodDBClient:
    '''
        THis class will connect to DynamoDB using boto3
    '''
    def __init__(self):
        self.client = boto3.resource('dynamodb')


    def upload(self, table_name, payload):
        """
            This funtion will update the table with payload
        """
        print("============> The payload was pushed to table", table_name)
        try:
            payload["id"] = str(uuid.uuid4())
            return self.client.Table(table_name).put_item(Item=payload)
        except Exception as error:
            print ("Error happened while uploding to dynamodb", error)
            return {}

    def get_data(self, table_name, payload):
        """
            This function will retrive the data
            from table
        """
        print("The request payload", payload)
        try:
            return self.client.Table(table_name).get_item(Key=payload)

        except Exception as err:
            print("Error happened while getting data from dynamodb", err)
            return {}