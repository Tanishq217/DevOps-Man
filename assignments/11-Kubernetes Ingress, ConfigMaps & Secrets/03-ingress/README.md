# Ingress — Single Entry Point for All Cluster Microservices

## Why Do We Need Ingress?

### The Problem: LoadBalancer Per Service Causes Cost & Port Sprawl
In modern microservice architectures, an application consists of multiple discrete components (Frontend, Backend API, Authentication, Billing). Exposing each component using standard `LoadBalancer` services leads to:
1. **Financial Overhead:** Every cloud `LoadBalancer` service creates an external cloud load balancer (e.g. AWS ALB/NLB at ~$25/month each).
2. **Port & IP Fragmentation:** Users and frontend clients must manage multiple IPs or port ranges instead of standard ports 80 and 443.
3. **No Centralized Layer 7 Routing:** Simple L4 services cannot inspect HTTP request headers, hostnames, or URI paths.

### The Solution: Kubernetes Ingress & Ingress Controller
Kubernetes `Ingress` is a Layer 7 (HTTP/HTTPS) routing specification. Combined with an **Ingress Controller** (such as `ingress-nginx`), a single public IP serves as the unified gateway:
- Routes requests by hostname (`api.domain.com` vs `app.domain.com`).
- Routes requests by URL path (`/` vs `/api/`).
- Handles centralized SSL/TLS termination so internal pods communicate over plain HTTP.

```
Public Request (Port 80 / 443)
              │
              ▼
   [NGINX Ingress Controller]
              │
       ┌──────┴────────┐
       ▼               ▼
 Path: /           Path: /api/*
       ▼               ▼
 [Frontend Svc]   [Backend Svc]
  (ClusterIP)      (ClusterIP)
```

---

## Key Characteristics

1. **Rule Specification vs Implementation:** An Ingress manifest is only metadata rules. An active Ingress Controller daemon must be running in the cluster to translate these rules into NGINX routing tables.
2. **`ingressClassName`:** Specifies the controller implementation that manages this resource (standardized in Kubernetes v1.18+).
3. **Path Rewriting:** The annotation `nginx.ingress.kubernetes.io/rewrite-target: /$2` strips routing prefixes like `/api/` before forwarding the request to the upstream pod.
4. **SSL/TLS Termination:** Offloads public HTTPS decryption at the Ingress controller, simplifying pod configuration.

---

## Manifest Reference

### `03-ingress/ingress-routes.yaml` (Path-Based Routing)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: yatri-ingress
  labels:
    app: yatri-app
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
    nginx.ingress.kubernetes.io/use-regex: "true"
spec:
  ingressClassName: nginx
  rules:
    - host: yatri.local
      http:
        paths:
          - path: /api(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: yatri-backend-service
                port:
                  number: 80
          - path: /
            pathType: Prefix
            backend:
              service:
                name: yatri-frontend-service
                port:
                  number: 80
```

---

## Host-Based & TLS Hands-on Workflow

### Step 1: Generate Self-Signed Certificate with Subject Alternative Names (SAN)
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key \
  -out tls.crt \
  -subj "/CN=campus.local/O=CampusDevOps" \
  -addext "subjectAltName=DNS:campus.local,DNS:portal.campus.local,DNS:api.campus.local"
```

### Step 2: Store TLS Certificate as a Kubernetes Secret
```bash
kubectl create secret tls campus-tls-cert \
  --cert=tls.crt \
  --key=tls.key
```

### Step 3: Apply the Ingress with TLS & Host-Based Routing
```bash
kubectl apply -f 03-ingress/ingress-tls.yaml
kubectl get ingress campus-ingress-tls
```

Expected Output:
```text
NAME                 CLASS   HOSTS                                  ADDRESS        PORTS     AGE
campus-ingress-tls   nginx   portal.campus.local,api.campus.local   192.168.49.2   80, 443   15s
```

### Step 4: Test HTTPS Host Routing
```bash
INGRESS_IP=$(kubectl get ingress campus-ingress-tls -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

curl -k --resolve portal.campus.local:443:$INGRESS_IP https://portal.campus.local/
curl -k --resolve api.campus.local:443:$INGRESS_IP https://api.campus.local/api/
```
