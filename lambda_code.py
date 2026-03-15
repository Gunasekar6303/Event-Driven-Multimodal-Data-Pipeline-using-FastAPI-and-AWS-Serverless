import boto3
import csv
import urllib.parse
from io import StringIO

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("your dynamodb table name")

def lambda_handler(event, context):

    # get bucket and file name
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key']
    )

    print("Processing file:", key)

    # read file from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')

    csv_file = StringIO(content)
    reader = csv.DictReader(csv_file)

    # insert rows into DynamoDB
    with table.batch_writer() as batch:
        for row in reader:
            print("Inserting:", row)
            batch.put_item(Item=row)

    return {
        "statusCode": 200,
        "message": "CSV processed successfully"
    }