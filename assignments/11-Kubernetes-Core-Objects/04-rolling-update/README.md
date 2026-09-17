# Rolling Update Strategy

## Overview

A **Rolling Update** is the default deployment strategy in Kubernetes. It incrementally replaces old Pods with new Pods without taking down the service.

```
Initial State:           [v1] [v1] [v1] [v1]
Surge New Pod:           [v1] [v1] [v1] [v1] + [v2]
v2 Passes Readiness:     [v1] [v1] [v1] [v2]
Repeat until all v2:     [v2] [v2] [v2] [v2]
```

---

## The RollingUpdate Parameters

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1       # Maximum extra pods that can be created above desired replica count
    maxUnavailable: 0 # Maximum pods that can be unavailable during update (0 guarantees zero-downtime)
```

---

## Step-by-Step Execution

```bash
# 1. Deploy v1
kubectl apply -f 04-rolling-update/deployment-v1.yaml
kubectl apply -f 04-rolling-update/service.yaml
kubectl rollout status deployment/app-rolling

# 2. Trigger Rolling Update to v2
kubectl apply -f 04-rolling-update/deployment-v2.yaml
kubectl rollout status deployment/app-rolling

# 3. View Rollout History
kubectl rollout history deployment/app-rolling

# 4. Instant Rollback
kubectl rollout undo deployment/app-rolling
kubectl rollout status deployment/app-rolling

# Cleanup
kubectl delete -f 04-rolling-update/service.yaml
kubectl delete -f 04-rolling-update/deployment-v1.yaml
```
