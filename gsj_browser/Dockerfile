FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy

RUN pip install fastapi uvicorn

COPY server.py /app/server.py
COPY run.sh /run.sh

WORKDIR /app
RUN chmod +x /run.sh

CMD ["/run.sh"]
