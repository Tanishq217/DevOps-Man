# Full Demo — ConfigMap + Secret + Ingress End-to-End Architecture

## System Architecture

This integrated lab deploys a complete two-tier cloud-native application on Kubernetes:

- **Frontend Tier (`/`):** An NGINX web server serving static assets. Reads non-sensitive environment variables (`ENVIRONMENT`, `LOG_LEVEL`) directly from a ConfigMap.
- **Backend Tier (`/api/`):** A lightweight Python REST API server. Reads configuration parameters from a ConfigMap and sensitive database credentials from a Secret.
- **Ingress Layer (`yatri.local`):** An NGINX Ingress Controller routing external traffic at Layer 7 using URL paths (`/` and `/api/`). Both backend services remain internal `ClusterIP` services.

```
Host Browser / curl
         │
         │ Host: yatri.local
         ▼
[Minikube Ingress Controller (Port 80)]
         │
         ├─────────────────────────────────────────┐
         │ Path: /                                 │ Path: /api/*
         ▼                                         ▼
[Frontend Service: ClusterIP]             [Backend Service: ClusterIP]
         │                                         │
         ▼                                         ▼
[yatri-frontend Pods (nginx)]             [yatri-backend Pods (python)]
         │                                         │
         ▼                                         ├─────────────────────────┐
   yatri-app-config                                ▼                         ▼
     (ConfigMap)                            yatri-app-config          yatri-db-secret
                                              (ConfigMap)                (Secret)
```

---

## Resource Summary

| File | Kind | Role |
| :--- | :--- | :--- |
| `configmap.yaml` | `ConfigMap` | Injects application configuration (`ENVIRONMENT`, `LOG_LEVEL`, `PORT`, `CURRENCY`) |
| `secret.yaml` | `Secret` | Injects sensitive PostgreSQL credentials (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`) |
| `frontend.yaml` | `Deployment` + `Service` | 2 replicas running NGINX exposed internally on port 80 |
| `backend.yaml` | `Deployment` + `Service` | 2 replicas running Python HTTP server exposed internally on port 80 |
| `ingress.yaml` | `Ingress` | Layer 7 routing rules mapping `yatri.local/` and `yatri.local/api/*` |
| `run-demo.sh` | Shell Script | Automated end-to-end setup script |
| `cleanup.sh` | Shell Script | Resource teardown and cleanup |

---

## Step-by-Step Manual Deployment

### 1. Enable Minikube Ingress Controller
```bash
minikube addons enable ingress
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=180s
```

### 2. Apply ConfigMap & Secret
```bash
kubectl apply -f 04-full-demo/configmap.yaml
kubectl apply -f 04-full-demo/secret.yaml
```

### 3. Deploy Frontend & Backend Services
```bash
kubectl apply -f 04-full-demo/frontend.yaml
kubectl apply -f 04-full-demo/backend.yaml

kubectl rollout status deployment/yatri-frontend --timeout=90s
kubectl rollout status deployment/yatri-backend --timeout=90s
```

### 4. Deploy Ingress Routing Rules
```bash
kubectl apply -f 04-full-demo/ingress.yaml
kubectl get ingress yatri-ingress
```

### 5. Configure Local Host Resolution
Retrieve Minikube IP and verify hosts entry:
```bash
minikube ip
# Add "<MINIKUBE_IP> yatri.local" to /etc/hosts if resolving natively
```

---

## Testing & Verification

### Test 1: Frontend Route (`/`)
```bash
curl -s -H "Host: yatri.local" http://$(minikube ip)/ | grep -i "<title>"
```
Expected:
```text
<title>Welcome to nginx!</title>
```

### Test 2: Backend API Route (`/api/`)
```bash
curl -s -H "Host: yatri.local" http://$(minikube ip)/api/
```
Expected Output:
```text
Yatri Backend API
=================
ENVIRONMENT     : production
LOG_LEVEL       : INFO
DEFAULT_CURRENCY: INR
POSTGRES_USER   : yatri_admin
POSTGRES_DB     : yatri_production_db
```

### Test 3: Inspect Injected Pod Environment Variables
```bash
kubectl exec -it deployment/yatri-backend -- env | grep -E "ENVIRONMENT|LOG_LEVEL|POSTGRES"
```

### Test 4: Live ConfigMap Update & Rolling Restart
```bash
# Update ConfigMap
kubectl patch configmap yatri-app-config --type merge -p '{"data":{"ENVIRONMENT":"staging"}}'

# Verify pod still has old value (env vars are fixed at container start)
kubectl exec -it deployment/yatri-backend -- env | grep ENVIRONMENT

# Trigger rolling restart to load new config
kubectl rollout restart deployment/yatri-backend
kubectl rollout status deployment/yatri-backend

# Verify updated value
kubectl exec -it deployment/yatri-backend -- env | grep ENVIRONMENT
```

---

## Teardown
```bash
bash 04-full-demo/cleanup.sh
```
