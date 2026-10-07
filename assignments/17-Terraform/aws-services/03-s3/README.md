# AWS Service Deep Dive: S3 (Simple Storage Service)

**Student Name:** Tanishq  
**Enrollment Number:** 24bcs10303  
**Course:** DevOps & Cloud Engineering  
**Module:** Session 17 - Infrastructure as Code & AWS Architecture  

---

## 1. What is AWS S3?

**Amazon Simple Storage Service (Amazon S3)** is an industry-leading, highly scalable, and secure **object storage service** engineered for high availability and industry-standard durability. Unlike block storage (EBS) or file storage (EFS), S3 stores data as unstructured objects within logical containers called **buckets**.

S3 is natively designed to deliver **99.999999999% (11 9s) of data durability** by automatically storing data redundantly across a minimum of three geographically separated Availability Zones (AZs) within an AWS Region.

```
       ┌────────────────────────────────────────────────────────┐
       │                   AWS S3 Object Storage                │
       └──────────────────────────┬─────────────────────────────┘
                                  │
                                  ▼
      ┌────────────────────────────────────────────────────────┐
      │  Bucket: tanishq-devops-s3-demo-24bcs10303 (ap-south-1)│
      │  - Globally Unique Namespace                           │
      │  - Regional Data Residency                             │
      │  - Default Encryption: SSE-S3 (AES-256)                │
      │  - Versioning: Enabled                                 │
      └──────────────────────────┬─────────────────────────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 ▼               ▼               ▼
          ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
          │   Object    │ │   Object    │ │   Object    │
          │ index.html  │ │ app-v1.zip  │ │ backup.sql  │
          │ (Standard)  │ │ (Intelligent│ │  (Glacier   │
          │             │ │   Tiering)  │ │   Archive)  │
          └─────────────┘ └─────────────┘ └─────────────┘
```

---

## 2. Core S3 Architectural Primitives

### 2.1 Buckets
An S3 **Bucket** is a top-level logical container for storing objects.
- **Globally Unique Namespace:** Bucket names are shared across all AWS accounts worldwide. Two accounts cannot possess buckets with the same name.
- **Naming Conventions:** 3 to 63 characters, lowercase letters, numbers, and hyphens only; no uppercase letters or underscores.
- **Regional Isolation:** Although the namespace is global, you specify the physical AWS Region where bucket data resides to satisfy data sovereignty and compliance laws.

### 2.2 Objects
An **Object** is the fundamental entity stored in S3, consisting of:
- **Key:** The unique string identifier (full path name) of the object within the bucket (e.g., `images/profile.png`).
- **Value:** The binary data payload (file size ranging from 0 bytes up to 5 TB).
- **Version ID:** A unique string identifying the object revision when versioning is active.
- **Metadata:** Key-value pairs describing the object (Content-Type, creation date, custom user tags).
- **Access Control Information:** Object-level ACLs or bucket ownership controls.

---

## 3. S3 Storage Classes Matrix

AWS offers specialized storage classes optimized for varying data access patterns and cost structures:

| Storage Class | Designed Durability | Availability | Minimum Storage Duration | Retrieval Fee | Typical Use Case |
|---|---|---|---|---|---|
| **S3 Standard** | 99.999999999% (11 9s) | 99.99% | None | None | Active website assets, dynamic big data analytics |
| **S3 Intelligent-Tiering** | 99.999999999% (11 9s) | 99.9% | None | None | Unpredictable or unknown access patterns (automatic cost optimization) |
| **S3 Standard-IA** (Infrequent Access) | 99.999999999% (11 9s) | 99.9% | 30 days | Per-GB fee | Disaster recovery backups, long-term reference stores |
| **S3 One Zone-IA** | 99.999999999% (11 9s in 1 AZ) | 99.5% | 30 days | Per-GB fee | Secondary copies, reproducible analytical scratch data |
| **S3 Glacier Instant Retrieval** | 99.999999999% (11 9s) | 99.9% | 90 days | Per-GB fee | Medical records, media archives needing millisecond retrieval |
| **S3 Glacier Flexible Retrieval** | 99.999999999% (11 9s) | 99.9% | 90 days | Per-GB fee | Legacy backups; retrieval takes minutes to hours |
| **S3 Glacier Deep Archive** | 99.999999999% (11 9s) | 99.9% | 180 days | Per-GB fee | Long-term regulatory compliance data (lowest cost: ~$1/TB/month) |

