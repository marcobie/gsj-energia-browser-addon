#!/usr/bin/env bash
echo "Starting GSJ Browser API..."
cd /app
uvicorn server:app --host 0.0.0.0 --port 8124
