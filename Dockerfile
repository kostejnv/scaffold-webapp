# Stage 1: Compile and build stage
ARG BASE_IMAGE=python
ARG BASE_TAG=3.12

FROM --platform=linux/amd64 ${BASE_IMAGE}:${BASE_TAG} as compile-image

ENV POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR="/tmp/poetry_cache" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    WORK_DIR=/app \
    PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR ${WORK_DIR}

# Copy only the dependencies configuration files to cache them in Docker layer
COPY pyproject.toml poetry.lock ${WORK_DIR}/

# Install system dependencies required for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    curl \
    && python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install poetry==${POETRY_VERSION} \
    && rm -rf /var/lib/apt/lists/*

# Install project dependencies
RUN  poetry config virtualenvs.create false
RUN  poetry install --no-interaction --no-root --only main --no-dev

# Stage 2: Final Image
FROM --platform=linux/amd64 ${BASE_IMAGE}:${BASE_TAG} as final-image

LABEL maintainer="Vít Koštejn v.kostejn.vk@gmail.com"

ENV PATH="/opt/venv/bin:$PATH" \
WORK_DIR=/app \
USER=admin \
PYTHONUNBUFFERED=1 \
PYTHONDONTWRITEBYTECODE=1

# Install Tini
RUN apt-get update && apt-get install -y --no-install-recommends \
    tini \
    && adduser --disabled-password --gecos '' --uid 1001 ${USER} \
    && mkdir -p ${WORK_DIR} \
    && chown -R ${USER}:${USER} ${WORK_DIR} \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${WORK_DIR}

# Copy the pre-built virtual environment
COPY --from=compile-image /opt/venv /opt/venv

# Copy the application code with proper permissions
COPY --chown=${USER}:${USER} . ${WORK_DIR}

USER ${USER}

ENTRYPOINT ["/usr/bin/tini", "--"]

HEALTHCHECK --interval=30s --timeout=15s --start-period=5s --retries=3 \
CMD [ "curl", "-f", "http://localhost:8000/health-check" ] || exit 1
