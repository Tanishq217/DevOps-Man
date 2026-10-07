# Troubleshooting: Service Connectivity, DNS & Pod Networking Issues

## 1. Problem Identification
A client application attempts to make HTTP calls to internal backend service `auth-service`, but all requests immediately fail:

```bash
kubectl exec dns-test-client -- curl -I --connect-timeout 3 http://auth-service
```
Error Output:
```
curl: (28) Failed to connect to auth-service port 80: Connection timed out
```
Or:
```
curl: (7) Failed to connect to auth-service port 80: Connection refused
```

---

## 2. Investigation Steps

### Step 1: Check if the Service Exists and has a ClusterIP
```bash
kubectl get svc auth-service
```
Output:
```
NAME           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
auth-service   ClusterIP   10.96.140.210   <none>        80/TCP    2m
```
The Service object exists and has an allocated ClusterIP.

### Step 2: Check Service Endpoints (`kubectl get endpoints`)
A Kubernetes Service routes traffic by maintaining an `Endpoints` (or `EndpointSlice`) list composed of healthy Pod IPs matching its selector:
```bash
kubectl get endpoints auth-service
```
Output:
```
NAME           ENDPOINTS   AGE
auth-service   <none>      2m
```
**Key Discovery:** The `ENDPOINTS` list is completely empty (`<none>`)! No Pods are receiving traffic from this Service.

### Step 3: Compare Service Selector vs Pod Labels
Inspect what selector the Service is using:
```bash
kubectl describe svc auth-service | grep Selector
```
Output:
```
Selector:  app=auth-backend
```
Inspect what labels the target Pods actually have:
```bash
kubectl get pods --show-labels
```
Output:
```
NAME                                       READY   STATUS    RESTARTS   AGE   LABELS
auth-service-deployment-7bb9cbbf45-k9q2m   1/1     Running   0          3m    app=auth-service,pod-template-hash=7bb9cbbf45
auth-service-deployment-7bb9cbbf45-x8w1p   1/1     Running   0          3m    app=auth-service,pod-template-hash=7bb9cbbf45
```
**Mismatch Identified:** The Service selects `app=auth-backend`, but the Pods have `app=auth-service`.

### Step 4: Validate DNS Resolution
Verify CoreDNS functionality by executing `nslookup` inside the client container:
```bash
kubectl exec dns-test-client -- nslookup auth-service
```
Output:
```
Server:    10.96.0.10
Address:   10.96.0.10#53

Name:      auth-service.default.svc.cluster.local
Address:   10.96.140.210
```
CoreDNS properly resolves `auth-service` to its ClusterIP. The failure is not DNS resolution, but the absence of backend Pod endpoints behind that IP.

---

## 3. Root Cause Analysis
The Service selector `app=auth-backend` did not match any running Pod labels (`app=auth-service`). Because no endpoints were registered in the EndpointSlice, `kube-proxy` had no routing rules configured for the virtual IP, causing connection timeouts.

---

## 4. Solution & Fix
Update `selector.app` to match `auth-service` in `fixed-service.yaml`:

```yaml
spec:
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
  selector:
    app: auth-service
```

Apply the fix:
```bash
kubectl apply -f fixed-service.yaml
```

---

## 5. Verification
Verify that endpoints are automatically registered:
```bash
kubectl get endpoints auth-service
```
Output:
```
NAME           ENDPOINTS                           AGE
auth-service   10.244.0.14:80,10.244.0.15:80       4m
```

Verify end-to-end HTTP connectivity from `dns-test-client`:
```bash
kubectl exec dns-test-client -- curl -s -I http://auth-service
```
Output:
```
HTTP/1.1 200 OK
Server: nginx/1.27.0
Content-Type: text/html
Content-Length: 615
Connection: keep-alive
```
The Service and DNS routing are completely restored!
