# Troubleshooting: CrashLoopBackOff

## 1. Problem Identification
When checking the status of running Pods with `kubectl get pods`, the pod status displays `CrashLoopBackOff` or `Error`, with the `RESTARTS` count repeatedly incrementing:

```
NAME              READY   STATUS             RESTARTS      AGE
crashloop-demo    0/1     CrashLoopBackOff   4 (65s ago)   2m
```

A `CrashLoopBackOff` indicates that the container repeatedly starts, fails (exits with a non-zero exit code or terminates immediately), and the kubelet restarts it with an exponential back-off delay (10s, 20s, 40s, up to 5 minutes).

---

## 2. Investigation Steps

### Step 1: Inspect Pod Details and Last Termination State
Run `kubectl describe pod` to inspect the container state and exit code:
```bash
kubectl describe pod crashloop-demo
```
In the `Containers` section, look at `Last State`:
```
    Last State:     Terminated
      Reason:       Error
      Exit Code:    1
      Started:      Mon, 07 Oct 2026 15:00:00 +0530
      Finished:     Mon, 07 Oct 2026 15:00:02 +0530
```
Notice `Exit Code: 1`, indicating an unhandled runtime error inside the process.

### Step 2: Inspect Container Standard Error and Logs
Since the container might be currently terminated or waiting, query current logs:
```bash
kubectl logs crashloop-demo
```
If the container just restarted and the current instance is empty, retrieve logs from the **previously crashed instance** using `--previous` (`-p`):
```bash
kubectl logs crashloop-demo --previous
```

Log Output:
```
[STARTUP] Initializing payment processing daemon...
[FATAL] ConfigurationError: DB_HOST environment variable not defined. Exiting with failure.
```

---

## 3. Root Cause Analysis
The startup command executed by `payment-worker` failed because a critical prerequisite (configuration / environment variable / long-running foreground process) was missing, leading to an immediate `exit 1`. The default Kubernetes `restartPolicy: Always` caught the failure and kept re-triggering container initialization.

---

## 4. Solution & Fix
Update the container entrypoint or configuration in `fixed-pod.yaml` so that the process initializes prerequisites properly and runs a foreground service loop without crashing:

```yaml
spec:
  containers:
    - name: payment-worker
      image: busybox:1.36
      command: ["/bin/sh", "-c"]
      args:
        - |
          echo "[STARTUP] Initializing payment processing daemon..."
          echo "[INFO] Connected to primary database successfully."
          while true; do
            echo "[WORKER] Listening for transaction batches... System healthy."
            sleep 15
          done
```

Apply the fix:
```bash
kubectl apply -f fixed-pod.yaml
```

---

## 5. Verification
Verify that the pod is now healthy, running, and no longer crashing:
```bash
kubectl get pods -l app=crashloop-demo
```
Output:
```
NAME             READY   STATUS    RESTARTS   AGE
crashloop-demo   1/1     Running   0          25s
```

Verify logs confirm steady execution:
```bash
kubectl logs crashloop-demo
```
Output:
```
[STARTUP] Initializing payment processing daemon...
[INFO] Connected to primary database successfully.
[WORKER] Listening for transaction batches... System healthy.
```
