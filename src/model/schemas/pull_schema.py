from pyspark.sql.types import StructType, StructField, StringType, BooleanType, TimestampType

pull_schema = StructType([
        StructField("title", StringType(), True),
        StructField("state", StringType(), True),
        StructField("url", StringType(), True),
        StructField("merged", BooleanType(), True),
        StructField("create_at", TimestampType(), True),
        StructField("last_modified", TimestampType(), True)
    ])