# DaemonSet — Running Agent Pods on Every Node

## Overview

A `DaemonSet` ensures that all (or eligible) worker nodes in a Kubernetes cluster run exactly **one copy** of a specified Pod.
- When new nodes are added to the cluster, the DaemonSet controller automatically schedules a Pod on them.
- When nodes are removed from the cluster, those Pods are garbage collected.
- Deleting a DaemonSet cleans up all Pods it created across all nodes.

---

## Production Use Cases

1. **Cluster Storage Daemons:** Running distributed storage pods like Ceph or GlusterFS on each storage node.
2. **Node Log Collectors:** Running log shippers like Fluentd, Fluent Bit, or Promtail on every node to collect container logs.
3. **Node Monitoring Agents:** Running metrics collectors like Prometheus Node Exporter or Datadog agent.
4. **Network Plugins:** Running CNI daemons (Calico node agent, Cilium, kube-proxy).

---

## Commands & Verification

```bash
# 1. Apply DaemonSet
kubectl apply -f 03-daemonset/node-agent-ds.yaml

# 2. Inspect DaemonSet
kubectl get ds node-logging-agent
kubectl get pods -l app=node-logging-agent -o wide

# 3. View Logs from Agent Pod
POD_NAME=$(kubectl get pods -l app=node-logging-agent -o jsonpath='{.items[0].metadata.name}')
kubectl logs $POD_NAME

# Cleanup
kubectl delete ds node-logging-agent
```
