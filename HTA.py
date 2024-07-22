import streamlit as st
import boto3
import json
from datetime import datetime
import base64
from io import BytesIO

# AWS configuration
aws_region = 'your-region'  # Replace with your AWS region
lambda_function_name = 'your-lambda-function-name'  # Replace with your Lambda function name
dynamodb_table_name = 'Posts'  # DynamoDB table name

# Initialize AWS clients
client = boto3.client('lambda', region_name=aws_region)
dynamodb = boto3.resource('dynamodb', region_name=aws_region)
table = dynamodb.Table(dynamodb_table_name)

def upload_file(file, file_type):
    """Helper function to upload file to S3."""
    s3 = boto3.client('s3', region_name=aws_region)
    bucket_name = 'your-bucket-name'  # Replace with your S3 bucket name
    file_name = file.name
    s3.upload_fileobj(file, bucket_name, file_name)
    return f'https://{bucket_name}.s3.{aws_region}.amazonaws.com/{file_name}'

def compose_and_publish_post():
    st.header("Compose and Publish Post")

    post_content = st.text_area("Write your post here...")
    hashtags = st.text_input("Enter hashtags (comma-separated)")
    
    # Upload media files
    uploaded_file = st.file_uploader("Choose a file (image, audio, video)", type=['jpg', 'png', 'jpeg', 'mp3', 'wav', 'mp4'])
    file_url = None

    if uploaded_file is not None:
        file_url = upload_file(uploaded_file, uploaded_file.type)
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)  # Preview for images
        st.audio(uploaded_file, format='audio/mp3')  # Preview for audio
        st.video(uploaded_file)  # Preview for video

    if st.button("Post"):
        if post_content or file_url:
            hashtags_list = [tag.strip() for tag in hashtags.split(',')] if hashtags else []
            payload = {
                "post_content": post_content,
                "hashtags": hashtags_list,
                "file_url": file_url
            }
            response = client.invoke(
                FunctionName=lambda_function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload)
            )
            response_payload = json.loads(response['Payload'].read())
            st.success(response_payload['body'])
        else:
            st.error("Post content or file is required.")

def show_trending_hashtags():
    st.header("Trending Hashtags")
    if st.button("Show Trending Hashtags"):
        response = table.scan()
        items = response.get('Items', [])
        hashtag_counts = {}
        for item in items:
            for hashtag in item.get('Hashtags', []):
                hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
        if hashtag_counts:
            st.subheader("Trending Hashtags")
            for hashtag, count in sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True):
                st.write(f"{hashtag}: {count} times")
        else:
            st.write("No hashtags found.")

def display_dynamic_trending_hashtags():
    st.header("Live Trending Hashtags")
    hashtag_counts = fetch_trending_hashtags()
    if hashtag_counts:
        for hashtag, count in sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True):
            st.write(f"{hashtag}: {count} times")
    else:
        st.write("No hashtags found.")

def fetch_trending_hashtags():
    response = table.scan()
    items = response.get('Items', [])
    hashtag_counts = {}
    for item in items:
        for hashtag in item.get('Hashtags', []):
            hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
    return hashtag_counts

def main():
    st.title("Social Media Hashtag Trend Analyzer")
    compose_and_publish_post()
    show_trending_hashtags()
    display_dynamic_trending_hashtags()

if __name__ == "__main__":
    main()
