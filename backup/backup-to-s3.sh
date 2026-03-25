#!/bin/bash
# backup/backup-to-s3.sh — Auto-backup data/ to S3 or MinIO

set -e

echo "📦 Backing up data/ to S3..."

# Configure (uses your existing AWS CLI config)
S3_BUCKET="s3://policyfx-backup"
TODAY=$(date +%Y-%m-%d)

# Sync with encryption & versioning
aws s3 sync \
  --sse AES256 \
  --storage-class STANDARD_IA \
  ../data/ \
  ${S3_BUCKET}/${TODAY}/ \
  --exclude "*.log" \
  --include "data/fx/*" \
  --include "data/policy/*" \
  --include "data/shanghai/*" \
  --include "data/alerts/*" \
  --include "data/analytics/*"

echo "✅ Backup completed: ${S3_BUCKET}/${TODAY}/"