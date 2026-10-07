# Kubernetes Volumes & Storage Architecture

## Overview

In Kubernetes, containers are ephemeral by default. When a container crashes, Kubelet restarts it with a fresh filesystem, wiping any unpersisted runtime data. Moreover, if a Pod is rescheduled to another node or deleted, the container filesystem is permanently destroyed.

Kubernetes solves this with **Volumes**—abstractions that decouple storage lifecycles from container and Pod lifecycles.

```
Container (ephemeral)
       │
       ▼ writes data
[ Volume Mount: /data ]
       │
       ▼ backed by
[ Storage Backend: emptyDir / hostPath / PersistentVolume / Cloud Disk ]
```

---

## 1. `emptyDir`

### What is `emptyDir`?
An `emptyDir` volume is created when a Pod is assigned to a node. It exists as long as that Pod runs on that node. As the name says, it is initially empty. All containers in the same Pod can read and write the same files in the `emptyDir` volume (even if mounted at different container paths).

### Key Characteristics:
- **Lifetime tied to Pod:** If a container crashes, the `emptyDir` data **survives** the container restart. But if the **Pod** is deleted or evicted, the data in `emptyDir` is **permanently deleted**.
- **Storage media:** By default, it uses node disk space, but setting `emptyDir.medium: Memory` mounts a tmpfs (RAM-backed, fast, but consumes pod memory limit).

### Real-World Use Cases:
1. **Shared scratch space:** Multi-container pods where one container downloads or extracts files and a sidecar serves or compresses them.
2. **Temporary cache:** Fast in-memory caching or sorting buffers for batch processing jobs.
3. **Checkpointing:** Long computation jobs saving intermediate state against container crashes.

### Practical Example: `emptydir-pod.yaml`
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: emptydir-demo
spec:
  containers:
    - name: app
      image: nginx:1.27
      volumeMounts:
        - name: app-storage
          mountPath: /data
  volumes:
    - name: app-storage
      emptyDir: {}
```

### Hands-on Verification:
```bash
# 1. Apply the Pod
kubectl apply -f 01-kubernetes-volumes/emptydir-pod.yaml
kubectl wait --for=condition=Ready pod/emptydir-demo --timeout=60s

# 2. Write a file inside the container
kubectl exec -it emptydir-demo -- sh -c 'echo "Persisting data in emptyDir" > /data/test.txt'

# 3. Read the file
kubectl exec emptydir-demo -- cat /data/test.txt
# Output: Persisting data in emptyDir

# 4. Delete the pod and recreate it
kubectl delete pod emptydir-demo
kubectl apply -f 01-kubernetes-volumes/emptydir-pod.yaml
kubectl wait --for=condition=Ready pod/emptydir-demo --timeout=60s

# 5. Check if file survived
kubectl exec emptydir-demo -- cat /data/test.txt
# Output: cat: /data/test.txt: No such file or directory
```
> **Finding:** Data is lost when the Pod is deleted. `emptyDir` is strictly ephemeral storage tied to Pod lifespan.

---

## 2. `hostPath`

### What is `hostPath`?
A `hostPath` volume mounts a specific file or directory from the host worker node's filesystem directly into the container.

### Key Characteristics:
- **Node-dependent:** Data stays on the node where the pod was running. If the Pod is rescheduled to a *different* node, it sees that node's filesystem instead!
- **Security risk:** Pods can potentially inspect or modify sensitive host node files (`/var/run/docker.sock`, `/etc/`, `/var/log`).
- **Good for single-node / local testing:** Works smoothly on Minikube or Docker Desktop, but unsuitable for multi-node stateful production apps.

### Real-World Use Cases:
1. **Host monitoring agents:** Running DaemonSets (like cAdvisor, Fluentd, or Node Exporter) that need access to host metrics or `/var/log/pods`.
2. **Container runtime integration:** Accessing container engine sockets like `/var/run/dockershim.sock` or `/run/containerd/containerd.sock`.
3. **Local development & debugging:** Testing persistent volume interactions on single-node clusters without cloud block storage.

### Practical Example: `hostpath-pod.yaml`
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hostpath-demo
spec:
  containers:
    - name: app
      image: nginx:1.27
      volumeMounts:
        - name: host-storage
          mountPath: /data
  volumes:
    - name: host-storage
      hostPath:
        path: /tmp/hostpath-data
        type: DirectoryOrCreate
```

