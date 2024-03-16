import json
import pandas as pd
import boto3
import datetime

s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

sns_arn = 'arn:aws:sns:us-east-1:730335310416:email-processing-notification-doordash'

def lambda_handler(event, context):
    print("Event: ", event)

    try:

        bucket_name = event['Records']['s3']['bucket']['name']
        key_name = event['Records']['s3']['object']['key']

        print("Bucket name: ", bucket_name)
        print("Object name: ", key_name)

        s3_path = s3_client.get_object(Bucket=bucket_name, Key=key_name)

        df = pd.read_csv(s3_path['Body'], sep=",")

        print(df.head(2))

        df_filtered = df[df['status'] == 'delivered']

        json_object = df_filtered.to_json(orient ='records')

        file_name = datetime.date.today().strftime('%Y-%m-%d') + '-processed.json'

        response = s3_client.put_object(Body=json.dumps(json_object), Bucket='doordash-target-zn-aws', Key=file_name)

        print(response)

        message_body = f"{file_name} successfully processed and saved in s3 bucket."

        subject = "SUCCESS - Daily Data Processing"

        sns_response = sns_client.publish(TargetArn=sns_arn, Message=message_body, Subject=subject, MessageStructure='text')

    except Exception as e:
        print(e)
        subject = "Failed to process the file."
        message_body = "FAILED - Daily Data Processing"
        sns_response = sns_client.publish(TargetArn=sns_arn, Message=message_body, Subject=subject, MessageStructure='text')
