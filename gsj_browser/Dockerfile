FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy

RUN apt-get update && apt-get install -y curl

COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
