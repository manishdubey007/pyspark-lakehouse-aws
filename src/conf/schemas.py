from pyspark.sql.types import StringType, StructField, StructType

customers_schema = StructType(
    [
        StructField("customer_id", StringType(), True),
        StructField("customer_unique_id", StringType(), True),
        StructField(
            "customer_zip_code_prefix",
            StringType(),
            True,
            metadata={"comment": "Kept as string to preserve leading zeros"},
        ),
        StructField("customer_city", StringType(), True),
        StructField("customer_state", StringType(), True),
    ]
)

products_schema = StructType(
    [
        StructField("product_id", StringType(), True),
        StructField("product_category_name", StringType(), True),
        StructField(
            "product_name_lenght",
            StringType(),
            True,
            metadata={"comment": "Misspelling ('lenght') preserved from source column name"},
        ),
        StructField(
            "product_description_lenght",
            StringType(),
            True,
            metadata={"comment": "Misspelling ('lenght') preserved from source column name"},
        ),
        StructField("product_photos_qty", StringType(), True),
        StructField("product_weight_g", StringType(), True),
        StructField("product_length_cm", StringType(), True),
        StructField("product_height_cm", StringType(), True),
        StructField("product_width_cm", StringType(), True),
    ]
)

sellers_schema = StructType(
    [
        StructField("seller_id", StringType(), True),
        StructField(
            "seller_zip_code_prefix",
            StringType(),
            True,
            metadata={"comment": "Kept as string to preserve leading zeros"},
        ),
        StructField("seller_city", StringType(), True),
        StructField("seller_state", StringType(), True),
    ]
)

geolocation_schema = StructType(
    [
        StructField(
            "geolocation_zip_code_prefix",
            StringType(),
            True,
            metadata={"comment": "Kept as string to preserve leading zeros"},
        ),
        StructField("geolocation_lat", StringType(), True),
        StructField("geolocation_lng", StringType(), True),
        StructField("geolocation_city", StringType(), True),
        StructField("geolocation_state", StringType(), True),
    ]
)

category_translation_schema = StructType(
    [
        StructField("product_category_name", StringType(), True),
        StructField("product_category_name_english", StringType(), True),
    ]
)

order_items_schema = StructType(
    [
        StructField("order_id", StringType(), True),
        StructField("order_item_id", StringType(), True),
        StructField("product_id", StringType(), True),
        StructField("seller_id", StringType(), True),
        StructField("shipping_limit_date", StringType(), True),
        StructField("price", StringType(), True),
        StructField("freight_value", StringType(), True),
    ]
)

order_payments_schema = StructType(
    [
        StructField("order_id", StringType(), True),
        StructField("payment_sequential", StringType(), True),
        StructField("payment_type", StringType(), True),
        StructField("payment_installments", StringType(), True),
        StructField("payment_value", StringType(), True)
    ]
)


order_schema = StructType(
    [
        StructField("order_id", StringType(), True),
        StructField("customer_id", StringType(), True),
        StructField("order_status", StringType(), True),
        StructField("order_purchase_timestamp", StringType(), True),
        StructField("order_approved_at", StringType(), True),
        StructField("order_delivered_carrier_date", StringType(), True),
        StructField("order_delivered_customer_date", StringType(), True),
        StructField("order_estimated_delivery_date", StringType(), True),
    ]
)


order_reviews_schema = StructType(
    [
        StructField("review_id", StringType(), True),
        StructField("order_id", StringType(), True),
        StructField("review_score", StringType(), True),
        StructField("review_comment_title", StringType(), True),
        StructField("review_comment_message", StringType(), True),
        StructField("review_creation_date", StringType(), True),
        StructField("review_answer_timestamp", StringType(), True),
    ]
)

SCHEMAS = {
    "olist_customers_dataset": customers_schema,
    "olist_products_dataset": products_schema,
    "olist_sellers_dataset": sellers_schema,
    "olist_geolocation_dataset": geolocation_schema,
    "product_category_name_translation": category_translation_schema,
    "olist_order_items_dataset": order_items_schema,
    "olist_order_payments_dataset": order_payments_schema,
    "olist_orders_dataset": order_schema,
    "olist_order_reviews_dataset": order_reviews_schema,
}
