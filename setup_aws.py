import boto3
import json
from botocore.exceptions import ClientError

# AWS configuration
aws_profile = 'devi_profile'  # Name of the profile configured with aws configure
aws_region = 'us-east-1'
role_name = 'MyLambdaDynamoDBRole'
lambda_function_name = 'MyHashtagFunction'
dynamodb_table_name = 'Posts'
lambda_zip_file = 'function.zip'  # Ensure you have this zip file ready

# Initialize clients with profile
session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
iam_client = session.client('iam')
lambda_client = session.client('lambda')
dynamodb = session.resource('dynamodb')

# Create IAM Role
def create_iam_role():
    try:
        assume_role_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }
            ]
        }

        # Create role
        role = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy)
        )
        print(f"Role created: {role_name}")

        # Attach policies
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AWSLambda_FullAccess'
        )
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess'
        )
        print(f"Policies attached to role: {role_name}")

        return role['Role']['Arn']

    except ClientError as e:
        print(f"Error creating IAM role: {e}")
        return None

# Create DynamoDB Table
def create_dynamodb_table():
    try:
        table = dynamodb.create_table(
            TableName=dynamodb_table_name,
            KeySchema=[
                {'AttributeName': 'PostID', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'PostID', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=dynamodb_table_name)
        print(f"DynamoDB table created: {dynamodb_table_name}")

    except ClientError as e:
        print(f"Error creating DynamoDB table: {e}")

# Create Lambda Function
def create_lambda_function(role_arn):
    try:
        response = lambda_client.create_function(
            FunctionName=lambda_function_name,
            Runtime='python3.8',
            Role=role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': open(lambda_zip_file, 'rb').read()},
            Description='Lambda function for hashtag analysis',
            Timeout=30,
            MemorySize=128
        )
        print(f"Lambda function created: {lambda_function_name}")
        print("Function ARN:", response['FunctionArn'])

    except ClientError as e:
        print(f"Error creating Lambda function: {e}")

def main():
    # Create IAM role
    role_arn = create_iam_role()
    if role_arn:
        # Create DynamoDB table
        create_dynamodb_table()
        # Create Lambda function
        create_lambda_function(role_arn)

if __name__ == "__main__":
    main()
