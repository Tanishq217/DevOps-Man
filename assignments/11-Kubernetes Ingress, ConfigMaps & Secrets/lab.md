# Lab Guide: Ingress, ConfigMaps & Secrets in Kubernetes

## Lab Objectives

1. Decouple plain-text configuration from container images using Kubernetes **ConfigMaps**.
2. Store and manage sensitive credentials securely using Kubernetes **Secrets**.
3. Implement Layer 7 HTTP path-based and host-based routing using an **NGINX Ingress Controller**.
4. Configure end-to-end HTTPS/TLS termination using self-signed certificates and Kubernetes TLS Secrets.
5. Diagnose and prevent common configuration pitfalls (such as the base64 trailing newline bug).
6. Understand configuration propagation and live pod updates via rolling restarts.

---

## Lab Architecture

```
Client (Browser / curl)
          │
          │ http://yatri.local
          ▼
 [NGINX Ingress Controller]
          │
     ┌────┴────────────────────────┐
     │ Path: /                     │ Path: /api/*
     ▼                             ▼
[Frontend Service: ClusterIP]  [Backend Service: ClusterIP]
     │                             │
     ▼                             ▼
[Frontend Pods: NGINX]        [Backend Pods: Python]
     │                             │
     ▼                             ├──────────────────────────┐
yatri-app-config                   ▼                          ▼
  (ConfigMap)              yatri-app-config           yatri-db-secret
                             (ConfigMap)                 (Secret)
```

---

## Part 1: Working with ConfigMaps

### 1. Inspect and Apply the ConfigMap
```bash
kubectl apply -f 01-configmap/app-config.yaml
kubectl get configmap yatri-app-config
kubectl describe configmap yatri-app-config
```

### 2. Read a ConfigMap Value Directly
```bash
kubectl get configmap yatri-app-config -o jsonpath='{.data.LOG_LEVEL}'
```

---

## Part 2: Working with Secrets

### 1. Generate Base64 Encoded Values Without Trailing Newlines
```bash
echo -n "yatri_admin" | base64
echo -n "secretpassword" | base64
echo -n "yatri_production_db" | base64
```

### 2. Apply and Verify Secret
```bash
kubectl apply -f 02-secret/db-secret.yaml
kubectl get secret yatri-db-secret
kubectl describe secret yatri-db-secret
```

### 3. Decode Secret for Verification
```bash
kubectl get secret yatri-db-secret -o jsonpath='{.data.POSTGRES_PASSWORD}' | base64 --decode
```

---

## Part 3: Deploying Microservices (Frontend & Backend)

### 1. Deploy Frontend Deployment and Service
```bash
kubectl apply -f 04-full-demo/frontend.yaml
kubectl get pods -l app=yatri-frontend
kubectl get svc yatri-frontend-service
```

### 2. Deploy Backend Deployment and Service
```bash
kubectl apply -f 04-full-demo/backend.yaml
kubectl rollout status deployment/yatri-backend --timeout=90s
kubectl get pods -l app=yatri-backend
kubectl get svc yatri-backend-service
```

### 3. Verify Internal ClusterIP Communication
Both services are of type `ClusterIP` and only accessible within the cluster. Ingress is required to expose them outside the cluster.

---

## Part 4: Ingress — One Entry Point for Both Services

### 1. Enable Minikube Ingress Controller
```bash
minikube addons enable ingress
kubectl get pods -n ingress-nginx
```

### 2. Apply Ingress Routing Rules
```bash
kubectl apply -f 04-full-demo/ingress.yaml
kubectl get ingress yatri-ingress
kubectl describe ingress yatri-ingress
```

---

## Part 5: Testing End-to-End Routing

### 1. Test Root Path (`/`) -> Routes to Frontend (NGINX)
```bash
curl -s -H "Host: yatri.local" http://$(minikube ip)/ | grep -i "<title>"
```

### 2. Test API Path (`/api/`) -> Routes to Backend (Python API)
```bash
curl -s -H "Host: yatri.local" http://$(minikube ip)/api/
```

### 3. Confirm Injected Environment Variables Inside Backend Pod
```bash
kubectl exec -it deployment/yatri-backend -- env | grep -E "ENVIRONMENT|LOG_LEVEL|POSTGRES"
```

---

## Part 6: Live ConfigMap Update & Rolling Restart Drill

### 1. Patch the ConfigMap
```bash
kubectl patch configmap yatri-app-config --type merge -p '{"data":{"ENVIRONMENT":"staging"}}'
```

### 2. Check Running Pod (Value Unchanged)
```bash
kubectl exec -it deployment/yatri-backend -- env | grep ENVIRONMENT
```

### 3. Perform Rolling Restart to Apply Changes
```bash
kubectl rollout restart deployment/yatri-backend
kubectl rollout status deployment/yatri-backend
kubectl exec -it deployment/yatri-backend -- env | grep ENVIRONMENT
```

---

## Part 7: The Newline Bug Debugging Drill

```bash
# Buggy encoding (with newline)
echo "secretpassword" | base64
# Output: c2VjcmV0cGFzc3dvcmQK

# Correct encoding (without newline)
echo -n "secretpassword" | base64
# Output: c2VjcmV0cGFzc3dvcmQ=
```

---

## Lab Cleanup

```bash
bash 04-full-demo/cleanup.sh
```
