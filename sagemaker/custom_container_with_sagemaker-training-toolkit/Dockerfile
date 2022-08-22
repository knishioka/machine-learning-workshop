FROM python:3.10.6-bullseye

RUN pip install -U pip && \
    pip install sagemaker-training

COPY train.py /opt/ml/code/train.py

ENV SAGEMAKER_PROGRAM train.py