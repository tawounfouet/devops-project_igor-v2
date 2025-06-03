#!/bin/bash
set -e

echo "Running temporary Docker container to update poetry.lock file..."

docker run --rm -v $(pwd):/app -w /app python:3.11-slim bash -c "\
    apt-get update && \
    apt-get install -y build-essential gcc libpq-dev && \
    pip install poetry==2.1.3 && \
    poetry lock"

echo "Poetry lock file has been updated."
