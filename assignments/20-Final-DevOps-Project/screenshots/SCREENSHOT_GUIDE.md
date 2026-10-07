# Capstone Screenshots Submission Guide

Save all captured screenshots directly inside this `screenshots/` directory with the following exact filenames:

| Screenshot File | Description | How to Capture / Command |
|---|---|---|
| `01-local-app-ui.png` | TaskBoard SaaS UI Dashboard | Open `http://localhost:3000` in browser showing tasks and KPI cards |
| `02-docker-compose-up.png` | Docker Compose Stack Running | `docker compose up -d && docker compose ps` |
| `03-pytest-passing.png` | Pytest Unit Tests Green | `pytest application/backend/tests -v` |
| `04-sast-bandit-scan.png` | Bandit SAST Scan Output | `bandit -r application/backend/app -ll` |
| `05-trivy-container-scan.png` | Trivy Container Security Scan | `trivy image --severity HIGH,CRITICAL ghcr.io/tanishq217/taskboard-backend:latest` |
| `06-github-actions-pipeline.png` | Green CI/CD Pipeline on GitHub | GitHub repository -> **Actions** tab showing successful workflow |
| `07-ghcr-packages.png` | GHCR Published Packages | GitHub profile/repo -> **Packages** showing published backend & frontend |
| `08-terraform-apply.png` | Terraform Infrastructure Provisioned | `cd terraform && terraform apply -auto-approve` |
| `09-k8s-pods-running.png` | Kubernetes Pods & Services in Running State | `kubectl get pods,svc,ingress,hpa -n taskboard` |
| `10-helm-list-deploy.png` | Helm Release Status | `helm list -n taskboard && helm status taskboard -n taskboard` |
| `11-metrics-endpoint.png` | Prometheus `/metrics` Output | `curl -s http://localhost:8000/metrics \| head -n 30` |
| `12-troubleshooting-fixed.png` | Troubleshooting Diagnosis & Resolution | Output showing pod fixed from CrashLoopBackOff to 1/1 Running |
