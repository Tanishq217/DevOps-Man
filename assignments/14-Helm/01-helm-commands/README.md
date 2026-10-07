# Task 1: Essential Helm Commands Reference & Hands-on Guide

Helm is the official package manager for Kubernetes. It automates the creation, packaging, configuration, and deployment of Kubernetes applications into reproducible units known as **Charts**.

---

## Command Reference & Hands-On Walkthrough

### 1. `helm version`
Checks the installed Helm client version and the compiled Kubernetes client library version.

```bash
helm version
```

Output:
```text
version.BuildInfo{Version:"v4.3.0", GitCommit:"...", GitTreeState:"clean", GoVersion:"go1.27.1", KubeClientVersion:"v1.37"}
```

---

### 2. `helm repo`
Manages remote Helm chart repositories (HTTP registries housing pre-packaged charts and their `index.yaml`).

- **Add repository:**
  ```bash
  helm repo add bitnami https://charts.bitnami.com/bitnami
  ```
- **List repositories:**
  ```bash
  helm repo list
  ```
- **Update local repository cache:**
  ```bash
  helm repo update
  ```

---

### 3. `helm search`
Searches for public or private Helm charts across configured repositories or the public Artifact Hub.

- **Search configured repositories:**
  ```bash
  helm search repo bitnami/nginx
  ```
- **Search Artifact Hub:**
  ```bash
  helm search hub redis
  ```

---

### 4. `helm create`
Scaffolds a brand-new directory structure containing boilerplate chart manifests.

```bash
helm create demo-chart
```

Generates:
```text
demo-chart/
├── Chart.yaml          # Metadata: chart name, version, description
├── values.yaml         # Default configurable values
├── charts/             # Sub-chart dependencies
└── templates/          # Templated Kubernetes manifests
    ├── deployment.yaml
    ├── service.yaml
    ├── serviceaccount.yaml
    ├── hpa.yaml
    ├── ingress.yaml
    ├── _helpers.tpl    # Reusable Go template snippets
    ├── NOTES.txt       # Post-install usage instructions
    └── tests/
```

---

### 5. `helm lint`
Validates chart syntax, checks for missing required metadata fields, and flags structural antipatterns.

```bash
helm lint ./demo-chart
```

Output:
```text
==> Linting ./demo-chart
[INFO] Chart.yaml: icon is recommended
1 chart(s) linted, 0 chart(s) failed
```

---

### 6. `helm template`
Renders Kubernetes YAML manifests locally without contacting the Kubernetes cluster. Invaluable for debugging Go template interpolation and verifying value substitutions before deployment.

```bash
helm template demo-release ./demo-chart
```

Displays rendered Deployment, Service, ServiceAccount, and Test pod YAML.

---

### 7. `helm install`
Deploys a Helm chart onto the target Kubernetes cluster as an active named **Release**.

```bash
helm install demo-release ./demo-chart
```

Output:
```text
NAME: demo-release
LAST DEPLOYED: Mon Oct  7 16:00:00 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
1. Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=demo-chart,app.kubernetes.io/instance=demo-release" -o jsonpath="{.items[0].metadata.name}")
...
```

Verify deployed workloads:
```bash
kubectl get pods -l app.kubernetes.io/instance=demo-release
```

---

### 8. `helm list`
Lists all active Helm releases in the current namespace (or across all namespaces with `-A`).

```bash
helm list
```

Output:
```text
NAME          NAMESPACE  REVISION  UPDATED                               STATUS    CHART            APP VERSION
demo-release  default    1         2026-10-07 16:00:00.123456 +0530 IST  deployed  demo-chart-0.1.0 1.16.0
```

---

### 9. `helm status`
Retrieves detailed operational status of a deployed release, including its current state, last deployed timestamp, active revision, and `NOTES.txt` output.

```bash
helm status demo-release
```

---

### 10. `helm get`
Inspects internal metadata, rendered manifests, or user-supplied values stored for a release.

- **View user-supplied override values:**
  ```bash
  helm get values demo-release
  ```
- **View fully rendered Kubernetes manifests stored in cluster:**
  ```bash
  helm get manifest demo-release
  ```
- **View all release information:**
  ```bash
  helm get all demo-release
  ```
- **View chart post-install notes:**
  ```bash
  helm get notes demo-release
  ```

---

### 11. `helm upgrade`
Upgrades an existing release with updated values, a newer chart version, or modified templates, creating a new **Revision**.

```bash
helm upgrade demo-release ./demo-chart --set replicaCount=3
```

Output:
```text
Release "demo-release" has been upgraded. Happy Helming!
NAME: demo-release
LAST DEPLOYED: Mon Oct  7 16:05:00 2026
NAMESPACE: default
STATUS: deployed
REVISION: 2
```

Verify scaled pods:
```bash
kubectl get pods -l app.kubernetes.io/instance=demo-release
```

---

### 12. `helm history`
Displays the complete revision lifecycle and rollout audit log of a release.

```bash
helm history demo-release
```

Output:
```text
REVISION  UPDATED                   STATUS      CHART             APP VERSION  DESCRIPTION
1         Mon Oct  7 16:00:00 2026  superseded  demo-chart-0.1.0  1.16.0       Install complete
2         Mon Oct  7 16:05:00 2026  deployed    demo-chart-0.1.0  1.16.0       Upgrade complete
```

---

### 13. `helm rollback`
Rolls back a release to a specific previous revision number. Helm generates a *new* revision pointing to the historical state.

```bash
helm rollback demo-release 1
```

Output:
```text
Rollback was a success! Happy Helming!
```

Checking history shows Revision 3 with description `Rollback to 1`.

---

### 14. `helm uninstall`
Deletes an active release and cleans up all associated Kubernetes workloads, Services, and Secrets.

```bash
helm uninstall demo-release
```

Output:
```text
release "demo-release" uninstalled
```
