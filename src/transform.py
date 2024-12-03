import logging
import os

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, when, max, lower, split, coalesce, explode_outer, lit
from model.schemas.repo_schema import repo_schema
from utils.spark_utils import create_spark_session
from utils.const import ORGANIZATION_VAR_NAME, TRANSFORM_INPUT_FILE_PATH

logger = logging.getLogger(__name__)


def transform(organization: str) -> DataFrame:
    """
        Transforms pull request data for a specified GitHub organization using Apache Spark.

        This function initializes a Spark session and reads JSON files containing repository data
        for the specified organization. It processes the data to calculate the number of pull requests
        and the number of merged pull requests for each repository. Additionally, it checks for compliance
        based on specific criteria and returns a DataFrame with the results.

        :param organization: The name of the GitHub organization for which to transform pull request data.
        :type organization: str

        :return: A Spark DataFrame containing the transformed data with the following columns:
            - Organization_Name: The name of the organization.
            - repository_id: The unique identifier of the repository.
            - repository_name: The name of the repository.
            - repository_owner: The owner of the repository.
            - num_prs: The total number of pull requests.
            - num_prs_merged: The number of merged pull requests.
            - merged_at: The timestamp of the last merged pull request.
            - is_compliant: A boolean indicating compliance based on the number of merged pull requests and the owner's name.

        :rtype: pyspark.sql.DataFrame
    """
    logger.info("Initialize Spark session")
    spark = create_spark_session()

    # Read multiple JSON files into a DataFrame
    # Replace 'path/to/json/files' with the actual path to your JSON files
    logger.info("Read Json files")
    df = spark.read.schema(repo_schema).json(f"{TRANSFORM_INPUT_FILE_PATH}/{organization}/*.json")

    # Explode the 'pulls' array to process each pull request individually, using explode_outer to include rows with
    # empty arrays
    exploded_df = df.withColumn("pull", explode_outer("pulls"))

    # Calculate the number of PRs and merged PRs
    num_prs_df = exploded_df.groupBy("id", "name", "full_name", "owner").agg(
        count("pull").alias("num_prs"),
        count(when(col("pull.merged") == True, 1)).alias("num_prs_merged"),
        max("pull.last_modified").alias("merged_at")
    )

    # Add compliance check
    result_df = num_prs_df.withColumn(
        "is_compliant",
        (col("num_prs") == col("num_prs_merged")) & (lower(col("owner")).contains("scytale"))
    ).select(
        split(col("full_name"), '/')[0].alias("Organization_Name"),
        col("id").alias("repository_id"),
        col("name").alias("repository_name"),
        col("owner").alias("repository_owner"),
        coalesce(col("num_prs"), lit(0)).alias("num_prs"),
        coalesce(col("num_prs_merged"), lit(0)).alias("num_prs_merged"),
        col("merged_at"),
        col("is_compliant")
    )

    return result_df


if __name__ == "__main__":
    # Local Testing
    organization = os.environ[ORGANIZATION_VAR_NAME]
    result_df = transform(organization)
