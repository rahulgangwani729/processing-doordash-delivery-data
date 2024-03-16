# Processing Daily data using AWS

Objective:

This project involves creating an automated AWS-based solution for processing daily data. Daily JSON file will be uploaded to an
Amazon S3 bucket. An AWS Lambda function, triggered by the file upload, will filter the
records and save the filtered data to another S3 bucket.
Notifications regarding the processing outcome will be sent via Amazon SNS.


AWS Services:

 - Amazon S3 buckets
 - AWS Lambda
 - Amazon SNS
 - AWS IAM (for permissions)
 - AWS CodeBuild (for CI/CD)
