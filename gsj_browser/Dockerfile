FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy

RUN pip install fastapi uvicorn

WORKDIR /app

COPY server.py /app/server.py
COPY run.sh /app/run.sh

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
