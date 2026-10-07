# Troubleshooting: ImagePullBackOff & ErrImagePull

## 1. Problem Identification
When inspecting workloads via `kubectl get pods`, the pod status displays `ErrImagePull` initially and subsequently switches to `ImagePullBackOff`:

```
NAME               READY   STATUS             RESTARTS   AGE
imagepull-demo     0/1     ImagePullBackOff   0          45s
```

`ErrImagePull` indicates that the container runtime on the worker node attempted to fetch the container image from the registry and encountered a failure.  
`ImagePullBackOff` indicates that Kubernetes has placed the pull request into an exponential back-off loop before retrying.

---

## 2. Investigation Steps

### Step 1: Inspect Pod Events
Run `kubectl describe pod` to view the specific registry error recorded by the kubelet:
```bash
kubectl describe pod imagepull-demo
```

Under the `Events:` section at the bottom of the output:
```
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Normal   Scheduled  52s                default-scheduler  Successfully assigned default/imagepull-demo to minikube
  Normal   Pulling    24s (x2 over 51s)  kubelet            Pulling image "nginx:non-existent-v99.99"
  Warning  Failed     23s (x2 over 50s)  kubelet            Failed to pull image "nginx:non-existent-v99.99": rpc error: code = NotFound desc = failed to pull and unpack image "docker.io/library/nginx:non-existent-v99.99": failed to resolve reference "docker.io/library/nginx:non-existent-v99.99": docker.io/library/nginx:non-existent-v99.99: not found
  Warning  Failed     23s (x2 over 50s)  kubelet            Error: ErrImagePull
  Normal   BackOff    10s (x3 over 49s)  kubelet            Back-off pulling image "nginx:non-existent-v99.99"
  Warning  Failed     10s (x3 over 49s)  kubelet            Error: ImagePullBackOff
```

### Step 2: Categorize Common Root Causes
The most common reasons for `ImagePullBackOff` include:
1. **Invalid or non-existent tag:** Typo in image name or version tag (e.g., `v99.99`).
2. **Missing image pull secret:** Attempting to pull from a private registry (Docker Hub private repo, ECR, GCR, Harbor) without configuring `imagePullSecrets`.
3. **Network or registry downtime:** Node unable to resolve registry DNS or firewall blocking registry port 443.

---

## 3. Root Cause Analysis
In this scenario, the image specification requested `nginx:non-existent-v99.99`. Docker Hub responded with HTTP 404 / `manifest unknown`, meaning that specific tag does not exist in the public repository.

---

## 4. Solution & Fix
Edit the manifest or apply `fixed-pod.yaml` with an existing, verified image tag (e.g., `nginx:1.27`):

```yaml
spec:
  containers:
    - name: web-server
      image: nginx:1.27
      ports:
        - containerPort: 80
```

Apply the fix:
```bash
kubectl delete pod imagepull-demo --grace-period=0 --force
kubectl apply -f fixed-pod.yaml
```

*(Or if using a Deployment, simply running `kubectl set image deployment/<name> <container>=<new-image>` triggers a rolling update).*

---

## 5. Verification
Verify that the kubelet pulls the image successfully and starts the container:
```bash
kubectl get pods -l app=imagepull-demo
```
Output:
```
NAME             READY   STATUS    RESTARTS   AGE
imagepull-demo   1/1     Running   0          18s
```

Check the new events:
```bash
kubectl describe pod imagepull-demo | grep -A 5 Events:
```
Output:
```
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  22s   default-scheduler  Successfully assigned default/imagepull-demo to minikube
  Normal  Pulling    21s   kubelet            Pulling image "nginx:1.27"
  Normal  Pulled     19s   kubelet            Successfully pulled image "nginx:1.27" in 1.95s
  Normal  Created    19s   kubelet            Created container web-server
  Normal  Started    18s   kubelet            Started container web-server
```
