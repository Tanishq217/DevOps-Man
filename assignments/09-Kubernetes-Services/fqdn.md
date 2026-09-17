# Kubernetes FQDN & CoreDNS Reference Guide

## 1. What is an FQDN?

**FQDN** stands for **Fully Qualified Domain Name**. It is the absolute, unambiguous address of a resource on a network.

### Analogy:
- If you are in the same room as your friend Rahul, saying *"Hey Rahul"* (**Short Name**) works because everyone in the room knows who you are addressing.
- If you send postal mail to Rahul from another country, writing *"Rahul"* fails. You must provide the full address: `Rahul, Flat 402, Sunshine Heights, Mumbai, Maharashtra, India` (**FQDN**).

In Kubernetes:
- **Same Namespace:** Pods can communicate using the short name (`web-service`).
- **Cross-Namespace:** Pods must communicate using the FQDN (`web-service.production.svc.cluster.local`).

---

## 2. Anatomy of a Kubernetes FQDN

Every Kubernetes Service automatically gets an FQDN structured as follows:

```
  web-service-clusterip .   default   .   svc   .  cluster.local
  └──────────┬──────────┘  └────┬────┘  └──┬──┘  └──────┬──────┘
             │                  │          │            │
        Service Name        Namespace   Resource  Cluster Domain
```

| Component | Meaning | Example |
| :--- | :--- | :--- |
| **Service Name** | Name declared in `metadata.name` | `web-service-clusterip` |
| **Namespace** | The namespace where the Service resides | `default`, `prod`, `dev` |
| **Resource** | Identifies the object type | `svc` for Services |
| **Cluster Domain** | Base domain of the cluster | `cluster.local` (default) |

---

## 3. What is CoreDNS?

**CoreDNS** is the authoritative DNS server running inside the `kube-system` namespace. It watches the Kubernetes API server for Service and Pod creations, updates, and deletions, dynamically maintaining internal DNS records.

```bash
# Verify CoreDNS pods running in the cluster:
kubectl get pods -n kube-system -l k8s-app=kube-dns
```

---

## 4. Inside a Pod: How `/etc/resolv.conf` Works

When a Pod is scheduled, the Kubelet automatically populates its `/etc/resolv.conf` file:

```text
nameserver 10.96.0.10
search default.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

### Explanation of Search Domains:
If a Pod runs `curl http://backend`:
1. CoreDNS appends `default.svc.cluster.local` -> queries `backend.default.svc.cluster.local`.
2. If found, it resolves immediately!
3. If not found, it tries `backend.svc.cluster.local`, then `backend.cluster.local`.

---

## 5. FQDN for Services vs StatefulSet Pods

| Resource | FQDN Format | Resolves To |
| :--- | :--- | :--- |
| **Service (ClusterIP)** | `<service>.<namespace>.svc.cluster.local` | Single virtual ClusterIP |
| **Service (Headless)** | `<service>.<namespace>.svc.cluster.local` | Multiple A records (all Pod IPs) |
| **StatefulSet Pod** | `<pod-name>.<service>.<namespace>.svc.cluster.local` | Direct specific Pod IP |

---

## 6. How to Test & Debug DNS in Your Cluster

```bash
# Run a temporary curl client
kubectl run curl-test --rm -it --image=curlimages/curl:8.5.0 --restart=Never -- sh

# Perform nslookup on a service
nslookup web-service-clusterip
nslookup web-service-clusterip.default.svc.cluster.local

# View the pod's DNS configuration
cat /etc/resolv.conf
exit
```
