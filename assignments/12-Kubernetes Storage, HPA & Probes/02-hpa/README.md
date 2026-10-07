# Horizontal Pod Autoscaler (HPA) Hands-on Guide

## Overview

The **Horizontal Pod Autoscaler** (HPA) automatically scales the number of Pod replicas in a Deployment, ReplicaSet, or StatefulSet based on observed resource utilization (such as CPU, Memory, or custom metrics).

```
Traffic Load Increases
         │
         ▼
CPU Utilization Spikes (> 50%)
         │
         ▼ detected by
  [ Metrics Server ]
         │
         ▼ queried every 15s by
[ HorizontalPodAutoscaler (HPA) ]
         │
         ▼ scales out
[ Deployment: hpa-demo (1 -> 5 Replicas) ]
```

---

## Prerequisites: Metrics Server

HPA cannot function without the Kubernetes Metrics Server, which collects resource metrics from Kubelets via the `metrics.k8s.io` API.

```bash
# On Minikube, enable the metrics-server addon:
minikube addons enable metrics-server

# Verify the metrics-server pod is Running:
kubectl get pods -n kube-system -l k8s-app=metrics-server
```

Test metrics availability:
```bash
kubectl top nodes
kubectl top pods
```
> If `kubectl top pods` outputs metrics (e.g. `1m`, `15Mi`), the metrics pipeline is operational.

---

## 1. Why CPU Requests Are Mandatory for HPA

In `deployment.yaml`:
```yaml
resources:
  requests:
    cpu: 100m
  limits:
    cpu: 200m
```
HPA calculates CPU utilization as a percentage of the Pod's **requested** CPU:
$$\text{CPU Utilization \%} = \frac{\text{Actual CPU Usage}}{\text{Requested CPU}} \times 100$$

If `resources.requests.cpu` is omitted:
- HPA cannot calculate the percentage target.
- `kubectl get hpa` shows `TARGETS: <unknown>/50%`.
- Autoscaling will never trigger.

---

## 2. Deploy Application & Expose Service

```bash
# 1. Apply Deployment and Service
kubectl apply -f 02-hpa/deployment.yaml
kubectl apply -f 02-hpa/service.yaml

# 2. Verify Deployment and Pod are healthy
kubectl rollout status deployment/hpa-demo
kubectl get pods -l app=hpa-demo
kubectl get svc hpa-demo-service
```

Expected output:
```text
deployment.apps/hpa-demo created
service/hpa-demo-service created

NAME                        READY   STATUS    RESTARTS   AGE
hpa-demo-6869769584-7k8qm   1/1     Running   0          15s

NAME               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
hpa-demo-service   ClusterIP   10.104.215.110   <none>        80/TCP    15s
```

---

## 3. Configure and Verify HPA

Apply the HPA manifest:
```bash
kubectl apply -f 02-hpa/hpa.yaml
```

Inspect the HPA:
```bash
kubectl get hpa hpa-demo
```
Expected output:
```text
NAME       REFERENCE             TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
hpa-demo   Deployment/hpa-demo   0%/50%    1         5         1          10s
```

Inspect detailed HPA metrics and conditions:
```bash
kubectl describe hpa hpa-demo
```
Expected output:
```text
Name:                                                  hpa-demo
Namespace:                                             default
Reference:                                             Deployment/hpa-demo
Metrics:                                               ( current / target )
  resource cpu on pods  (as a percentage of request):  0% (1m) / 50%
Min replicas:                                          1
Max replicas:                                          5
Deployment pods:                                       1 current / 1 desired
Conditions:
  Type            Status  Reason               Message
  ----            ------  ------               -------
  AbleToScale     True    ScaleDownStabilized  recent recommendations were higher than current one
  ScalingActive   True    ValidMetricFound     the HPA was able to successfully calculate a replica count
Events:           <none>
```

---

## 4. Deploy Load Generator & Observe Scaling

In Terminal 1, watch HPA in real time:
```bash
kubectl get hpa hpa-demo -w
```

In Terminal 2, watch Pods scaling out:
```bash
kubectl get pods -l app=hpa-demo -w
```

