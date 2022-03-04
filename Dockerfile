FROM python:3.9-slim

ENV PYTHONPATH=/app/ \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_NO_CACHE_DIR=off

RUN apt-get update -y && \
  apt-get install -y --no-install-recommends \
  postgresql-client

WORKDIR /app
COPY ./requirements/base.txt /app/

RUN pip install -r base.txt --quiet
COPY . /code/

EXPOSE 8000

CMD [ "scripts/start-dev.sh" ]