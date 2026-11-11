FROM apache/spark-py:v3.4.0

USER root

# JupyterLab for exploration notebooks (notebooks/). Runs inside this container
# because only the Docker network can reach MinIO at the `minio` hostname.
# httpx<0.28: jupyterlab 4.2.5 passes the `proxies` argument that httpx 0.28 removed.
RUN pip install --no-cache-dir jupyterlab==4.2.5 "httpx<0.28"
