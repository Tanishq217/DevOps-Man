# AWS Service Deep Dive: VPC (Virtual Private Cloud)

**Student Name:** Tanishq  
**Enrollment Number:** 24bcs10303  
**Course:** DevOps & Cloud Engineering  
**Module:** Session 17 - Infrastructure as Code & AWS Architecture  

---

## 1. What is AWS VPC?

**Amazon Virtual Private Cloud (Amazon VPC)** is a foundational networking service that enables you to provision a logically isolated, software-defined virtual network within the AWS Cloud. Within your VPC, you retain complete administrative control over your virtual networking environment, including selection of IP address ranges, subnet topology, configuration of route tables, and network gateway integration.

A VPC spans all Availability Zones (AZs) within a single AWS Region, providing a private perimeter for hosting compute instances (EC2, ECS, EKS) and data repositories (RDS, ElastiCache).

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │                      AWS Region: ap-south-1 (Mumbai)                   │
 │                                                                        │
 │  ┌──────────────────────────────────────────────────────────────────┐  │
 │  │                 Amazon VPC (CIDR: 10.0.0.0/16)                   │  │
 │  │                                                                  │  │
 │  │  ┌─────────────────────────────┐  ┌───────────────────────────┐  │  │
 │  │  │ Public Subnet (10.0.1.0/24) │  │ Private Subnet (10.0.2.0) │  │  │
 │  │  │ - Availability Zone: 1a     │  │ - Availability Zone: 1a   │  │  │
 │  │  │ - NAT Gateway (Public IP)   │  │ - Backend App Servers     │  │  │
 │  │  │ - Public Load Balancer      │  │ - Private RDS Databases   │  │  │
 │  │  └──────────────┬──────────────┘  └─────────────┬─────────────┘  │  │
 │  │                 │ Route Table                   │ Route Table    │  │
 │  │                 │ (0.0.0.0/0 -> IGW)            │ (0.0.0.0/0->NAT│  │
 │  │                 ▼                               ▼                │  │
 │  │  ┌─────────────────────────────┐  ┌───────────────────────────┐  │  │
 │  │  │  Internet Gateway (IGW)     │  │  NAT Gateway              │  │  │
 │  │  └──────────────┬──────────────┘  └───────────────────────────┘  │  │
 │  └─────────────────┼────────────────────────────────────────────────┘  │
 └────────────────────┼───────────────────────────────────────────────────┘
                      ▼
               [ Public Internet ]
```

---

## 2. Core VPC Networking Primitives

### 2.1 CIDR (Classless Inter-Domain Routing)
When creating a VPC, you assign an IPv4 CIDR block (typically from private RFC 1918 address spaces).
- **Recommended VPC Block:** `/16` block (provides $2^{16} = 65,536$ private IP addresses, e.g., `10.0.0.0/16`).
- **Allowable Block Sizes:** Between `/16` (largest, 65,536 IPs) and `/28` (smallest, 16 IPs).
- **Reserved IPs per Subnet:** In every subnet, AWS reserves the first 4 and last 1 IP address (total of 5 IPs reserved for network, router, DNS, future use, and broadcast).

### 2.2 Subnets
A **Subnet** is a discrete segment of your VPC's IP address range allocated to a specific Availability Zone.
- **Public Subnet:** A subnet whose associated route table has a route to an Internet Gateway (`0.0.0.0/0 -> igw-xxxx`). Instances launched here can receive public IPv4 addresses and communicate directly with the internet.
- **Private Subnet:** A subnet whose route table does NOT route directly to an IGW. Instances have private IPs only and are isolated from inbound internet traffic.
- **Multi-AZ Resilience:** Best practices mandate creating at least two public and two private subnets across two distinct Availability Zones for high availability.

### 2.3 Route Tables
A **Route Table** contains a set of rules (routes) that determine where network traffic from your subnet or gateway is directed:
- **Local Route:** Every VPC route table contains a default immutable `local` route (e.g., `10.0.0.0/16 -> local`) allowing internal communication between all subnets within the VPC.
- **Custom Routes:** Explicit destination CIDRs paired with target gateways (e.g., `0.0.0.0/0 -> igw-xxxx` or `0.0.0.0/0 -> nat-xxxx`).

### 2.4 Internet Gateway (IGW)
An **Internet Gateway** is a horizontally scaled, redundant, and highly available VPC component that enables bidirectional communication between instances in your VPC and the internet.
- Performs 1-to-1 Network Address Translation (NAT) between private and public IPv4 addresses.
- Imposes zero availability risk or bandwidth bottleneck on your network traffic.

### 2.5 NAT Gateway (Network Address Translation)
A **NAT Gateway** enables instances in a **private subnet** to connect to services outside your VPC (e.g., for operating system security updates, downloading npm/pip packages) while preventing external internet entities from initiating inbound connections to those private instances.
- **Deployment Location:** Must always be deployed within a **Public Subnet**.
- **Elastic IP Requirement:** Requires an allocated Elastic IP (static public IPv4) for outbound translation.
- **Route Table Association:** The private subnet's route table directs internet-bound traffic (`0.0.0.0/0`) to the NAT Gateway target ID (`nat-xxxx`).

---

## 3. Defense-in-Depth: Security Groups vs. Network ACLs

AWS implements a layered two-tier security perimeter within every VPC:

```
 Incoming Traffic ──► [ Subnet: Network ACL (NACL) ] ──► [ ENI: Security Group ] ──► EC2 Instance
```

| Feature | Security Group (SG) | Network ACL (NACL) |
|---|---|---|
| **Operating Layer** | Instance / ENI level (Virtual Firewall) | Subnet level (Boundary Firewall) |
| **State Tracking** | **Stateful:** Return traffic is automatically allowed | **Stateless:** Return traffic must be explicitly permitted in both directions |
| **Rule Capabilities**| Supports **Allow** rules only (Implicit deny all else) | Supports both **Allow** and **Deny** rules |
| **Rule Order** | Evaluates **all rules** before granting access | Evaluates rules in strict **numerical order** (lowest number first) |
| **Ephemerality** | Automatic connection tracking | Requires opening ephemeral ports (1024–65535) for return traffic |

---

## 4. Architectural Comparison: Public vs. Private Subnets

| Characteristic | Public Subnet | Private Subnet |
|---|---|---|
| **Internet Reachability** | Inbound & Outbound over Internet | Outbound ONLY (via NAT Gateway); Zero Inbound |
| **Default Route Target** | `0.0.0.0/0` $\to$ **Internet Gateway (IGW)** | `0.0.0.0/0` $\to$ **NAT Gateway (in public subnet)** |
| **Auto-assign Public IP** | Enabled (`MapPublicIpOnLaunch = true`) | Disabled (`MapPublicIpOnLaunch = false`) |
| **Workloads Hosted** | Public ALBs, NAT Gateways, Bastion Hosts | Application Microservices, EKS Worker Nodes, RDS DBs |
| **Security Risk Profile** | Moderate; exposed to internet port scans | Minimal; air-gapped from direct internet routing |

---

## 5. Technical Interview / Viva Q&A

**Q1: Why does a subnet with a CIDR of `/24` have 251 usable IP addresses instead of 256?**  
In any AWS subnet, AWS reserves 5 IP addresses:
1. `10.0.0.0`: Network address.
2. `10.0.0.1`: Reserved by AWS for the VPC router.
3. `10.0.0.2`: Reserved by AWS for DNS resolution (Route 53 Resolver).
4. `10.0.0.3`: Reserved by AWS for future use.
5. `10.0.0.255`: Network broadcast address (broadcast is not supported in VPC, but reserved).  
$256 - 5 = 251$ usable addresses.

**Q2: What is the difference between a NAT Gateway and a NAT Instance?**  
A NAT Gateway is a fully managed AWS service that scales automatically up to 45 Gbps, requires no OS management or security patching, and provides built-in high availability. A NAT Instance is an individual EC2 instance running Linux iptables, which requires manual maintenance, failover scripting, and instance sizing.

**Q3: Can instances in two different subnets within the same VPC communicate by default?**  
Yes. Every route table inside a VPC contains an immutable default `local` route covering the entire VPC CIDR block. As long as Security Groups and NACLs permit the traffic, all subnets route to each other privately without traversing gateways.
