from src.conf.logging_config import configure_logging
from src.conf.schemas import SCHEMAS
from src.conf.spark_session import get_spark_session
from src.bronze.data_ingestion import loader
from src.conf.config import BRONZE_PATH, RAW_DATA_PATH


def main():
    configure_logging()
    spark = get_spark_session(app_name="olist-ingestion")
    for file_name, schema in SCHEMAS.items():
        loader(
            spark=spark, 
            source_path=RAW_DATA_PATH, 
            file_name=file_name, 
            schema=schema, 
            target_path=BRONZE_PATH
            )


if __name__ == "__main__":
    main()