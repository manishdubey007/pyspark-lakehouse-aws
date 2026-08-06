#!/usr/bin/env bash
set -euo pipefail

# Downloads the Olist Brazilian E-Commerce dataset from Kaggle into data/raw.
# Prerequisites:
#   pip install kaggle
#   Kaggle API token at ~/.kaggle/kaggle.json
#   (Kaggle account -> Settings -> API -> "Create New Token")

DATASET="olistbr/brazilian-ecommerce"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAW_DIR="${SCRIPT_DIR}/../data/raw"

if ! command -v kaggle >/dev/null 2>&1; then
  echo "kaggle CLI not found. Install it with: pip install kaggle" >&2
  exit 1
fi

if [ ! -f "${HOME}/.kaggle/kaggle.json" ]; then
  echo "Kaggle API token not found at ~/.kaggle/kaggle.json" >&2
  echo "Get one from https://www.kaggle.com/settings -> API -> Create New Token" >&2
  exit 1
fi

mkdir -p "${RAW_DIR}"

echo "Downloading ${DATASET} into ${RAW_DIR}..."
kaggle datasets download --dataset "${DATASET}" --path "${RAW_DIR}" --unzip

echo "Done. Contents of ${RAW_DIR}:"
ls -la "${RAW_DIR}"
