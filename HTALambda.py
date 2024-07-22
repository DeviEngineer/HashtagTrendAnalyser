import json
import boto3
from uuid import uuid4
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Posts')

def lambda_handler(event, context):
    post_id = str(uuid4())
    post_content = event.get('post_content', '')
    hashtags = event.get('hashtags', [])
    file_url = event.get('file_url', '')
    timestamp = datetime.utcnow().isoformat()

    table.put_item(
        Item={
            'PostID': post_id,
            'PostContent': post_content,
            'Hashtags': set(hashtags),
            'FileURL': file_url,
            'Timestamp': timestamp
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Post saved successfully!')
    }