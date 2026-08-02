# PySpark Lakehouse (AWS)

End-to-end PySpark pipeline that ingests the Olist Brazilian E-Commerce dataset, applies non-trivial transformation logic (dedup, enrichment joins, window functions, SCD Type 2), and writes the result to S3 in three table formats — Parquet, Delta Lake, and Iceberg — for a side-by-side comparison of schema evolution, time travel, and partition pruning behavior.

Part of a larger [Data Engineering portfolio](#) — Project 1 of 13 (+ bonus).

## What this demonstrates

- Idiomatic Spark method-chaining transformations (not just "read CSV, write Parquet")
- ELT pattern: raw data lands first (bronze), transforms happen after landing
- SCD Type 2 dimensional modeling (customer dimension)
- Local-first development against S3-compatible storage (MinIO), migrating cleanly to real AWS S3
- Table format mechanics: Parquet vs Delta Lake vs Iceberg — schema evolution, time travel, partition pruning
- Querying via AWS Glue Data Catalog + Athena

## Architecture

```
Olist CSVs (Kaggle)
      │
      ▼
Raw / bronze landing (MinIO, local S3-compatible)  ──▶  real AWS S3 (final stage)
      │
      ▼
PySpark transformations
  - cleaning / dedup
  - enrichment joins (orders ⋈ customers ⋈ products ⋈ sellers)
  - window functions (customer order recency/sequence)
  - SCD Type 2 (customer dimension)
      │
      ▼
Written to S3 in three formats: Parquet | Delta Lake | Iceberg
      │
      ▼
Glue Data Catalog + Athena (query layer)
```

*(diagram will be refined once the pipeline is actually built)*

## Dataset

[Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle) — orders, order_items, customers, products, sellers, reviews.

## Stack

- PySpark, run locally via Docker (no EMR/EKS)
- MinIO for local S3-compatible development
- Delta Lake, Apache Iceberg (Hadoop catalog, local)
- AWS S3, Glue Data Catalog, Athena (final query layer)

## Setup

> To be filled in as the pipeline is built.

```bash
# clone
git clone https://github.com/<you>/pyspark-lakehouse-aws.git
cd pyspark-lakehouse-aws

# start local stack (MinIO + Spark)
docker compose up -d

# run the pipeline
# (commands TBD once stage 1 is built)
```

## Key design decisions

- **MinIO from day one**: development targets `s3a://` from the start (backed by MinIO locally) rather than plain local filesystem, so the same code path carries over to real S3 unchanged — only the endpoint/credentials config changes.
- **Delta Lake built first**: lowest setup overhead of the three formats: get one format working end-to-end and documented before adding Parquet and Iceberg.
- **Iceberg catalog**: Hadoop catalog (file-based metadata) for local dev — no external catalog service needed, and migrates cleanly to Glue Data Catalog once pointed at real S3.

## Project status

Not yet started. Build stages tracked in Jira under epic `SCRUM-1`:

- [ ] Docker Compose setup (MinIO + PySpark) + raw ingestion
- [ ] Cleaning + dedup transformation
- [ ] Enrichment joins + window functions
- [ ] SCD Type 2 on customer dimension
- [ ] Write to Delta Lake + README v1
- [ ] Athena/Glue registration + Parquet/Iceberg comparison

## Design write-up

Fuller architecture notes and decisions live in Confluence: *Project 1 — PySpark Lakehouse (AWS)*.
