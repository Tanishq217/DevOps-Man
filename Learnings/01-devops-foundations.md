# DevOps — Chapter 1: Foundations

## 1. What is DevOps?

**DevOps = Development + Operations**

DevOps is a set of practices, tools, culture, and automation techniques used to make software development and software operations work together efficiently.

Traditionally:

- **Development (Dev)** writes and changes the application.
- **Operations (Ops)** runs, deploys, maintains, and monitors the application.

The problem is that software does not become useful merely because developers write code. It must also be:

1. Built
2. Tested
3. Packaged
4. Deployed
5. Run reliably
6. Monitored
7. Updated
8. Secured

DevOps connects these activities into a continuous process.

### Simple example

Suppose we have a Spring Boot application.

Without a good DevOps process:

```text
Developer writes code
        ↓
Developer sends code to someone
        ↓
Someone manually builds it
        ↓
Someone manually tests it
        ↓
Someone manually copies files to a server
        ↓
Application runs
        ↓
Something breaks
        ↓
Someone investigates manually
```

With DevOps:

```text
Developer writes code
        ↓
Git
        ↓
CI pipeline
        ↓
Build
        ↓
Automated tests
        ↓
Security checks
        ↓
Package / Container image
        ↓
Deployment
        ↓
Monitoring
        ↓
Feedback
        ↓
Developer makes the next change
```

The goal is not simply "use many tools". The goal is to create a **reliable, repeatable, automated software delivery system**.

---

# 2. Why DevOps Exists

Common problems DevOps tries to reduce:

- Slow releases
- Manual deployment errors
- Poor communication between teams
- "It works on my machine" problems
- Difficult rollbacks
- No automated testing
- Poor visibility into production
- Infrastructure configured manually
- Security being added too late
- Applications becoming difficult to operate

DevOps addresses these through:

- Version control
- Automation
- CI/CD
- Infrastructure as Code
- Containers
- Configuration management
- Monitoring
- Security automation
- Collaboration

---

# 3. Important DevOps Principles

## 3.1 Automation

Anything performed repeatedly by humans should be considered for automation.

Examples:

- Running tests
- Building applications
- Creating Docker images
- Deploying applications
- Creating cloud infrastructure
- Installing software on servers
- Collecting monitoring data

Automation gives us:

- Speed
- Consistency
- Repeatability
- Fewer manual mistakes

---

## 3.2 Collaboration

DevOps encourages Development, Operations, Security, QA, and other teams to work together instead of operating as isolated groups.

---

## 3.3 Continuous Improvement

DevOps is not a one-time process.

We continuously:

```text
Build → Measure → Learn → Improve → Repeat
```

---

## 3.4 Everything as Code

Modern DevOps tries to represent infrastructure and processes in files that can be version-controlled.

Examples:

- Application code → Git
- CI/CD pipeline → YAML
- Infrastructure → Terraform
- Server configuration → Ansible
- Container definition → Dockerfile
- Kubernetes configuration → YAML

This makes changes reviewable and repeatable.

---

# 4. DevOps Lifecycle

A commonly used DevOps lifecycle is:

```text
Plan
  ↓
Code
  ↓
Build
  ↓
Test
  ↓
Release
  ↓
Deploy
  ↓
Operate
  ↓
Monitor
  ↓
Feedback → Plan
```

The lifecycle is continuous.

## 4.1 Plan

Decide:

- What feature should be developed?
- What bug should be fixed?
- What infrastructure is required?
- What should be deployed?

Typical activities:

- Requirements
- Task management
- Sprint planning
- Architecture planning

---

## 4.2 Code

Developers write application code.

Common tools:

- Java
- Python
- JavaScript
- Go
- Git
- GitHub / GitLab / Bitbucket

---

## 4.3 Build

Source code is converted into a deployable artifact.

For example, a Java Maven application can be compiled and packaged into a JAR.

```text
Source Code
    ↓
Compiler / Build Tool
    ↓
JAR / Artifact
```

Common build tools:

- Maven
- Gradle
- npm
- Make

---

## 4.4 Test

Tests verify whether the application behaves correctly.

Examples:

- Unit tests
- Integration tests
- API tests
- End-to-end tests
- Security tests

Automation is important because tests can run automatically whenever code changes.

---

## 4.5 Release

A tested artifact is prepared for deployment.

A release may include:

- Version number
- Build artifact
- Release notes
- Approval
- Security results

---

## 4.6 Deploy

The application is placed into an environment where it can run.

Common environments:

