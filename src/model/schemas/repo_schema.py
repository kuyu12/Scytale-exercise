from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType, ArrayType

from model.schemas.pull_schema import pull_schema

repo_schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("full_name", StringType(), True),
        StructField("owner", StringType(), True),
        StructField("created_at", TimestampType(), True),
        StructField("pulls", ArrayType(pull_schema), True)
    ])