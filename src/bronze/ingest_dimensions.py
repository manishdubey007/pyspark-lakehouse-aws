import logging

from config.logging_config import configure_logging
from config.schemas import SCHEMAS
from config.spark_session import get_spark_session
from pyspark.sql.types import StructType

logger = logging.getLogger(__name__)


def ingest_dimensions(file_name: str, schema: StructType) -> None:
    spark = get_spark_session()

    logger.info("Reading %s", file_name)
    try:
        dimensions_df = spark.read.schema(schema).option("multiline", "true").csv(
            f"data/raw/{file_name}.csv", header=True
        )
        row_count = dimensions_df.count()
        logger.info("Read %d rows for %s", row_count, file_name)
    except Exception:
        logger.exception("Failed to read %s", file_name)
        raise

    try:
        dimensions_df.write.mode("overwrite").csv(
            f"s3a://bronze/{file_name}/",
            header=True
        )
    except Exception:
        logger.exception("Failed to write %s to bronze", file_name)
        raise

    logger.info("Wrote %s to bronze", file_name)


def main():
    configure_logging()
    for file_name, schema in SCHEMAS.items():
        ingest_dimensions(file_name, schema)


if __name__ == "__main__":
    main()