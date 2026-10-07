# Kubernetes Services — Master Architecture & Comparison Guide

## 1. Master Comparison Table

| Feature / Criteria | 1. ClusterIP | 2. NodePort | 3. LoadBalancer | 4. ExternalName | 5. Headless (`None`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Default Type?** | Yes | No | No | No | No (`clusterIP: None`) |
| **ClusterIP Allocated?** | Yes (Virtual Private IP) | Yes (Underlying VIP) | Yes (Underlying VIP) | No | No (Explicitly disabled) |
| **External Access?** | No (Cluster-internal only) | Yes (via `<NodeIP>:<NodePort>`) | Yes (Public Cloud Load Balancer IP) | N/A (Redirects to outside FQDN) | No (Direct Pod-to-Pod) |
| **Port Range** | 1–65535 | 30000–32767 on all nodes | Any standard port (80, 443) | Uses external target port | Any valid port |
| **DNS Record Created** | Single `A` record pointing to VIP | Single `A` record pointing to VIP | Single `A` record pointing to VIP | `CNAME` record pointing to external FQDN | Multiple `A` records (one per Pod IP) |
| **Cloud Provider Required?**| No | No | Yes (AWS, GCP, Azure) | No | No |
| **Load Balancing Mode** | Layer 4 via `kube-proxy` | Layer 4 via `kube-proxy` | Cloud LB + `kube-proxy` | Handled by DNS client | Client-side load balancing |
| **Manages Endpoints?** | Yes | Yes | Yes | No (DNS alias only) | Yes (Direct Pod IPs) |
| **Primary Use Case** | Internal microservices & databases | Development, bare-metal access | Exposing web services in cloud | Accessing external RDS / APIs | StatefulSets (Kafka, Mongo, DB clusters) |

---

## 2. The 4 Ports Explained

```
External User / Browser
          │
          │ Hits: http://<NodeIP>:30080
          ▼
   [ nodePort: 30080 ]        <- Port on the Worker Node (30000-32767)
          │
          │ Forwarded to:
          ▼
   [ port: 80 ]               <- Port exposed by the Service object internally
          │
          │ Forwarded to:
          ▼
   [ targetPort: 80 ]         <- Port receiving traffic on the target container
          │
          ▼
   [ containerPort: 80 ]      <- Port declared in the container spec
```

---

## 3. How `kube-proxy` Works Under the Hood

Kubernetes Services are not physical processes or software daemons running on every node. Instead, a Service's `ClusterIP` is a **virtual IP address**.

When you send a packet to `10.96.150.45:80`:
1. `kube-proxy` watches the Kubernetes API for Service and Endpoints changes.
2. In **iptables mode** (default), `kube-proxy` writes deterministic Linux packet-filtering rules. When a packet targets the Service VIP, iptables rewrites the destination IP (DNAT) to one of the healthy Pod IPs selected randomly or round-robin.
3. In **IPVS mode** (high-performance clusters), `kube-proxy` uses Linux IP Virtual Server kernel hashing, which scales efficiently beyond thousands of services.

---

## 4. Services Without Selectors (Manual Endpoints)

If you omit the `selector` block from a Service manifest, Kubernetes creates the Service **without creating Endpoints automatically**.

You can then manually create an `Endpoints` object pointing to external physical servers or legacy databases outside Kubernetes:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: legacy-database
spec:
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432
---
apiVersion: v1
kind: Endpoints
metadata:
  name: legacy-database
subsets:
  - addresses:
      - ip: 192.168.1.100    # External database IP outside Kubernetes
    ports:
      - port: 5432
```

---

## 5. Decision Tree: Which Service Should You Pick?

- **Do you need to access an external database or third-party domain using a clean DNS name?**  
  👉 Use **ExternalName**.
- **Are you deploying a clustered database (Kafka, Cassandra, MongoDB) where nodes need individual identities?**  
  👉 Use **Headless (`clusterIP: None`)**.
- **Does this service communicate only with other pods inside the cluster?**  
  👉 Use **ClusterIP**.
- **Do you need external browser access on a local Minikube or on-prem cluster without a cloud provider?**  
  👉 Use **NodePort**.
- **Are you running on a managed cloud platform (AWS, GCP, Azure) and need a dedicated public IP?**  
  👉 Use **LoadBalancer**.
