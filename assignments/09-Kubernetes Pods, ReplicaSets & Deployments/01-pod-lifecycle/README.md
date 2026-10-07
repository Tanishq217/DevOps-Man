# Pod Lifecycle, Probes & Container States

## Overview

A Kubernetes Pod passes through distinct phases during its lifecycle:
1. **Pending:** Pod accepted by cluster, but one or more containers are not yet created or scheduled.
2. **Running:** Pod bound to a node, all containers created, and at least one container is currently running or in the process of starting.
3. **Succeeded:** All containers terminated successfully (exit code 0) and will not be restarted.
4. **Failed:** All containers terminated, with at least one container failing (non-zero exit code).
5. **Unknown:** State could not be obtained (usually due to node communication failure).

---

## Difference Between Pod Phases and Status Strings

| Reported Status | Pod Phase | What It Actually Means |
| :--- | :--- | :--- |
| `Running` | `Running` | Container process is active |
| `Completed` | `Succeeded` | Batch job finished with exit code 0 |
| `Error` | `Failed` | Process exited with non-zero status code |
| `CrashLoopBackOff` | `Running` | Container keeps crashing; kubelet adds exponential restart backoff |
| `ImagePullBackOff` | `Pending` | Container cannot pull image tag or registry credentials failed |
| `Terminating` | `Terminating` | Pod received `SIGTERM` and has `terminationGracePeriodSeconds` to drain |

---

## Probes: Startup vs Liveness vs Readiness

```
Container Created
       │
       ▼
[Startup Probe]  ──(Fails)──> Kubelet kills & restarts container (protects slow-starting apps)
       │ (Passes)
       ├────────────────────────────────────────┐
       ▼                                        ▼
[Liveness Probe]                        [Readiness Probe]
  Fails -> Restarts container             Fails -> Removes pod IP from Service Endpoints
  (Recovers from deadlocks)               (Stops sending incoming user traffic)
```

---

## Commands & Verification

```bash
# 1. Run live watch in Terminal 1
kubectl get pods -w

# 2. Test Running & Pending
kubectl apply -f 01-pod-lifecycle/01-running.yaml
kubectl apply -f 01-pod-lifecycle/02-pending.yaml
kubectl describe pod lifecycle-pending

# 3. Test Failure & CrashLoopBackOff
kubectl apply -f 01-pod-lifecycle/05-crashloopbackoff.yaml
kubectl logs lifecycle-crashloop
kubectl logs lifecycle-crashloop --previous

# 4. Test ImagePullBackOff
kubectl apply -f 01-pod-lifecycle/06-imagepullbackoff.yaml
kubectl describe pod lifecycle-image-error

# 5. Test Readiness & Liveness Probes
kubectl apply -f 01-pod-lifecycle/07-readiness.yaml
kubectl apply -f 01-pod-lifecycle/08-liveness.yaml
kubectl describe pod lifecycle-readiness
kubectl describe pod lifecycle-liveness

# 6. Test Multi-Container and Init Containers
kubectl apply -f 01-pod-lifecycle/10-init-container.yaml
kubectl apply -f 01-pod-lifecycle/11-multi-container.yaml
kubectl logs lifecycle-multi-container -c sidecar

# Cleanup
kubectl delete pod -l app=lifecycle-test
```
