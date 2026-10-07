# Recreate Deployment Strategy

## Overview

The **Recreate** deployment strategy terminates all existing pods simultaneously before spinning up the new version.
- **Downtime Window:** There is an explicit period where zero pods are running. Requests during this interval return connection errors or 503s.
- **Architectural Justification:** Required for non-backward-compatible database schema changes, ReadWriteOnce (RWO) storage volume locks, or legacy single-instance applications.

```
[v1 Pods Running]
       │
       ▼ (Update applied)
[v1 Pods Terminating]
       │
       ▼
[0 Pods Running]  <--- DOWNTIME WINDOW
       │
       ▼
[v2 Pods Creating]
       │
       ▼
[v2 Pods Running]
```

---

## Step-by-Step Execution

```bash
# 1. Deploy v1
kubectl apply -f 07-recreate/deployment-v1.yaml
kubectl apply -f 07-recreate/service.yaml
kubectl get pods -l app=app-recreate

# 2. Watch Pods in Terminal 1
kubectl get pods -l app=app-recreate -w

# 3. Trigger Recreate Update in Terminal 2
kubectl apply -f 07-recreate/deployment-v2.yaml

# 4. Observe the Downtime Window and Rollout Completion
kubectl rollout status deployment/app-recreate

# 5. Rollback
kubectl rollout undo deployment/app-recreate

# Cleanup
kubectl delete -f 07-recreate/service.yaml
kubectl delete -f 07-recreate/deployment-v2.yaml
```
