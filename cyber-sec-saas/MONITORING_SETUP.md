# MONITORING_SETUP.md

## Monitoring Stack Overview

This project uses Prometheus and Grafana for metrics collection and visualization.

### Components
- **Prometheus**: Scrapes backend metrics from `/metrics` endpoint.
- **Grafana**: Visualizes metrics with pre-configured dashboards.
- **Backend**: Exposes Prometheus metrics and health endpoint.
- **Postgres**: Database for backend.

## Setup Instructions

### 1. Docker Compose

All services are defined in `docker-compose.yml`:
- `db`: Postgres database
- `backend`: FastAPI backend (exposes `/metrics`)
- `frontend`: React/Vite frontend
- `prometheus`: Scrapes backend metrics
- `grafana`: Visualizes metrics

### 2. Prometheus Configuration

- Config file: `prometheus.yml`
- Scrapes `backend:8000/metrics` every 15s

### 3. Grafana Configuration

- Configured to use Prometheus as datasource
- Dashboard: `grafana/dashboard.json`
- Panels: Risk Score, Active Alerts, HTTP Requests, Latency, CPU %, Memory %

### 4. Running the Stack

Run all services:

```bash
docker-compose up --build
```

### 5. Accessing Dashboards

- **Grafana**: [http://localhost:3000](http://localhost:3000)
  - Username: `admin`, Password: `admin`
- **Prometheus**: [http://localhost:9090](http://localhost:9090)
- **Backend Health**: [http://localhost:8000/health](http://localhost:8000/health)
- **Backend Metrics**: [http://localhost:8000/metrics](http://localhost:8000/metrics)

### 6. Customizing Dashboards

- Edit `grafana/dashboard.json` for new panels.
- Add new metrics in `backend/app/metrics.py`.

### 7. Troubleshooting

- Ensure backend exposes `/metrics` and `/health`.
- Check Prometheus targets in UI for scrape errors.
- Check Grafana datasource settings.

### 8. Security

- Change default Grafana admin password for production.
- Restrict CORS and allowed hosts in backend.

---

For advanced setup, see `DEPLOYMENT.md` and `ENTERPRISE_IMPLEMENTATION.md`.
