# Blue-Green Deployment Strategy

## Overview

**Blue-Green Deployment** provisions two identical environments running side-by-side:
- **Blue (v1):** The active production environment currently handling 100% of user traffic.
- **Green (v2):** The new version deployed and tested in isolation, taking 0% of user traffic.

When ready, the operator changes the Service `selector` label (`slot: blue` -> `slot: green`). Traffic flips instantaneously with zero downtime.

---

## Architecture Flow

```
1. Active State:
   Traffic -> Service (selector: slot=blue) -> [Blue Pods (v1)] (LIVE)
                                               [Green Pods (v2)] (STANDBY)

2. Cutover State:
   Traffic -> Service (selector: slot=green) -> [Green Pods (v2)] (LIVE)
                                                [Blue Pods (v1)] (STANDBY / ROLLBACK TARGET)
```

---

## Step-by-Step Execution

```bash
# 1. Deploy Both Environments
kubectl apply -f 05-blue-green/deployment-blue.yaml
kubectl apply -f 05-blue-green/deployment-green.yaml
kubectl get pods -l app=myapp --show-labels

# 2. Direct Service to Blue (v1)
kubectl apply -f 05-blue-green/service-blue.yaml
kubectl get endpoints myapp-service
curl http://$(minikube ip):30020

# 3. Flip Traffic to Green (v2) Instantly
kubectl apply -f 05-blue-green/service-green.yaml
kubectl get endpoints myapp-service
curl http://$(minikube ip):30020

# 4. Instant Rollback to Blue (if needed)
kubectl apply -f 05-blue-green/service-blue.yaml
curl http://$(minikube ip):30020

# Cleanup
kubectl delete -f 05-blue-green/service-blue.yaml
kubectl delete -f 05-blue-green/deployment-blue.yaml
kubectl delete -f 05-blue-green/deployment-green.yaml
```
