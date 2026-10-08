# Session 19: Screenshot Capture Guide

This guide gives you the exact commands and browser URLs to capture all 14 project screenshots matching the instructor's syllabus and friend's reference repository.

---

## Screenshot Matrix & Overview

| Screenshot File | Topic / Domain | Type | Command / URL to Capture |
|---|---|:---:|---|
| **`part1-1.png`** | Kubernetes Workload Startup | Terminal | `kubectl apply -f k8s/` and `kubectl get pods -n session19-monitoring` |
| **`part1-2.png`** | App Logs & Describe Deployment | Terminal | `kubectl logs deployment/session19-demo -n session19-monitoring` & `kubectl describe` |
| **`part1-3.png`** | Deployment Events & Lifecycle | Terminal | `kubectl get events -n session19-monitoring` |
| **`part2-1.png`** | Docker Compose Prometheus Startup | Terminal | `docker-compose ps` showing Prometheus running on port 9090 |
| **`part2-2.png`** | Prometheus Web UI | Browser | `http://localhost:9090` (Prometheus Query & Alerts tab) |
| **`part2-3.png`** | Raw `/metrics` Endpoint | Browser | `http://localhost:9090/metrics` |
| **`part2-4.png`** | PromQL Health Query (`up`) | Browser | `http://localhost:9090` running query `up` returning `1` |
| **`part3-1.png`** | Docker Compose Stack Status | Terminal | `docker-compose ps` showing both Prometheus (9090) & Grafana (3000) running |
| **`part3-2.png`** | Prometheus Query Page | Browser | `http://localhost:9090` query interface |
| **`part3-3.png`** | Grafana Login Screen | Browser | `http://localhost:3000` (or `http://localhost:3000/login`) |
| **`part3-4.png`** | Grafana Home Page | Browser | `http://localhost:3000/?orgId=1` (Explore, Dashboards, Connections menu) |
| **`part3-5.png`** | Prometheus Data Source Connected | Browser | `http://localhost:3000/connections/datasources` ("Successfully queried the Prometheus API") |
| **`part3-6.png`** | Grafana Dashboard / Panel | Browser | `http://localhost:3000/d/aw9s4z/session-19-system-and-application-observability` |
| **`part4-1.png`** | GitOps Declarative Reconciliation | Terminal | `kubectl apply` & `kubectl scale deployment ... --replicas=3` showing 3/3 ready |

---

## Step-by-Step Screenshot Capture Instructions

### PART 1: Kubernetes Workload Monitoring (Terminal Screenshots)

#### 📸 `part1-1.png` — Cluster Startup & Application Deployment
1. Run in your terminal:
   ```bash
   cd "/Users/tanishqsingh/Documents/Code Boost/DevOps-Man/assignments/19-Monitoring, Observability&GitOps"
   kubectl apply -f k8s/namespace.yaml -f k8s/deployment.yaml -f k8s/service.yaml
   kubectl get pods -n session19-monitoring -o wide
   ```
2. Take a screenshot of the terminal output.
3. Save as: `screenshots/part1-1.png`

---

#### 📸 `part1-2.png` — Pod Logs & Deployment Description
1. Run in your terminal:
   ```bash
   kubectl logs deployment/session19-demo -n session19-monitoring --tail=10
   kubectl describe deployment session19-demo -n session19-monitoring
   ```
2. Take a screenshot showing the log stream (`[INFO] Health check OK...`) and deployment conditions (`Available=True`).
3. Save as: `screenshots/part1-2.png`

---

#### 📸 `part1-3.png` — Deployment Events
1. Run in your terminal:
   ```bash
   kubectl get events -n session19-monitoring --sort-by='.metadata.creationTimestamp'
   ```
2. Take a screenshot showing the replica set scale up events.
3. Save as: `screenshots/part1-3.png`

---

### PART 2: Prometheus Metrics & Health (Terminal & Browser)

#### 📸 `part2-1.png` — Docker Compose Prometheus Running
1. Run in your terminal:
   ```bash
   cd "/Users/tanishqsingh/Documents/Code Boost/DevOps-Man/assignments/19-Monitoring, Observability&GitOps"
   docker-compose ps
   ```
2. Take a screenshot showing `session19-prometheus` running on `0.0.0.0:9090->9090/tcp`.
3. Save as: `screenshots/part2-1.png`

---

#### 📸 `part2-2.png` — Prometheus Web UI
1. Open your web browser to:
   ```text
   http://localhost:9090
   ```
