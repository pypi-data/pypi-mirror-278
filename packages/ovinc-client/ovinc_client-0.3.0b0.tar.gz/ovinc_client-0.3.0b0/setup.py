#!/usr/bin/env python

from setuptools import setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ovinc_client",
    version="0.3.0b0",
    author="OVINC",
    url="https://www.ovinc.cn/",
    author_email="contact@ovinc.cn",
    description="A Tool for OVINC Union API",
    packages=[
        "ovinc_client",
        "ovinc_client.account",
        "ovinc_client.account.migrations",
        "ovinc_client.components",
        "ovinc_client.core",
        "ovinc_client.trace",
    ],
    install_requires=[
        "django>=4,<5",
        "django_environ>=0.10.0,<1",
        "djangorestframework>=3.14.0,<4",
        "mysqlclient>=2.1.1,<3",
        "django-cors-headers>=3.11.0,<4",
        "pytz>=2022.4,<2025",
        "django-sslserver>=0.22,<1",
        "pyOpenSSL>=22.1.0,<25",
        "django-simpleui>=2023.8.28,<2025",
        "adrf==0.1.6",
        "redis>=5.0.0,<6",
        "django-redis>=5.0.0,<6",
        "channels[daphne]==4.1.0",
        "Twisted[http2,tls]==24.3.0",
        "python_json_logger>=2.0.3,<3",
        "httpx[http2]>=0.23.2,<1",
        "requests>=2.28.0,<3",
        "protobuf>=3.19.5,<6",
        "opentelemetry-api==1.24.0",
        "opentelemetry-sdk==1.24.0",
        "opentelemetry-exporter-jaeger==1.21.0",
        "opentelemetry-exporter-otlp==1.24.0",
        "opentelemetry-instrumentation==0.45b0",
        "opentelemetry-instrumentation-asgi==0.45b0",
        "opentelemetry-instrumentation-django==0.45b0",
        "opentelemetry-instrumentation-dbapi==0.45b0",
        "opentelemetry-instrumentation-redis==0.45b0",
        "opentelemetry-instrumentation-requests==0.45b0",
        "opentelemetry-instrumentation-celery==0.45b0",
        "opentelemetry-instrumentation-logging==0.45b0",
        "opentelemetry-instrumentation-httpx==0.45b0",
        "ipython>=8.10.0,<9",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
