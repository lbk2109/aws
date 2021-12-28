import boto3

### https://dev-navill.tistory.com/12
### aws configure 또는 IAM Role을 통해 이미 액세스가 가능한 경우
''' 1. Client
Client is low-level interface.
AWS API와 1:1 매칭되며 botocore 수준에서 조작이 필요할때
method is defined as snake_case.
'''
client = boto3.client('s3')

''' 2. Session
설정상태를 저장하고 client & resource 서비스를 생성하기 위한 권한을 부여하기 위해 사용
'''
session = boto3.Session()

''' 3. Resource
Resource is high-level object-oriented interface.
식별자(identifier)와 속성(attribute)을 사용.
자원에 대한 조작 위주
'''
bucket = boto3.resource('s3').Bucket(name="bucketName")


### S3 bucket에 연결
try:
  #client = boto3.client('s3')
  s3 = boto3.resource('s3')
except ClientError:
  from getpass import getpass
  s3 = boto3.resource('s3', aws_access_key_id=getpass('AWS_ACCESS_KEY_ID: '), aws_secret_access_key=getpass('AWS_SECRET_ACCESS_KEY: '), region_name=input('AWS_DEFAULT_REGION: '))
bucket = s3.Bucket(name="hyd-ojt-s3-01")

### Get file list from S3
bucket.object.filter(Delimeter='fileName', Prefix='folderName')

### Read file from S3 bucket
obj.get()['Body'].read().decode('utf-8')

### Read CSV from pandas
import pandas as pd
pd.read_csv(obj.get()['Body'])

### Download CSV from S3
bucket.download_file('key', 'fileName')
