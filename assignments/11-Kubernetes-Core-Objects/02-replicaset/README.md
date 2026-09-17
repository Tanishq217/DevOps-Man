# ReplicaSet — Self-Healing & Horizontal Scaling

## Overview

A `ReplicaSet` ensures that a specified number of identical Pod replicas are running at all times.
- **Reconciliation Loop:** The ReplicaSet controller continuously checks the current state against the desired state (`spec.replicas`).
- **Self-Healing:** If a pod crashes or is manually deleted with `kubectl delete pod`, the ReplicaSet immediately spawns a replacement pod to restore the desired count.
- **Dynamic Scaling:** You can scale up or scale down replicas declaratively via YAML or imperatively via `kubectl scale`.

---

## Why Use Deployments Instead of Bare ReplicaSets?

In modern Kubernetes, you rarely create bare ReplicaSets directly. A `Deployment` manages ReplicaSets automatically underneath:
- ReplicaSets handle pod replication and self-healing.
- Deployments add declarative updates, rollout pausing/resuming, and instant rollback history.

---

## Commands & Verification

```bash
# 1. Apply ReplicaSet
kubectl apply -f 02-replicaset/backend-rs.yaml
kubectl get rs yatri-backend-rs
kubectl get pods -l app=yatri-backend

# 2. Test Self-Healing (Delete one pod)
POD_NAME=$(kubectl get pods -l app=yatri-backend -o jsonpath='{.items[0].metadata.name}')
kubectl delete pod $POD_NAME
kubectl get pods -l app=yatri-backend
# Observe that a replacement pod was immediately provisioned!

# 3. Scale Up to 5 Replicas
kubectl scale rs yatri-backend-rs --replicas=5
kubectl get pods -l app=yatri-backend

# 4. Scale Down to 2 Replicas
kubectl scale rs yatri-backend-rs --replicas=2
kubectl get pods -l app=yatri-backend

# Cleanup
kubectl delete rs yatri-backend-rs
```
