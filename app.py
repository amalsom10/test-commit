from flask import Flask
from flask import request, jsonify
import boto3
import datetime
import os
from botocore.exceptions import ClientError
import logging
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='appLog.log',
                    filemode='w')

def get_requesttype(headers):
    requestHeaders = dict(headers)
    return requestHeaders['Content-Type']


# defines an object for the application
app = Flask(__name__)

# os.environ['AWS_SECRET_ACCESS_KEY'] = "ADSDFSGFVHSGFVSDCSGCHSSCHG"
# os.environ['AWS_ACCESS_KEY_ID'] = 'ADSHGDDHGSCDSHGDCH'


db = boto3.resource('dynamodb', endpoint_url='http://dynamohost:8000', region_name="us-west-2")


def create_dynamodb():
    table = db.create_table(
        TableName='chatbox',
        KeySchema=[
            {
                'AttributeName': 'created',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'conversation_id',
                'KeyType': 'RANGE'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'created',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'conversation_id',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 8,
            'WriteCapacityUnits': 8,
        }
    )
    logging.info('Waiting for table to created')
    logging.info("Table status:", table.table_status)


client = boto3.client('dynamodb', endpoint_url='http://dynamohost:8000', region_name='us-west-2')


def check_dynamo():
    try:
        response = client.describe_table(TableName='chatbox')
    except ClientError as ce:
        if ce.response['Error']['Code'] == 'ResourceNotFoundException':
            logging.debug("Table   does not exist. Create the table ")
            create_dynamodb()
        else:
            logging.error("Unknown exception occurred while querying for the  table. Printing full error:")
            logging.error(ce.response)


check_dynamo()


def generate_response(status, action, info=None, error=None, response=None):
    responsedata = {
      'status': status,
      'action': action,
      'info': info,
      'error': error,
      'response': response
    }
    return jsonify(responsedata)


table_name = db.Table('chatbox')


# Allows the user to post messages to the store using the HTTP POST method
@app.route('/message', methods=['POST'])
def add_message():
    if get_requesttype(request.headers) == 'application/x-www-form-urlencoded':
        requestdata = request.form
    elif get_requesttype(request.headers) == 'application/json':
        requestdata = request.json
    else:
        return generate_response(451, "Add Message", info="Failed", error="Invalid request: Only x-www-form-urlencoded or json")

    if requestdata['message'] is None or requestdata['message'] not in ["", " "] or requestdata['sender'] not in ["", " "] or requestdata['conversation_id'] not in ["", " "]:
        logging.debug("Missing fields in post requests")
        return generate_response(200, "Add Message", info="Failed", error="No or Blank field  data")

    message_data = {
      'created': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
      'conversation_id': requestdata['conversation_id'],
      'sender': requestdata['sender'],
      'message': requestdata['message']
    }
    table_name.put_item(Item=message_data)
    return generate_response(200, "Add Message", info="Success", response=message_data)

# Allows the user to retrieve specific message from the store using the HTTP GET method and


@app.route('/conversations/<conversation_id>', methods=['GET'])
def list_specificmessage(conversation_id):
    all_message = table_name.scan()
    my_message = []
    for i in all_message['Items']:
        if i['conversation_id'] == conversation_id:
            my_message.append(i)
    for ele in my_message:
        del ele['conversation_id']
    data={}
    data['id'] = conversation_id
    data['messages'] = my_message
    if my_message == []:
        logging.debug("No messages found with conversation_id")
        return generate_response(404, "List messages under a conversation id", info="Failed", error="No message with conversation id " + conversation_id)
    else:
        return generate_response(200, "List messages under a conversation id", info="Success::", response=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
