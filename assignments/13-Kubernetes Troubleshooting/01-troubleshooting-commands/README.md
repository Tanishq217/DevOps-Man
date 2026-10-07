# Task 1: Essential Kubernetes Troubleshooting Commands

This module documents hands-on investigation workflows using primary Kubernetes inspection and diagnostics CLI commands.

---

## Command Reference & Usage Guide

### 1. `kubectl get`
Lists resources in the cluster and reports their high-level operational state.
- **Basic Usage:** `kubectl get pods`, `kubectl get nodes`, `kubectl get svc`
- **Detailed wide output (`-o wide`):** Displays IP addresses, node assignment, read status, and image details:
  ```bash
  kubectl get pods -o wide
  kubectl get nodes -o wide
  kubectl get svc -o wide
  ```
- **Label filtering:**
  ```bash
  kubectl get pods -l app=describe-demo --show-labels
  ```
- **Output formatting:**
  ```bash
  kubectl get pod describe-demo -o yaml
  kubectl get pod describe-demo -o jsonpath='{.status.podIP}'
  ```

---

### 2. `kubectl describe`
Provides exhaustive detailed runtime inspection of a specific resource, including:
- Metadata, labels, annotations.
- Container state (Running, Waiting, Terminated), exit codes, restart count.
- Resource requests, limits, environment variables, mounts.
- **Events Section:** Critical timeline showing scheduling decisions (`Scheduled`), image pulling (`Pulling`, `Pulled`), container creation (`Created`), container start (`Started`), and any errors (`FailedScheduling`, `BackOff`, `Failed`).

```bash
kubectl describe pod describe-demo
kubectl describe node minikube
```

---

### 3. `kubectl logs`
Streams standard output (stdout) and standard error (stderr) emitted by containerized processes.
- **Standard logs:**
  ```bash
  kubectl logs logs-demo
  ```
- **Follow log stream in real time (`-f`):**
  ```bash
  kubectl logs -f logs-demo
  ```
- **Inspect last N lines (`--tail`):**
  ```bash
  kubectl logs logs-demo --tail=10
  ```
- **Include timestamps (`--timestamps`):**
  ```bash
  kubectl logs logs-demo --timestamps
  ```
- **Inspect previously crashed container instance (`-p` / `--previous`):**
  ```bash
  kubectl logs broken-pod --previous
  ```
- **Multi-container pod targeting:**
  ```bash
  kubectl logs <pod-name> -c <container-name>
  ```

---

### 4. `kubectl exec`
Executes interactive shells or one-off diagnostic commands directly inside a running container namespace.
- **Interactive Shell Session:**
  ```bash
  kubectl exec -it exec-demo -- /bin/sh
  ```
- **In-container Diagnostics:**
  ```bash
  # Check active environment variables
  kubectl exec exec-demo -- env

  # Verify process table
  kubectl exec exec-demo -- ps aux

  # Test DNS / connectivity from container
  kubectl exec exec-demo -- ping -c 3 8.8.8.8
  ```

---

### 5. `kubectl events` & `kubectl get events`
Captures cluster-wide control plane and kubelet event records across namespaces.
- **Sort by most recent timestamp:**
  ```bash
  kubectl get events --sort-by='.lastTimestamp'
  ```
- **Filter warning and error events:**
  ```bash
  kubectl get events --field-selector type=Warning
  ```
- **Stream events live:**
  ```bash
  kubectl get events -w
  ```

---

### 6. `kubectl explain`
Interactive inline schema documentation and API reference directly inside the terminal without leaving the shell.
- **Inspect Pod Spec fields:**
  ```bash
  kubectl explain pod.spec
  ```
- **Drill down into container resource settings:**
  ```bash
  kubectl explain pod.spec.containers.resources
  ```
- **Inspect probe definitions recursively:**
  ```bash
  kubectl explain pod.spec.containers.livenessProbe --recursive
  ```

---

### 7. `kubectl top`
Queries the Metrics Server API (`metrics.k8s.io`) to report real-time CPU (millicores) and Memory (bytes) consumption.
- **Node-level utilization:**
  ```bash
  kubectl top nodes
  ```
- **Pod-level utilization:**
  ```bash
  kubectl top pods
  ```
- **Namespace-wide utilization:**
  ```bash
  kubectl top pods -A --sort-by=cpu
  ```

---

## Step-by-Step Hands-On Practice

1. **Deploy practice pods:**
   ```bash
   kubectl apply -f get-demo.yaml
   kubectl apply -f describe-demo.yaml
   kubectl apply -f logs-demo.yaml
   kubectl apply -f exec-demo.yaml
   kubectl apply -f events-demo.yaml
   ```

2. **Run inspections:**
   ```bash
   kubectl get pods -o wide
   kubectl describe pod describe-demo
   kubectl logs logs-demo --tail=10 --timestamps
   kubectl exec -it exec-demo -- env
   kubectl top pods
   kubectl get events --sort-by='.lastTimestamp'
   kubectl explain pod.spec.containers.resources
   ```

3. **Cleanup:**
   ```bash
   kubectl delete -f get-demo.yaml -f describe-demo.yaml -f logs-demo.yaml -f exec-demo.yaml -f events-demo.yaml
   ```
