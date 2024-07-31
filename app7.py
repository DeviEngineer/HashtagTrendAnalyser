import streamlit as st
import boto3
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from botocore.exceptions import ClientError
from streamlit_option_menu import option_menu  # For navigation menu
from PIL import Image

# Set page config first
st.set_page_config(page_title="Hashtag Analyzer", page_icon="")

# Apply custom UI
def apply_ui():
    primaryColor = "#4CAF50"
    secondaryColor = "#E0E0E0"
    backgroundColor = "#E1D6EF"
    sidebarBackgroundColor = "#F0F0F0"
    buttonColor = "#6A1B9A"
    title_color = "#6A1B9A"
    header_color = "#12BE5D"

    custom_css = f"""
    <style>
    body {{
        background-color: {secondaryColor};
        font-family: Arial, sans-serif;
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: {sidebarBackgroundColor};
        font-family: Arial, sans-serif;
        color: #333333;
    }}
    .stButton > button {{
        background-color: {buttonColor};
        color: white;
        padding: 15px 25px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        border-radius: 5px;
    }}
    .stButton > button:hover {{
        background-color: #4A148C;
    }}
    .sidebar-header {{
        font-size: 24px;
        color: {title_color};
        font-weight: bold;
    }}
    
    
    </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)

 
st.sidebar.image("C://Users//ADMIN//Desktop//GUVI//HTimg.png", use_column_width=True)
st.title("Data Engineering Insights and Trends")
apply_ui()

# AWS configuration
aws_profile = 'devi_profile'
aws_region = 'us-east-1'
dynamodb_table_name = 'Posts'

# Initialize AWS clients with profile
session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
dynamodb = session.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)

# Recommended hashtags (static list)
recommended_hashtags = [
    "#dataengineering",
    "#datascience",
    "#bigdata",
    "#machinelearning",
    "#ai",
    "#deeplearning",
    "#data",
    "#analytics",
    "#iot",
    "#cloudcomputing"
]

# Function to fetch trending hashtags
def fetch_trending_hashtags():
    try:
        one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)
        response = table.scan()
        print(response)
        items = response.get('Items', [])

        hashtag_counts = {}
        for item in items:
            if 'timestamp' in item:
                post_time = datetime.fromisoformat(item['timestamp'])
                if post_time >= one_day_ago:
                    for hashtag in item.get('hashtags', []):
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

# Display post content and hashtags section
def post_content_page():
    st.header("Compose and Publish Post")

    post_content = st.text_area("Write your post content here...", "")
    if post_content:
        selected_hashtags = st.multiselect(
            "Select from recommended hashtags",
            options=recommended_hashtags
        )
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
                        table.put_item(Item=payload)
                        st.success("Post published successfully.")
                        st.experimental_rerun()
                    except ClientError as e:
                        st.error(f"Error publishing post: {e}")
                else:
                    st.error("At least one hashtag is required.")
            else:
                st.error("Hashtags are required.")
    else:
        st.error("Post content is required.")

# Display post view page
def view_post_page():
    st.header("View Posts")
    posts = table.scan().get('Items', [])
    print(["test123"]+posts)
    if posts:
        post_titles = [" ".join(post['post_content'].split()[:4]) for post in posts]
        selected_title = st.selectbox("Select a post to view", options=post_titles)
        
        selected_post = next(post for post in posts if " ".join(post['post_content'].split()[:4]) == selected_title)
        
        st.subheader("Post Content")
        st.write(selected_post['post_content'])
        
        st.subheader("Hashtags")
        st.write(", ".join(selected_post['hashtags']))
        
        st.subheader("Timestamp")
        st.write(selected_post['timestamp'])
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

