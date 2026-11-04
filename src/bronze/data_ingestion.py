import logging

from pyspark.sql import DataFrame
from pyspark.sql.types import StructType

logger = logging.getLogger(__name__)


def loader(spark, source_path: str, file_name: str, schema: StructType, target_path: str) -> None:
    logger.info("Reading %s", file_name)
    df = read_data(spark, source_path, file_name, schema)
    write_data(df, target_path, file_name)
    df.unpersist()


def read_data(spark, source_path: str, file_name: str, schema: StructType) -> DataFrame:
    try:
        # Multiline values observed in some files which can split one record in to multiple rows.
        # This check has been enabled to handle multiline entries corrupting the actual record from all csv files.
        df = spark.read.schema(schema).option("multiline", "true").option("enforceSchema", "false").csv(
            f"{source_path}/{file_name}.csv", header=True
        )
        df = df.cache()
        row_count = df.count()
        logger.info("Read %d rows for %s", row_count, file_name)
        if row_count == 0:
            logger.error("There are no rows in the file %s", file_name)
            raise ValueError(f"There are no rows in the file {file_name}")
    except Exception:
        logger.exception("Failed to read %s", file_name)
        raise
    return df

def write_data(df: DataFrame, target_path: str, file_name: str) -> None:
    try:
        df.write.mode("overwrite").csv(
            f"{target_path}/{file_name}/",
            header=True
        )
    except Exception:
        logger.exception("Failed to write %s to %s", file_name, target_path)
        raise

    logger.info("Wrote %s to %s", file_name, target_path)