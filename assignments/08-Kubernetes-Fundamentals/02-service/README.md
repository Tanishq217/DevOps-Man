# Kubernetes Services — Networking & Service Discovery

## 1. Why Do We Need a Service?

In Kubernetes, Pods are ephemeral and mortal. Whenever a Pod crashes, gets deleted, or gets rescheduled on another node, it receives a **completely new internal IP address**.

If frontend containers or external clients attempted to connect directly to Pod IPs, every pod restart would break connectivity with `Connection refused`.

A **Service** provides an abstraction layer that solves this by giving you:
- **Stable Virtual IP (ClusterIP):** Remains unchanged throughout the Service's lifecycle.
- **Consistent DNS Record:** Resolvable inside the cluster (e.g. `nginx-service.default.svc.cluster.local`).
- **Automatic Layer 4 Load Balancing:** Uses `kube-proxy` (iptables or IPVS) to distribute traffic across all healthy Pods matching its label selector.

```
Client Traffic
      │
      ▼ http://nginx-service:80
+───────────────────────────────────────────────+
| Service: nginx-service                        |
| ClusterIP: 10.96.x.x                          |
| Port: 80                                      |
+───────────────────────────────────────────────+
         │                             │
         ▼                             ▼
+───────────────────────+     +───────────────────────+
| Pod 1 (10.244.0.15)   |     | Pod 2 (10.244.0.16)   |
| app=nginx             |     | app=nginx             |
| Container Port: 80    |     | Container Port: 80    |
+───────────────────────+     +───────────────────────+
```

---

## 2. Port Mapping Explained

Understanding ports in Kubernetes services can be confusing initially. Here is the distinction:

| Port Field | Component | Purpose | Example |
| :--- | :--- | :--- | :--- |
| `containerPort` | Pod Manifest | The port the containerized process listens on inside the container. | `80` |
| `targetPort` | Service Manifest | The port on the Pod to which the Service forwards incoming requests. Defaults to `port` if omitted. | `80` |
| `port` | Service Manifest | The virtual port exposed **internally** by the Service within the cluster. | `80` |
| `nodePort` | Service Manifest | A static port opened on **every cluster node's external IP** (range: `30000-32767`). | `30080` |

```
Client / Browser Request
          │
          ▼ http://<Node-IP>:30080        (nodePort on Node)
+──────────────────────────────────+
| Service (ClusterIP: 10.96.x.x)   |
| Virtual Port: 80                 |
+──────────────────────────────────+
          │
          ▼ forwards to targetPort: 80
+──────────────────────────────────+
| Pod Container                    |
| containerPort: 80                |
+──────────────────────────────────+
```

---

## 3. Kubernetes Service Types Overview

1. **ClusterIP (Default):**
   - Exposes the Service on an internal IP only reachable from within the cluster.
   - Ideal for backend services, internal APIs, and databases.
2. **NodePort:**
   - Exposes the Service on each Node's IP at a static port (`30000-32767`).
   - Forwards traffic to the internal ClusterIP.
   - Accessible from outside the cluster using `<NodeIP>:<NodePort>`.
3. **LoadBalancer:**
   - Builds on top of NodePort. Integrates with cloud providers (AWS, GCP, Azure) to provision an external cloud load balancer with a public IP.
4. **ExternalName:**
   - Maps the Service to a DNS CNAME record (external host outside the cluster) without proxying traffic.
5. **Headless Service (`clusterIP: None`):**
   - Does not allocate a virtual ClusterIP. Direct DNS queries return the list of individual Pod IPs (commonly used with StatefulSets).

---

## 4. Service Manifest (`nginx-service.yaml`)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  labels:
    app: nginx
spec:
  type: NodePort
  selector:
    app: nginx       # Matches Pods having the label 'app: nginx'
  ports:
    - name: http
      port: 80         # Internal Service port
      targetPort: 80   # Port on the target Pod
      nodePort: 30080  # Port opened on every cluster Node
      protocol: TCP
```

---

## 5. Lab Execution Steps

### Step 1: Ensure Target Pod is Running
```bash
kubectl apply -f 01-pod/nginx-pod.yaml
kubectl get pods -l app=nginx
```

### Step 2: Apply the Service Manifest
```bash
kubectl apply -f 02-service/nginx-service.yaml
```
**Output:**
```
service/nginx-service created
```

### Step 3: Inspect Service Details & Port Bindings
```bash
kubectl get svc nginx-service
kubectl describe svc nginx-service
```
**Output:**
```
NAME            TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
nginx-service   NodePort   10.108.180.201   <none>        80:30080/TCP   20s
```
> The syntax `80:30080/TCP` indicates that cluster internal port `80` maps to nodePort `30080`.

### Step 4: Verify Endpoints Association
```bash
kubectl get endpoints nginx-service
```
**Output:**
```
NAME            ENDPOINTS        AGE
nginx-service   10.244.0.15:80   45s
```
> If `ENDPOINTS` shows `<none>`, verify that your Service `selector` matches the Pod `labels` character-for-character.

### Step 5: Access the Application from Host Machine
For Minikube environments, access via NodePort:
```bash
# Obtain minikube ip and send curl request
curl http://$(minikube ip):30080

# Or let minikube generate the direct browser URL
minikube service nginx-service --url
```
You will receive the HTML response from Nginx:
```html
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
<h1>Welcome to nginx!</h1>
```

### Step 6: Test Internal DNS Resolution from Another Pod
To confirm the Service DNS name is resolvable internally by CoreDNS:
```bash
kubectl run curl-test --rm -it --image=curlimages/curl:8.5.0 --restart=Never -- \
  curl -s http://nginx-service.default.svc.cluster.local
```

### Step 7: Service Port-Forwarding (Alternative Debugging Route)
You can port-forward through the Service abstraction:
```bash
kubectl port-forward svc/nginx-service 8080:80
```
Open `http://localhost:8080` in your browser.

### Step 8: Scaling Limitations of Bare Pods
Attempt to scale a standalone Pod:
```bash
kubectl scale pod/nginx-pod --replicas=2
```
**Output:**
```
error: cannot scale a pod/nginx-pod
```
> **Explanation:** Standalone Pods are static objects. To achieve horizontal scaling, self-healing, rolling updates, and replication, Kubernetes uses higher-level controllers such as **ReplicaSets** and **Deployments**.

---

## 6. Cleanup Commands
```bash
kubectl delete -f 02-service/nginx-service.yaml
kubectl delete -f 01-pod/nginx-pod.yaml
```

---

## 7. Key Takeaways

1. **Services provide stable endpoints** for transient, mortal Pods.
2. **Endpoints are automatically maintained:** `kube-controller-manager` watches Pods and updates the Endpoints object when Pods come up or go down.
3. **NodePort enables external reachability** for development clusters without needing external cloud provider load balancers.
4. **Standalone Pods vs Deployments:** Bare Pods cannot scale dynamically; real-world systems always manage Pods with Deployments.