### Hands-on Verification:
```bash
# 1. Apply hostPath Pod
kubectl apply -f 01-kubernetes-volumes/hostpath-pod.yaml
kubectl wait --for=condition=Ready pod/hostpath-demo --timeout=60s

# 2. Write data from inside the Pod
kubectl exec -it hostpath-demo -- sh -c 'echo "Written from Pod to Node" > /data/node-shared.txt'

# 3. Delete and recreate the Pod
kubectl delete pod hostpath-demo
kubectl apply -f 01-kubernetes-volumes/hostpath-pod.yaml
kubectl wait --for=condition=Ready pod/hostpath-demo --timeout=60s

# 4. Check if file survived
kubectl exec hostpath-demo -- cat /data/node-shared.txt
# Output: Written from Pod to Node
```
> **Finding:** Data survived because it was written directly onto the host node filesystem at `/tmp/hostpath-data`.

---

## 3. PersistentVolume (PV)

### What is a PersistentVolume?
A `PersistentVolume` (PV) is a piece of storage in the cluster that has been provisioned by an administrator or dynamically provisioned using Storage Classes. It is a cluster-level resource (non-namespaced) just like a Node.

### PV Lifecycle & Reclaim Policies:
- **`Retain`**: When the claim is deleted, the PV remains intact with its data, allowing an admin to manually recover or archive the data.
- **`Delete`**: When the claim is deleted, the underlying storage asset (e.g. AWS EBS, GCP PD) is automatically deleted.
- **`Recycle`** (deprecated): Performs basic scrub (`rm -rf /thevolume/*`) to allow reuse.

### Access Modes:
| Access Mode | CLI Code | Description |
| :--- | :--- | :--- |
| **ReadWriteOnce** | `RWO` | Volume can be mounted read/write by a single node at a time. |
| **ReadOnlyMany** | `ROX` | Volume can be mounted read-only by multiple nodes simultaneously. |
| **ReadWriteMany** | `RWX` | Volume can be mounted read/write by multiple nodes simultaneously (e.g. NFS, Ceph, EFS). |
| **ReadWriteOncePod** | `RWOP` | Volume can be mounted read/write by a single Pod across the whole cluster. |

### Practical Example: `pv.yaml`
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: student-pv
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /tmp/student-pv-data
```

---

## 4. PersistentVolumeClaim (PVC)

### What is a PersistentVolumeClaim?
A `PersistentVolumeClaim` (PVC) is a request for storage by a user or application. It is a namespaced resource.
- Pods request CPU and Memory from Nodes; similarly, **Pods request Storage via PVCs from PVs**.
- The control plane automatically matches PVC requirements (storage size, access mode, StorageClass) with available PVs and **binds** them together.

### Practical Example: `pvc.yaml`
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: student-pvc
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
```

### Consuming PVC in a Pod: `pod-pvc.yaml`
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: storage-demo
spec:
  containers:
    - name: app
      image: nginx:1.27
      volumeMounts:
        - name: persistent-storage
          mountPath: /data
  volumes:
    - name: persistent-storage
      persistentVolumeClaim:
        claimName: student-pvc
```

### Hands-on Verification (PV + PVC + Pod):
```bash
# 1. Apply PV and PVC
kubectl apply -f 01-kubernetes-volumes/pv.yaml
kubectl apply -f 01-kubernetes-volumes/pvc.yaml

# 2. Verify Binding
kubectl get pv student-pv
kubectl get pvc student-pvc
```
Expected output:
```text
NAME         CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM                 STORAGECLASS   AGE
student-pv   1Gi        RWO            Retain           Bound       default/student-pvc   manual         12s

