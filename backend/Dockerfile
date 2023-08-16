FROM ubuntu:jammy

ARG PYTHON_VERSION

ENV DEBIAN_FRONTEND=noninteractive
ENV TARGET_PYTHON_VERSION=$PYTHON_VERSION

RUN apt update && apt upgrade -y

RUN apt-get install -y \
        build-essential \
        checkinstall \
        libreadline-dev \
        libncursesw5-dev \
        libssl-dev \
        libsqlite3-dev \
        tk-dev \
        libgdbm-dev \
        libc6-dev \
        libbz2-dev \
        libpq-dev \
        wget

WORKDIR /app

COPY .python-version ./

WORKDIR /tmp

RUN wget https://www.python.org/ftp/python/$TARGET_PYTHON_VERSION/Python-$TARGET_PYTHON_VERSION.tgz
RUN tar xzf ./Python-$TARGET_PYTHON_VERSION.tgz

WORKDIR /tmp/Python-$TARGET_PYTHON_VERSION

RUN ./configure && make install

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN python3 -m pip install -U pip==23.0.0 pip-tools==7.1.0
RUN python3 -m pip install -r ./requirements.txt

COPY ./rotini ./rotini

WORKDIR ./rotini

CMD python3 -m uvicorn main:app --host 0.0.0.0