In Terminal 3, deploy the load generator:
```bash
kubectl apply -f 02-hpa/load-generator.yaml
```
*(Alternatively, run an imperative busybox container)*:
```bash
kubectl run load-generator --image=busybox:1.36 --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://hpa-demo-service; done"
```

### Observing CPU Spike & Autoscaling:
Check actual pod utilization with `kubectl top pods`:
```bash
kubectl top pods -l app=hpa-demo
```
Output:
```text
NAME                        CPU(cores)   MEMORY(bytes)
hpa-demo-6869769584-7k8qm   380m         18Mi
```
> The pod is consuming 380m out of 100m requested ($380\%$ utilization!).

Within 30–60 seconds, watch the HPA log in Terminal 1:
```text
NAME       REFERENCE             TARGETS    MINPODS   MAXPODS   REPLICAS   AGE
hpa-demo   Deployment/hpa-demo   0%/50%     1         5         1          2m
hpa-demo   Deployment/hpa-demo   305%/50%   1         5         1          2m30s
hpa-demo   Deployment/hpa-demo   380%/50%   1         5         4          3m
hpa-demo   Deployment/hpa-demo   62%/50%    1         5         5          3m30s
```

And in Terminal 2, watch the Pods scale from 1 to 5:
```text
NAME                        READY   STATUS    RESTARTS   AGE
hpa-demo-6869769584-7k8qm   1/1     Running   0          3m
hpa-demo-6869769584-9klm2   0/1     Pending   0          0s
hpa-demo-6869769584-xvn98   0/1     Pending   0          0s
hpa-demo-6869769584-b4qwz   0/1     Pending   0          0s
hpa-demo-6869769584-9klm2   1/1     Running   0          5s
hpa-demo-6869769584-xvn98   1/1     Running   0          5s
hpa-demo-6869769584-b4qwz   1/1     Running   0          5s
hpa-demo-6869769584-p8xtc   1/1     Running   0          8s
```

Check `describe hpa` to see the scaling event log:
```bash
kubectl describe hpa hpa-demo
```
Event section:
```text
Events:
  Type    Reason             Age   From                       Message
  ----    ------             ----  ----                       -------
  Normal  SuccessfulRescale  60s   horizontal-pod-autoscaler  New size: 4; reason: cpu resource utilization (percentage of request) above target
  Normal  SuccessfulRescale  30s   horizontal-pod-autoscaler  New size: 5; reason: cpu resource utilization (percentage of request) above target
```

---

## 5. Stop Load & Observe Scale-Down

Delete the load generator:
```bash
kubectl delete pod load-generator
```

Watch HPA:
```bash
kubectl get hpa hpa-demo -w
```
Expected output:
```text
NAME       REFERENCE             TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
hpa-demo   Deployment/hpa-demo   0%/50%    1         5         5          6m
```
> **Note on Scale-Down Stabilization Window:** Kubernetes maintains a default **5-minute stabilization window** (`behavior.scaleDown.stabilizationWindowSeconds: 300`) before reducing replica count. This prevents rapid flapping (thrashing) between scale-out and scale-in. After ~5 minutes of idle traffic, replicas smoothly scale back down to 1.

---

## Key HPA Formula

$$\text{Desired Replicas} = \left\lceil \text{Current Replicas} \times \left( \frac{\text{Current Metric Value}}{\text{Target Metric Value}} \right) \right\rceil$$

For example:
$$\text{Desired Replicas} = \left\lceil 1 \times \left( \frac{305\%}{50\%} \right) \right\rceil = \lceil 6.1 \rceil = 7 \implies \text{capped at maxReplicas } (5)$$

---

## Useful Diagnostic Commands

```bash
kubectl get hpa
kubectl get pods -l app=hpa-demo
kubectl top pods -l app=hpa-demo
kubectl describe hpa hpa-demo
kubectl get events --sort-by=.lastTimestamp
```

---

## Cleanup
```bash
kubectl delete -f 02-hpa/hpa.yaml
kubectl delete -f 02-hpa/service.yaml
kubectl delete -f 02-hpa/deployment.yaml
kubectl delete pod load-generator --ignore-not-found=true
```
