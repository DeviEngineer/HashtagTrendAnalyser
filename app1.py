import streamlit as st
import boto3
from uuid import uuid4
from datetime import datetime, timezone
from botocore.exceptions import ClientError
from ui import apply_ui  # Import the UI function

# Apply custom UI
apply_ui()

# AWS configuration
aws_profile = 'devi_profile'  # Name of the profile configured with aws configure
aws_region = 'us-east-1'
lambda_function_name = 'MyHashtagFunction'
dynamodb_table_name = 'Posts'

# Initialize AWS clients with profile
session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
client = session.client('lambda')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)

# Function to fetch trending hashtags
def fetch_trending_hashtags():
    try:
        response = table.scan()
        items = response.get('Items', [])
        hashtag_counts = {}
        for item in items:
            for hashtag in item.get('hashtags', []):
                if hashtag in hashtag_counts:
                    hashtag_counts[hashtag] += 1
                else:
                    hashtag_counts[hashtag] = 1
        return hashtag_counts
    except ClientError as e:
        st.sidebar.error(f"Error fetching hashtags: {e}")
        return {}

# Sidebar display for trending hashtags
with st.sidebar:
    st.header("Trending Hashtags")
    hashtag_counts = fetch_trending_hashtags()
    if hashtag_counts:
        top_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        for hashtag, count in top_hashtags:
            st.write(f"{hashtag}: {count} times")
    else:
        st.write("No trending hashtags found.")

# Main app


# Post Section
st.header("Compose and Publish Post")

post_content = st.text_area("Write your post here...")
hashtags = st.text_input("Enter hashtags (comma-separated)")
audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"])
video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

if st.button("Post"):
    if post_content and hashtags:
        hashtags_list = [tag.strip() for tag in hashtags.split(',')]
        post_id = str(uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        payload = {
            "PostID": post_id,
            "post_content": post_content,
            "hashtags": hashtags_list,
            "timestamp": timestamp
        }
        try:
            # Save post to DynamoDB
            table.put_item(Item=payload)
            st.success("Post published successfully.")
        except ClientError as e:
            st.error(f"Error publishing post: {e}")
    else:
        st.error("Post content and hashtags are required.")
