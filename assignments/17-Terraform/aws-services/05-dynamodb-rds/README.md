# AWS Service Deep Dive: DynamoDB & RDS (Database Services)

**Student Name:** Tanishq  
**Enrollment Number:** 24bcs10303  
**Course:** DevOps & Cloud Engineering  
**Module:** Session 17 - Infrastructure as Code & AWS Architecture  

---

## 1. Overview of AWS Database Paradigms

Modern cloud architectures distinguish fundamentally between **NoSQL Key-Value/Document Datastores** (optimized for horizontal elasticity, predictable single-digit millisecond latency, and flexible schemas) and **Relational Database Management Systems (RDBMS)** (optimized for ACID transactions, complex SQL joins, and relational integrity).

```
                             ┌───────────────────────────────┐
                             │     AWS Database Services     │
                             └───────────────┬───────────────┘
                                             │
                    ┌────────────────────────┴────────────────────────┐
                    ▼                                                 ▼
     ┌─────────────────────────────┐                   ┌─────────────────────────────┐
     │       Amazon DynamoDB       │                   │         Amazon RDS          │
     │      (NoSQL Database)       │                   │    (Relational Database)    │
     ├─────────────────────────────┤                   ├─────────────────────────────┤
     │ - Serverless & Auto-scaling │                   │ - Managed RDBMS Engines     │
     │ - Single-digit ms latency   │                   │ - ACID Transactions & Joins │
     │ - Key-Value & Document      │                   │ - Multi-AZ High Availability│
     │ - Partition + Sort Keys     │                   │ - Read Replicas             │
     └─────────────────────────────┘                   └─────────────────────────────┘
```

---

## 2. Amazon DynamoDB: Serverless NoSQL

### 2.1 Core Concepts
**Amazon DynamoDB** is a fully managed, serverless, key-value and document database designed for internet-scale applications requiring consistent, single-digit millisecond performance at any scale.

- **Tables:** The top-level collection of data items (analogous to a relational table).
- **Items:** A single record within a table, consisting of multiple attributes (analogous to a relational row). Items can have up to 400 KB in size.
- **Attributes:** The fundamental data elements (analogous to relational columns/fields). Except for primary key attributes, DynamoDB is **schema-less**; items in the same table can possess entirely different attributes.

### 2.2 Primary Key Architectures
DynamoDB uniquely identifies every item using one of two primary key designs:

1. **Simple Primary Key (Partition Key / Hash Key):**
   - Composed of a single attribute.
   - DynamoDB feeds the partition key value into an internal cryptographic hash function to determine the physical storage partition where the item resides.
   - *Example:* `UserID = "usr_1092"`
2. **Composite Primary Key (Partition Key + Sort Key / Range Key):**
   - Composed of two attributes: a **Partition Key (PK)** and a **Sort Key (SK)**.
   - All items sharing the same PK are stored together in physical proximity, sorted in ascending order by SK.
   - Allows complex range queries (e.g., `begins_with`, `between`, `<`, `>`).
   - *Example:* PK: `CustomerID = "c_442"`, SK: `OrderTimestamp = "2026-10-07T12:00:00Z"`

### 2.3 Secondary Indexes
- **Global Secondary Index (GSI):** An index with a partition key and an optional sort key that can be different from those on the base table. Can be queried across all partitions.
- **Local Secondary Index (LSI):** An index that has the same partition key as the base table, but a different sort key. Scoped strictly to a single partition.

### 2.4 Capacity & Billing Modes
- **On-Demand Mode:** Automatically adapts to application traffic spikes; charges strictly per read/write request unit without manual capacity planning.
- **Provisioned Mode:** Specify dedicated Read Capacity Units (RCUs) and Write Capacity Units (WCUs) with optional Auto Scaling for predictable, steady-state workloads.

### 2.5 DynamoDB Real-World Use Cases
- High-volume user session management and authentication tokens.
- Real-time IoT sensor telemetry and time-series metrics.
- Global gaming leaderboards and player profiles.
- E-commerce shopping carts and order processing pipelines.

---

## 3. Amazon RDS: Managed Relational Database Service

### 3.1 Core Architecture
**Amazon Relational Database Service (Amazon RDS)** automates time-consuming administrative tasks such as hardware provisioning, database setup, patching, automated backups, and failure detection.

