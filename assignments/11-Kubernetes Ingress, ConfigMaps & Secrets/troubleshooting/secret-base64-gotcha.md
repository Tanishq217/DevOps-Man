# Troubleshooting Guide: The Trailing Newline Secret Bug

## The Production Incident Scenario
- **Symptom:** The backend application repeatedly fails to authenticate with PostgreSQL, logging:  
  `FATAL: password authentication failed for user "yatri_admin"`
- **Initial Assumption:** The engineer claims: *"I encoded the password directly with `echo "secretpassword" | base64`, so the secret matches my database password!"*

---

## Root Cause Analysis & Deep Dive

When `echo "string"` runs in bash or zsh, it automatically appends a terminating ASCII newline character (`0x0A` or `\n`).

### Inspecting Raw Hex Bytes
```bash
echo "secretpassword" | xxd
```
Output:
```text
00000000: 7365 6372 6574 7061 7373 776f 7264 0a   secretpassword.
```
Notice byte index 15: `0a`. That is the newline character.

### Comparing Base64 Outputs

1. **With Newline (Standard `echo`):**
   ```bash
   echo "secretpassword" | base64
   # Output: c2VjcmV0cGFzc3dvcmQK
   ```
   Notice that the base64 string ends in `QK` or `Ao=`. When Kubernetes injects this into the container, the environment variable contains:
   `secretpassword\n` (15 characters).
   PostgreSQL expects `secretpassword` (14 characters), rejecting the connection with authentication error.

2. **Without Newline (`echo -n`):**
   ```bash
   echo -n "secretpassword" | base64
   # Output: c2VjcmV0cGFzc3dvcmQ=
   ```
   Notice the string cleanly ends in `=`. The application receives exactly 14 characters, matching PostgreSQL records.

---

## Live Verification & Demonstration

To demonstrate the issue in your local terminal:

```bash
# 1. Decode the faulty string
echo "c2VjcmV0cGFzc3dvcmQK" | base64 --decode
# Note the cursor drops to the following line due to the embedded newline.

# 2. Decode the clean string
echo "c2VjcmV0cGFzc3dvcmQ=" | base64 --decode
# The output directly precedes the prompt without an intervening line break.
```

---

## Standard Prevention Rules

1. **Always use `-n`:**  
   `echo -n "<secret-value>" | base64`
2. **Use `stringData` in YAML manifests:**  
   Kubernetes supports the `stringData` field in Secret manifests. This allows plain text input which the API server automatically encodes to Base64 without hidden newlines:
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: yatri-db-secret
   type: Opaque
   stringData:
     POSTGRES_PASSWORD: secretpassword
   ```
3. **Automate with Secrets Controllers:**  
   Use External Secrets Operator or HashiCorp Vault integration in production pipelines to eliminate manual base64 encoding errors completely.