```text
Development
    ↓
Testing
    ↓
Staging
    ↓
Production
```

Deployment can be:

- Manual
- Semi-automated
- Fully automated

DevOps aims to make deployment repeatable and automated.

---

## 4.7 Operate

The application is running.

Operations includes:

- Server management
- Application configuration
- Scaling
- Availability
- Backups
- Incident handling

---

## 4.8 Monitor

We continuously observe the system.

We may monitor:

- CPU
- RAM
- Disk
- Network
- Application errors
- Response time
- Request rate
- Availability

Tools include:

- Prometheus
- Grafana
- Cloud monitoring services

---

# 5. DevOps Feedback Loop

Monitoring gives information about the running system.

For example:

```text
Application deployed
      ↓
Users send requests
      ↓
Metrics + logs collected
      ↓
High latency discovered
      ↓
Team investigates
      ↓
Code / infrastructure improved
      ↓
New version deployed
```

This feedback loop is one of the most important ideas in DevOps.

---

# 6. Monolithic Architecture

A monolithic application is designed as one major application unit.

Example:

```text
                Monolithic Application
        ┌───────────────────────────────┐
        │ User Management               │
        │                               │
        │ Payment                       │
        │                               │
        │ Orders                        │
        │                               │
        │ Notifications                 │
        └───────────────────────────────┘
                       │
                    Database
```

The components may be logically separated inside the code, but they are generally built and deployed together.

## Advantages

- Simple to start
- Simple deployment initially
- Easier for small applications
- Less infrastructure complexity

## Disadvantages

- Large codebase can become difficult to maintain
- Components are tightly coupled
- Scaling one feature may require scaling the entire application
- A small change may require rebuilding and redeploying the whole application
- Large applications can become harder to understand

---

# 7. Microservices Architecture

In microservices, an application is divided into smaller services.

Example:

```text
                 Application
                     │
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
   User Service   Order Service  Payment Service
       │             │             │
       ↓             ↓             ↓
    Database      Database       Database
```

Each service is responsible for a specific business capability.

## Advantages

- Services can be deployed independently
- Individual services can be scaled
- Teams can work independently
- Fault isolation can be better
- Large systems can be divided into manageable components

## Disadvantages

- More infrastructure
- Networking becomes important
- Distributed-system failures become possible
- Monitoring becomes more complicated
- Deployment becomes more complicated
- Data management becomes more complicated

### Important

Microservices are **not automatically better**.

For a small application, a monolith can be the better engineering decision.

---

# 8. CI — Continuous Integration

Continuous Integration means frequently integrating code changes into a shared codebase and automatically validating those changes.

Typical flow:

```text
Developer
   ↓
git push
   ↓
CI starts
   ↓
Build
   ↓
Tests
   ↓
Quality / Security checks
   ↓
Pass or Fail
```

Benefits:

- Bugs are discovered earlier
- Integration problems are found sooner
- Tests become repeatable
- Developers receive faster feedback

Common CI tools:

- GitHub Actions
- Jenkins
- CircleCI
- GitLab CI/CD

---

# 9. CD — Continuous Delivery vs Continuous Deployment

These terms are related but should not be treated as identical.

## Continuous Delivery

The software is automatically built, tested, and prepared so it is always ready to deploy.

A production deployment may still require a human approval.

```text
Code
 ↓
Build
 ↓
Test
 ↓
Ready for Production
 ↓
Human Approval
 ↓
Production
```

## Continuous Deployment

Every change that successfully passes the required automated checks can be automatically deployed to production.

```text
Code
 ↓
Build
 ↓
Test
 ↓
Checks
 ↓
Automatic Production Deployment
```

### Easy memory trick

- **Continuous Delivery:** always ready to deploy
- **Continuous Deployment:** automatically deploy

---

# 10. CI/CD Example

Imagine a developer changes a Java application.

```text
1. Developer edits code
2. git add
3. git commit
4. git push
5. CI pipeline starts
6. Dependencies are installed
7. Application is built
8. Tests run
9. Security/quality checks run
10. Artifact or Docker image is created
11. Deployment occurs
12. Application is monitored
```

This is a practical DevOps pipeline.

---

# 11. Core DevOps Technologies

DevOps is a broad field. We will learn these areas progressively.

## 11.1 Linux

Linux is extremely important because many servers, cloud machines, containers, and infrastructure systems run Linux.

You need to understand:

- File system
- Shell
- Commands
- Permissions
- Users
- Processes
- Services
- Networking
- Package management
- Bash scripting

---

## 11.2 Networking

DevOps engineers need networking fundamentals.

