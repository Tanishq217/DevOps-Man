# Kubernetes Pods — Hands-on Lab & Notes

## 1. What is a Pod?

In Kubernetes, a **Pod** is the smallest and simplest unit you can create and deploy. Rather than deploying a container directly onto a node, Kubernetes wraps one or more containers inside a Pod.

Containers inside the same Pod share:
- **Network namespace:** They share a single IP address and port space (they can communicate over `localhost`).
- **Storage volumes:** Any shared storage configured for the Pod is accessible to all containers in it.
- **Lifecycle:** They are scheduled, started, stopped, and destroyed together.

While multi-container Pods are useful for sidecar patterns (like logging agents or proxy sidecars), the standard practice in microservices is one container per Pod.

```
+-------------------------------------------------------+
| Pod: nginx-pod (IP: 10.244.0.x)                       |
|                                                       |
|  +-------------------------------------------------+  |
|  | Container: nginx-container                      |  |
|  | Image: nginx:1.25-alpine                        |  |
|  | Port: 80                                        |  |
|  +-------------------------------------------------+  |
+-------------------------------------------------------+
                           |
       Scheduled on worker node by kube-scheduler
       Managed and monitored by kubelet
```

---

## 2. Pod Lifecycle & States

When you submit a Pod manifest, it goes through several phases:

| Status / Phase | Meaning |
| :--- | :--- |
| `Pending` | Pod is accepted by the cluster, but one or more containers are not created yet (downloading images or waiting for scheduling). |
| `ContainerCreating` | Pod is assigned to a node; container runtime is pulling the image and setting up network/storage. |
| `Running` | Pod is bound to a node and all containers are created. At least one container is currently running or starting. |
| `Succeeded` | All containers in the Pod completed successfully and will not restart (common for Batch Jobs). |
| `Failed` | All containers in the Pod terminated, and at least one container failed (non-zero exit code). |
| `CrashLoopBackOff` | Container started, crashed, and Kubernetes is waiting before trying to restart it again. |
| `ImagePullBackOff` | Cluster failed to pull the container image (typo in image name, bad tag, or auth failure). |
| `Terminating` | Pod deletion requested; processes receive `SIGTERM`, wait for grace period, then `SIGKILL`. |

---

## 3. Pod Manifest Anatomy (`nginx-pod.yaml`)

```yaml
apiVersion: v1          # Core API group
kind: Pod               # Resource type
metadata:
  name: nginx-pod       # Unique name within the namespace
  labels:               # Key-value tags for discovery & grouping
    app: nginx
    tier: frontend
spec:
  containers:
    - name: nginx-container
      image: nginx:1.25-alpine
      ports:
        - containerPort: 80   # Informational port exposed by container process
      resources:
        requests:             # Minimum guaranteed resources for scheduling
          cpu: "50m"
          memory: "64Mi"
        limits:               # Maximum hard ceiling
          cpu: "200m"
          memory: "128Mi"
```

### Important YAML Details:
1. **Indentation:** Spaces only (strictly 2 spaces per level), no tabs allowed.
2. **Requests vs Limits:**
   - `requests`: The scheduler uses this to pick a node that has enough capacity.
   - `limits`: Enforced at runtime by cgroups. If memory goes over limit, the container is OOM-killed; if CPU goes over, it is throttled.

---

## 4. Labels vs Selectors

- **Labels:** Metadata tags you stick onto your objects (`app: nginx`, `tier: frontend`).
- **Selectors:** Queries used by Services, Deployments, and CLI queries to find objects matching specific labels (`app=nginx`).

```
Labels:    Attached to the Pod        -->  [nginx-pod: app=nginx, tier=frontend]
Selector:  Used by Service or Query   -->  "Give me all pods where app=nginx"
```

If a Service selector doesn't match the Pod labels exactly, the Service will have **no endpoints** and traffic fails.

---

## 5. Lab Execution Steps

### Step 1: Apply the Pod Manifest
```bash
kubectl apply -f 01-pod/nginx-pod.yaml
```
**Output:**
```
pod/nginx-pod created
```

### Step 2: Check Pod Status and Node Assignment
```bash
kubectl get pods
kubectl get pods -o wide
```
**Output:**
```
NAME        READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
nginx-pod   1/1     Running   0          30s   10.244.0.15   minikube   <none>           <none>
```

### Step 3: Inspect Detailed Pod Configuration & Events
```bash
kubectl describe pod nginx-pod
```
> Read the bottom `Events:` table first whenever debugging a Pod that fails to start or gets stuck in `Pending` / `CrashLoopBackOff`.

### Step 4: View Application Logs
```bash
kubectl logs nginx-pod
```
**Output:**
```
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Configuration complete; ready for start up
```

### Step 5: Execute Commands Inside the Container
```bash
kubectl exec -it nginx-pod -- sh
```
Inside the container shell:
```sh
hostname -i
id
exit
```

### Step 6: Query Pods Using Label Selectors
```bash
kubectl get pods -l app=nginx
kubectl get pods -l tier=frontend
kubectl get pods --show-labels
```

### Step 7: Access the Pod via Port-Forwarding (Local Debugging)
```bash
kubectl port-forward pod/nginx-pod 8080:80
```
Open `http://localhost:8080` in your web browser or run:
```bash
curl http://localhost:8080
```
> `kubectl port-forward` directly tunnels your workstation to the Pod network namespace. It's meant for local testing and debugging, not production traffic.

### Step 8: Observe Pod Ephemeral Nature (IP Replacement)
Pods are temporary objects. If a Pod is destroyed and recreated, it does not keep its previous IP address:
```bash
# Check current IP
kubectl get pod nginx-pod -o wide

# Delete and recreate
kubectl delete pod nginx-pod
kubectl apply -f 01-pod/nginx-pod.yaml

# Check new IP
kubectl get pod nginx-pod -o wide
```
Notice that the IP address changes! Because Pod IPs are dynamic and ephemeral, we never connect to individual Pod IPs directly. Instead, we use a **Service**.

---

## 6. Key Takeaways

1. **Pod is the unit of scheduling**, not a single container.
2. **Ephemeral IPs:** Pods are mortal. Never hardcode Pod IPs into applications or client configs.
3. **Labels & Selectors:** The backbone of Kubernetes decoupling. Services discover Pods through label matching.
4. **Requests vs Limits:** Essential for production cluster stability to avoid resource starvation and unpredictable evictions.
