from src.bronze.data_ingestion import land_raw_file_in_bronze
from src.conf.config import BRONZE_PATH, RAW_DATA_PATH
from src.conf.logging_config import configure_logging
from src.conf.schemas import SCHEMAS
from src.conf.spark_session import get_spark_session


def main():
    configure_logging()
    spark = get_spark_session(app_name="olist-ingestion")
    for file_name, schema in SCHEMAS.items():
        land_raw_file_in_bronze(
            spark=spark,
            source_path=RAW_DATA_PATH,
            file_name=file_name,
            schema=schema,
            target_path=BRONZE_PATH,
        )


if __name__ == "__main__":
    main()
