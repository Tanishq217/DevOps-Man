# AWS Service Deep Dive: IAM (Identity and Access Management)

**Student Name:** Tanishq  
**Enrollment Number:** 24bcs10303  
**Course:** DevOps & Cloud Engineering  
**Module:** Session 17 - Infrastructure as Code & AWS Architecture  

---

## 1. What is AWS IAM?

**AWS Identity and Access Management (IAM)** is a foundational, web-scale security service that provides fine-grained access control and identity governance across all AWS resources and APIs. IAM is a **global service** (not tied to any specific AWS region), meaning identities and policies defined in IAM apply globally across the entire AWS cloud estate.

With IAM, you centrally control:
- **Authentication (AuthN):** *Who* can access your AWS environment (verifying identity via credentials, MFA, or federation).
- **Authorization (AuthZ):** *What* resources and actions the authenticated entity is allowed or denied to execute.

```
       ┌────────────────────────────────────────────────────────┐
       │                   AWS Cloud Perimeter                  │
       └──────────────────────────┬─────────────────────────────┘
                                  │
                       [ Incoming API Request ]
                                  │
                                  ▼
                     ┌─────────────────────────┐
                     │   Authentication (AuthN) │
                     │   - Access Keys / Tokens │
                     │   - MFA Verification     │
                     └────────────┬────────────┘
                                  │
                                  ▼
                     ┌─────────────────────────┐
                     │   Authorization (AuthZ) │
                     │   - IAM Policies        │
                     │   - Permission Boundary │
                     │   - SCP Evaluation      │
                     └────────────┬────────────┘
                                  │
                ┌─────────────────┴─────────────────┐
                ▼                                   ▼
        [ Explicit Deny? ]                 [ Explicit Allow? ]
           (YES ──► 403 Forbidden)            (YES ──► 200 OK Execution)
           (NO  ──► Check Allows)             (NO  ──► Default Deny)
```

---

## 2. Core IAM Building Blocks

### 2.1 IAM Users
An **IAM User** represents an individual person or dedicated application requiring persistent access to AWS services.
- **Root User:** Created automatically upon AWS account creation. Has unrestricted permissions across all resources and billing. **Must never be used for everyday tasks.**
- **Standard IAM User:** Has no permissions by default (implicit deny). Must be explicitly granted permissions via policies or group membership.
- **Credential Types:**
  - *Console Access:* Username + Password (+ mandatory MFA).
  - *Programmatic Access:* Access Key ID + Secret Access Key (used by AWS CLI, SDKs, and Terraform).

### 2.2 IAM Groups
An **IAM User Group** is a collection of IAM users. Groups simplify permission administration at scale by enabling policy assignment to multiple users simultaneously.
- A user can belong to multiple groups (up to 10 groups by default).
- Groups **cannot** be nested (a group cannot contain another group).
- Groups cannot be identified as a `Principal` in resource-based policies.
- Typical group structures follow corporate roles: `Admins`, `Developers`, `SecurityAuditors`, `DevOpsEngineers`.

### 2.3 IAM Roles
An **IAM Role** is an AWS identity with specific permissions, but **without persistent credentials** (no long-term passwords or access keys). Instead, roles issue temporary security credentials via the **AWS Security Token Service (STS)**.
- **AssumeRole Workflow:** An identity (human user, AWS service like EC2 or Lambda, or external identity provider via OIDC/SAML) temporarily assumes the role.
- **STS Credentials:** Temporary access key, secret key, and security token that expire automatically (typically between 15 minutes and 12 hours).
- **Core Components of a Role:**
  1. *Trust Policy (AssumeRolePolicyDocument):* Defines *who* is allowed to assume the role.
  2. *Permissions Policy:* Defines *what* actions the assumed role can perform.

### 2.4 IAM Policies
An **IAM Policy** is a formal JSON document that explicitly defines permissions. AWS supports two primary policy categories:

1. **Identity-Based Policies:** Attached directly to an IAM user, group, or role.
   - *AWS Managed Policies:* Maintained and updated by AWS (e.g., `AdministratorAccess`, `AmazonS3ReadOnlyAccess`).
   - *Customer Managed Policies:* Custom, standalone policies crafted by your team with precise scoping.
   - *Inline Policies:* Embedded directly within a single user or role (not reusable).
2. **Resource-Based Policies:** Attached directly to AWS resources (e.g., S3 Bucket Policies, KMS Key Policies, SQS Queue Policies).

---

## 3. Structure of a JSON IAM Policy