---

## 4. Security, Versioning & Lifecycle Management

### 4.1 S3 Versioning
Enabling **Versioning** preserves, retrieves, and restores every historical version of every object stored in your bucket:
- **Accidental Overwrite Protection:** Overwriting `app.jar` assigns a new version ID while keeping the historical binary intact.
- **Accidental Deletion Protection:** Deleting an object places a **Delete Marker** on top of the object stack. The original data remains recoverable by deleting the marker.
- **MFA Delete:** Requires hardware/app TOTP MFA before permanently destroying any object version.

### 4.2 S3 Lifecycle Management Policies
Lifecycle rules automate data transitions and expirations to drastically reduce ongoing cloud expenditure:
- **Transition Actions:** Automatically shift objects from `Standard` $\to$ `Standard-IA` after 30 days $\to$ `Glacier Deep Archive` after 90 days.
- **Expiration Actions:** Automatically purge noncurrent versions after 365 days or remove incomplete multipart uploads after 7 days.

```
 [ Day 0: Object Created ] ──► S3 Standard ($0.023/GB)
            │
            ▼ (After 30 Days of Inactivity)
 [ Transition Rule 1 ]     ──► S3 Standard-IA ($0.0125/GB)
            │
            ▼ (After 90 Days)
 [ Transition Rule 2 ]     ──► S3 Glacier Deep Archive ($0.00099/GB)
            │
            ▼ (After 365 Days)
 [ Expiration Rule ]       ──► Permanently Expired & Deleted
```

### 4.3 S3 Encryption Mechanisms
S3 provides end-to-end data protection at rest and in transit:
1. **Server-Side Encryption with S3 Managed Keys (SSE-S3):** Default standard using 256-bit Advanced Encryption Standard (AES-256) at zero additional cost.
2. **Server-Side Encryption with AWS KMS (SSE-KMS):** Provides audited cryptographic control, key rotation, and separate permissions on the KMS customer managed key (CMK).
3. **Server-Side Encryption with Customer-Provided Keys (SSE-C):** Customer manages encryption keys; AWS manages cryptographic execution.
4. **Client-Side Encryption:** Data is encrypted on the client machine before transmission over HTTPS to AWS.

### 4.4 S3 Bucket Policies
A **Bucket Policy** is a resource-based JSON policy attached directly to the bucket to control access from IAM principals, external accounts, or anonymous internet users:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EnforceTLSRequestsOnly",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::tanishq-devops-s3-demo-24bcs10303",
        "arn:aws:s3:::tanishq-devops-s3-demo-24bcs10303/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

---

## 5. Common Production Use Cases

| Use Case | Implementation Strategy |
|---|---|
| **Static Website Hosting** | Configure S3 bucket for website hosting, fronted by Amazon CloudFront (CDN) with Origin Access Control (OAC) and an ACM SSL/TLS certificate. |
| **Big Data Lake & Analytics** | Store raw telemetry (Parquet/JSON) in S3 Standard; query in place with Amazon Athena, AWS Glue, and Amazon EMR without provisioning databases. |
| **Enterprise Backup & Archival** | Database dumps and filesystem snapshots synchronized to S3 with automated lifecycle rules moving older revisions to Glacier Deep Archive. |
| **Application Artifact Repository** | Store CI/CD compiled packages (JARs, tarballs, container layers) with S3 Versioning and Object Lock for immutability. |

---

## 6. Technical Interview / Viva Q&A

**Q1: What does "11 9s of Durability" mean in practice?**  
It means that if you store 10,000,000 (ten million) objects in Amazon S3, you can expect to lose on average a single object once every 10,000 years. Durability is achieved through automated synchronous erasure coding across $\ge 3$ physical availability zones.

**Q2: What is the difference between S3 Durability and S3 Availability?**  
- **Durability** guarantees that your data will not be corrupted or permanently lost.
- **Availability** measures the percentage of time that the S3 API endpoint is reachable and responsive to retrieve or upload your data (e.g., 99.99% uptime for S3 Standard).

**Q3: How does S3 Object Lock prevent ransomware and accidental data deletion?**  
S3 Object Lock enforces **WORM (Write Once, Read Many)** storage. In Compliance Mode, even the root user of the AWS account cannot delete or overwrite an object version until the retention period has elapsed.
