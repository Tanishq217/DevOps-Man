# Capstone Screenshots Verification Guide

This directory contains the verified screenshots for the **Session 20: Final DevOps Project & Troubleshooting** capstone:

| Screenshot File | Description | Verification Details |
|---|---|---|
| `01-docker-compose-startup.png` | Docker Compose Stack Startup | Build and initialization of PostgreSQL, FastAPI backend, and React frontend containers |
| `02-docker-compose-running.png` | Multi-Container Runtime Status | `docker compose ps` showing all 3 containers healthy and listening on ports 8000, 3000, and 5432 |
| `03-pytest-unit-tests.png` | Automated Test Suite | `pytest` output confirming 15/15 unit and integration tests passing in 0.49s |
| `04-sast-bandit-scan.png` | Static Application Security Testing (SAST) | `bandit -r application/backend/app -ll` confirming 0 vulnerabilities across 240 lines of code |
| `05-trivy-container-scan.png` | Container Vulnerability Scanning | Trivy scanning `taskboard-backend:latest` detecting 0 CRITICAL CVEs |
| `06-terraform-init.png` | Terraform Initialization | `terraform init` successfully installing HashiCorp AWS provider v5.100.0 |
| `07-terraform-plan.png` | Terraform Execution Plan | `terraform plan` output detailing 13 cloud resources to add (VPC, Subnets, SG, EC2, S3) |
| `08-terraform-apply.png` | Infrastructure Provisioning | `terraform apply` confirming 13 resources created and displaying outputs (IPs, S3 bucket, SG) |
| `09-helm-lint-verify.png` | Helm Chart Syntax Validation | `helm lint helm/taskboard` passing with 0 failures, along with HPA definition |
| `10-helm-k8s-deployment.png` | Kubernetes & Helm Deployment | `helm upgrade --install` deploying release `taskboard`, and `kubectl get pods,svc,ingress,hpa` |
| `11-troubleshooting-diagnosis.png` | Troubleshooting Runbook (Scenario 4) | Diagnostic analysis and remediation instructions for probe failures and routing |
| `12-troubleshooting-resolution.png` | Troubleshooting Validation & Fix | Terminal output diagnosing Kubernetes deployment validation and verifying remediation |
