import boto3
import botocore
import os
import pickle
import io
import sys
from research_framework.base.storage.base_storage import BaseStorage

class S3Storage(BaseStorage):
    def __init__(self, bucket):
        self.client = boto3.client(
                service_name='s3',
                region_name=os.environ['REGION_NAME'],
                aws_access_key_id=os.environ['ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['ACCESS_KEY'],
                endpoint_url=os.environ["ENDPOINT_URL"],
                use_ssl=True
        )
        self.bucket = bucket

    def upload_file(self, file, file_name, direct_stream=False):
        try:
            binary = pickle.dumps(file)
            print("- Binary prepared!")
            stream = io.BytesIO(binary)
            print("- Stream ready!")
            print(f" \t * Object size {sys.getsizeof(binary) * 1e-9} GBs ")
            self.client.put_object(
                Body=stream,
                Bucket=self.bucket,
                Key=file_name
            )
            
            print('Upload Complete!')
            return file_name
        except Exception as ex:
            print(f'An error ocurred > {ex}')
            return None

    def list_stored_files(self):
        try:
            return self.client.list_objects_v2(Bucket=self.bucket)['Contents']
        except Exception as ex:
            print(f'An error ocurred > {ex}')
            return None

    def get_file_by_id(self, file_id):
        try:
            obj = self.client.get_object(Bucket=self.bucket, Key=file_id)
            return obj['Body'].read()
        except Exception as ex:
            print(f'An error ocurred > {ex}')
            return None

    def check_if_exists(self, file_id):
        try:
            self.client.head_object(Bucket=self.bucket, Key=file_id)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                print(f'An error ocurred > {e}')
                return None
            
        return True

    def download_file(self, file_id=None):
        try:
            obj = self.client.get_object(Bucket=self.bucket, Key=file_id)
            return pickle.loads(obj['Body'].read())
        except Exception as ex:
            print(f'An error ocurred > {ex}')
            return None

    def delete_file(self, file_id):
        try:
            if self.check_if_exists(file_id):
                self.client.delete_object(Bucket=self.bucket, Key=file_id)
                if self.check_if_exists(file_id):
                    print("Couldn't delete file")
                else:
                    print("Deleted!")
            else:
                raise FileExistsError("No existe en el bucket")
            
        except Exception as ex:
            print(f'An error ocurred > {ex}')
