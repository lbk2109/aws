S3_JSON = "s3://jk-jobia-dev-s3-rawdata-temp/kjs_test/table/etlprop.json"
df = spark.read.option("multiline","true").json(S3_JSON) # from JSON files
print(df)
df.show()


database=df.select("database").show()
print(f'database:{database}')
table_name=df.select("table_list.table_name").show()
print(f'table_name:{table_name}')



pandasDF = df.toPandas()

for index, row in pandasDF.iterrows():
    message_body = generate_message(
        row['bucket'], row['key'], row['version_id'])
    send_message(sqs_queue, json.loads(json.dumps(message_body)))
