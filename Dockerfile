FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYVECTORHOUND_HOST=0.0.0.0 \
    PYVECTORHOUND_PORT=8006

WORKDIR /app

COPY pyproject.toml README.md ./
COPY pyvectorhound ./pyvectorhound
COPY src ./src
COPY Cargo.toml Cargo.lock ./

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir ".[server]"

EXPOSE 8006

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8006/health', timeout=3)"

CMD ["python", "-m", "pyvectorhound.server"]
