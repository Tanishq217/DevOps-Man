# Canary Deployment Strategy

## Overview

A **Canary Deployment** exposes a new release to a small fraction of real user traffic while the rest of the workload runs on the existing stable version.
- Allows testing new releases under genuine production conditions without risking 100% outage.
- In native Kubernetes, traffic distribution is proportional to the **pod replica ratio**.

```
Traffic (Port 30030)
       │
       ▼
 [myapp-canary-service (selector: app=myapp-canary)]
       │
       ├─────────────────────────────────────────┐
       ▼ (90% traffic)                           ▼ (10% traffic)
[app-stable (9 pods, v1)]                 [app-canary (1 pod, v2)]
```

---

## Step-by-Step Execution

```bash
# 1. Deploy Stable Version (9 pods = 90%)
kubectl apply -f 06-canary/deployment-stable.yaml
kubectl apply -f 06-canary/service.yaml
kubectl rollout status deployment/app-stable

# 2. Deploy Canary Version (1 pod = 10%)
kubectl apply -f 06-canary/deployment-canary.yaml
kubectl rollout status deployment/app-canary

# 3. Test Traffic Distribution (Run curl in a loop)
for i in $(seq 1 20); do curl -s http://$(minikube ip):30030 | grep -o "STABLE v1\|CANARY v2"; done

# 4. Scale Up Canary Traffic to 30%
kubectl scale deployment app-canary --replicas=3
kubectl scale deployment app-stable --replicas=7
for i in $(seq 1 10); do curl -s http://$(minikube ip):30030 | grep -o "STABLE v1\|CANARY v2"; done

# 5. Full Promotion (100% to Canary)
kubectl scale deployment app-canary --replicas=9
kubectl scale deployment app-stable --replicas=0

# Cleanup
kubectl delete -f 06-canary/service.yaml
kubectl delete -f 06-canary/deployment-canary.yaml
kubectl delete -f 06-canary/deployment-stable.yaml
```
