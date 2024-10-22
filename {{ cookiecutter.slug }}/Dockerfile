# syntax = docker/dockerfile:1

FROM python:3.11-slim-bullseye as base

# Environment Variables
## No more .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
## Ensures that all output is immediately flushed to stdout/stderr
ENV PYTHONUNBUFFERED 1
## Declare the argument for the build environment
ARG BUILD_ENVIRONMENT
## Environment variable for the build environment
ENV BUILD_ENVIRONMENT $BUILD_ENVIRONMENT

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt apt update \
    && DEBIAN_FRONTEND="noninteractive" apt install -y \
    gcc \
    build-essential \
    libc-dev \
    gettext \
    libpq-dev \
    curl \
    vim \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements requirements
RUN --mount=type=cache,target=/root/.cache/pip pip install --default-timeout=6000 -U pip && \
    pip install --default-timeout=6000 -r /app/requirements/${BUILD_ENVIRONMENT}.txt

RUN mkdir /app/static

# Copy the project code
COPY backend/ .

# Copy Scripts
COPY scripts/ /scripts

# Copy configs
COPY configs/ /configs

# Make scripts executable
RUN chmod ug+x /scripts/*.sh
