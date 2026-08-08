import logging

from config.logging_config import configure_logging
from config.schemas import SCHEMAS
from config.spark_session import get_spark_session
from pyspark.sql.types import StructType

logger = logging.getLogger(__name__)


def ingest_dimensions(file_name: str, schema: StructType, target_bucket: str) -> None:
    spark = get_spark_session()

    logger.info("Reading %s", file_name)
    try:
        # Multiline values observed in some files which can split one record in to multiple rows. 
        # This check has been enabled to handle multiline entries corrupting the actual record from all csv files.
        dimensions_df = spark.read.schema(schema).option("multiline", "true").option("enforceSchema", "false").csv(
            f"data/raw/{file_name}.csv", header=True
        )
        dimensions_df = dimensions_df.cache()
        row_count = dimensions_df.count()
        logger.info("Read %d rows for %s", row_count, file_name)
        if row_count == 0:
            logger.error("There are no rows in the file %s", file_name)
            raise ValueError(f"There are no rows in the file {file_name}")
    except Exception:
        logger.exception("Failed to read %s", file_name)
        raise

    try:
        dimensions_df.write.mode("overwrite").csv(
            f"s3a://{target_bucket}/{file_name}/",
            header=True
        )
    except Exception:
        logger.exception("Failed to write %s to %s", file_name, target_bucket)
        raise

    logger.info("Wrote %s to %s", file_name, target_bucket)


def main():
    configure_logging()
    for file_name, schema in SCHEMAS.items():
        ingest_dimensions(file_name, schema, "bronze")


if __name__ == "__main__":
    main()