### 3.2 Supported Database Engines
1. **Amazon Aurora:** Cloud-native MySQL and PostgreSQL-compatible engine offering up to $5\times$ the throughput of standard MySQL.
2. **PostgreSQL:** Industry-standard open-source object-relational database.
3. **MySQL:** Popular open-source web application database.
4. **MariaDB:** Community-driven drop-in MySQL fork.
5. **Oracle:** Enterprise commercial database (BYOL or License Included).
6. **Microsoft SQL Server:** Enterprise commercial database.

### 3.3 Security & Isolation
- **VPC Subnet Groups:** RDS instances are placed in private subnets across $\ge 2$ Availability Zones with zero public internet exposure.
- **Security Groups:** Inbound port access (e.g., 5432 for PostgreSQL, 3306 for MySQL) restricted strictly to application security group IDs.
- **Encryption at Rest:** Automated encryption of storage volumes, automated backups, read replicas, and snapshots via AWS KMS (AES-256).
- **IAM Database Authentication:** Authenticate to database instances using IAM roles instead of hardcoded database user passwords.

### 3.4 High Availability & Disaster Recovery

#### Multi-AZ Deployments
- Automatically provisions and maintains a **synchronous standby replica** in a different Availability Zone within the same Region.
- In the event of primary instance failure or infrastructure maintenance, RDS triggers an **automated failover** in under 60–120 seconds with zero data loss (RPO = 0) by seamlessly redirecting the database CNAME endpoint.

```
       [ Application Servers ]
                  │
                  ▼ (DB CNAME Endpoint)
        ┌───────────────────┐
        │ Primary RDS (AZ 1)│
        └─────────┬─────────┘
                  │ Synchronous Replication
                  ▼ (Zero Data Loss)
        ┌───────────────────┐
        │ Standby RDS (AZ 2)│
        └───────────────────┘
```

#### Read Replicas
- Uses **asynchronous replication** to offload read-heavy SQL workloads from the primary writer instance.
- Can create up to 15 read replicas (or 15 for Aurora) across the same AZ, across different AZs, or across different AWS Regions.
- Can be independently promoted to a standalone primary database for regional disaster recovery.

---

## 4. Comprehensive Architectural Comparison: DynamoDB vs. RDS

| Dimension | Amazon DynamoDB | Amazon RDS |
|---|---|---|
| **Data Model** | NoSQL Key-Value & Document | Relational (SQL Tables with Foreign Keys) |
| **Scalability** | Horizontal auto-partitioning; limitless | Vertical instance scaling; Read Replicas for reads |
| **Transaction Model** | ACID support via `TransactWriteItems` | Full ACID transactions natively |
| **Complex Queries** | Single-table lookups, primary key range queries | Complex SQL `JOIN`, aggregations, window functions |
| **Latency Profile** | Single-digit millisecond at any concurrency | Millisecond-level; variable depending on query plan |
| **Maintenance** | 100% Serverless; zero patching or version upgrades | Minor version patching and OS maintenance windows |
| **Storage Limits** | Unlimited table size | Up to 64 TiB (or 128 TiB in Aurora) per instance |

---

## 5. Technical Interview / Viva Q&A

**Q1: What is the difference between a DynamoDB Partition Key and a Sort Key?**  
The **Partition Key** determines the physical storage partition where the item resides using an internal hash function. The **Sort Key** orders items that share the identical partition key physically adjacent to each other, allowing range searches (e.g., retrieving all orders between two dates for a specific customer).

**Q2: What is the difference between an RDS Multi-AZ Standby and a Read Replica?**  
- **Multi-AZ Standby:** Synchronous replication used purely for **High Availability and Disaster Recovery**. It cannot serve read queries; its sole job is automatic failover.
- **Read Replica:** Asynchronous replication used for **Read Scalability**. It can actively serve `SELECT` queries to reduce load on the primary writer.

**Q3: When should an architect select DynamoDB over RDS?**  
Choose DynamoDB when the application requires massive horizontal scale (millions of requests/second), simple access patterns (lookups by ID or ID + range), unpredictable bursty traffic, and low operational overhead (zero server management). Choose RDS when the application requires complex multi-table SQL joins, strict relational constraints, or compatibility with existing legacy SQL schemas.
