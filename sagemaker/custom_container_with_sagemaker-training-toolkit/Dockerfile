FROM python:3.9.13-bullseye

RUN pip install -U pip && \
    pip install sagemaker-training sklearn pandas

COPY train.py /opt/ml/code/train.py

ENV SAGEMAKER_PROGRAM train.py
