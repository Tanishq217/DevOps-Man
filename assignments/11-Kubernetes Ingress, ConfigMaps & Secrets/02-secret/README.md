# Secret — Protecting Sensitive Credentials in Kubernetes

## Why Do We Need Secrets?

### The Problem: Plain-Text Credentials & Accidental Leaks
Storing sensitive credentials (passwords, tokens, database connection strings) in plaintext inside code, Dockerfiles, or git repositories is a major security vulnerability.
- Committing passwords to git leaves permanent forensic trails in commit history.
- Baking credentials into images exposes them to anyone who pulls the container image.
- Placing credentials in ConfigMaps leaves them exposed to unprivileged users with basic read rights.

### The Solution: Kubernetes Secret
Kubernetes `Secret` objects store confidential data separately from application logic. The keys in the `data` field are **Base64-encoded**, and `kubectl describe secret` automatically redacts the values, displaying only byte counts.

```
Raw String:         secretpassword
                          │
            echo -n "secretpassword" | base64
                          ▼
Base64-Encoded:     c2VjcmV0cGFzc3dvcmQ=
```

---

## Critical Rules & Best Practices

1. **Base64 is Encoding, Not Encryption:**
   Base64 is a two-way encoding format, not an cryptographic cipher. Anyone with `kubectl get secret -o yaml` can decode it with `base64 --decode`. Security depends on strict Kubernetes RBAC, Namespace isolation, and etcd encryption-at-rest.
2. **The Newline Gotcha (`echo -n`):**
   Standard `echo` appends an ASCII newline character (`0x0a` / `\n`). Always pass `-n` so the trailing newline is omitted:
   ```bash
   # WRONG: Encodes secretpassword\n (ends in Ao=)
   echo "secretpassword" | base64

   # CORRECT: Encodes exact 14 characters without newline
   echo -n "secretpassword" | base64
   ```
3. **Production Secret Management:**
   In enterprise environments, secrets are backed by external Key Management Services (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault) synced into Kubernetes via the External Secrets Operator (ESO) or CSI Secret Store Driver.

---

## Manifest Reference

### `02-secret/db-secret.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: yatri-db-secret
  labels:
    app: yatri-backend
type: Opaque
data:
  # Base64 for 'yatri_admin' -> echo -n "yatri_admin" | base64
  POSTGRES_USER: eWF0cmlfYWRtaW4=
  # Base64 for 'secretpassword' -> echo -n "secretpassword" | base64
  POSTGRES_PASSWORD: c2VjcmV0cGFzc3dvcmQ=
  # Base64 for 'yatri_production_db' -> echo -n "yatri_production_db" | base64
  POSTGRES_DB: eWF0cmlfcHJvZHVjdGlvbl9kYg==
```

---

## Verification & Commands

```bash
# 1. Apply the Secret
kubectl apply -f 02-secret/db-secret.yaml

# 2. Inspect Secret (values are redacted)
kubectl get secret yatri-db-secret
kubectl describe secret yatri-db-secret

# 3. Decode a specific value
kubectl get secret yatri-db-secret -o jsonpath='{.data.POSTGRES_PASSWORD}' | base64 --decode
```

Expected Output:
```text
NAME              TYPE     DATA   AGE
yatri-db-secret   Opaque   3      12s

Name:         yatri-db-secret
Type:         Opaque

Data
====
POSTGRES_DB:        22 bytes
POSTGRES_PASSWORD:  14 bytes
POSTGRES_USER:      11 bytes

secretpassword
```
