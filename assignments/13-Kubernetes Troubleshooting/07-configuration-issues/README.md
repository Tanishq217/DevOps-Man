# Troubleshooting: Configuration Issues & CreateContainerConfigError

## 1. Problem Identification
When inspecting a newly deployed Pod, its status is stuck at `CreateContainerConfigError`:

```
NAME                READY   STATUS                       RESTARTS   AGE
config-issue-demo   0/1     CreateContainerConfigError   0          38s
```

`CreateContainerConfigError` indicates that the pod was successfully scheduled to a node, but the kubelet was unable to assemble the configuration (environment variables, ConfigMaps, Secrets, or Downward API fields) required to launch the container sandbox.

---

## 2. Investigation Steps

### Step 1: Inspect Pod Events and Container States
Run `kubectl describe pod` to identify the missing configuration reference:
```bash
kubectl describe pod config-issue-demo
```

Under `Containers -> api-server -> State`:
```
    State:          Waiting
      Reason:       CreateContainerConfigError
      Message:      configmap "app-database-config" not found
```

Under `Events:`:
```
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Normal   Scheduled  45s                default-scheduler  Successfully assigned default/config-issue-demo to minikube
  Warning  Failed     10s (x6 over 44s)  kubelet            Error: configmap "app-database-config" not found
```

### Step 2: Categorize Common Configuration Pitfalls
1. **Missing ConfigMap / Secret:** Pod references an object name that hasn't been created yet.
2. **Missing Key:** The ConfigMap exists, but the specified `key` does not exist inside its `data:` map.
3. **Namespace Mismatch:** The ConfigMap exists in `dev`, but the Pod is running in `production`.
4. **Non-Optional References:** By default, `configMapKeyRef` is strict (`optional: false`). If optional values are acceptable, specify `optional: true`.

---

## 3. Root Cause Analysis
The Pod definition attempted to bind an environment variable `DATABASE_HOST` using `valueFrom.configMapKeyRef` pointing to `app-database-config`. However, no ConfigMap with that name existed in the namespace.

---

## 4. Solution & Fix
Apply `configmap.yaml` to provision the expected configuration data:
```bash
kubectl apply -f configmap.yaml
```
*(Or apply `fixed-pod.yaml` which pairs the ConfigMap and the Pod specification together).*

Once the ConfigMap is present in the namespace, the kubelet detects the dependency automatically on the next reconciliation cycle and proceeds with container creation without needing manual intervention.

---

## 5. Verification
Verify that the pod immediately transitions from `CreateContainerConfigError` to `Running`:
```bash
kubectl get pods -l app=config-issue-demo
```
Output:
```
NAME                READY   STATUS    RESTARTS   AGE
config-issue-demo   1/1     Running   0          1m12s
```

Verify that the environment variable was successfully injected into the container:
```bash
kubectl exec config-issue-demo -- env | grep DATABASE
```
Output:
```
DATABASE_HOST=postgres-cluster.database.svc.cluster.local
DATABASE_PORT=5432
```
The configuration dependency is resolved!
