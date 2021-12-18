

import sys
import boto3
import json
from typing import Mapping
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from datetime import datetime


# from datetime import datetime

class StopWatch:
    def __init__(self):
        self.reset()

    def reset(self):
        self.start_datetime = None
        self.end_datetime = None
        self.message = None
        
    def start(self, message):
        self.reset()
        self.start_datetime = datetime.now()
        self.message = message
        print(f'### StopWatch::Start({self.message}, {self.start_datetime})')
        
    def stop(self):
        self.end_datetime = datetime.now()
        return self.get_elapsed_seconds()
        
    def get_elapsed_seconds(self):
        assert isinstance(self.start_datetime, datetime), 'call start() first'
        assert isinstance(self.end_datetime, datetime),   'call end() fist'
        # Return the total number of seconds contained in the duration
        # Equivalent to td / timedelta(seconds=1)
        elapsed_seconds =  (self.end_datetime - self.start_datetime).total_seconds()
        print(f'### StopWatch::Stop({self.message}, {self.end_datetime})')
        print(f'### StopWatch::Elapsed_Seconds: {elapsed_seconds}')


# Glue Job 수행에 필요한 기본 변수 선언 glue context, spark session 등..
# args = getResolvedOptions(sys.argv, ['JOB_NAME', 'TABLE_LIST'])
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
logger = glueContext.get_logger()


job.init(args['JOB_NAME'], args)


#SecretsManager 
secret_name = "JK-JOBIA-DEV-ETL-TEST-SECRET"
region_name = "ap-northeast-2"

# Create a Secrets Manager client
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name=region_name
)

get_secret_value_response = client.get_secret_value(
    SecretId=secret_name
)
secret = json.loads(get_secret_value_response['SecretString'])


# test_rst_cols = ["source_db", "source_table", "cnt_cols", "start_time", "end_time"]
# test_rst_data = []

# table_list = json.loads(args["TABLE_LIST"])
table_list = {
    "database": "JOB_DB30_GG",
    "table_list": [
        {
            "table_name": "Pass_User_Career_DB"
        }
    ]
}

database_name = table_list["database"]

stopwatch = StopWatch()

for table_info in table_list["table_list"]:
    
    # start_time = datetime.now()
    
    
    table_name = table_info["table_name"]
    print("###table_name: " + table_name)
    
    conn_mssql_op = {
        "url": f'jdbc:{secret["engine"]}://{secret["host"]}:{secret["port"]};databaseName={database_name}',
        "dbtable": table_name,
        "user": secret["username"],
        "password": secret["password"],
        "hashexpression": "IDX"
    }
    
    stopwatch.start(f'create_dynamic_frame_from:: {database_name}.{table_name}')
    raw_dyf = glueContext.create_dynamic_frame.from_options(connection_type = 'sqlserver', connection_options = conn_mssql_op)
    stopwatch.stop()
    logger.info("### DynamicFrame으로 로드완료")
    
    # raw_dyf의 스키마 출력
    raw_dyf.printSchema()
    stopwatch.start(f'counting data:: {database_name}.{table_name}')
    data_cnt = raw_dyf.count()
    stopwatch.stop()
    logger.info(f'### Count: {data_cnt}')
    
    # if 'drop_cols' in table_info:
    #     raw_dyf = raw_dyf.drop_fileds(paths=table_info['drop_cols'])
        

# # S3에 데이터 작성 방법 2: sink 사용하여 s3에 데이터 로드 및 glue 카탈로그 생성

    stopwatch.start(f'write data:: {database_name}.{table_name}')
    sink = glueContext.getSink(connection_type="s3", path = f's3://jk-jobia-dev-s3-rawdata-temp/{database_name}/{table_name}/', enableUpdateCatalog=True, updateBehavior="UPDATE_IN_DATABASE")
    sink.setFormat("json")
    sink.setCatalogInfo(catalogDatabase="jk-jobia-dev-raw-database", catalogTableName = table_name)
    sink.writeFrame(raw_dyf)
    stopwatch.stop()
    
    # end_time = datetime.now()
    # test_rst_data.append((database_name,table_name,cnt_cols,start_time,end_time))
    
# test_rst_df = spark.createDataFrame(test_rst_data).toDF(*test_rst_cols)
# print("####Result####")
# test_rst_df.show()

job.commit()