# Hashtag Analyzer Application

## Overview
The Hashtag Analyzer Application is a platform that allows users to compose and publish posts, view posts, and analyze trending hashtags. The application leverages Streamlit for the user interface and AWS services such as DynamoDB and Lambda for backend functionality.

## Features
- **Compose and Publish Posts:** Users can write posts and include hashtags.
- **View Posts:** Users can view previously published posts.
- **Trending Hashtags:** Displays trending hashtags based on recent posts.

## Technologies Used
- **Frontend:** Streamlit
- **Backend:** AWS DynamoDB, AWS Lambda
- **Language:** Python

## Setup and Installation

### Prerequisites
- AWS CLI configured with a profile
- Python 3.8 or later
- Boto3
- Streamlit
- PIL

### Steps

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/hashtag-analyzer.git
    cd hashtag-analyzer
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up AWS Resources:**
    - Ensure your AWS CLI is configured with the profile specified in the code (`devi_profile`).
    - Run the AWS setup script to create the necessary IAM role, DynamoDB table, and Lambda function.
        ```bash
        python aws_setup.py
        ```

4. **Run the Streamlit Application:**
    ```bash
    streamlit run app.py
    ```

## AWS Setup Details
The `aws_setup.py` script performs the following:
- Creates an IAM role for the Lambda function with necessary permissions.
- Creates a DynamoDB table named `Posts` to store the posts.
- Deploys a Lambda function for hashtag analysis.

## Usage
- **Compose and Publish Post:**
    - Navigate to the "Post" page.
    - Write your post content.
    - Select or type hashtags.
    - Click "Post" to publish.
- **View Posts:**
    - Navigate to the "View" page.
    - Select a post to view its content, hashtags, and timestamp.
- **Trending Hashtags:**
    - Trending hashtags are displayed in the sidebar.
