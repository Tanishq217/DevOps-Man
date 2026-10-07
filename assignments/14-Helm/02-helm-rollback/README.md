# Task 2: Complete Helm Rollback Workflow

In mission-critical production environments, zero-downtime deployment strategies require instant, predictable rollback mechanisms when an upgrade introduces a regression or broken dependency.

This guide documents the full lifecycle:
```text
Install (Rev 1)
       ↓
Upgrade (Rev 2: Valid Production)
       ↓
Verify (Rev 2 Healthy)
       ↓
Upgrade Again (Rev 3: Broken Image)
       ↓
Verify (Rev 3 Failure Detected)
       ↓
Rollback (Rev 4: Restoring Rev 2)
       ↓
Verify (Full Recovery)
```

---

## How Helm Manages Revisions & Rollbacks

1. **Release State Storage:**
   In Helm 3, every release revision is persisted as an encrypted/compressed Kubernetes Secret in the release namespace:
   ```bash
   kubectl get secrets -l owner=helm,name=notes-dev
   ```
   Each revision has a corresponding secret: `sh.helm.release.v1.notes-dev.v1`, `sh.helm.release.v1.notes-dev.v2`, etc.

2. **Immutable Audit Trail:**
   `helm rollback` does **not** erase history or delete intermediate revisions. Instead, it reads the target historical manifest and creates a **brand-new revision** (e.g., Revision 4 that duplicates Revision 2's desired state), preserving a complete audit trail.

3. **Helm Upgrade CLI Caveat:**
   By default, `helm upgrade` marks the release as `deployed` as soon as the Kubernetes API server accepts the updated YAML manifests. It does *not* wait for pods to pass readiness probes unless invoked with `--wait` or `--atomic`.

---

## Hands-On Step-by-Step Rollback Workflow

### Step 1: Initial Installation (Revision 1)
Deploy the development baseline configuration:
```bash
helm install notes-dev ../mini-project/notes-chart
```

Verify status:
```bash
helm list
kubectl get pods -l app=notes-dev
```
Output:
```text
NAME                     READY   STATUS    RESTARTS   AGE
notes-dev-deploy-xxxxx   1/1     Running   0          25s
```

---

### Step 2: Valid Upgrade to Production (Revision 2)
Upgrade the release to use `values-prod.yaml` (scaling to 3 replicas with `nginx:1.25`):
```bash
helm upgrade notes-dev ../mini-project/notes-chart -f ../mini-project/notes-chart/values-prod.yaml
```

Output:
```text
Release "notes-dev" has been upgraded. Happy Helming!
NAME: notes-dev
STATUS: deployed
REVISION: 2
```

---

### Step 3: Verify Revision 2 Health
Check that all 3 replicas are running:
```bash
kubectl get pods -l app=notes-dev
helm history notes-dev
```

Output:
```text
NAME                     READY   STATUS    RESTARTS   AGE
notes-dev-deploy-aaaaa   1/1     Running   0          18s
notes-dev-deploy-bbbbb   1/1     Running   0          18s
notes-dev-deploy-ccccc   1/1     Running   0          18s

REVISION  UPDATED                   STATUS      CHART             APP VERSION  DESCRIPTION
1         Mon Oct  7 16:10:00 2026  superseded  notes-chart-0.1.0 1.0          Install complete
2         Mon Oct  7 16:12:00 2026  deployed    notes-chart-0.1.0 1.0          Upgrade complete
```

---

### Step 4: Upgrade Again with a Broken Image (Revision 3)
Simulate a deployment failure by providing an invalid, non-existent container tag:
```bash
helm upgrade notes-dev ../mini-project/notes-chart --set image.tag=broken-tag-does-not-exist
```

Output:
```text
Release "notes-dev" has been upgraded. Happy Helming!
NAME: notes-dev
STATUS: deployed
REVISION: 3
```

---

### Step 5: Verify the Failure
Inspect active pods:
```bash
kubectl get pods -l app=notes-dev
```

Output:
```text
NAME                                READY   STATUS             RESTARTS   AGE
notes-dev-deploy-aaaaa              1/1     Running            0          2m
notes-dev-deploy-bbbbb              1/1     Running            0          2m
notes-dev-deploy-ccccc              1/1     Running            0          2m
notes-dev-deploy-broken-xxxxx       0/1     ImagePullBackOff   0          25s
```

**Observation:** The rolling update mechanism halted because the new pod cannot start (`ImagePullBackOff`). The previous healthy pods continue serving traffic, but the deployment rollout is stalled.

---

### Step 6: Execute Rollback to Revision 2
Roll back to the last known stable state (Revision 2):
```bash
helm rollback notes-dev 2
```

Output:
```text
Rollback was a success! Happy Helming!
```

---

### Step 7: Verify System Recovery
Check release history:
```bash
helm history notes-dev
```

Output:
```text
REVISION  UPDATED                   STATUS      CHART             APP VERSION  DESCRIPTION
1         Mon Oct  7 16:10:00 2026  superseded  notes-chart-0.1.0 1.0          Install complete
2         Mon Oct  7 16:12:00 2026  superseded  notes-chart-0.1.0 1.0          Upgrade complete
3         Mon Oct  7 16:15:00 2026  superseded  notes-chart-0.1.0 1.0          Upgrade complete
4         Mon Oct  7 16:18:00 2026  deployed    notes-chart-0.1.0 1.0          Rollback to 2
```

Check pods:
```bash
kubectl get pods -l app=notes-dev
```

Output:
```text
NAME                     READY   STATUS    RESTARTS   AGE
notes-dev-deploy-aaaaa   1/1     Running   0          3m
notes-dev-deploy-bbbbb   1/1     Running   0          3m
notes-dev-deploy-ccccc   1/1     Running   0          3m
```
The failing pod is terminated, and the 3 healthy production pods are running smoothly.

---

## Defensive Engineering: Automated Rollbacks with `--atomic`

To prevent bad releases from ever remaining in a broken state, use `--atomic` combined with `--timeout`:

```bash
helm upgrade notes-dev ../mini-project/notes-chart \
  --set image.tag=invalid-tag \
  --atomic \
  --timeout 1m
```

When `--atomic` is enabled:
1. Helm monitors pod readiness until `--timeout` expires.
2. If pods fail to become ready within the time limit, Helm **automatically triggers a rollback** to the prior healthy revision.
3. The command exits with a failure code, alerting CI/CD automation pipelines immediately.
