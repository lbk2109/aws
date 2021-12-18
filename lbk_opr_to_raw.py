# -*- coding: utf-8 -*-
# lbk_opr_to_raw.py
#------------------------------------------------------------------------------
#ReRUN을 위한정리
# 초기적재(INI)의 경우
#  1.대상S3 초기화
#  2.대상테이블 초기화
# 증분적재(INC) 변경적재의 경우
#  1.증분 대상만 삭제
#
# Hist_User_DB_Mon_Change
# Pstn_Suggest_Inqry
# SM3_Mem_Profile_Jobtype_Kwrd
# Pass_User_Wish_Work
# #Pass_User_Career_DB
#------------------------------------------------------------------------------
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
from stopwatch import StopWatch

#
import time
from pytz import timezone
def time_Stamp(stime,msg):
  elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time()-stime))
  print('\n현재[%s]소요시간[%s] MSG[%s]\n'% (datetime.now(timezone('Asia/Seoul')).strftime("%Y/%m/%d %H:%M:%S"),elapsed,msg))
#  

# Glue Job 수행에 필요한 기본 변수 선언
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
logger= glueContext.get_logger()
job   = Job(glueContext)
args  = getResolvedOptions(sys.argv,['JOB_NAME','job_gbn','job_base_dt','database_name','table_name','target_db'])
job.init(args['JOB_NAME'],args)
stopwatch = StopWatch()
#
job_name      = args["JOB_NAME"]
job_gbn       = args["job_gbn"]
job_base_dt   = args["job_base_dt"]
database_name = args["database_name"]
table_name    = args["table_name"]
target_db     = args["target_db"]
print(f'job_name     :[{job_name}]')
print(f'job_gbn      :[{job_gbn}]')
print(f'job_base_dt  :[{job_base_dt}]')
print(f'database_name:[{database_name}]')
print(f'table_name   :[{table_name}]')
print(f'target_db    :[{target_db}]')

print(f'====작업시작====')
#------------------------------------------------------------------------------
stopwatch.start(f'1.DB 접속정보 설정')
#
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

conn_mssql_op = {
    "url": f'jdbc:{secret["engine"]}://{secret["host"]}:{secret["port"]};databaseName={database_name}',
    "dbtable": table_name,
    "user": secret["username"],
    "password": secret["password"],
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# conn_mssql_op = {
#     "url": f'jdbc:{secret["engine"]}://{secret["host"]}:{secret["port"]};databaseName={database_name}',
#     "dbtable": table_name,
#     "user": secret["username"],
#     "password": secret["password"],
#     "hashexpression": "Work_Wish_Idx"
# }

stopwatch.stop()
#------------------------------------------------------------------------------
stopwatch.start(f'2.DB에 접속하여 DynamicFrame으로 데이터 읽어오기')
raw_dyf = glueContext.create_dynamic_frame.from_options(connection_type = 'sqlserver', connection_options = conn_mssql_op)
# raw_dyf = raw_dyf.coalesce(1)
raw_dyf.printSchema()
# raw_dyf.toDF().show()
# logger.info(f'### numPartitions : {raw_dyf.rdd.getNumPartititons()}')
stopwatch.stop()
#------------------------------------------------------------------------------
# stopwatch.start(f'3.DB에서 가져온 원천 데이터건수 얻기.')
# raw_cnt=raw_dyf.toDF().count()
# print(f'raw_cnt:{raw_cnt}')
# stopwatch.stop()
#------------------------------------------------------------------------------
stopwatch.start(f'4.DynamicFrame을 S3에 저장(Glue Catalog가 없으면 생성후)')
if spark.catalog._jcatalog.tableExists(f'{target_db}.{table_name}'):
    print(f'4.1 {target_db}.{table_name}:Exists!')
    # S3에 데이터 작성 방법 1: write_dynamic_frame 사용
    glueContext.write_dynamic_frame.from_options(frame = raw_dyf,connection_type = "s3",connection_options = {"path": "s3://jk-jobia-dev-s3-rawdata-temp/lbk_test/" + table_name},format = "json")
else:
    print(f'4.2 {target_db}.{table_name}:Not exists!')
    # S3에 데이터 작성 방법 2: sink 사용하여 s3에 데이터 로드 및 glue 카탈로그 생성
    sink = glueContext.getSink(connection_type="s3", path = "s3://jk-jobia-dev-s3-rawdata-temp/lbk_test/" + table_name, enableUpdateCatalog=True, updateBehavior="UPDATE_IN_DATABASE")
    sink.setFormat("json")
    sink.setCatalogInfo(catalogDatabase=target_db, catalogTableName = table_name)
    sink.writeFrame(raw_dyf)
stopwatch.stop()
#------------------------------------------------------------------------------
#
# 파티션 테이블 재정리 작업
# spark.sql(f'MSCK REPAIR TABLE {target_db}.{table_name}');                   
#------------------------------------------------------------------------------
job.commit()
print(f'====작업종료====')
#------------------------------------------------------------------------------
#


git test