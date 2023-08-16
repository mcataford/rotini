ARG PYTHON_VERSION

FROM python:$PYTHON_VERSION-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y

RUN apt-get install -y \
        gcc \
        libpq-dev

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN python3 -m pip install -U pip==23.0.0 pip-tools==7.1.0
RUN python3 -m pip install -r ./requirements.txt

COPY ./rotini ./rotini

WORKDIR ./rotini

CMD python3 -m uvicorn main:app --host 0.0.0.0
