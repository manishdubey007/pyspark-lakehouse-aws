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
Olist CSVs (Kaggle) ── kept untouched in data/raw/
      │
      ▼
Bronze landing: Parquet, all columns StringType, no transformation
  (MinIO, local S3-compatible  ──▶  real AWS S3 in the final stage)
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

Full setup (MinIO credentials, dataset download, local venv, Java 17), run commands and troubleshooting are in [`run.md`](run.md). Quick start once set up:

```bash
docker compose up -d                             # start MinIO + Spark
docker compose exec spark python3 -m src.app     # land raw CSVs in the bronze bucket
pytest                                           # tests run locally, no MinIO needed
```

## ELT, not ETL

Raw data lands first and is transformed only after landing:

- **Raw**: the original Olist CSVs stay untouched in `data/raw/`, reproducible with `scripts/download_data.sh`.
- **Bronze**: the same data, untransformed. Every column is landed as `StringType` (no casting, cleaning or dedup), so nothing is lost or reinterpreted at ingestion. Ingestion only fails fast on unreadable input: a header that doesn't match the declared schema, or a file with zero rows.
- **Silver / gold**: casting, cleaning, dedup, joins and SCD2 all happen here, reading from bronze.

## Key design decisions

- **Bronze is Parquet, not CSV**: format conversion isn't a content transformation, so ELT still holds. Parquet stores its own schema and has no record delimiters, so CSV parsing quirks (quoted fields with embedded newlines that need `multiline`, header handling) are dealt with once at the ingestion boundary instead of by every downstream reader. A Spark-written CSV wouldn't have been a byte-for-byte copy of the source anyway; the originals stay in `data/raw/`.
- **MinIO from day one**: development targets `s3a://` from the start (backed by MinIO locally) rather than plain local filesystem, so the same code path carries over to real S3 unchanged — only the endpoint/credentials config changes.
- **Delta Lake built first**: lowest setup overhead of the three formats: get one format working end-to-end and documented before adding Parquet and Iceberg.
- **Iceberg catalog**: Hadoop catalog (file-based metadata) for local dev — no external catalog service needed, and migrates cleanly to Glue Data Catalog once pointed at real S3.

## Project status

Stage 1 done; stage 2 in progress. Build stages tracked in Jira under epic `SCRUM-1`:

- [x] Docker Compose setup (MinIO + PySpark) + raw ingestion
- [ ] Cleaning + dedup transformation
- [ ] Enrichment joins + window functions
- [ ] SCD Type 2 on customer dimension
- [ ] Write to Delta Lake + README v1
- [ ] Athena/Glue registration + Parquet/Iceberg comparison

## Design write-up

Fuller architecture notes and decisions live in Confluence: *Project 1 — PySpark Lakehouse (AWS)*.

[`docs/`](docs/) holds my learning notes from building this (Spark caching, logging, testing, error handling), not project documentation.
