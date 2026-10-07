# Security Policy

## DevSecOps Security Framework

This repository adheres to automated DevSecOps continuous compliance guidelines:
- **SAST (Static Application Security Testing):** Scanned via GitHub CodeQL and Bandit.
- **SCA (Software Composition Analysis):** Scanned via pip-audit against CVE databases.
- **Secret Scanning:** Automated secret detection blocking committed keys and tokens.
- **Container Hardening:** Non-root execution and Trivy vulnerability assessment.

## Supported Versions

| Version | Supported          | Security Maintenance Status |
| ------- | ------------------ | --------------------------- |
| 1.0.x   | :white_check_mark: | Actively supported          |
| < 1.0   | :x:                | Deprecated                  |

## Reporting a Vulnerability

If you discover a security vulnerability or potential credential exposure:
1. Do not open a public GitHub issue.
2. Contact the maintainer privately: `tanishqsinghtanishq135@gmail.com`.
3. Provide steps to reproduce and potential impact.
