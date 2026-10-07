# 05 – Headless Service (Direct Pod-to-Pod Discovery & StatefulSets)

## 1. What is a Headless Service?

A **Headless Service** is defined by explicitly setting:
```yaml
spec:
  clusterIP: None
```

When `clusterIP: None` is specified:
1. Kubernetes **does not allocate a virtual IP (VIP)**.
2. `kube-proxy` does not configure any iptables/IPVS rules or perform Layer 4 load balancing.
3. Instead, when a client queries CoreDNS for the Service name, CoreDNS returns **the individual IP addresses of all healthy matching Pods** (multiple DNS `A` records).

```
Client Pod (curl-client-headless)
    │
    │ DNS Query: "Where is web-headless?"
    ▼
+───────────────────────────────────────────────────────────+
| CoreDNS                                                   |
| Returns individual Pod IPs directly (no virtual VIP):     |
| - 10.244.0.41                                             |
| - 10.244.0.42                                             |
| - 10.244.0.43                                             |
+───────────────────────────────────────────────────────────+
    │
    │ Client decides which specific Pod to connect to
    ▼
[ web-stateful-0 ]   [ web-stateful-1 ]   [ web-stateful-2 ]
```

---

## 2. StatefulSets & Unique Pod FQDNs

When paired with a **StatefulSet**, a Headless Service assigns each individual Pod a predictable, stable DNS hostname:

```
<pod-name>.<service-name>.<namespace>.svc.cluster.local
```

For example:
- `web-stateful-0.web-headless.default.svc.cluster.local`
- `web-stateful-1.web-headless.default.svc.cluster.local`
- `web-stateful-2.web-headless.default.svc.cluster.local`

### Why is this essential for stateful systems?
In distributed databases (like Apache Kafka, MongoDB Replica Sets, Cassandra, and ZooKeeper), nodes must communicate with specific peers (e.g. Master vs Read Replica). Random load balancing through a standard ClusterIP would corrupt database clustering.

---

## 3. Hands-on Execution Steps

### Step 1: Deploy StatefulSet, Headless Service, and Client
```bash
kubectl apply -f 05-headless/service.yaml
kubectl apply -f 05-headless/app-statefulset.yaml
kubectl apply -f 05-headless/client-pod.yaml

# Wait for StatefulSet pods to transition to Running
kubectl get pods -l app=web-headless -o wide
```

### Step 2: Inspect the Headless Service
```bash
kubectl get svc web-headless
```
**Expected Output:**
```
NAME           TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
web-headless   ClusterIP   None         <none>        80/TCP    20s
```
Notice `CLUSTER-IP` is explicitly `None`.

### Step 3: Query DNS for the Service Name (Multiple A Records)
```bash
kubectl exec -it curl-client-headless -- nslookup web-headless
```
**Expected Output:**
```
Server:    10.96.0.10
Address:   10.96.0.10#53

Name:      web-headless.default.svc.cluster.local
Address:   10.244.0.41
Name:      web-headless.default.svc.cluster.local
Address:   10.244.0.42
Name:      web-headless.default.svc.cluster.local
Address:   10.244.0.43
```
Unlike ClusterIP which returns a single virtual IP, the Headless Service returns the exact Pod IPs!

### Step 4: Resolve an Individual StatefulSet Pod by DNS
```bash
kubectl exec -it curl-client-headless -- nslookup web-stateful-0.web-headless.default.svc.cluster.local
```
**Expected Output:**
```
Name:      web-stateful-0.web-headless.default.svc.cluster.local
Address:   10.244.0.41
```

---

## 4. Cleanup Commands
```bash
kubectl delete -f 05-headless/service.yaml
kubectl delete -f 05-headless/app-statefulset.yaml
kubectl delete -f 05-headless/client-pod.yaml
```
