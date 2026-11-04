# Running the project

All commands run from the project root (`pyspark-lakehouse-aws/`).

## Where things run

| What | Where | Why |
|---|---|---|
| Pipeline (`src/app.py`) | Docker (`spark` container) | Needs MinIO credentials and the `minio` hostname, which only exist on the Docker network |
| Tests (`pytest`) | Mac, local `.venv` | Tests use a plain local Spark session and `tmp_path` — no MinIO needed |

## One-time setup

### 1. MinIO credentials

Create `.env` in the project root (gitignored):

```bash
MINIO_ROOT_USER=<user>
MINIO_ROOT_PASSWORD=<password>
```

### 2. Download the Olist dataset

Needs the Kaggle CLI and a token at `~/.kaggle/kaggle.json`.

```bash
./scripts/download_data.sh      # writes CSVs to data/raw/
```

### 3. Local Python environment (for tests)

```bash
python3.12 -m venv .venv        # python3.11 is a closer match for PySpark 3.4
source .venv/bin/activate
which python                    # must point into this project's .venv
pip install -r requirements.txt
```

A venv stores its absolute path, so it can't be moved or renamed. If the project
folder moves, delete `.venv` and recreate it.

### 4. Java 17 (for local tests)

Spark 3.4 supports Java 8/11/17 only — Java 21 fails at startup. Add to `~/.zshrc`:

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
export PATH="$JAVA_HOME/bin:$PATH"
```

## Run the pipeline

```bash
docker compose up -d                             # start MinIO + Spark
docker compose exec spark python3 -m src.app     # run the pipeline
```

- MinIO console: http://localhost:9001 (log in with the `.env` credentials)
- Output lands in the `bronze` bucket

Stop the stack:

```bash
docker compose down             # keeps MinIO data
docker compose down -v          # also deletes MinIO data and the Ivy jar cache
```

## Run the tests

```bash
source .venv/bin/activate
python -m pytest
```

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'src'` / `'config'` | Ran `python src/app.py` — Python only searches the script's own folder | Run as a module from the project root: `python -m src.app` |
| `ModuleNotFoundError: No module named 'pyspark'` | `python` isn't the venv's Python (`which python` shows Homebrew) | Re-activate the venv; if it's still wrong, the project folder moved — recreate `.venv` |
| `KeyError: 'MINIO_ROOT_USER'` | Pipeline run on the Mac instead of in Docker | Use `docker compose exec spark python3 -m src.app` |
| `NoSuchMethodException: java.nio.DirectByteBuffer.<init>(long,int)` | Java 21 | Set `JAVA_HOME` to Java 17 (see setup step 4) |
| `ClassNotFoundException: org.apache.hadoop.fs.s3a.S3AFileSystem` | `hadoop-aws` jar not loaded | Check `spark.jars.packages` in `src/conf/spark_session.py`; keep `hadoop-aws` at 3.3.4 to match Spark's Hadoop |
| Traceback shows an old file path with `???` | Stale `__pycache__` from before a folder move | `find . -name "__pycache__" -not -path "./.venv/*" -exec rm -rf {} +` |
