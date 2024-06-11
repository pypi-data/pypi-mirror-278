import boto3
import os
import json
from botocore.exceptions import ClientError

class S3Client:
    def __init__(self):
        self.service_name = "s3"
        self.access_key = os.getenv("ACCESS_KEY")
        self.secret_key = os.getenv("SECRET_KEY")
        # self.region_name = os.getenv("S3_REGION_NAME")
        self.bucket_name = os.getenv("DOWNLOAD_BUCKET_NAME")


    def upload_file(self, file_name, original_file_name, object_name=None):
        s3_client = boto3.client(
            self.service_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            endpoint_url=os.getenv("ENDPOINT_URL")
        )
        response = s3_client.upload_file(
            file_name,
            self.bucket_name,
            object_name,
            ExtraArgs={
                'ContentDisposition': f'attachment; filename="{original_file_name}"'
            })
        return response

    def create_bucket(self, bucket_name):
        s3_client = boto3.client(
            self.service_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            endpoint_url=os.getenv("ENDPOINT_URL")
        )

        try:
            response = s3_client.create_bucket(Bucket=bucket_name)

            bucket_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
                    }
                ]
            }

            # 버킷 정책 설정
            policy_string = json.dumps(bucket_policy)
            s3_client.put_bucket_policy(Bucket=bucket_name, Policy=policy_string)
            return response
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'BucketAlreadyExists' or error_code == 'BucketAlreadyOwnedByYou':
                pass
            else:
                raise