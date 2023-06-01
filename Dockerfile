FROM python:3 AS kupo-backend

RUN pip install cbor2 uplc

COPY ./dns-kupo.py /app.py

ENTRYPOINT /app.py
