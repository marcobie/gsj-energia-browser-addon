#!/usr/bin/with-contenv bash
echo "Starting GSJ Browser API..."
uvicorn server:app --host 0.0.0.0 --port 8124
