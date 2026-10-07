# Troubleshooting: ContainerCreating

## 1. Problem Identification
When observing pod lifecycle states, the pod remains indefinitely in `ContainerCreating`:

```
NAME                     READY   STATUS              RESTARTS   AGE
containercreating-demo   0/1     ContainerCreating   0          1m45s
```

`ContainerCreating` indicates that the pod was successfully scheduled to a worker node, but the local `kubelet` and container runtime (containerd/CRI-O) cannot assemble the container sandbox and its dependencies to transition it to `Running`.

---

## 2. Investigation Steps

### Step 1: Inspect Pod Events
Run `kubectl describe pod` to examine why the container sandbox creation stalled:
```bash
kubectl describe pod containercreating-demo
```

Under the `Events:` section:
```
Events:
  Type     Reason       Age                From               Message
  ----     ------       ----               ----               -------
  Normal   Scheduled    2m                 default-scheduler  Successfully assigned default/containercreating-demo to minikube
  Warning  FailedMount  15s (x8 over 2m)   kubelet            MountVolume.SetUp failed for volume "missing-volume-mount" : configmap "non-existent-app-settings" not found
```

### Step 2: Categorize Common Root Causes
A pod gets stuck in `ContainerCreating` due to:
1. **Unresolved Volume Mounts (`FailedMount`):** Attempting to mount a non-existent ConfigMap, Secret, or PVC.
2. **PersistentVolume Attachment Latency (`FailedAttachVolume`):** Waiting for cloud disk controller attachment or volume lock release from an older terminated pod.
3. **Container Network Interface (CNI) Latency:** Waiting for IP address allocation from Calico, Flannel, or Cilium IPAM.
4. **Host Node Storage Shortage:** Node filesystem full (`DiskPressure`), preventing filesystem overlay creation.

---

## 3. Root Cause Analysis
In this scenario, the pod volume definition referenced `configMap: name: non-existent-app-settings`. Because this ConfigMap was never applied to the namespace, kubelet's volume setup hook blocked the container creation pipeline.

---

## 4. Solution & Fix
Apply `fixed-pod.yaml`, which provisions the missing `app-settings` ConfigMap alongside the pod:

```bash
kubectl delete pod containercreating-demo --grace-period=0 --force
kubectl apply -f fixed-pod.yaml
```

---

## 5. Verification
Verify that the volume mounts cleanly and the container reaches `Running` status:
```bash
kubectl get pods -l app=containercreating-demo
```
Output:
```
NAME                     READY   STATUS    RESTARTS   AGE
containercreating-demo   1/1     Running   0          22s
```

Inspect the container filesystem to verify the mount:
```bash
kubectl exec containercreating-demo -- cat /etc/configs/app.conf
```
Output:
```
server_mode=production
cache_enabled=true
```
