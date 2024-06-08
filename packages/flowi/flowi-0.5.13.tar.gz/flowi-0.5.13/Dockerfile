FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ENV PYTHON_VERSION=3.10
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt update && \
    apt install --no-install-recommends build-essential software-properties-common -y && \
    apt install libgl1 ffmpeg libsm6 libxext6 cuda-compiler-11-8 -y

RUN add-apt-repository -y ppa:deadsnakes/ppa && \
    apt update && \
    apt install --no-install-recommends -y curl python${PYTHON_VERSION} python${PYTHON_VERSION}-dev python${PYTHON_VERSION}-distutils python${PYTHON_VERSION}-venv python3-distutils python3-pip && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10 && \
    apt remove python3-blinker -y && \
    rm usr/bin/python3 && \
    ln -sf /usr/bin/python${PYTHON_VERSION}         /usr/bin/python && \
    ln -sf /usr/bin/python${PYTHON_VERSION}         /usr/local/bin/python && \
    ln -sf /usr/bin/python${PYTHON_VERSION}         /usr/bin/python3 && \
    ln -sf /usr/bin/python${PYTHON_VERSION}         /usr/local/bin/python3 && \
    ln -sf /usr/bin/pip${PYTHON_VERSION}            /usr/bin/pip && \
    ln -sf /usr/bin/pip${PYTHON_VERSION}            /usr/bin/pip3 && \
    apt clean

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade setuptools wheel six

WORKDIR opt

COPY pyproject.toml README.md ./
COPY flowi/ ./flowi/
RUN pip install --no-cache-dir .


RUN mkdir -p /airflow/xcom/
