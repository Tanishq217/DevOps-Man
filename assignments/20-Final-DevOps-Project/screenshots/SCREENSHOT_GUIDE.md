# Capstone Screenshots Verification & Capture Guide

This guide details all screenshots included in the **Session 20 / Session 21 Final DevOps Project (TaskBoard SaaS)**.

---

## 1. Verified Master Screenshots (Already Embedded in README.md)

These 12 core screenshots are verified, properly named, and embedded across Section 12 of [`README.md`](../README.md):

| # | Screenshot Filename | Description | Verified Evidence Details |
|---|---|---|---|
| **01** | `01-docker-compose-startup.png` | Docker Compose Stack Startup | Build and startup sequence of PostgreSQL, FastAPI backend, and React frontend |
| **02** | `02-docker-compose-running.png` | Multi-Container Runtime Status | `docker compose ps` showing all 3 containers healthy on ports 8000, 3000, and 5432 |
| **03** | `03-pytest-unit-tests.png` | Automated Test Suite | `pytest` terminal run showing 15/15 unit and integration tests passing in 0.49s |
| **04** | `04-sast-bandit-scan.png` | Bandit SAST Security Scan | Static Application Security Testing showing 0 vulnerabilities across 240 LOC |
| **05** | `05-trivy-container-scan.png` | Trivy Container Security Scan | Vulnerability scan of `taskboard-backend` confirming 0 CRITICAL CVEs |
| **06** | `06-terraform-init.png` | Terraform Initialization | HashiCorp AWS provider v5.100.0 initialization in `terraform/` |
| **07** | `07-terraform-plan.png` | Terraform Execution Plan | Plan output detailing 13 cloud resources to provision (VPC, Subnet, SG, EC2, S3) |
| **08** | `08-terraform-apply.png` | Cloud Resource Provisioning | Successful apply creating 13 AWS resources and displaying Terraform outputs |
| **09** | `09-helm-lint-verify.png` | Helm Chart Lint & Validation | `helm lint ./helm/taskboard` passing with 0 errors, plus HPA manifest inspection |
| **10** | `10-helm-k8s-deployment.png` | Kubernetes & Helm Deployment | `helm upgrade --install` deployment and `kubectl get pods,svc,ingress,hpa` |
| **11** | `11-troubleshooting-diagnosis.png` | Troubleshooting Runbook (Scenario 4) | Detailed diagnostic analysis and remediation runbook for probe failures |
| **12** | `12-troubleshooting-resolution.png` | Troubleshooting Validation & Fix | Terminal output diagnosing Kubernetes pod logs and verifying resolution |

---

## 2. Bonus Browser & Pipeline Screenshots (Optional - For 100/100 Perfection)

If you would like to add additional visual proof directly matching the instructor's rubric in `GRADING.md`, take these 4 screenshots:

### Screenshot 13: Browser Application UI (`13-browser-app-ui.png`)
* **URL:** `http://localhost:3000`
* **What it shows:** The live TaskBoard dashboard with dark theme, KPI summary cards, sprint filters, and tasks loaded from the FastAPI backend.
* **Capture Step:**
  1. Open your browser and navigate to `http://localhost:3000`
  2. Take a screenshot of the entire dashboard window
  3. Save as: `screenshots/13-browser-app-ui.png`

### Screenshot 14: GitHub Actions Green Pipeline (`14-github-actions-green-pipeline.png`)
* **URL:** `https://github.com/Tanishq217/devsecops-pipeline/actions/runs/37764438909`
* **What it shows:** All 4 pipeline stages completed with green checkmarks:
  * 🧪 Build & Unit Tests
  * 🛡️ DevSecOps Security Scanning
  * 🐳 Docker Build, Trivy Scan & Push
  * ☸️ Deploy to Kubernetes (Kind)
* **Capture Step:**
  1. Open `https://github.com/Tanishq217/devsecops-pipeline/actions/runs/37764438909` in your browser
  2. Take a screenshot showing the green checkmarks across all jobs
  3. Save as: `screenshots/14-github-actions-green-pipeline.png`

### Screenshot 15: GitHub Container Registry Published Packages (`15-ghcr-published-packages.png`)
* **URL:** `https://github.com/Tanishq217?tab=packages`
* **What it shows:** Published GHCR container packages:
  * `taskboard-backend`
  * `taskboard-frontend`
* **Capture Step:**
  1. Open `https://github.com/Tanishq217?tab=packages`
  2. Take a screenshot showing both published packages
  3. Save as: `screenshots/15-ghcr-published-packages.png`

### Screenshot 16: Live Prometheus Metrics Endpoint (`16-prometheus-metrics-endpoint.png`)
* **URL:** `http://localhost:8000/metrics`
* **Command:** `curl -s http://localhost:8000/metrics | head -n 35`
* **What it shows:** Live Prometheus telemetry export (Python GC, memory, request counters, HTTP latency metrics).
* **Capture Step:**
  1. Open `http://localhost:8000/metrics` in browser OR run `curl -s http://localhost:8000/metrics | head -n 35` in your terminal
  2. Take a screenshot of the output
  3. Save as: `screenshots/16-prometheus-metrics-endpoint.png`
