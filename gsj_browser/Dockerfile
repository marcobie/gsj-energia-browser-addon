FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy

# Doinstaluj biblioteki Pythona
RUN pip install fastapi uvicorn playwright

WORKDIR /app

COPY server.py .
COPY run.sh .

# Usunięcie CRLF i nadanie praw
RUN sed -i 's/\r$//' run.sh && chmod +x run.sh

CMD ["bash", "/app/run.sh"]