2. Take a screenshot of the Prometheus web interface (Expression / Query bar and top navigation bar).
3. Save as: `screenshots/part2-2.png`

---

#### 📸 `part2-3.png` — Raw Prometheus Metrics Endpoint
1. Open your web browser to:
   ```text
   http://localhost:9090/metrics
   ```
2. Take a screenshot of the raw text metrics output (showing `# HELP` and `# TYPE` metrics).
3. Save as: `screenshots/part2-3.png`

---

#### 📸 `part2-4.png` — PromQL `up` Query Execution
1. Open your web browser to:
   ```text
   http://localhost:9090
   ```
2. Type `up` in the query expression bar and click **Execute**.
3. Take a screenshot showing the table with:
   * `up{instance="localhost:9090", job="prometheus"}  1`
4. Save as: `screenshots/part2-4.png`

---

### PART 3: Grafana Dashboards & Telemetry (Browser Screenshots)

#### 📸 `part3-1.png` — Docker Compose Prometheus & Grafana Status
1. Run in your terminal:
   ```bash
   cd "/Users/tanishqsingh/Documents/Code Boost/DevOps-Man/assignments/19-Monitoring, Observability&GitOps"
   docker-compose ps
   ```
2. Take a screenshot showing both `session19-prometheus` (:9090) and `session19-grafana` (:3000) in `Up` status.
3. Save as: `screenshots/part3-1.png`

---

#### 📸 `part3-2.png` — Prometheus Query Explorer Page
1. Open your web browser to:
   ```text
   http://localhost:9090/graph
   ```
2. Take a screenshot of the query execution view.
3. Save as: `screenshots/part3-2.png`

---

#### 📸 `part3-3.png` — Grafana Login Page
1. Open an incognito browser window or logout to:
   ```text
   http://localhost:3000/login
   ```
2. Take a screenshot of the Grafana authentication login screen.
3. Save as: `screenshots/part3-3.png`

---

#### 📸 `part3-4.png` — Grafana Home Page
1. Login to Grafana at `http://localhost:3000` with:
   * **Username**: `admin`
   * **Password**: `admin`
2. Take a screenshot of the Grafana Home dashboard showing the left navigation panel (Dashboards, Explore, Alerting, Connections).
3. Save as: `screenshots/part3-4.png`

---

#### 📸 `part3-5.png` — Prometheus Data Source Connected
1. In Grafana, navigate to:
   ```text
   http://localhost:3000/connections/datasources
   ```
2. Click on **Prometheus**, scroll down, and click **Save & test**.
3. It will display the green notification:
   > **"Successfully queried the Prometheus API."**
4. Take a screenshot of this page showing the success message.
5. Save as: `screenshots/part3-5.png`

---

#### 📸 `part3-6.png` — Grafana Dashboard & Telemetry Panel
1. In Grafana, open the pre-created dashboard at:
   ```text
   http://localhost:3000/d/aw9s4z/session-19-system-and-application-observability
   ```
2. Take a screenshot showing the active visual panels (Application Health, Active Goroutines, Process Resident Memory, and CPU Usage).
3. Save as: `screenshots/part3-6.png`

---

### PART 4: GitOps Declarative Scaling & Reconciliation (Terminal Screenshot)

#### 📸 `part4-1.png` — GitOps Declarative Manifests & Scaling
1. Run in your terminal:
   ```bash
   kubectl scale deployment session19-demo -n session19-monitoring --replicas=3
   kubectl get deployment session19-demo -n session19-monitoring
   kubectl get pods -n session19-monitoring
   ```
2. Take a screenshot showing the deployment running with `READY 3/3` pods.
3. Save as: `screenshots/part4-1.png`

---

## Summary Checklist

- [ ] `screenshots/part1-1.png`
- [ ] `screenshots/part1-2.png`
- [ ] `screenshots/part1-3.png`
- [ ] `screenshots/part2-1.png`
- [ ] `screenshots/part2-2.png`
- [ ] `screenshots/part2-3.png`
- [ ] `screenshots/part2-4.png`
- [ ] `screenshots/part3-1.png`
- [ ] `screenshots/part3-2.png`
- [ ] `screenshots/part3-3.png`
- [ ] `screenshots/part3-4.png`
- [ ] `screenshots/part3-5.png`
- [ ] `screenshots/part3-6.png`
- [ ] `screenshots/part4-1.png`
