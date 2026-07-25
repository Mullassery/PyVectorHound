# PyVectorHound Production Deployment Guide

Complete guide for deploying PyVectorHound in production environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [Cloud Platforms](#cloud-platforms)
5. [Configuration & Scaling](#configuration--scaling)
6. [Monitoring & Observability](#monitoring--observability)
7. [Security Best Practices](#security-best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites

```bash
python >= 3.8
pip or uv
```

### Installation

```bash
# Clone repository
git clone https://github.com/Mullassery/PyVectorHound.git
cd pyvectorhound

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Start example application
python examples/retrieval_debug.py
```

### Configuration

Create `.env` file for local development:

```env
# Database Configuration
VECTOR_DB_TYPE=qdrant
VECTOR_DB_ENDPOINT=localhost:6333

# Observability
OTEL_ENABLED=true
OTEL_BACKEND=logging

# Application
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
```

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY pyvectorhound/ ./pyvectorhound/
COPY examples/ ./examples/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["python", "-m", "pyvectorhound.server", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose (with Qdrant)

```yaml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_storage:/qdrant/storage
    environment:
      QDRANT_API_KEY: ${QDRANT_API_KEY}

  pyvectorhound:
    build: .
    ports:
      - "8000:8000"
    environment:
      VECTOR_DB_TYPE: qdrant
      VECTOR_DB_ENDPOINT: qdrant:6333
      OTEL_BACKEND: jaeger
      JAEGER_ENDPOINT: http://jaeger:14268/api/traces
    depends_on:
      - qdrant
      - jaeger
    volumes:
      - ./logs:/app/logs

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "6831:6831/udp"
      - "16686:16686"

volumes:
  qdrant_storage:
```

### Build and Run

```bash
# Build image
docker build -t pyvectorhound:latest .

# Run container
docker run -p 8000:8000 \
  -e VECTOR_DB_TYPE=qdrant \
  -e VECTOR_DB_ENDPOINT=localhost:6333 \
  pyvectorhound:latest

# Using Docker Compose
docker-compose up -d
```

---

## Kubernetes Deployment

### Helm Chart Structure

```
helm/pyvectorhound/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   └── hpa.yaml
```

### Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pyvectorhound
  namespace: pyvectorhound
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pyvectorhound
  template:
    metadata:
      labels:
        app: pyvectorhound
        version: v1.0.0
    spec:
      containers:
      - name: pyvectorhound
        image: pyvectorhound:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: VECTOR_DB_TYPE
          valueFrom:
            configMapKeyRef:
              name: pyvectorhound-config
              key: db_type
        - name: OTEL_BACKEND
          valueFrom:
            configMapKeyRef:
              name: pyvectorhound-config
              key: otel_backend
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
```

### Service Definition

```yaml
apiVersion: v1
kind: Service
metadata:
  name: pyvectorhound
  namespace: pyvectorhound
spec:
  type: LoadBalancer
  selector:
    app: pyvectorhound
  ports:
  - name: http
    port: 80
    targetPort: 8000
```

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: pyvectorhound-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: pyvectorhound
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace pyvectorhound

# Apply manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -n pyvectorhound
kubectl get svc -n pyvectorhound

# View logs
kubectl logs -f deployment/pyvectorhound -n pyvectorhound

# Port forward for local testing
kubectl port-forward svc/pyvectorhound 8000:80 -n pyvectorhound
```

---

## Cloud Platforms

### AWS ECS

```json
{
  "family": "pyvectorhound",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "pyvectorhound",
      "image": "ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/pyvectorhound:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "VECTOR_DB_TYPE",
          "value": "qdrant"
        },
        {
          "name": "OTEL_BACKEND",
          "value": "datadog"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/pyvectorhound",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud Run

```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/pyvectorhound

# Deploy to Cloud Run
gcloud run deploy pyvectorhound \
  --image gcr.io/PROJECT_ID/pyvectorhound:latest \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --set-env-vars VECTOR_DB_TYPE=qdrant,OTEL_BACKEND=datadog \
  --allow-unauthenticated
```

### Azure Container Instances

```bash
# Create resource group
az group create --name pyvectorhound --location eastus

# Deploy container
az container create \
  --resource-group pyvectorhound \
  --name pyvectorhound \
  --image pyvectorhound:latest \
  --ports 8000 \
  --environment-variables \
    VECTOR_DB_TYPE=qdrant \
    OTEL_BACKEND=datadog \
  --memory 0.5 \
  --cpu 0.5
```

---

## Configuration & Scaling

### Environment Variables

```env
# Application
APP_ENV=production                    # development, staging, production
DEBUG=false                          # Enable debug mode
LOG_LEVEL=INFO                       # DEBUG, INFO, WARNING, ERROR
MAX_WORKERS=4                        # Worker threads

# Database Configuration
VECTOR_DB_TYPE=qdrant               # qdrant, chroma, milvus, weaviate, pgvector, pinecone
VECTOR_DB_ENDPOINT=localhost:6333   # Database endpoint
VECTOR_DB_API_KEY=${VECTOR_DB_API_KEY}  # API key if needed
VECTOR_DB_TIMEOUT=30                # Connection timeout in seconds
VECTOR_DB_MAX_RETRIES=3             # Max retry attempts

# Observability
OTEL_ENABLED=true                   # Enable OpenTelemetry
OTEL_BACKEND=jaeger                 # jaeger, datadog, new_relic, honeycomb, prometheus
OTEL_SAMPLE_RATE=1.0                # Trace sampling rate (0-1)
JAEGER_ENDPOINT=http://jaeger:14268 # Jaeger collector endpoint
DATADOG_API_KEY=${DATADOG_API_KEY}  # Datadog API key
DATADOG_SITE=datadoghq.com          # Datadog region

# Performance
BATCH_SIZE=100                      # Batch size for operations
CACHE_TTL=300                       # Cache time-to-live in seconds
MAX_CONCURRENT_REQUESTS=100         # Max concurrent requests
```

### Performance Tuning

```python
# config.py
from pyvectorhound import Hound
from pyvectorhound.db_adapters import DatabaseType, DatabaseConfig

# Optimize for throughput
config = DatabaseConfig(
    db_type=DatabaseType.QDRANT,
    endpoint="qdrant:6333",
    batch_size=500,  # Increase batch size
    timeout_seconds=60,
)

# Optimize for latency
config = DatabaseConfig(
    db_type=DatabaseType.QDRANT,
    endpoint="qdrant:6333",
    batch_size=10,  # Smaller batches for lower latency
    timeout_seconds=5,
)
```

### Database Connection Pooling

```python
# Use connection pooling for better performance
from pyvectorhound.db_adapters import DatabaseConfig, MockDatabaseAdapter

config = DatabaseConfig(
    db_type=DatabaseType.QDRANT,
    endpoint="qdrant:6333",
    batch_size=100,
    additional_params={
        "pool_size": 20,
        "max_overflow": 40,
        "pool_recycle": 3600,
    }
)
```

---

## Monitoring & Observability

### OpenTelemetry Setup

```python
from pyvectorhound.otel_integration import OTelConfig, OTelBackend, OTelInstrument

# Configure OpenTelemetry
config = OTelConfig(
    enabled=True,
    service_name="pyvectorhound",
    backend=OTelBackend.DATADOG,
    endpoint="https://api.datadoghq.com",
    api_key=os.getenv("DATADOG_API_KEY"),
    sample_rate=1.0,
)

instrument = OTelInstrument(config)

# Record metrics
instrument.record_metric("retrieval.latency_ms", latency, "ms")
instrument.record_metric("retrieval.recall", recall, "ratio")
instrument.record_metric("cost.monthly_estimate", cost, "usd")
```

### Prometheus Metrics

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'pyvectorhound'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### Alert Rules

```yaml
# alerts.yml
groups:
  - name: pyvectorhound
    rules:
      - alert: HighLatency
        expr: retrieval_latency_ms > 1000
        for: 5m
        annotations:
          summary: "High retrieval latency (> 1s)"

      - alert: LowRecall
        expr: retrieval_recall < 0.7
        for: 10m
        annotations:
          summary: "Low retrieval recall (< 0.7)"

      - alert: HighCost
        expr: cost_monthly_estimate > 10000
        for: 1h
        annotations:
          summary: "Monthly cost forecast > $10k"
```

---

## Security Best Practices

### Secrets Management

```bash
# Use environment variables or secrets manager
export VECTOR_DB_API_KEY="your-api-key"
export DATADOG_API_KEY="your-datadog-key"

# Or use Kubernetes secrets
kubectl create secret generic pyvectorhound-secrets \
  --from-literal=vector-db-api-key=${VECTOR_DB_API_KEY} \
  --from-literal=datadog-api-key=${DATADOG_API_KEY} \
  -n pyvectorhound
```

### Network Security

```yaml
# Network Policy - restrict ingress/egress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: pyvectorhound-netpol
spec:
  podSelector:
    matchLabels:
      app: pyvectorhound
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
      - podSelector:
          matchLabels:
            app: nginx
      ports:
      - protocol: TCP
        port: 8000
  egress:
    - to:
      - podSelector:
          matchLabels:
            app: qdrant
      ports:
      - protocol: TCP
        port: 6333
```

### TLS/HTTPS

```python
# Enable HTTPS in production
from fastapi import FastAPI
import uvicorn

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="/path/to/key.pem",
        ssl_certfile="/path/to/cert.pem",
    )
```

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Timeout

```python
# Increase timeout
config = DatabaseConfig(
    db_type=DatabaseType.QDRANT,
    endpoint="localhost:6333",
    timeout_seconds=60,  # Increase from default 30
)
```

#### 2. Memory Usage Growing

```bash
# Monitor memory usage
docker stats pyvectorhound

# Check for memory leaks
# Reduce batch size or enable garbage collection
export PYTHONUNBUFFERED=1
python -u app.py
```

#### 3. High Latency

```python
# Profile latency
from pyvectorhound.otel_integration import OTelInstrument

instrument = OTelInstrument(config)
span = instrument.start_span("query_operation")
try:
    # Your operation
    pass
finally:
    instrument.record_span(span)
```

### Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("pyvectorhound")
logger.debug("Detailed diagnostic information")
```

### Health Checks

```bash
# Check application health
curl -s http://localhost:8000/health | jq .

# Expected response:
# {
#   "status": "healthy",
#   "timestamp": "2026-07-26T12:00:00Z",
#   "version": "1.0.0"
# }
```

---

## Support & Resources

- **Documentation**: https://github.com/Mullassery/PyVectorHound/wiki
- **Issues**: https://github.com/Mullassery/PyVectorHound/issues
- **Discord**: [Join Community](https://discord.gg/pyvectorhound)
- **Email**: support@pyvectorhound.dev

---

**Last Updated**: 2026-07-26  
**Version**: 1.0.0