Every IAM policy follows the standard AWS Policy grammar:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ReadAndPutDevOpsBucket",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::tanishq-devops-s3-demo-24bcs10303",
        "arn:aws:s3:::tanishq-devops-s3-demo-24bcs10303/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "true"
        }
      }
    }
  ]
}
```

| Element | Description |
|---|---|
| `Version` | Language syntax version. Always set to `"2012-10-17"`. |
| `Statement` | Container array holding one or more individual permission statements. |
| `Sid` (Optional) | Statement ID: A unique human-readable tag describing the statement's purpose. |
| `Effect` | Required evaluation outcome: either `"Allow"` or `"Deny"`. |
| `Principal` | Required in resource-based policies; specifies the account/user/service being granted access. |
| `Action` | The exact API operations being permitted or denied (e.g., `s3:GetObject`, `ec2:DescribeInstances`). |
| `Resource` | The Amazon Resource Name (ARN) identifying the target entity. |
| `Condition` (Optional) | Contextual constraints under which the policy applies (IP CIDRs, MFA status, SSL transport). |

---

## 4. Permissions Evaluation Logic & The Principle of Least Privilege

### 4.1 AWS Policy Evaluation Logic
When an AWS API request arrives, IAM applies strict mathematical evaluation order:
1. **Default Deny:** All requests start implicitly denied.
2. **Explicit Deny Override:** If *any* applicable policy (identity, resource, boundary, or SCP) contains an explicit `Deny`, the request is **immediately blocked**, overriding any `Allow`.
3. **Explicit Allow Requirement:** If no explicit deny exists, at least one applicable policy must contain an explicit `Allow`.
4. **Final Decision:** If neither condition 2 nor 3 evaluates to true, the request remains denied.

```
       [ Request Received ]
                │
                ▼
      ┌───────────────────┐
      │  Explicit Deny?   │────( YES )───► [ ACCESS DENIED ]
      └─────────┬─────────┘
                │ ( NO )
                ▼
      ┌───────────────────┐
      │  Explicit Allow?  │────( YES )───► [ ACCESS GRANTED ]
      └─────────┬─────────┘
                │ ( NO )
                ▼
       [ ACCESS DENIED ]
       (Default Implicit Deny)
```

### 4.2 Principle of Least Privilege (PoLP)
The Principle of Least Privilege dictates that any identity (human or software service) should be granted **only the absolute minimum set of permissions necessary** to perform its legitimate function, and for the shortest duration required.

- Avoid broad wildcard actions like `"Action": "*"` or `"Resource": "*"`.
- Use read-only access for auditing and telemetry.
- Enforce resource-level ARNs rather than account-wide access.

---

## 5. IAM Best Practices

1. **Lock Away the AWS Account Root User:**
   - Delete root access keys.
   - Configure hardware or authenticator app Multi-Factor Authentication (MFA) with strict physical isolation.
   - Use root exclusively for account closure, billing modifications, or root-level support requests.
2. **Enforce Multi-Factor Authentication (MFA):**
   - Mandate MFA for all human users accessing the AWS Management Console.
   - Use IAM Condition keys (`aws:MultiFactorAuthPresent`) to require MFA for sensitive CLI operations.
3. **Prefer IAM Roles over Long-Lived Access Keys:**
   - Never embed hardcoded `AWS_ACCESS_KEY_ID` or `AWS_SECRET_ACCESS_KEY` in source code, Dockerfiles, or Git repositories.
   - Use **EC2 Instance Profiles** or **EKS Pod Identities** for compute workloads.
4. **Regularly Rotate & Audit Credentials:**
   - Automate key rotation every 90 days.
   - Disable or delete unused credentials after 45 days of inactivity.
5. **Implement Permission Boundaries:**
   - Define maximum allowable permissions for delegated administrators to prevent privilege escalation.
6. **Leverage AWS IAM Access Analyzer:**
   - Continuously audit resource-based policies to detect unintended public or cross-account access.

---

## 6. Common Real-World Use Cases

| Use Case | Implementation Strategy |
|---|---|
| **EC2 Web Server accessing S3** | Attach an **IAM Instance Profile (Role)** to the EC2 instance granting `s3:GetObject` on the assets bucket. EC2 automatically retrieves temporary credentials via the Instance Metadata Service (IMDSv2). |
| **CI/CD Pipeline (GitHub Actions)** | Use **OpenID Connect (OIDC) Federation** to assume a short-lived IAM role directly from GitHub Actions without storing long-lived AWS keys in GitHub secrets. |
| **Cross-Account Deployment** | Allow a centralized Deployment Account (`Account A`) to assume an `OrganizationDeployerRole` in Staging (`Account B`) or Production (`Account C`). |
| **Temporary Support Access** | Grant on-call engineers temporary elevation to a triage role via AWS IAM Identity Center (Single Sign-On) with automated session timeouts. |

---

## 7. Technical Interview / Viva Q&A

**Q1: What is the critical difference between an IAM User and an IAM Role?**  
An IAM User has persistent long-term credentials (password, secret access keys) and is typically tied to a specific person. An IAM Role has no long-term credentials; it relies on temporary tokens issued by AWS STS and can be assumed by any authorized entity (services, external accounts, federated users).

**Q2: What happens if an IAM User has an attached policy allowing `s3:*` on all buckets, but the S3 bucket policy contains an explicit `Deny` for that user's ARN?**  
The user will be **denied access**. In AWS evaluation logic, an explicit `Deny` strictly overrides all `Allow` statements across all policies.

**Q3: Why is IMDSv2 preferred over IMDSv1 for retrieving EC2 role credentials?**  
IMDSv2 is a session-oriented metadata service that requires a PUT request with a custom token header (`X-aws-ec2-metadata-token`) to obtain a session token before fetching metadata. This prevents Server-Side Request Forgery (SSRF) vulnerabilities from leaking IAM credentials to unauthorized web clients.
