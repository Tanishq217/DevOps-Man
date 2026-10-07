# 03 – LoadBalancer Service (Cloud VIP & Ingress Routing)

## 1. What is a LoadBalancer Service?

A `LoadBalancer` service is designed for production environments running on cloud platforms (AWS, GCP, Azure, DigitalOcean). It:
1. Creates an underlying `ClusterIP` service.
2. Allocates a `NodePort` on every cluster node.
3. Calls the cloud provider's API to provision an external cloud load balancer (e.g., AWS Network Load Balancer, Google Cloud Load Balancer) with a dedicated **public IP / DNS address**.

Traffic reaches the cloud load balancer, which distributes it across the worker nodes' `NodePort`s, which in turn routes to the backend Pods.

```
Internet Clients
       │
       ▼ Public Cloud IP (e.g. 35.200.x.x)
+───────────────────────────────────────────────+
| Cloud Load Balancer (AWS NLB / GCP LB)        |
+───────────────────────────────────────────────+
       │                                │
       ▼ Node 1 (30xxx)                 ▼ Node 2 (30xxx)
+──────────────────────+        +──────────────────────+
| Worker Node 1        |        | Worker Node 2        |
| kube-proxy           |        | kube-proxy           |
+──────────────────────+        +──────────────────────+
       │                                │
       └────────────────┬───────────────┘
                        ▼
           +─────────────────────────+
           | Target Pods (Port: 80)  |
           +─────────────────────────+
```

---

## 2. Minikube & The `minikube tunnel` Gotcha

On bare-metal or local Minikube installations, there is no cloud provider to provision an external load balancer. Therefore, `EXTERNAL-IP` will remain in a `<pending>` status indefinitely.

To simulate a cloud provider locally, Minikube provides the `minikube tunnel` command:
- It creates a network route to Services deployed with type `LoadBalancer`.
- It assigns a local IP (typically `127.0.0.1` or a private subnet IP) to `EXTERNAL-IP`.

---

## 3. Hands-on Execution Steps

### Step 1: Deploy Backend Application
```bash
kubectl apply -f 03-loadbalancer/app-deployment.yaml
kubectl get pods -l app=web-loadbalancer
```

### Step 2: Apply the LoadBalancer Service
```bash
kubectl apply -f 03-loadbalancer/service.yaml
kubectl get svc web-service-loadbalancer
```
**Initial Output:**
```
NAME                       TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
web-service-loadbalancer   LoadBalancer   10.108.95.210   <pending>     80:31234/TCP   10s
```

### Step 3: Run Minikube Tunnel (In a separate terminal or background)
```bash
# Run minikube tunnel (requires sudo password on macOS)
minikube tunnel
```

### Step 4: Verify External IP Allocation
```bash
kubectl get svc web-service-loadbalancer
```
**Output after tunnel:**
```
NAME                       TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)        AGE
web-service-loadbalancer   LoadBalancer   10.108.95.210   127.0.0.1       80:31234/TCP   1m
```

### Step 5: Test External Access
```bash
# Query via the allocated external IP
curl http://127.0.0.1:80
```
Open `http://127.0.0.1` in your browser to confirm Nginx is reachable.

---

## 4. Cleanup Commands
```bash
kubectl delete -f 03-loadbalancer/service.yaml
kubectl delete -f 03-loadbalancer/app-deployment.yaml
```
