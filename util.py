import boto3

# AWS configuration

aws_profile = 'devi_profile'  # Name of the profile configured with aws configure
aws_region = 'us-east-1'
role_name = 'MyLambdaDynamoDBRole'
lambda_function_name = 'MyHashtagFunction'
dynamodb_table_name = 'Posts'
lambda_zip_file = 'function.zip'

recommended_hashtags = [    "#dataengineering",    "#datascience",    "#bigdata",
    "#machinelearning",   "#ai",   "#deeplearning",    "#data",    "#analytics",
    "#iot",    "#cloudcomputing"]

def initialize_aws_clients():
    session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(dynamodb_table_name)
    return dynamodb,table
