import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):

    source = event['currentIntent']['slots']['Source']
    destination = event['currentIntent']['slots']['Destination']
    
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    table = dynamodb.Table('city')
    
    response = table.query(
        KeyConditionExpression=Key('source').eq('Chicago') & Key('destination').eq('urbana')
    )
    
    for i in response['Items']:
        distance = i['distance']
        
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "SSML",
              "content": "The distance between {source} and {destination} is {distance}.".format(source=source, destination=destination, distance=distance)
            },
        }
    }
    print('result = ' + str(response))
    return response