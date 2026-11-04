import logging

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType

logger = logging.getLogger(__name__)


def land_raw_file_in_bronze(
    spark: SparkSession, source_path: str, file_name: str, schema: StructType, target_path: str
) -> None:
    logger.info("Reading %s", file_name)
    df = read_raw_file(spark, source_path, file_name, schema)
    write_raw_file(df, target_path, file_name)
    df.unpersist()


def read_raw_file(
    spark: SparkSession, source_path: str, file_name: str, schema: StructType
) -> DataFrame:
    try:
        # some fields contain embedded newlines, so a quoted value can span several lines.
        df = (
            spark.read.schema(schema)
            .option("multiline", "true")
            .option("enforceSchema", "false")
            .csv(f"{source_path}/{file_name}.csv", header=True)
        )
        df = df.cache()
        row_count = df.count()
        logger.info("Read %d rows for %s", row_count, file_name)
    except Exception:
        logger.exception("Failed to read %s", file_name)
        raise

    if row_count == 0:
        logger.error("There are no rows in the file %s", file_name)
        raise ValueError(f"There are no rows in the file {file_name}")

    return df


def write_raw_file(df: DataFrame, target_path: str, file_name: str) -> None:
    try:
        df.write.mode("overwrite").csv(f"{target_path}/{file_name}/", header=True)
    except Exception:
        logger.exception("Failed to write %s to %s", file_name, target_path)
        raise

    logger.info("Wrote %s to %s", file_name, target_path)
