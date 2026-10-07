# DevSecOps Security Policy & Governance Framework

This document outlines the DevSecOps controls, vulnerability thresholds, and shift-left security enforcement for the **TaskBoard Cloud Platform**.

---

## 1. Security Gate Architecture

```text
Developer Commit
       |
       v
[Stage 1: Secret Scanning]  ---> Detects committed API keys, tokens, credentials (Gitleaks)
       |
       v
[Stage 2: SAST (Bandit)]     ---> Python static code analysis for SQLi, XSS, unsafe deserialization
       |
       v
[Stage 3: SCA (pip-audit)]   ---> Dependency vulnerability scanning against PyPI & OSV advisory DBs
       |
       v
[Stage 4: Container Build]   ---> Non-root user, slim base images, minimal attack surface
       |
       v
[Stage 5: Trivy Scan]        ---> Scans container OS packages & application libraries for CVEs
       |
       v
[Security Gate Decision]     ---> Fails pipeline if CRITICAL/HIGH CVEs with known fixes are found
       |
       v
Registry Push & K8s Deploy
```

---

## 2. Policy Thresholds & Enforcement

| Security Control | Tool | Severity Threshold | Enforcement Action |
|---|---|---|---|
| **Secret Scanning** | Gitleaks / TruffleHog | ANY secret detected | Reject commit / Fail build |
| **SAST** | Bandit | High / Medium severity | Block pipeline until remediation |
| **SCA** | pip-audit | Critical / High CVEs | Upgrade vulnerable library |
| **Container Scan** | Trivy | Critical CVEs (with fix) | Halt container promotion |
| **Container User** | Dockerfile check | Root user (UID 0) disallowed | Run as non-root UID 10001 |
| **K8s Security** | PodSecurityContext | Privileged containers forbidden | Drop ALL capabilities |

---

## 3. Explaining Vulnerability Analysis (Viva Preparation)

### What does Trivy scan?
Trivy scans both the base operating system packages (e.g. Alpine/Debian apt packages) and the application-level language packages (e.g. Python pip packages, Node npm packages) against the National Vulnerability Database (NVD) and GitHub Advisory Database.

### What does a Clean Scan mean?
A clean scan (0 HIGH / 0 CRITICAL CVEs) verifies that:
1. Base image is up-to-date (`python:3.12-slim` and `nginx:1.27-alpine`).
2. All third-party packages in `requirements.txt` are pinned to secure, non-deprecated releases.
3. No known remote code execution (RCE) or denial of service (DoS) vulnerabilities exist in the runtime image.
