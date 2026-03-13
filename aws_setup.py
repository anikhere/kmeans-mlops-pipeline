import os 
import boto3
from dotenv import load_dotenv
load_dotenv()
def connect_to_s3():
        s3_client = boto3.client(
            's3',
            aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key = os.getenv('AWS_SECRET_KEY'),
            region_name = os.getenv('AWS_REGION','ap-south-1')
        
        )
        return s3_client

def upload_to_s3(local_file:str,bucket_name:str,s3_file_name:str):
        
        s3 = connect_to_s3()
        s3.upload_file(local_file,bucket_name,s3_file_name)
        print(f"✅ Uploaded {local_file} to s3://{bucket_name}/{s3_file_name}")


def download_from_s3(bucket_name:str,s3_file_name:str,local_file_path:str):
        
        s3 = connect_to_s3()
        s3.download_file(bucket_name,s3_file_name,local_file_path)
        print(f"✅ Downloaded s3://{bucket_name}/{s3_file_name} to {local_file_path}")


def create_s3_bucket(bucket_name:str):
        s3 = connect_to_s3()
        region = os.getenv('AWS_REGION','ap-south-1')
        try:
            s3.create_bucket(
            Bucket = bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint':region
            }
              )
            print(f"✅ Bucket {bucket_name} created in {region}")
        except Exception as e:
               print(f'ok the {e} exists')


if __name__ == "__main__":
        Bucket = 'kmeans-mlops-bucket-user'
        create_s3_bucket(bucket_name=Bucket)
        upload_to_s3(bucket_name=Bucket,s3_file_name='results.png',local_file='outputs/results.png')
        download_from_s3(Bucket, s3_file_name="results.png",local_file_path= "outputs/results.png")

