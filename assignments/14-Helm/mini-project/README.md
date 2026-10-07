# Mini Project: Package and Deploy the Notes App with Helm

This mini-project demonstrates packaging a multi-tier microservice architecture into a reusable, parameter-driven Helm chart called `notes-chart`.

---

## Architecture & Directory Layout

```text
notes-chart/
├── Chart.yaml
├── values.yaml
├── values-prod.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    └── configmap.yaml
```

The application uses an Nginx-backed web workload to simulate a microservice Notes application with environment-specific configuration maps and NodePort networking.

---

## Configuration Files

### 1. `Chart.yaml`
Declares metadata, semantic chart version, and application release version:
```yaml
apiVersion: v2
name: notes-chart
description: A simple Notes application Helm chart
type: application
version: 0.1.0
appVersion: "1.0"
```

### 2. `values.yaml` (Development Defaults)
```yaml
replicaCount: 1

image:
  repository: nginx
  tag: "1.24"

service:
  port: 80
  nodePort: 30090

app:
  name: notes-app
  environment: development
```

### 3. `values-prod.yaml` (Production Overrides)
```yaml
replicaCount: 3

image:
  repository: nginx
  tag: "1.25"

service:
  port: 80
  nodePort: 30090

app:
  name: notes-app
  environment: production
```

### 4. `templates/configmap.yaml`
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-config
data:
  APP_NAME: {{ .Values.app.name | quote }}
  ENVIRONMENT: {{ .Values.app.environment | quote }}
```

### 5. `templates/deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-deploy
  labels:
    app: {{ .Release.Name }}
    environment: {{ .Values.app.environment }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app: {{ .Release.Name }}
    spec:
      containers:
        - name: notes
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: {{ .Values.service.port }}
          envFrom:
            - configMapRef:
                name: {{ .Release.Name }}-config
```

### 6. `templates/service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-svc
spec:
  type: NodePort
  selector:
    app: {{ .Release.Name }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.port }}
      nodePort: {{ .Values.service.nodePort }}
```

---

## Deployment & Verification Workflow

### Step 1: Lint Chart
```bash
helm lint notes-chart
```
Output:
```text
==> Linting notes-chart
1 chart(s) linted, 0 chart(s) failed
```

### Step 2: Render Manifests Locally
```bash
helm template notes-dev notes-chart
```
Verifies that all Go template substitutions (`{{ .Release.Name }}`, `{{ .Values... }}`) are properly evaluated without syntax errors.

### Step 3: Install in Development Mode
```bash
helm install notes-dev notes-chart
```
Verify deployed resources:
```bash
kubectl get pods
kubectl get services
kubectl get configmaps
```

### Step 4: Upgrade with Production Values
```bash
helm upgrade notes-dev notes-chart -f notes-chart/values-prod.yaml
```
Verifies scale-out to 3 replicas and version upgrade to `nginx:1.25`:
```bash
kubectl get pods
helm history notes-dev
```

### Step 5: Simulate Failed Upgrade
```bash
helm upgrade notes-dev notes-chart --set image.tag=broken-tag-does-not-exist
```
Inspect pods to observe failure:
```bash
kubectl get pods
```
Output shows new pod entering `ImagePullBackOff` or `ErrImagePull`, while existing pods maintain application uptime.

### Step 6: Rollback to Healthy Revision
```bash
helm rollback notes-dev 2
```
Output:
```text
Rollback was a success! Happy Helming!
```
Verify that all 3 production pods return to `Running`:
```bash
kubectl get pods
```

### Step 7: Clean Up
```bash
helm uninstall notes-dev
```

---

## Summary of Practiced Competencies
- Created parameterized Helm chart from scratch.
- Implemented environment separation via `values.yaml` and `values-prod.yaml`.
- Validated YAML using `helm lint` and dry-run rendering with `helm template`.
- Managed release lifecycles across install, rolling upgrade, broken upgrade, and instant rollback.