Important topics:

- IP addresses
- IPv4
- IPv6
- TCP
- UDP
- Ports
- DNS
- HTTP
- HTTPS
- SSH
- Routing
- Subnets
- Firewalls
- NAT

These will be studied properly later.

---

## 11.3 Git and GitHub

Git is a distributed version control system.

It tracks changes to files.

Important concepts:

```text
Repository
Commit
Branch
Merge
Remote
Clone
Pull
Push
Pull Request
Merge Conflict
```

GitHub is a platform for hosting Git repositories and collaborating around them.

---

## 11.4 Programming and Scripting

DevOps engineers do not necessarily need to be application developers, but programming and scripting are extremely useful.

Common languages:

- Bash
- Python
- Go

We will use scripting for automation.

---

# 12. Docker

Docker provides a way to package applications and their required environment into containers.

Important concepts:

- Image
- Container
- Dockerfile
- Volume
- Network
- Registry

Basic mental model:

```text
Dockerfile
    ↓
Docker Image
    ↓
Docker Container
```

We will study Docker separately and deeply.

---

# 13. Kubernetes

Kubernetes is a container orchestration platform.

It helps manage containers across machines.

Important concepts:

- Cluster
- Node
- Pod
- Control Plane
- Deployment
- ReplicaSet
- Service
- ConfigMap
- Secret
- Namespace

Cloud Kubernetes services include:

- AWS EKS
- Azure AKS
- Google GKE

We will study Kubernetes after understanding Docker and networking.

---

# 14. Terraform

Terraform is an Infrastructure as Code tool.

Instead of manually creating infrastructure, infrastructure can be described using configuration files.

Concept:

```text
Terraform Configuration
        ↓
Terraform
        ↓
Cloud Provider API
        ↓
Infrastructure
```

Examples of resources:

- Virtual machines
- Networks
- Databases
- Storage
- Kubernetes resources

---

# 15. Ansible

Ansible is commonly used for configuration management and automation.

Example:

```text
10 servers
   ↓
Ansible
   ↓
Install Nginx
Configure Nginx
Start Nginx
```

Instead of manually connecting to every server, automation can perform the same operation consistently.

---

# 16. Monitoring

Monitoring tells us what is happening in our systems.

Important metrics:

- CPU usage
- Memory usage
- Disk usage
- Network traffic
- Request count
- Error rate
- Latency
- Availability

### Prometheus

Prometheus is commonly used for collecting and storing metrics.

### Grafana

Grafana is commonly used to visualize metrics using dashboards.

Simple relationship:

```text
Application / Servers
        ↓
     Metrics
        ↓
   Prometheus
        ↓
     Grafana
        ↓
    Dashboard
```

---

# 17. DevSecOps

DevSecOps means integrating security into the software delivery lifecycle instead of treating security as a final step.

Traditional idea:

```text
Develop → Deploy → Security Check
```

DevSecOps:

```text
Plan
 ↓
Code + Security
 ↓
Build + Security
 ↓
Test + Security
 ↓
Deploy + Security
 ↓
Monitor + Security
```

Security becomes continuous.

---

# 18. SAST

**SAST = Static Application Security Testing**

SAST analyzes source code or compiled code without executing the application in its normal running environment.

It can help identify:

- Vulnerable coding patterns
- Security issues
- Code quality problems

Example tool:

- SonarQube

---

# 19. DAST

**DAST = Dynamic Application Security Testing**

DAST tests an application while it is running.

Concept:

```text
Running Application
       ↑
       │
 Security Testing
       │
       ↓
Potential vulnerabilities
```

SAST and DAST are different:

| SAST | DAST |
|---|---|
| Tests code/application artifacts | Tests running application |
| Static analysis | Dynamic testing |
| Usually earlier in lifecycle | Usually after application is running |

---

# 20. OWASP

OWASP stands for **Open Worldwide Application Security Project**.

It provides widely used application-security knowledge and guidance.

One famous resource is the **OWASP Top 10**, which describes major categories of web application security risks.

---

# 21. Trivy

Trivy is a security scanner commonly used to scan:

- Container images
- Filesystems
- Git repositories
- Infrastructure-as-Code configurations

Example DevSecOps flow:

```text
Application
    ↓
Docker Image
    ↓
Trivy Scan
    ↓
Vulnerabilities?
   ↙       ↘
 Yes       No
 ↓          ↓
Fix       Continue
```

---

# 22. Important DevOps Job Roles

## DevOps Engineer

Focuses on automation, CI/CD, infrastructure, deployment, cloud, and operational reliability.

