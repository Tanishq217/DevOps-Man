# AWS Services Architecture & Governance Research

**Student Name:** Tanishq  
**Enrollment Number:** 24bcs10303  
**Course:** DevOps & Cloud Engineering  
**Session:** 17 - Terraform & Infrastructure as Code  

---

## Executive Overview

This module provides an exhaustive, production-grade architectural analysis of core Amazon Web Services (AWS) building blocks across governance, compute, storage, networking, and database paradigms.

```
                    ┌─────────────────────────────────────────┐
                    │      AWS Cloud Architectural Estate     │
                    └────────────────────┬────────────────────┘
                                         │
        ┌──────────────┬─────────────────┼─────────────────┬──────────────┐
        ▼              ▼                 ▼                 ▼              ▼
   ┌─────────┐   ┌───────────┐     ┌───────────┐     ┌───────────┐  ┌───────────┐
   │ 01. IAM │   │  02. EC2  │     │  03. S3   │     │  04. VPC  │  │  05. Data │
   ├─────────┤   ├───────────┤     ├───────────┤     ├───────────┤  ├───────────┤
   │Governance   │ Elastic   │     │ Simple    │     │ Virtual   │  │ DynamoDB  │
   │Identity &   │ Compute   │     │ Storage   │     │ Private   │  │ & RDS     │
   │Access       │ Cloud     │     │ Service   │     │ Cloud     │  │ Databases │
   └─────────┘   └───────────┘     └───────────┘     └───────────┘  └───────────┘
```

---

## Directory Index & Topic Coverage

| Module | Service Domain | Key Architectural Topics Covered | Documentation Link |
|---|---|---|---|
| **01. IAM** | Security & Governance | Users, Groups, Roles, Policies, Permissions, Least Privilege, MFA, IMDSv2, Cross-Account Access | [01-iam/README.md](file:///Users/tanishqsingh/Documents/Code%20Boost/DevOps-Man/assignments/17-Terraform/aws-services/01-iam/README.md) |
| **02. EC2** | Scalable Compute | AMIs, Instance Types, SSH Key Pairs, Security Groups, EBS Storage (gp3/io2), Public/Private/Elastic IPs, Lifecycle | [02-ec2/README.md](file:///Users/tanishqsingh/Documents/Code%20Boost/DevOps-Man/assignments/17-Terraform/aws-services/02-ec2/README.md) |
| **03. S3** | Durable Object Storage | Buckets, Objects, Storage Classes, Versioning, Lifecycle Policies, Encryption (SSE-S3/KMS), Bucket Policies | [03-s3/README.md](file:///Users/tanishqsingh/Documents/Code%20Boost/DevOps-Man/assignments/17-Terraform/aws-services/03-s3/README.md) |
| **04. VPC** | Software-Defined Network | CIDR Allocation, Public/Private Subnets, Route Tables, Internet Gateways (IGW), NAT Gateways, Security Groups vs NACLs | [04-vpc/README.md](file:///Users/tanishqsingh/Documents/Code%20Boost/DevOps-Man/assignments/17-Terraform/aws-services/04-vpc/README.md) |
| **05. Databases** | NoSQL & Relational DBs | DynamoDB (Partition/Sort Keys, GSIs/LSIs, Serverless) & Amazon RDS (PostgreSQL/MySQL, Multi-AZ, Read Replicas) | [05-dynamodb-rds/README.md](file:///Users/tanishqsingh/Documents/Code%20Boost/DevOps-Man/assignments/17-Terraform/aws-services/05-dynamodb-rds/README.md) |
