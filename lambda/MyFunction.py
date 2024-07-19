import json
import boto3

def main(event, context):
    for record in event['Records']:
        message = json.loads(record['body'])
        if 'type' in message and message['type'] == 'Order':
            client = boto3.client('events')
            client.put_events(
                Entries=[
                    {
                        'Source': 'my.source',
                        'DetailType': 'Order',
                        'Detail': json.dumps(message)
                    }
                ]
            )
    return "Message processed."
