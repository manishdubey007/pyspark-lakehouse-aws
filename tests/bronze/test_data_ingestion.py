from pathlib import Path

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType

from src.bronze.data_ingestion import read_raw_file
from src.conf.schemas import SCHEMAS, customers_schema, order_reviews_schema

CUSTOMERS_HEADER = (
    "customer_id,customer_unique_id,customer_zip_code_prefix,customer_city,customer_state"
)

REVIEW_HEADER = (
    "review_id,order_id,review_score,review_comment_title,"
    "review_comment_message,review_creation_date,review_answer_timestamp"
)
REVIEW_ROW_WITH_EMBEDDED_NEWLINE = (
    '"rev1","ord1",4,,"Mas um pouco ,travando...pelo valor ta Boa.\n"'
    ",2018-02-16 00:00:00,2018-02-20 10:52:22"
)


def test_customer_zip_code_prefix_preserves_leading_zero(spark: SparkSession, tmp_path: Path):
    file_name = "customers"
    csv_path = tmp_path / f"{file_name}.csv"
    csv_path.write_text(f"{CUSTOMERS_HEADER}\nabc123,unique123,01310,sao paulo,SP\n")

    df = read_raw_file(
        spark=spark,
        source_path=str(tmp_path),
        file_name=file_name,
        schema=customers_schema,
    )

    assert df.first()["customer_zip_code_prefix"] == "01310"


def test_review_with_embedded_newline_parses_as_single_record(spark: SparkSession, tmp_path: Path):
    file_name = "order_reviews"
    csv_path = tmp_path / f"{file_name}.csv"
    csv_path.write_text(f"{REVIEW_HEADER}\n{REVIEW_ROW_WITH_EMBEDDED_NEWLINE}\n")

    df = read_raw_file(
        spark=spark,
        source_path=str(tmp_path),
        file_name=file_name,
        schema=order_reviews_schema,
    )

    assert df.count() == 1
    row = df.collect()[0]
    assert row["review_comment_message"].startswith("Mas um pouco")
    assert row["review_answer_timestamp"] == "2018-02-20 10:52:22"


def test_review_with_embedded_newline_corrupts_without_multiline_option(
    spark: SparkSession, tmp_path: Path
):
    csv_path = tmp_path / "order_reviews.csv"
    csv_path.write_text(f"{REVIEW_HEADER}\n{REVIEW_ROW_WITH_EMBEDDED_NEWLINE}\n")

    df = spark.read.schema(order_reviews_schema).csv(str(csv_path), header=True)

    assert df.count() != 1


@pytest.mark.parametrize("file_name, schema", SCHEMAS.items())
def test_empty_file_raises_value_error(
    spark: SparkSession, tmp_path: Path, file_name: str, schema: StructType
):
    header = ",".join(schema.fieldNames())
    (tmp_path / f"{file_name}.csv").write_text(f"{header}\n")

    with pytest.raises(ValueError):
        read_raw_file(spark=spark, source_path=str(tmp_path), file_name=file_name, schema=schema)
