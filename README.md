# HashtagTrendAnalyser
# Social Media Hashtag Trend Analyzer

## Problem Statement
In today's era of social media dominance, users crave platforms that offer seamless posting experiences while also providing insights into trending topics. This project addresses these needs by developing a Streamlit application that allows users to compose and publish posts with text, hashtags, and media files (images, audio, and video). The application integrates with AWS Lambda and DynamoDB to process posts and analyze trending hashtags in real-time.

## Features
- **Post Composition**: Users can write posts containing text and hashtags, and upload media files (images, audio, video).
- **Post Submission**: Upon clicking the "Post" button, the application triggers a backend process that sends the post content and media to AWS Lambda.
- **AWS Lambda Integration**: AWS Lambda receives the post content and media, extracts hashtags, and stores the data in DynamoDB.
- **Trending Hashtags**: Users can view trending hashtags by clicking the "Show Trending Hashtags" button, which analyzes the DynamoDB table to identify popular hashtags.
- **Dynamic Updates**: Trending hashtags dynamically update as new posts are made, providing real-time insights.
- **User Interface**: The application offers an intuitive and user-friendly interface for composing posts and exploring trending hashtags.

## Tools Used
- **Streamlit**: For creating the frontend interface.
- **AWS Lambda**: For backend processing.
- **DynamoDB**: For storing post data and hashtag analysis.
- **Boto3**: AWS SDK for Python to interact with AWS services.

## Setup Instructions

### Prerequisites
- **Python**: Ensure Python 3.7 or later is installed.
- **AWS Account**: For deploying Lambda and DynamoDB.
- **S3 Bucket**: Create an S3 bucket for storing media files.

### Setup Steps

1. **Clone the Repository**
    ```sh
    git clone <repository_url>
    cd social_media_hashtag_trend_analyzer
    ```

2. **Install Dependencies**
    ```sh
    pip install streamlit boto3
    ```

3. **Set Up AWS Lambda**
    - Deploy the provided AWS Lambda function to your AWS account.
    - Make sure the Lambda function has permissions to read/write to DynamoDB and upload files to S3.

4. **Create DynamoDB Table**
    - Create a DynamoDB table named `Posts` with the following attributes:
        - `PostID` (Primary Key, String)
        - `PostContent` (String)
        - `Hashtags` (String Set)
        - `FileURL` (String)
        - `Timestamp` (String)

5. **Set Up S3 Bucket**
    - Create an S3 bucket for uploading media files.
    - Ensure the Lambda function has the necessary permissions to upload files to this bucket.

6. **Run the Streamlit App**
    ```sh
    streamlit run app.py
    ```

7. **Interact with the Application**
    - Compose and publish posts with text, hashtags, and media.
    - View and analyze trending hashtags.

## Future Enhancements
- **User Authentication**: Add user authentication to manage sessions and secure data.
- **Advanced Analytics and Visualizations**: Incorporate advanced analytics and visualizations for deeper insights.
- **Performance Optimization**: Optimize application performance, especially with large datasets.
