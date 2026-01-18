FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy

RUN pip install fastapi uvicorn

WORKDIR /app

COPY server.py .
COPY run.sh .

RUN sed -i 's/\r$//' run.sh && chmod +x run.sh

CMD ["bash", "/app/run.sh"]
