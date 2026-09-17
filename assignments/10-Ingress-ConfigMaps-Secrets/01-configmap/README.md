# ConfigMap — Decoupling Plain-Text Configuration from Container Images

## Why Do We Need ConfigMap?

### The Problem: Configuration Baked Into Docker Images
When building application container images, hardcoding settings inside code or configuration files causes major operational problems:
```python
LOG_LEVEL = "DEBUG"
PORT = 5000
DATABASE_HOST = "localhost"
```
If this image is pushed to production, running it requires different values:
- `LOG_LEVEL` should be `INFO` (not `DEBUG`)
- `DATABASE_HOST` should point to the internal database service (not `localhost`)

Baking configuration into the image forces you to re-build and re-push the entire Docker image whenever a config property changes. This breaks the 12-Factor App methodology:
> **The exact same application artifact must run across Development, Staging, and Production environments without rebuilding. Only runtime configuration should vary.**

### The Solution: Kubernetes ConfigMap
A `ConfigMap` externalizes non-sensitive configuration into key-value pairs stored in the Kubernetes cluster control plane. Workloads consume these values as environment variables, command-line arguments, or mounted configuration files at pod startup.

```
Without ConfigMap:
  Code + Config -> Docker Build -> Image v1 (Dev)
  Code + Config -> Docker Build -> Image v2 (Prod)

With ConfigMap:
  Code -> Docker Build -> Single App Image
                             │
       ┌─────────────────────┴─────────────────────┐
       ▼                                           ▼
  Dev Pod (mounts dev-config)               Prod Pod (mounts prod-config)
```

---

## Key Characteristics

1. **Non-Sensitive Data Only:** ConfigMaps are stored unencrypted by default in etcd. Never place passwords, tokens, or private keys inside a ConfigMap.
2. **Multiple Consumption Modes:**
   - Single environment variables via `valueFrom.configMapKeyRef`.
   - Batch environment variables via `envFrom.configMapRef`.
   - Read-only files mounted to a container directory via `volumes` and `volumeMounts`.
3. **Immutability Option:** Kubernetes allows setting `immutable: true` on ConfigMaps to protect against accidental changes and reduce kube-apiserver load.
4. **Size Constraint:** ConfigMaps cannot exceed 1 MiB.

---

## Real-World Use Cases

- Setting runtime parameters (`ENVIRONMENT=production`, `LOG_LEVEL=INFO`, `PORT=5000`).
- Overriding third-party configuration files (mounting custom `nginx.conf` or Prometheus alert rules into containers).
- Enabling or disabling runtime feature flags (`FEATURE_NEW_CHECKOUT=true`).

---

## Manifest Reference

### `01-configmap/app-config.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: yatri-app-config
  labels:
    app: yatri-backend
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
  PORT: "5000"
  DEFAULT_CURRENCY: "INR"
  MAX_BOOKING_DAYS: "30"
```

---

## Verification & Commands

```bash
# 1. Apply the ConfigMap
kubectl apply -f 01-configmap/app-config.yaml

# 2. Inspect created ConfigMap
kubectl get configmap yatri-app-config
kubectl describe configmap yatri-app-config

# 3. Read a specific key directly
kubectl get configmap yatri-app-config -o jsonpath='{.data.LOG_LEVEL}'
```

Expected Output:
```text
NAME               DATA   AGE
yatri-app-config   5      10s

Name:         yatri-app-config
Namespace:    default
Labels:       app=yatri-backend
Data
====
DEFAULT_CURRENCY:  INR
ENVIRONMENT:       production
LOG_LEVEL:         INFO
MAX_BOOKING_DAYS:  30
PORT:              5000
```
