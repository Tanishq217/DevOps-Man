# AWS Service Deep Dive: EC2 (Elastic Compute Cloud)

**Student Name:** Tanishq  
**Enrollment Number:** 24bcs10303  
**Course:** DevOps & Cloud Engineering  
**Module:** Session 17 - Infrastructure as Code & AWS Architecture  

---

## 1. What is AWS EC2?

**Amazon Elastic Compute Cloud (Amazon EC2)** is an Infrastructure-as-a-Service (IaaS) offering that provides scalable, secure, and resizable virtual compute capacity in the AWS cloud. EC2 eliminates the need to invest in physical hardware upfront, enabling developers to provision virtual server instances in minutes.

Key characteristics:
- **Elasticity:** Compute capacity can scale dynamically up or down in response to fluctuating web application traffic using Auto Scaling Groups (ASG).
- **Pay-as-you-go:** Billing is calculated per second or per hour based on instance type and operating system.
- **Complete Control:** Administrative root/Administrator-level access to the operating system via SSH (Linux) or RDP (Windows).

```
   ┌─────────────────────────────────────────────────────────────┐
   │                     Amazon EC2 Instance                     │
   │                                                             │
   │  ┌──────────────────┐  ┌──────────────────┐  ┌───────────┐  │
   │  │  Virtual CPUs    │  │   System RAM     │  │ OS Image  │  │
   │  │  (vCPU Cores)    │  │   (GiB Memory)   │  │   (AMI)   │  │
   │  └──────────────────┘  └──────────────────┘  └───────────┘  │
   │                                                             │
   │  Attached Storage:                     Network Interfaces:  │
   │  - Root EBS Volume (gp3/io2)           - Elastic Network    │
   │  - Optional Instance Store               Interface (ENI)    │
   │                                        - Private IP / Pub IP│
   │                                                             │
   │  Security Boundaries:                                       │
   │  - Security Group (Stateful Firewall)                       │
   │  - IAM Instance Profile (Temporary STS Credentials)         │
   └─────────────────────────────────────────────────────────────┘
```

---

## 2. Fundamental Architectural Components

### 2.1 Amazon Machine Image (AMI)
An **AMI** is a pre-configured template containing the software configuration (operating system, application server, runtime libraries, and packages) required to launch an EC2 instance.
- **AWS Provided AMIs:** Official Amazon Linux 2023, Ubuntu, Red Hat Enterprise Linux, Debian, Windows Server.
- **Custom AMIs (Golden Images):** Customized images pre-baked with company tooling, hardened security policies, and application binaries using tools like HashiCorp Packer.
- **AWS Marketplace AMIs:** Pre-packaged software from certified third-party vendors (e.g., CIS hardened OS, Palo Alto firewalls).
- **Community AMIs:** Publicly shared images created by the AWS developer community.

### 2.2 EC2 Instance Types & Families
AWS categorizes EC2 instances into distinct families optimized for specific workload profiles:

| Family | Prefix | Target Workloads | Example |
|---|---|---|---|
| **General Purpose** | `t3`, `t4g`, `m6i`, `m7g` | Balanced compute, memory, and networking; web servers, small databases, code repos | `t3.micro` (2 vCPU, 1 GiB RAM) |
| **Compute Optimized** | `c6i`, `c7g` | High-performance CPU tasks; batch processing, media transcoding, scientific modeling | `c7g.xlarge` (4 vCPU, 8 GiB RAM) |
| **Memory Optimized** | `r6i`, `r7g`, `x2idn` | In-memory caches, high-performance relational/NoSQL databases (Redis, SAP HANA) | `r6i.2xlarge` (8 vCPU, 64 GiB RAM) |
| **Storage Optimized** | `i3en`, `d3`, `d3en` | High sequential read/write operations; data warehouses, distributed file systems | `i3en.large` (2 vCPU, 16 GiB RAM) |
| **Accelerated Computing**| `p4de`, `g5` | Hardware GPU accelerators; machine learning training, LLM inference, 3D rendering | `g5.xlarge` (NVIDIA A10G GPU) |

### 2.3 Key Pairs (Authentication)
EC2 uses asymmetric public-key cryptography to authenticate connections:
- **Public Key:** Stored securely by AWS and injected into `~/.ssh/authorized_keys` inside the instance during initial boot.
- **Private Key (`.pem` / `.ppk`):** Kept strictly confidential on the developer's local machine. Used with SSH:
  ```bash
  chmod 400 my-keypair.pem
  ssh -i my-keypair.pem ec2-user@<public-ip>
  ```
- **Modern Alternative:** AWS Systems Manager (SSM) **Session Manager** allows secure browser-based and CLI shell access *without* opening inbound port 22 or managing key pair files.

