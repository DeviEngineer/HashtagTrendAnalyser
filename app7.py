import json
import streamlit as st
import boto3
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from botocore.exceptions import ClientError
from streamlit_option_menu import option_menu  # For navigation menu
import ui
import util as ut
from setup_aws import lambda_client 
dynamodb, table = ut.initialize_aws_clients()


# Set page config first
st.set_page_config(page_title="Hashtag Analyzer", page_icon="")
ui.apply_ui()
st.sidebar.image("C://Users//ADMIN//Desktop//GUVI//HTimg.png", use_column_width=True)
st.title("Data Engineering Insights and Trends")

def fetch_trending_hashtags():
    try:
        one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)
        response = table.scan()
        print(response)
        items = response.get('Items', [])

        hashtag_counts = {}
        for item in items:
            if 'Timestamp' in item:
                post_time = datetime.fromisoformat(item['Timestamp'])
                if post_time >= one_day_ago:
                    for hashtag in item.get('Hashtags', []):
                        if hashtag in hashtag_counts:
                            hashtag_counts[hashtag] += 1
                        else:
                            hashtag_counts[hashtag] = 1
        return hashtag_counts
    except ClientError as e:
        st.sidebar.error(f"Error fetching hashtags: {e}")
        return {}

# Display trending hashtags in sidebar
def display_trending_hashtags():
    with st.sidebar:
        st.header("Trending Hashtags")
        hashtag_counts = fetch_trending_hashtags()
        if hashtag_counts:
            total_counts = sum(hashtag_counts.values())
            top_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            for hashtag, count in top_hashtags:
                percentage = (count / total_counts) * 100
                st.write(f"{hashtag}: {percentage:.2f}%")
                st.progress(percentage / 100)
        else:
            st.write("No trending hashtags found.")
def post_content_page():# Display post content and hashtags section
    st.header("Compose and Publish Post")
    post_content = st.text_area("Write your post content here...", "")
    if post_content:
        selected_hashtags = st.multiselect("Select from recommended hashtags",options=ut.recommended_hashtags)
        custom_hashtags = st.text_input("Or type custom hashtags (comma-separated)")
        if st.button("Post"):
            if selected_hashtags or custom_hashtags:
                hashtags_list = selected_hashtags
                if custom_hashtags:
                    custom_tags = [tag.strip() for tag in custom_hashtags.split(',')]
                    hashtags_list.extend(custom_tags)
                if hashtags_list:
                    post_id = str(uuid4())
                    timestamp = datetime.now(timezone.utc).isoformat()
                    payload = {
                        "PostID": post_id,
                        "post_content": post_content,
                        "hashtags": hashtags_list,
                        "timestamp": timestamp
                    }
                    try:
                        print (lambda_client)
                        # Invoke the Lambda function
                        response = lambda_client.invoke(
                            FunctionName='MyHashtagFunction',  # Replace with your Lambda function name
                            InvocationType='RequestResponse',
                            Payload=json.dumps(payload)
                        )
                        print("tesat response")
                        print(response)
                        response_payload = json.loads(response['Payload'].read())
                        print("testresp111source")
                        print(response_payload)
                        if response['StatusCode'] == 200:
                            st.success("Post published successfully.")
                            st.rerun()
                        else:
                            st.error(f"Error publishing post: {response_payload}")
                    except Exception as e:
                        st.error(f"Error publishing post: {e}")
                    # try:
                    #     table.put_item(Item=payload)
                    #     st.success("Post published successfully.")
                    #     st.rerun()
                    # except ClientError as e:
                    #     st.error(f"Error publishing post: {e}")
                else:
                    st.error("At least one hashtag is required.")
            else:
                st.error("Hashtags are required.")
    else:
        st.error("Post content is required.")

# def post_content_page():
#     st.header("Compose and Publish Post")
#     post_content = st.text_area("Write your post content here...", "")
#     if post_content:
#         selected_hashtags = st.multiselect("Select from recommended hashtags", options=ut.recommended_hashtags)
#         custom_hashtags = st.text_input("Or type custom hashtags (comma-separated)")
#         if st.button("Post"):
#             if selected_hashtags or custom_hashtags:
#                 hashtags_list = selected_hashtags
#                 if custom_hashtags:
#                     custom_tags = [tag.strip() for tag in custom_hashtags.split(',')]
#                     hashtags_list.extend(custom_tags)
#                 if hashtags_list:
#                     post_id = str(uuid4())
#                     timestamp = datetime.now(timezone.utc).isoformat()
#                     payload = {
#                          "PostID": post_id,
#                          "post_content": post_content,
#                          "hashtags": hashtags_list,
#                          "file_url": "Test",
#                          "timestamp": timestamp
#                      }
#                     print("tesat payloa")
#                     print(payload)
#                     try:
#                         print (lambda_client)
#                         # Invoke the Lambda function
#                         response = lambda_client.invoke(
#                             FunctionName='MyHashtagFunction',  # Replace with your Lambda function name
#                             InvocationType='RequestResponse',
#                             Payload=json.dumps(payload)
#                         )
#                         print("tesat response")
#                         print(response)
#                         response_payload = json.loads(response['Payload'].read())
#                         print("testresp111source")
#                         print(response_payload)
#                         if response['StatusCode'] == 200:
#                             st.success("Post published successfully.")
#                             st.rerun()
#                         else:
#                             st.error(f"Error publishing post: {response_payload}")
#                     except Exception as e:
#                         st.error(f"Error publishing post: {e}")
#                 else:
#                     st.error("At least one hashtag is required.")
#             else:
#                 st.error("Hashtags are required.")
#     else:
#         st.error("Post content is required.")





# Display post view page
def view_post_page():
    st.header("View Posts")
    posts = table.scan().get('Items', [])
    print(["test123"]+posts)
    if posts:
        post_titles = [" ".join(post['PostContent'].split()[:4]) for post in posts]
        selected_title = st.selectbox("Select a post to view", options=post_titles)
        
        selected_post = next(post for post in posts if " ".join(post['PostContent'].split()[:4]) == selected_title)
        
        st.subheader("Post Content")
        st.write(selected_post['PostContent'])
        
        st.subheader("Hashtags")
        st.write(", ".join(selected_post['Hashtags']))
        
        st.subheader("Timestamp")
        st.write(selected_post['Timestamp'])
    else:
        st.write("No posts found.")

# Main page navigation
def main():
    display_trending_hashtags()
    
    menu = option_menu(
        menu_title=None,
        options=["Post", "View"],
        icons=["pencil", "eye"],
        default_index=0,
        orientation="horizontal",
    )

    if menu == "Post":
        post_content_page()
    elif menu == "View":
        view_post_page()

if __name__ == "__main__":
    main()