## Site Reliability Engineer (SRE)

Focuses strongly on reliability, availability, performance, automation, and production systems.

## Platform Engineer

Builds internal platforms and tools that make it easier for developers to build and deploy applications.

## Cloud Engineer

Works heavily with cloud infrastructure and services.

## Infrastructure Engineer

Focuses on infrastructure such as compute, networking, storage, operating systems, and automation.

## DevSecOps Engineer

Combines DevOps with security automation and security practices.

## MLOps Engineer

Applies DevOps principles to machine-learning systems.

Typical concerns include:

- Model deployment
- Model versioning
- Data/model pipelines
- Monitoring

## AIOps

AIOps generally refers to using AI/ML techniques to improve IT operations, monitoring, incident analysis, and automation.

## System Administrator

Manages systems such as servers, users, operating systems, services, storage, and networking.

## Solution Architect

Designs high-level technical solutions and makes architectural decisions across systems and services.

## AI Cloud Engineer

Works at the intersection of cloud infrastructure and AI workloads.

## Developer Advocate

Helps developers understand and use technologies through education, documentation, demos, talks, and community work.

---

# 23. Emerging DevOps Trends

## AI in DevOps

AI can assist with:

- Log analysis
- Incident investigation
- Code generation
- Test generation
- Anomaly detection
- Infrastructure assistance
- Documentation

AI does not remove the need to understand the underlying systems.

## GitOps

GitOps treats Git as a central source of truth for managing infrastructure and application deployment.

A simplified idea:

```text
Git Repository
      ↓
Desired Configuration
      ↓
Automation
      ↓
Environment
```

---

# 24. The Most Important Mental Model

Do not try to memorize DevOps as a list of tools.

Think about the problem being solved:

```text
Code
 ↓
Version Control
 ↓
Build
 ↓
Test
 ↓
Security
 ↓
Package
 ↓
Deploy
 ↓
Operate
 ↓
Monitor
 ↓
Improve
```

Tools are selected to automate these stages.

---

# 25. DevOps Learning Roadmap

Our learning sequence will be:

```text
1. DevOps Foundations
2. Linux
3. Shell / Bash
4. Networking
5. Git + GitHub
6. CI/CD
7. Docker
8. Cloud Fundamentals
9. AWS / Azure / Cloud Services
10. Terraform
11. Ansible
12. Kubernetes
13. Monitoring
14. DevSecOps
15. Real DevOps Project
16. Revision + Exam Preparation
```

The exact order can be adjusted according to the college course.

---

# 26. Exam Preparation Strategy

For every topic, learn four things:

### 1. Definition

What is it?

### 2. Why

Why do we need it?

### 3. How

How does it work?

### 4. Hands-on

Can I actually use it?

For example:

```text
Docker

Definition:
Containerization platform/tooling.

Why:
Package applications consistently.

How:
Images are used to create containers.

Hands-on:
Build and run an image.
```

This approach is much stronger than memorizing definitions alone.

---

# 27. Chapter 1 Quick Revision

### DevOps

Development + Operations; practices and culture for reliable, automated software delivery and operations.

### CI

Continuously integrate and validate code changes.

### Continuous Delivery

Keep software continuously ready for deployment.

### Continuous Deployment

Automatically deploy successful changes.

### Monolith

One major application unit.

### Microservices

Application divided into independently deployable services.

### Docker

Containerization technology.

### Kubernetes

Container orchestration platform.

### Terraform

Infrastructure as Code tool.

### Ansible

Automation/configuration-management tool.

### Prometheus

Metrics collection and monitoring system.

### Grafana

Visualization and dashboards.

### SAST

Static Application Security Testing.

### DAST

Dynamic Application Security Testing.

### DevSecOps

Security integrated throughout DevOps.

---

# 28. Key Exam Questions

1. What is DevOps?
2. Why is DevOps needed?
3. Explain the DevOps lifecycle.
4. Explain Continuous Integration.
5. Differentiate Continuous Delivery and Continuous Deployment.
6. Compare monolithic and microservices architecture.
7. What is Docker?
8. What is Kubernetes?
9. What is Infrastructure as Code?
10. What is Terraform?
11. What is Ansible?
12. What is monitoring?
13. What are Prometheus and Grafana?
14. What is DevSecOps?
15. Differentiate SAST and DAST.
16. What is OWASP?
17. What is Trivy?
18. What is GitOps?
19. Explain the role of a DevOps Engineer.
20. Explain the relationship between development, deployment, and operations.
