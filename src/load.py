import os
from enum import Enum
from typing import Union

from pyspark.sql import DataFrame

from utils.const import TRANSFORM_OUTPUT_FILE_PATH


class FileFormat(Enum):
    parquet = "parquet"
    json = "json"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


def load(organization: str, dataframe: DataFrame, mode="overwrite",
         fileFormat: Union[FileFormat, str] = FileFormat.parquet) -> None:
    """
    Saves a Spark DataFrame to a specified directory in Parquet format.

    This function writes the provided Spark DataFrame to a directory specific to the given
    organization. The data is saved in Parquet format, and any existing data in the target
    directory is overwritten.

    :param fileFormat: file output format
    :param mode: Spark write mode - append,overwrite,error,ignore
    :param organization: The name of the GitHub organization for which to save the data.

    :param dataframe: The Spark DataFrame to be saved.
    :type dataframe: pyspark.sql.DataFrame

    :return: None

    :raises OSError: If there is an issue creating the output directory.
    """
    fileFormatValue = fileFormat if type(fileFormat) == str else fileFormat.value
    if not FileFormat.has_value(fileFormatValue):
        raise KeyError("format need to be FileFormat value")

    output_folder = f'{TRANSFORM_OUTPUT_FILE_PATH}/{organization}'
    os.makedirs(output_folder, exist_ok=True)

    if fileFormatValue == FileFormat.parquet.value:
        dataframe.write.mode(mode).parquet(output_folder)
    if fileFormatValue == FileFormat.json.value:
        dataframe.write.mode(mode).json(output_folder)
