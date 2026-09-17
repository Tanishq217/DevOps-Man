# 02 – NodePort Service (External Node-Level Access)

## 1. What is a NodePort Service?

A `NodePort` service builds directly on top of `ClusterIP`. When you declare `type: NodePort`, Kubernetes:
1. Allocates an internal `ClusterIP` address.
2. Allocates a dedicated port from the reserved range **`30000–32767`** (e.g. `30080`).
3. Opens this port on **every single worker node** across the entire cluster.

Any incoming traffic sent to `<Any-Worker-Node-IP>:<NodePort>` is received by `kube-proxy` on that node and forwarded to the Service's backend Pods, regardless of which node the actual Pod is running on!

```
External User / Browser
          │
          │ Hits: http://<Minikube-Node-IP>:30080
          ▼
+───────────────────────────────────────────────────+
| Minikube Node (IP: 192.168.49.2)                  |
| Opened Port: 30080                                |
|                                                   |
| Forwarded to Service VIP: 10.96.x.x (Port: 80)    |
+───────────────────────────────────────────────────+
                          │
          Forwarded to targetPort 80 on Pod
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
+────────────────────────+ +────────────────────────+
| Pod 1 (10.244.0.31:80) | | Pod 2 (10.244.0.32:80) |
+────────────────────────+ +────────────────────────+
```

---

## 2. Port Nomenclature Breakdown

- **`nodePort: 30080`**: Exposed on the host node IP.
- **`port: 80`**: The virtual port exposed inside the cluster.
- **`targetPort: 80`**: The port on the container inside the Pod receiving traffic.
- **`containerPort: 80`**: Informational declaration in the Pod template.

---

## 3. Hands-on Execution Steps

### Step 1: Deploy Backend Application
```bash
kubectl apply -f 02-nodeport/app-deployment.yaml
kubectl get deployments -l app=web-nodeport
kubectl get pods -l app=web-nodeport -o wide
```

### Step 2: Apply the NodePort Service
```bash
kubectl apply -f 02-nodeport/service.yaml
kubectl get svc web-service-nodeport
```
**Expected Output:**
```
NAME                   TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
web-service-nodeport   NodePort   10.105.120.45    <none>        80:30080/TCP   10s
```

### Step 3: Inspect Endpoints
```bash
kubectl get endpoints web-service-nodeport
```

### Step 4: Access Application from Host Terminal
```bash
# Query Minikube Node IP directly on port 30080
curl http://$(minikube ip):30080
```
**Expected Output:**
```html
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
<h1>Welcome to nginx!</h1>
```

### Step 5: Launch & Access in Web Browser
```bash
# Open directly in browser via Minikube helper
minikube service web-service-nodeport
# Or print the direct browser URL:
minikube service web-service-nodeport --url
```

---

## 4. Cleanup Commands
```bash
kubectl delete -f 02-nodeport/service.yaml
kubectl delete -f 02-nodeport/app-deployment.yaml
```
