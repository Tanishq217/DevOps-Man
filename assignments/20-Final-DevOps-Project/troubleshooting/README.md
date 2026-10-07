# Kubernetes Troubleshooting Challenges & Diagnostic Runbook

This runbook documents the four intentional failure scenarios engineered into the TaskBoard cloud environment, detailing the discovery process, command logs, root-cause analysis, and verified remediation.

---

## Scenario 1: CrashLoopBackOff

### 1. Problem Identification
When inspecting pods in the `taskboard` namespace:
```bash
kubectl get pods -n taskboard
```
**Output:**
```text
NAME                                         READY   STATUS             RESTARTS      AGE
taskboard-broken-crashloop-7b49cf566-x8m9p   0/1     CrashLoopBackOff   4 (35s ago)   2m10s
```

### 2. Investigation & Log Analysis
Check container termination logs:
```bash
kubectl logs taskboard-broken-crashloop-7b49cf566-x8m9p -n taskboard --previous
```
**Output:**
```text
Booting backend...
command terminated with exit code 1
```

Inspect pod lifecycle events:
```bash
kubectl describe pod taskboard-broken-crashloop-7b49cf566-x8m9p -n taskboard
```
**Key Events:**
```text
Last State:     Terminated
  Reason:       Error
  Exit Code:    1
Warning  BackOff  28s (x8 over 112s)  kubelet  Back-off restarting failed container backend
```

### 3. Root Cause
The container command was explicitly configured to execute `exit 1` immediately upon startup, causing the container process to die. The kubelet restart policy repeatedly attempted restarts with exponential backoff delay.

### 4. Remediation
Update the container command in the manifest to start the Uvicorn ASGI server:
```yaml
command: ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

### 5. Verification
Apply the fix and verify pod status:
```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl get pods -n taskboard -l app=taskboard-backend
```
**Result:** Pod transitions to `1/1 Running` with 0 restarts.

---

## Scenario 2: ImagePullBackOff / ErrImagePull

### 1. Problem Identification
```bash
kubectl get pods -n taskboard
```
**Output:**
```text
NAME                                     READY   STATUS              RESTARTS   AGE
taskboard-broken-image-5d9859f5f6-w2k8l   0/1     ImagePullBackOff    0          45s
```

### 2. Investigation & Log Analysis
```bash
kubectl describe pod taskboard-broken-image-5d9859f5f6-w2k8l -n taskboard
```
**Key Events:**
```text
Warning  Failed     32s (x2 over 48s)  kubelet  Failed to pull image "ghcr.io/tanishq217/taskboard-backend:v999.0-nonexistent-tag": rpc error: code = NotFound desc = failed to pull and unpack image ... manifest unknown
Warning  Failed     32s (x2 over 48s)  kubelet  Error: ErrImagePull
Normal   BackOff    18s (x3 over 47s)  kubelet  Back-off pulling image "ghcr.io/tanishq217/taskboard-backend:v999.0-nonexistent-tag"
Warning  Failed     18s (x3 over 47s)  kubelet  Error: ImagePullBackOff
```

### 3. Root Cause
The image reference specified a non-existent tag `v999.0-nonexistent-tag`. The container runtime failed registry manifest resolution on GitHub Container Registry (GHCR).

### 4. Remediation
Correct the image tag to reference the active release tag or `:latest`:
```yaml
containers:
  - name: backend
    image: ghcr.io/tanishq217/taskboard-backend:latest
```

### 5. Verification
```bash
kubectl set image deployment/taskboard-broken-image backend=ghcr.io/tanishq217/taskboard-backend:latest -n taskboard
kubectl rollout status deployment/taskboard-broken-image -n taskboard
```
**Result:** Image layers download successfully and pod enters `1/1 Running`.

---

## Scenario 3: Service Port & Selector Mismatch (Endpoints Empty)

### 1. Problem Identification
Requests sent to the backend service fail with `Connection refused` or `502 Bad Gateway`:
```bash
kubectl exec -it deploy/taskboard-frontend -n taskboard -- curl -v http://taskboard-broken-service:8000/health
```
**Output:**
```text
curl: (7) Failed to connect to taskboard-broken-service port 8000: Connection refused
```

### 2. Investigation & Log Analysis
Inspect the service endpoints list:
```bash
kubectl get endpoints taskboard-broken-service -n taskboard
```
**Output:**
```text
NAME                      ENDPOINTS   AGE
taskboard-broken-service  <none>      3m
```

Inspect service definition:
```bash
kubectl describe svc taskboard-broken-service -n taskboard
```
**Output:**
```text
Selector:   app=non-existent-backend-label
Port:       http 8000/TCP
TargetPort: 9090/TCP
Endpoints:  <none>
```

### 3. Root Cause
Two critical configuration defects:
1. **Label Selector Mismatch**: The service selector looked for `app=non-existent-backend-label`, matching 0 pods in the cluster.
2. **TargetPort Mismatch**: `targetPort` was set to `9090`, whereas FastAPI listens on port `8000`.

### 4. Remediation
Patch both the selector and targetPort:
```bash
kubectl patch svc taskboard-broken-service -n taskboard --type='json' -p='[
  {"op": "replace", "path": "/spec/selector/app", "value": "taskboard-backend"},
  {"op": "replace", "path": "/spec/ports/0/targetPort", "value": 8000}
]'
```

### 5. Verification
```bash
kubectl get endpoints taskboard-broken-service -n taskboard
```
**Result:** Endpoints populated with backend pod IPs (`10.244.0.15:8000, 10.244.0.16:8000`). Curl returns `{"status":"UP"}`.

---

## Scenario 4: Readiness Probe Failure (0/1 Ready)

### 1. Problem Identification
The pod is in `Running` state, but `READY` column stays `0/1`:
```bash
kubectl get pods -n taskboard -l app=taskboard-broken-probe
```
**Output:**
```text
NAME                                      READY   STATUS    RESTARTS   AGE
taskboard-broken-probe-6dfb4c7987-9k3lp   0/1     Running   0          2m45s
```

### 2. Investigation & Log Analysis
```bash
kubectl describe pod taskboard-broken-probe-6dfb4c7987-9k3lp -n taskboard
```
**Key Events:**
```text
Warning  Unhealthy  4s (x18 over 85s)  kubelet  Readiness probe failed: HTTP probe failed with statuscode: 404
```

### 3. Root Cause
The readiness probe was pointing to `/api/invalid-non-existent-probe-endpoint`. The FastAPI application returned HTTP 404 Not Found, preventing the kubelet from marking the container as Ready.

### 4. Remediation
Update probe path in the manifest:
```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
```

### 5. Verification
```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl get pods -n taskboard
```
**Result:** Readiness probe succeeds with HTTP 200 and pod transitions to `1/1 Ready`.
