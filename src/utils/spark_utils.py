import logging
import os

from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)


def create_spark_session():
    spark_mode = os.getenv("SPARK_MODE", "local")
    spark_builder = SparkSession.builder.appName("Transform JSON Files")

    if spark_mode == "local":
        logger.info("Running Spark in local mode")
        spark_builder = spark_builder.master("local[*]")
    elif spark_mode == "remote":
        spark_master_url = os.getenv("SPARK_MASTER_URL", "spark://spark-master:7077")
        logger.info(f"Running Spark in remote mode with master URL: {spark_master_url}")
        spark_builder = spark_builder.master(spark_master_url)
    else:
        raise ValueError(f"Unknown SPARK_MODE: {spark_mode}")

    return spark_builder.getOrCreate()