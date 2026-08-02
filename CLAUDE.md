# Project context for Claude Code

## What this is

Project 1 of a Data Engineering portfolio (13 projects + bonus, tracked in a separate
Claude Project / Jira / Confluence). This repo: PySpark pipeline reading the Olist
Brazilian E-Commerce dataset (Kaggle), applying non-trivial transformations, writing
to S3 in three table formats (Parquet, Delta Lake, Iceberg) for comparison, queried
via Glue Data Catalog + Athena.

Two goals held at once: rebuilding daily hands-on coding fluency, and building a
portfolio for a Senior Data Engineer job search. Daily transformation-writing reps
are the priority to protect if a session's time is tight — not breadth/tooling.

## Stack / constraints

- PySpark, local via Docker — **no EMR/EKS**
- **MinIO** for local S3-compatible dev (`s3a://` from day one) — same code path
  carries to real AWS S3 later with only endpoint/credential config changing
- Delta Lake built first (lowest setup overhead), then Parquet, then Iceberg
- Iceberg: Hadoop catalog locally (file-based metadata, no external catalog service)
- Real AWS S3 + Glue Data Catalog + Athena only for the final query-layer stage
  (batched into one Pluralsight sandbox session — flag when we're close to that point)

## Build stages (this project)

Tracked in Jira epic `SCRUM-1`:
1. Docker Compose (MinIO + PySpark) + raw ingestion of Olist CSVs to bronze bucket
2. Cleaning + dedup transformation
3. Enrichment joins + window functions
4. SCD Type 2 on customer dimension
5. Write to Delta Lake + README v1
6. Athena/Glue registration + Parquet/Iceberg comparison

Work one stage at a time. Review output at each stage before moving to the next.
Stages should be small enough to finish in one sitting where possible.

## Code style bar

- Idiomatic Spark method-chaining (`.filter().withColumn().groupBy()`) — avoid manual
  loops and mutable accumulators.
- NOT the same thing: maximal line-count compression (nested lambdas, `reduce` over
  conditions). That's clever, not senior — it trades away debuggability. When a chain
  gets long or a step is worth inspecting on its own, break it into a named
  intermediate DataFrame.
- Naming (variables, functions, classes) should communicate intent.
- No dead code, no copy-paste cruft.

## Testing bar

Tests required for **functional correctness** (right output for representative +
edge-case input) before a stage is considered done — not blanket line/branch
coverage. Not required every single session; can defer to when a piece of logic
settles, but required before marking a stage complete.

## ELT pattern (required)

Land raw data first (bronze/raw zone), transform after landing — not ETL-before-
landing. Call this out explicitly in the README.

## Working style

- **I write the code first, you review after — don't write the implementation for
  me by default.** This repo exists partly to rebuild hands-on coding fluency, not
  just to produce a finished pipeline. For each stage: agree the short plan, then I
  write a first pass, then I share it and you review — critique directly, point out
  what's wrong or non-idiomatic, suggest the better approach, but don't just hand me
  corrected code to paste in. Let me revise based on your feedback and re-share.
- Exception: boilerplate with no learning value (e.g. a standard Dockerfile/
  docker-compose skeleton, dependency pinning) — fine for you to draft directly
  rather than making me hand-write it. Use judgment on what's "learning" code
  (transformation logic, Spark API usage) vs. pure scaffolding.
- If I explicitly ask you to just write something (I'm stuck, time is short, or it's
  scaffolding), that's fine — this default is about the normal case, not a hard rule.
- Critique code directly — no false encouragement.
- Propose a short plan before writing code for a new stage (architecture-level, not
  a design doc) — sanity check, not a blocker.
- Flag it directly if a stage is trending toward needing more than a few sessions —
  propose a smaller cut rather than letting scope grow quietly.
- No class-vs-plain-functions rule yet for any future utils module — that's an open
  discussion to have against the real first case, not a decision to make abstractly.

## Out of scope for this repo

- Framework code (Python framework #7) — only gets extracted here once a pattern
  (read/write/dedup) has genuinely repeated a third time. Don't design it upfront.
- EMR, EKS, cluster/infra management generally.
