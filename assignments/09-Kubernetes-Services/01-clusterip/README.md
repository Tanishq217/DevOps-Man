# 01 – ClusterIP Service (Internal Microservice Communication)

## 1. What is a ClusterIP Service?

`ClusterIP` is the **default service type** in Kubernetes. If you create a Service without specifying `spec.type`, Kubernetes defaults to `ClusterIP`.

When created, Kubernetes allocates a stable, virtual IP address (VIP) from an internal cluster subnet (e.g. `10.96.0.0/12`). This virtual IP exists purely in software and is reachable **only from inside the cluster**. It is not directly accessible from your host machine or public internet without port-forwarding or an ingress layer.

```
                  +───────────────────────────────+
                  |     Client Pod (curl-client)  |
                  +───────────────────────────────+
                                  │
                  http://web-service-clusterip:80
                                  ▼
                  +───────────────────────────────+
                  |  ClusterIP Service            |
                  |  VIP: 10.96.x.x (Port: 80)    |
                  +───────────────────────────────+
                                  │
                   Load balanced via kube-proxy
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
+─────────────────+      +─────────────────+      +─────────────────+
| Pod 1           |      | Pod 2           |      | Pod 3           |
| (10.244.0.21)   |      | (10.244.0.22)   |      | (10.244.0.23)   |
| app: web-cl...  |      | app: web-cl...  |      | app: web-cl...  |
+─────────────────+      +─────────────────+      +─────────────────+
```

---

## 2. Why Do We Need It?

1. **Pod IPs are Ephemeral:** Whenever a Pod restarts or dies, it gets a completely new IP address. A Service acts as a static gateway with an unchanging virtual IP and DNS name.
2. **Layer 4 Load Balancing:** Automatically balances incoming TCP/UDP connections across all healthy Pods listed in its `Endpoints` object.
3. **Internal Service Discovery:** CoreDNS automatically maps `web-service-clusterip` to its assigned ClusterIP.

---

## 3. Hands-on Execution Steps

### Step 1: Deploy the Backend App (3 Replicas)
```bash
kubectl apply -f 01-clusterip/app-deployment.yaml
kubectl get deployments -l app=web-clusterip
kubectl get pods -l app=web-clusterip -o wide
```

### Step 2: Deploy the ClusterIP Service
```bash
kubectl apply -f 01-clusterip/service.yaml
kubectl get svc web-service-clusterip
```

### Step 3: Inspect Endpoints Association
```bash
kubectl get endpoints web-service-clusterip
kubectl describe svc web-service-clusterip
```
You should see all 3 Pod IPs listed under `Endpoints: 10.244.0.x:80,10.244.0.y:80,10.244.0.z:80`.

### Step 4: Deploy the Curl Client Pod
```bash
kubectl apply -f 01-clusterip/client-pod.yaml
kubectl get pod curl-client
```

### Step 5: Test Connectivity from Within the Cluster
```bash
# Query the service using its short service name
kubectl exec -it curl-client -- curl -s http://web-service-clusterip:80

# Query using full FQDN
kubectl exec -it curl-client -- curl -s http://web-service-clusterip.default.svc.cluster.local:80
```
**Expected Output:**
HTML output containing `<h1>Welcome to nginx!</h1>`.

### Step 6: Verify CoreDNS Name Resolution
```bash
kubectl exec -it curl-client -- nslookup web-service-clusterip
```
**Expected Output:**
```
Server:    10.96.0.10
Address:   10.96.0.10#53

Name:      web-service-clusterip.default.svc.cluster.local
Address:   10.96.x.x
```
CoreDNS returns the single stable ClusterIP virtual address.

---

## 4. Cleanup Commands
```bash
kubectl delete -f 01-clusterip/service.yaml
kubectl delete -f 01-clusterip/client-pod.yaml
kubectl delete -f 01-clusterip/app-deployment.yaml
```