### 2.4 Security Groups (Virtual Firewalls)
A **Security Group** acts as a stateful virtual firewall controlling inbound and outbound traffic at the individual instance network interface level.
- **Stateful Nature:** If an inbound request is permitted on a port, the outbound response is **automatically allowed**, regardless of outbound rules.
- **Rule Structure:** Protocols (TCP, UDP, ICMP), Port ranges (e.g., 22, 80, 443), and Source/Destination (IP CIDR, prefix list, or another Security Group ID).
- **Default Behavior:** By default, all inbound traffic is blocked, and all outbound traffic is permitted.

### 2.5 Elastic Block Store (EBS)
**Amazon EBS** provides persistent, high-performance block-level storage volumes designed for use with EC2 instances.
- **Persistence:** Unlike ephemeral *Instance Store* storage (which is wiped upon instance stop), EBS volume data persists across instance stops and starts.
- **Volume Types:**
  - `gp3` (General Purpose SSD): Baseline 3,000 IOPS and 125 MB/s throughput; cost-effective default.
  - `io2` (Provisioned IOPS SSD): Sub-millisecond latency for mission-critical databases; up to 256,000 IOPS.
  - `st1` (Throughput Optimized HDD): Low-cost magnetic storage for large streaming workloads.
- **EBS Snapshots:** Incremental point-in-time backups stored with $11\times9\text{s}$ durability in Amazon S3.

---

## 3. Public vs. Private IP Addresses & Elastic IPs

| IP Type | Persistence Across Stop/Start | Routable Over Internet | Cost | Typical Use Case |
|---|---|---|---|---|
| **Private IPv4** | Retained for instance lifespan | No (Internal VPC only) | Free | Inter-service communication, database backends |
| **Public IPv4** | **Lost** and re-allocated upon stop/start | Yes (Public internet) | Hourly IPv4 charge | Disposable dev/test public web servers |
| **Elastic IP (EIP)**| **Static & Persistent** until released | Yes (Public internet) | Free while attached to a running instance | Production public API endpoints, Bastion hosts |

---

## 4. EC2 Instance Lifecycle

An EC2 instance transitions through discrete operational states:

```
           [ Launch Request ]
                   │
                   ▼
             ┌───────────┐
             │  pending  │
             └─────┬─────┘
                   │ (Boot Completed)
                   ▼
            ┌─────────────┐   Stop Action   ┌─────────────┐
            │   running   │────────────────►│  stopping   │
            └──────┬──────┘                 └──────┬──────┘
                   │                               │
        Reboot     │                               ▼
      (Preserves   │                        ┌─────────────┐
        Memory)    │                        │   stopped   │
                   │                        └──────┬──────┘
                   │                               │
                   │ Terminate Action              │ Start Action
                   ▼                               ▼
            ┌───────────────┐               (Returns to
            │ shutting-down │                'pending')
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │  terminated   │
            └───────────────┘
```

1. **Pending:** The instance is being provisioned on physical hardware; EBS volumes are attaching.
2. **Running:** Operating system has booted; network interface is active and passing status checks.
3. **Stopping / Stopped:** Operating system halts. RAM is cleared. Public IPv4 is released. Root EBS volume data is preserved. Compute charges stop.
4. **Shutting-down / Terminated:** The virtual instance is destroyed permanently. The root EBS volume is deleted (unless `DeleteOnTermination=false` was configured).

---

## 5. Common Production Use Cases

| Use Case | Recommended Configuration |
|---|---|
| **High-Traffic Web Applications** | EC2 `t3`/`m6i` instances behind an Application Load Balancer (ALB) managed by an Auto Scaling Group across multiple Availability Zones. |
| **High-Performance Relational DBs** | Memory Optimized `r6i` instances with provisioned IOPS `io2` EBS volumes and automated snapshot lifecycles. |
| **Batch Processing & Worker Queues** | Amazon EC2 **Spot Instances** (spare AWS compute at up to 90% discount) polling work from Amazon SQS queues. |
| **Bastion Host / Jump Server** | Hardened minimal `t3.nano` instance in a public subnet allowing SSH traffic solely from the corporate office CIDR. |

---

## 6. Technical Interview / Viva Q&A

**Q1: What is the primary difference between Security Groups and Network ACLs (NACLs)?**  
Security Groups operate at the instance level (ENI) and are **stateful** (return traffic is automatically allowed). NACLs operate at the subnet boundary and are **stateless** (return traffic must be explicitly allowed in both inbound and outbound rule tables).

**Q2: What happens to data stored on an Instance Store volume versus an EBS volume when an instance is stopped?**  
Data on an Instance Store volume is **permanently lost** because the physical host hardware is released. Data on an EBS volume remains intact and is re-attached when the instance is restarted.

**Q3: How do EC2 Spot Instances work and when should they NOT be used?**  
Spot Instances let you take advantage of unused EC2 capacity at steep discounts. However, AWS can reclaim the instance with a 2-minute interruption notice if capacity is needed elsewhere. They should **never** be used for critical single-node databases or stateful applications that cannot tolerate abrupt termination.
