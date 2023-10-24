ARG PYTHON_VERSION

FROM python:$PYTHON_VERSION-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y

RUN apt-get install -y \
        gcc \
        libpq-dev

WORKDIR /app

COPY ./pyproject.toml ./pyproject.toml

COPY ./rotini ./rotini

RUN python3 -m pip install -U pip
RUN python3 -m pip install -e .

WORKDIR ./rotini

CMD python3 -m uvicorn main:app --host 0.0.0.0
