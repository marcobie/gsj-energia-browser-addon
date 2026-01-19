#!/usr/bin/env bash

export GSJ_USERNAME="${USERNAME}"
export GSJ_PASSWORD="${PASSWORD}"

echo "Starting GSJ Browser API with user: $GSJ_USERNAME"

cd /app
uvicorn server:app --host 0.0.0.0 --port 8124
