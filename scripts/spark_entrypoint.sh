#!/bin/sh
set -eu

# py4j's exact filename is version-suffixed and tied to whatever the
# apache/spark-py image happens to bundle -- resolve it at startup instead
# of hardcoding the version in docker-compose.yml, so bumping the image tag
# doesn't silently break the Python path.
#
# This has to be written as a .pth file in site-packages rather than an
# exported PYTHONPATH: `docker compose exec` starts a fresh process that
# does NOT inherit variables `export`ed by this script -- only the entrypoint
# process's own children would see them. A .pth file is read by every
# python3 invocation at interpreter startup, regardless of how it was
# launched, so it isn't subject to that inheritance gap.
py4j_zip=$(ls /opt/spark/python/lib/py4j-*-src.zip 2>/dev/null | head -n 1)
if [ -z "$py4j_zip" ]; then
    echo "spark_entrypoint.sh: no py4j-*-src.zip found under /opt/spark/python/lib" >&2
    exit 1
fi

site_dir=$(python3 -c "import site; print(site.getsitepackages()[0])")
printf '/opt/app\n/opt/spark/python\n%s\n' "$py4j_zip" > "${site_dir}/spark_paths.pth"

exec "$@"
