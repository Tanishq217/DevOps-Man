# Kubernetes Troubleshooting Drills

## Drill 1: Broken Image Rollout Stall (`broken-image.yaml`)

### The Problem
When a deployment rollout references a non-existent container image, the new surge pod enters `ImagePullBackOff` or `ErrImagePull`.

### Expected Behavior
Because `maxUnavailable: 0` is set, Kubernetes refuses to terminate old running pods until the new pod becomes `Ready`. Thus, user traffic is never interrupted!

### Commands
```bash
kubectl apply -f troubleshooting/broken-image.yaml
kubectl rollout status deployment/yatri-backend-broken
# Output hangs: Waiting for deployment "yatri-backend-broken" rollout to finish...

kubectl get pods -l app=yatri-backend
# Observe new pod in ImagePullBackOff

# Rollback
kubectl rollout undo deployment/yatri-backend-broken
```

---

## Drill 2: Selector Mismatch Error (`selector-mismatch.yaml`)

### The Problem
If `spec.selector.matchLabels` does not match `spec.template.metadata.labels`, the API server immediately rejects the manifest with a validation error.

### Command & Verification
```bash
kubectl apply -f troubleshooting/selector-mismatch.yaml
```

**Expected Error Output:**
```text
The Deployment "selector-error-demo" is invalid: spec.template.metadata.labels: Invalid value: map[string]string{"app":"wrong-app-name"}: `selector` does not match template `labels`
```