NAME          STATUS   VOLUME       CAPACITY   ACCESS MODES   STORAGECLASS   AGE
student-pvc   Bound    student-pv   1Gi        RWO            manual         8s
```

```bash
# 3. Apply Pod
kubectl apply -f 01-kubernetes-volumes/pod-pvc.yaml
kubectl wait --for=condition=Ready pod/storage-demo --timeout=60s

# 4. Write data to PVC
kubectl exec storage-demo -- sh -c 'echo "Database record 101" > /data/db.log'

# 5. Delete Pod, recreate it, and check persistence
kubectl delete pod storage-demo
kubectl apply -f 01-kubernetes-volumes/pod-pvc.yaml
kubectl wait --for=condition=Ready pod/storage-demo --timeout=60s

kubectl exec storage-demo -- cat /data/db.log
# Output: Database record 101
```

---

## 5. StorageClass & Dynamic Provisioning

### The Static Provisioning Bottleneck:
In static provisioning, an administrator must pre-create physical disks and write PV manifests ahead of time. When 100 microservices need storage, administrators quickly become a major bottleneck.

### The Solution: Dynamic Provisioning with StorageClass
A **StorageClass** defines a provisioner plugin and volume parameters. When a developer submits a PVC referencing that StorageClass:
1. The **Provisioner** (e.g. `k8s.io/minikube-hostpath`, AWS EBS CSI, GCP PD CSI) automatically talks to the underlying storage provider.
2. The volume is created on the storage system on-the-fly.
3. The provisioner creates a corresponding `PersistentVolume` object inside the cluster.
4. Kubernetes binds the newly created PV to the PVC automatically.

```
Developer submits PVC
         │
         ▼
[ StorageClass: standard ]
         │
         ▼ triggers
[ CSI Volume Provisioner ]
         │
         ▼ provisions physical disk & creates PV
[ PersistentVolume (pvc-4b123...) ]
         │
         ▼ binds
[ PVC (Bound) ]
```

### Checking Existing StorageClasses:
```bash
kubectl get storageclass
```
Output:
```text
NAME                 PROVISIONER                RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
standard (default)   k8s.io/minikube-hostpath   Delete          Immediate           false                  45m
```

### Dynamic PVC Example: `storageclass-pvc.yaml`
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
  resources:
    requests:
      storage: 500Mi
```

### Hands-on Verification:
```bash
# 1. Apply Dynamic PVC (notice we did NOT create any PV beforehand!)
kubectl apply -f 01-kubernetes-volumes/storageclass-pvc.yaml

# 2. Check PVC and dynamically generated PV
kubectl get pvc dynamic-pvc
kubectl get pv
```
Expected output:
```text
NAME          STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
dynamic-pvc   Bound    pvc-8bf92da1-13ac-436d-9bcf-90226456df12   500Mi      RWO            standard       5s

NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                 STORAGECLASS
pvc-8bf92da1-13ac-436d-9bcf-90226456df12   500Mi      RWO            Delete           Bound    default/dynamic-pvc   standard
```

---

## Storage Types Comparison Matrix

| Storage Mechanism | Scope / Lifetime | Node Portability | Multi-Node Concurrency | Best Used For |
| :--- | :--- | :--- | :--- | :--- |
| **`emptyDir`** | Pod lifespan | Locked to Pod node | Yes (containers in same pod) | Caches, scratch buffers, sidecar file sharing |
| **`hostPath`** | Host filesystem | Node-pinned only | Only if pods land on same node | Node daemon agents, Docker socket, local dev |
| **`Static PV / PVC`** | Cluster lifespan | Backend-dependent | Defined by access mode (`RWO`/`RWX`) | Pre-allocated SAN/NFS/EBS disks |
| **`Dynamic StorageClass`**| Automatic lifecycle | Cloud / CSI managed | Defined by storage driver | Production microservices, StatefulSets, databases |

---

## Cleanup Commands
```bash
kubectl delete pod emptydir-demo hostpath-demo storage-demo --ignore-not-found=true
kubectl delete pvc student-pvc dynamic-pvc --ignore-not-found=true
kubectl delete pv student-pv --ignore-not-found=true
```
