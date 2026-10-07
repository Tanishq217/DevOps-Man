# End-to-End Mini-Project: Production Web Application

## Overview

This project brings together all core concepts from Session 12 into a production-grade microservice architecture:
1. **Isolated Namespace:** `production-webapp`
2. **Persistent Storage:** 500Mi PVC dynamically provisioned via default StorageClass
3. **Application Workload:** 2-replica NGINX deployment with CPU/Memory requests and limits
4. **Health Probes:** Liveness and Readiness probes guarding container status and routing
5. **Autoscaling:** Horizontal Pod Autoscaler scaling between 2 and 5 replicas targeting 50% CPU

```
Traffic Spike
     │
     ▼
[ Service: web-service ] (ClusterIP: port 80)
     │
     ├───────────────────────┬───────────────────────┐
     ▼                       ▼                       ▼
[ Pod: web-app-1 ]      [ Pod: web-app-2 ]      [ Pod: web-app-N ]
 ├─ Liveness Probe       ├─ Liveness Probe       ├─ Liveness Probe
 ├─ Readiness Probe      ├─ Readiness Probe      ├─ Readiness Probe
 └─ Mounts: /data        └─ Mounts: /data        └─ Mounts: /data
            │                       │                       │
            └───────────────────────┴───────────────────────┘
                                    │
                                    ▼
                         [ PVC: web-data (500Mi) ]
                                    │
                         [ StorageClass: standard ]
```

---

## Step-by-Step Deployment

```bash
# 1. Create Namespace
kubectl apply -f mini-project/namespace.yaml

# 2. Deploy PVC
kubectl apply -f mini-project/pvc.yaml
kubectl get pvc -n production-webapp

# 3. Deploy Application and Service
kubectl apply -f mini-project/deployment.yaml
kubectl apply -f mini-project/service.yaml
kubectl rollout status deployment/web-app -n production-webapp

# 4. Deploy HPA
kubectl apply -f mini-project/hpa.yaml
kubectl get hpa -n production-webapp
```

---

## Verification & Drills

### 1. Storage Persistence Test
Write data to the persistent volume inside one Pod, delete the Pod, and verify the replacement Pod reads the same file:

```bash
POD_NAME=$(kubectl get pods -n production-webapp -l app=web-app -o jsonpath='{.items[0].metadata.name}')

# Write data
kubectl exec -n production-webapp "$POD_NAME" -- sh -c 'echo "Database state preserved" > /data/persistence.txt'

# Verify
kubectl exec -n production-webapp "$POD_NAME" -- cat /data/persistence.txt

# Delete Pod
kubectl delete pod -n production-webapp "$POD_NAME"

# Check new Pod
NEW_POD=$(kubectl get pods -n production-webapp -l app=web-app -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n production-webapp "$NEW_POD" -- cat /data/persistence.txt
# Output: Database state preserved
```

### 2. Traffic Spike & Autoscaling Test
```bash
# Launch load generator
kubectl run load-gen -n production-webapp --image=busybox:1.36 --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://web-service; done"

# Watch autoscaling in real time
kubectl get hpa -n production-webapp -w
kubectl get pods -n production-webapp -w

# Cleanup load generator
kubectl delete pod load-gen -n production-webapp
```

---

## Cleanup
```bash
kubectl delete namespace production-webapp
```
