# Troubleshooting: Pending Pods

## 1. Problem Identification
When listing cluster workloads, a newly submitted Pod remains indefinitely in the `Pending` state:

```
NAME           READY   STATUS    RESTARTS   AGE
pending-demo   0/1     Pending   0          2m15s
```

A Pod in `Pending` has been accepted and recorded in `etcd` by the API server, but cannot yet run on any node. This phase usually means:
1. The **kube-scheduler** cannot place the pod on any worker node due to constraints (insufficient CPU/memory, nodeSelectors, affinities, taints).
2. The pod is waiting for a **PersistentVolumeClaim** to be bound or a volume to attach.

---

## 2. Investigation Steps

### Step 1: Inspect Pod Events
Run `kubectl describe pod` to inspect scheduling decision events:
```bash
kubectl describe pod pending-demo
```

Under the `Events:` section:
```
Events:
  Type     Reason            Age   From               Message
  ----     ------            ----  ----               -------
  Warning  FailedScheduling  35s   default-scheduler  0/1 nodes available: 1 node(s) didn't match Pod's node affinity/selector. preemption: 0/1 nodes available: 1 Preemption is not helpful for scheduling.
```

### Step 2: Compare Pod Requirements Against Node State
- If the event indicates **node affinity/selector mismatch**:
  Inspect node labels to check if the requested label exists:
  ```bash
  kubectl get nodes --show-labels
  ```
- If the event indicates **Insufficient cpu** or **Insufficient memory**:
  Inspect node allocatable capacity and existing commitments:
  ```bash
  kubectl describe node <node-name> | grep -A 10 "Allocated resources:"
  ```

---

## 3. Root Cause Analysis
The pod manifest requested a restrictive node selector:
```yaml
nodeSelector:
  disktype: ultra-nvme-ssd-zone-b
```
None of the cluster's worker nodes possess this label. Consequently, the Kubernetes scheduler could not place the pod onto any candidate node, keeping it in the `Pending` queue.

---

## 4. Solution & Fix
Either:
- Label an eligible node:
  ```bash
  kubectl label nodes minikube disktype=ultra-nvme-ssd-zone-b
  ```
- Or remove the unfulfillable node constraint in `fixed-pod.yaml`:
  ```bash
  kubectl delete pod pending-demo --grace-period=0 --force
  kubectl apply -f fixed-pod.yaml
  ```

---

## 5. Verification
Verify that the pod is immediately scheduled and transitioned to `Running`:
```bash
kubectl get pods -l app=pending-demo -o wide
```
Output:
```
NAME           READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
pending-demo   1/1     Running   0          12s   10.244.0.9   minikube   <none>           <none>
```

Verify scheduling events:
```bash
kubectl describe pod pending-demo | grep -A 3 Events:
```
Output:
```
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  15s   default-scheduler  Successfully assigned default/pending-demo to minikube
  Normal  Pulled     14s   kubelet            Container image "nginx:1.27" already present on machine
  Normal  Created    14s   kubelet            Created container data-processor
  Normal  Started    13s   kubelet            Started container data-processor
```
