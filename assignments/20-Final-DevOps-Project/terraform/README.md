# Cloud Infrastructure as Code (Terraform)

This module provisions cloud infrastructure for the TaskBoard application using **Terraform** with **LocalStack** support (zero cloud costs & zero AWS credentials required).

---

## 1. Architecture Components

- **VPC**: Isolated network (`10.0.0.0/16`) with DNS support & hostnames.
- **Internet Gateway**: Enables internet egress and ingress for the public subnets.
- **Subnets**:
  - 2 Public Subnets across Multi-AZ (`10.0.1.0/24`, `10.0.2.0/24`) with auto-assign public IP.
  - 2 Private Subnets across Multi-AZ (`10.0.10.0/24`, `10.0.20.0/24`).
- **Route Tables**: Default `0.0.0.0/0` route targeting the Internet Gateway.
- **Security Group**: Ingress rules for HTTP (80), HTTPS (443), FastAPI (8000), React (3000), SSH (22), and outbound egress.
- **EC2 Compute**: Virtual machine hosting Docker runtime and TaskBoard containers.
- **S3 Bucket**: Versioned bucket for artifacts, backups, and pipeline state.

---

## 2. Quickstart Execution (LocalStack)

### Step 1: Start LocalStack Container
```bash
docker run -d --name localstack -p 4566:4566 -e SERVICES=s3,ec2,sts,iam localstack/localstack:3.8.0
```

### Step 2: Initialize Terraform
```bash
cd terraform
terraform init
```

### Step 3: Validate and Plan
```bash
terraform validate
terraform plan
```

### Step 4: Provision Infrastructure
```bash
terraform apply -auto-approve
```

### Step 5: Verify Outputs
```bash
terraform output
```

### Step 6: Clean Up
```bash
terraform destroy -auto-approve
```
