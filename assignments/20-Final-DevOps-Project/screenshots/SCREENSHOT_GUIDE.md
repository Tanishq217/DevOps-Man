# Capstone Screenshots Master Verification Guide

This directory contains the complete set of **16 verified screenshots** for the **Session 20 / Session 21 Final DevOps Project (TaskBoard SaaS)**.

All screenshots are verified, properly named in two-digit sequence (`01-` to `16-`), and embedded across Section 12 of [`README.md`](../README.md):

| # | Screenshot Filename | Verification Domain | Technical Scope & Verification Details |
|---|---|---|---|
| **01** | `01-docker-compose-startup.png` | Docker & Local Stack | Build and startup sequence of PostgreSQL, FastAPI backend, and React frontend |
| **02** | `02-docker-compose-running.png` | Container Health & Ports | `docker compose ps` showing all 3 containers healthy on ports 8000, 3000, and 5432 |
| **03** | `03-pytest-unit-tests.png` | Automated Test Suite | `pytest` terminal output confirming 15/15 unit and integration tests passing in 0.49s |
| **04** | `04-sast-bandit-scan.png` | Static Security (SAST) | Bandit scan (`bandit -r application/backend/app -ll`) detecting 0 vulnerabilities |
| **05** | `05-trivy-container-scan.png` | Container Security (CVE) | Trivy scanning `taskboard-backend:latest` confirming 0 CRITICAL CVEs |
| **06** | `06-terraform-init.png` | Cloud IaC (Terraform) | HashiCorp AWS provider v5.100.0 initialization in `terraform/` |
| **07** | `07-terraform-plan.png` | Cloud IaC (Terraform) | Execution plan detailing 13 cloud resources to provision (VPC, Subnet, SG, EC2, S3) |
| **08** | `08-terraform-apply.png` | Cloud Provisioning | Successful apply creating 13 AWS resources and displaying Terraform outputs |
| **09** | `09-helm-lint-verify.png` | Helm Chart Syntax | `helm lint ./helm/taskboard` passing with 0 errors, plus HPA manifest inspection |
| **10** | `10-helm-k8s-deployment.png` | Kubernetes & Helm Rollout | `helm upgrade --install` deployment and `kubectl get pods,svc,ingress,hpa` |
| **11** | `11-troubleshooting-diagnosis.png` | Troubleshooting Runbook | Diagnostic analysis and remediation runbook for probe failures and routing |
| **12** | `12-troubleshooting-resolution.png` | Troubleshooting Fix | Terminal output diagnosing Kubernetes pod logs and verifying resolution |
| **13** | `13-browser-app-ui.png` | Production Frontend Dashboard | Browser UI at `http://localhost:3000` showing dark theme, KPI cards, and live tasks |
| **14** | `14-github-actions-green-pipeline.png` | CI/CD Automation | GitHub Actions Run #6 showing all 4 stages completed with green checkmarks |
| **15** | `15-ghcr-published-packages.png` | Artifact Registry (GHCR) | Published container images `taskboard-backend` and `taskboard-frontend` |
| **16** | `16-prometheus-metrics-endpoint.png` | Observability & Telemetry | Live `curl http://localhost:8000/metrics` output showing runtime metrics stream |
