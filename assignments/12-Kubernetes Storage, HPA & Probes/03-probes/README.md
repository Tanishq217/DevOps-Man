# Kubernetes Probes: Liveness, Readiness & Startup

## Overview

Kubernetes container health monitoring uses three specialized probes to ensure application reliability and prevent traffic routing to impaired or initializing workloads.

```
Container Initializing
         │
         ▼
[ Startup Probe ]  ──(Fails)──> Restarts container (protects slow-starting services)
         │ (Passes)
         ├────────────────────────────────────────┐
         ▼                                        ▼
[ Liveness Probe ]                       [ Readiness Probe ]
  Fails -> Kubelet restarts container      Fails -> Drops Pod IP from Service Endpoints
  (Recovers from deadlocks & hangs)        (Stops routing incoming user traffic)
```

---

## 1. Probe Comparison Matrix

| Probe | Core Question | Action on Failure | Typical Failure Scenario |
| :--- | :--- | :--- | :--- |
| **Startup** | *Has the application finished initialization?* | Kubelet kills and restarts the container | Heavy JVM warmups, cache pre-warming, migrations |
| **Readiness** | *Can this Pod accept incoming network traffic right now?* | Kubelet removes Pod IP from Service Endpoints (does NOT restart) | High queue saturation, database temporarily unreachable |
| **Liveness** | *Is the application still alive and healthy?* | Kubelet kills and restarts the container | Deadlocks, memory leaks, fatal unhandled event loops |

---

## 2. Probe Mechanisms

1. **`httpGet`**: Sends an HTTP GET request to a specific path/port. Responses with status codes $200 \le \text{code} < 400$ are considered successful.
2. **`tcpSocket`**: Attempts to open a TCP socket connection to a specific container port.
3. **`exec`**: Runs a specified shell command inside the container. Exit status code `0` is considered healthy.
4. **`grpc`**: Performs a gRPC health check endpoint test.

---

## 3. Hands-on Execution & Verification

### A. Readiness Probe (`readiness.yaml`)
```bash
kubectl apply -f 03-probes/readiness.yaml
kubectl get pod readiness-demo

# Expose as a service
kubectl expose pod readiness-demo --name=readiness-svc --port=80
kubectl get endpoints readiness-svc
```
> The pod's IP is registered in `readiness-svc` endpoints only after the probe passes.

### B. Liveness Probe (`liveness.yaml`)
```bash
kubectl apply -f 03-probes/liveness.yaml
kubectl get pod liveness-demo -w
```
> The pod creates `/tmp/healthy`, sleeps 20s, and deletes it. Watch the `RESTARTS` count increment from `0` to `1` as Kubelet restarts the container.

### C. Startup Probe (`startup.yaml`)
```bash
kubectl apply -f 03-probes/startup.yaml
kubectl describe pod startup-demo | grep -A 8 "Startup:"
```

---

## Cleanup
```bash
kubectl delete pod readiness-demo liveness-demo startup-demo --ignore-not-found=true
kubectl delete svc readiness-svc --ignore-not-found=true
```
