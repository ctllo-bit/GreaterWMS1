FROM --platform=linux/amd64 python:3.10.18-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /GreaterWMS

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel dj-database-url psycopg2-binary \
    && pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 8008

RUN chmod +x /GreaterWMS/backend_start.sh
CMD ["/GreaterWMS/backend_start.sh"]

