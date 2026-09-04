# Chapter 9 — Introduction to Kubernetes & Kubernetes Architecture

## 1. Introduction to Kubernetes

Kubernetes is an open-source platform used to **deploy, manage, scale, and operate containerized applications**.

It is commonly used when applications consist of many containers and managing those containers manually becomes difficult.

Kubernetes is also commonly abbreviated as:

```text
K8s
```

The name comes from the eight letters between:

```text
K + ubernete + s
```

Kubernetes is one of the most important technologies in modern DevOps and cloud-native environments.

---

## 2. Why Do We Need Kubernetes?

Before Kubernetes, we learned how to run containers using Docker.

For example:

```bash
docker run -d nginx
```

This works perfectly for a small number of containers.

But imagine an application running:

```text
10 containers
100 containers
1,000 containers
10,000 containers
```

Managing all of these manually becomes extremely difficult.

We would need to handle:

* Container creation
* Container failures
* Scaling
* Networking
* Load balancing
* Service discovery
* Deployment
* Updates
* Rollbacks
* Resource allocation
* High availability
* Health monitoring

This is where **container orchestration** becomes important.

---

## 3. Container Orchestration

Container orchestration means automatically managing a large number of containers.

An orchestration platform can help with:

* Deploying containers
* Starting containers
* Stopping containers
* Restarting failed containers
* Scaling applications
* Networking
* Load balancing
* Service discovery
* Rolling updates
* Rollbacks
* Resource management
* Maintaining the desired state

Kubernetes is a container orchestration platform.

---

## 4. Docker Swarm and Kubernetes

Docker Swarm is another container orchestration technology.

Historically, Docker Swarm was used to manage Docker containers across multiple machines.

However, Kubernetes became the dominant container orchestration platform because of its:

* Large ecosystem
* Extensibility
* Scalability
* Cloud-provider support
* Large community
* Rich networking capabilities
* Deployment capabilities
* Broad industry adoption

Today, Kubernetes is one of the most important platforms to understand for DevOps and cloud engineering.

---

## 5. Why Kubernetes Was Created

Kubernetes originated at Google.

Google had extensive experience running large-scale containerized workloads and developed technologies such as Borg and later Kubernetes.

Kubernetes was designed to solve problems associated with running applications at large scale.

Instead of manually managing individual containers, we describe what we want:

```text
I want:
5 copies of my application
```

Kubernetes continuously works toward maintaining that desired state.

For example:

```text
Desired:
5 Pods

Current:
4 Pods

Kubernetes:
Create 1 more Pod
```

If one fails:

```text
Desired:
5 Pods

Current:
4 Pods

Kubernetes:
Create replacement Pod
```

This is one of the fundamental ideas behind Kubernetes.

---

## 6. Kubernetes vs Docker

Docker and Kubernetes are not exactly competing technologies.

They solve different problems.

### Docker

Docker is primarily a platform/toolset for:

* Building images
* Packaging applications
* Running containers
* Managing container networks
* Managing container storage

### Kubernetes

Kubernetes is primarily a platform for:

* Orchestrating containers
* Managing workloads
* Scaling applications
* Service discovery
* Networking
* Deployments
* Self-healing
* Maintaining desired state

Conceptually:

```text
Docker
  |
  +-- Build image
  +-- Run container
  +-- Network
  +-- Volume

Kubernetes
  |
  +-- Deploy workloads
  +-- Scale workloads
  +-- Manage networking
  +-- Maintain desired state
  +-- Recover failed workloads
```

Kubernetes can use container images built using Docker or other compatible tools.

---

## 7. Important Docker Recap

Before learning Kubernetes, understand these Docker concepts:

### Images

```bash
docker images
```

### Containers

```bash
docker ps
docker ps -a
```

### Networks

```bash
docker network ls
docker network create my-network
```

### Volumes

```bash
docker volume ls
docker volume create my-volume
```

### Docker Compose

```bash
docker compose up -d
docker compose down
```

### Multi-stage Dockerfiles

Used to create optimized images with separate build and runtime stages.

---

## 8. Multi-Stage Dockerfile vs Multi-Container Application

These two concepts are easy to confuse.

### Multi-stage Dockerfile

A **single Dockerfile** contains multiple build stages.

Example:

```dockerfile
FROM node:22 AS builder

WORKDIR /app

COPY . .

RUN npm install
RUN npm run build


FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
```

The purpose is usually:

```text
Build Stage → Runtime Stage
```

It helps produce smaller and cleaner final images.

---

### Multi-container Application

A multi-container application consists of multiple containers/services.

For example:

```text
Frontend
   |
Backend
   |
Database
```

Docker Compose can manage these containers.

Example:

```text
Compose
  |
  +-- Frontend Container
  +-- Backend Container
  +-- Database Container
```

### Important difference

```text
Multi-stage build
    ↓
Multiple stages used to BUILD one final image

Multi-container application
    ↓
Multiple containers used to RUN an application
```

These are completely different concepts.

---

## 9. Kubernetes Cluster

A Kubernetes environment is called a **cluster**.

A cluster consists of:

* Control plane
* Worker nodes

Conceptually:

```text
                    Kubernetes Cluster
                           |
              +------------+------------+
              |                         |
              v                         v
        Control Plane              Worker Nodes
                                     /   |   \
                                    /    |    \
                                   v     v     v
                                 Node  Node  Node
```

---

## 10. Control Plane

The **control plane** manages the Kubernetes cluster.

It is responsible for making decisions about the cluster and maintaining the desired state.

Major control-plane components include:

1. API Server
2. etcd
3. Scheduler
4. Controller Manager

Other components may also exist in a production control plane, such as:

* Cloud Controller Manager

---

## 11. Worker Nodes

Worker nodes are the machines where application workloads run.

Worker nodes contain components such as:

1. Kubelet
2. Container runtime
3. kube-proxy (commonly deployed, but not strictly required in every networking implementation)

Worker nodes run Pods.

---

## 12. Kubernetes Architecture — High-Level View

```text
                         Kubernetes Cluster
                                 |
                +----------------+----------------+
                |                                 |
                v                                 v
         CONTROL PLANE                       WORKER NODE
                |                                 |
       +--------+--------+                +-------+-------+
       |        |        |                |       |       |
       v        v        v                v       v       v
   API Server  etcd  Scheduler         Kubelet  Runtime  kube-proxy
       |
       v
Controller Manager
```

A more practical representation:

```text
                    kubectl
                       |
                       v
                 +-----------+
                 | API Server|
                 +-----+-----+
                       |
          +------------+-------------+
          |            |             |
          v            v             v
        etcd       Scheduler   Controller Manager
                                      |
                                      |
                                      v
                              Desired State
                                      |
                                      v
                              Worker Nodes
                         +------------+------------+
                         |            |            |
                         v            v            v
                      Kubelet      Kubelet      Kubelet
                         |            |            |
                         v            v            v
                       Pods         Pods         Pods
```

---

## 13. API Server

The **Kubernetes API Server** is the central communication point for the Kubernetes control plane.

It exposes the Kubernetes API.

You can think of it as the **front door of the cluster**.

Almost all interactions with Kubernetes go through the API server.

For example:

```text
kubectl
   |
   v
API Server
   |
   +--> etcd
   +--> Scheduler
   +--> Controllers
   +--> Kubelets
```

---

## 14. `kubectl`

`kubectl` is the command-line tool used to communicate with a Kubernetes cluster.

Examples:

```bash
kubectl get pods
```

```bash
kubectl get nodes
```

```bash
kubectl get deployments
```

```bash
kubectl describe pod <pod-name>
```

When you execute:

```bash
kubectl get pods
```

the general flow is:

```text
kubectl
   |
   v
API Server
   |
   v
Kubernetes control plane
   |
   v
Response
   |
   v
kubectl
```

---

## 15. etcd

`etcd` is a distributed key-value store used by Kubernetes to store cluster state and configuration data.

It is one of the most critical components of the Kubernetes control plane.

Conceptually:

```text
Key                     Value
-----------------------------------------
cluster/config          ...
pod information         ...
deployment information  ...
service information     ...
node information        ...
```

Kubernetes uses etcd as the source of truth for much of the cluster's persistent state.

---

## 16. Why etcd Is Important

Suppose Kubernetes knows:

```text
Desired replicas = 5
```

That information needs to be stored reliably.

The control plane uses etcd to persist important cluster state.

If etcd is unavailable or corrupted, the control plane can be severely affected.

Therefore, production Kubernetes clusters need proper etcd:

* Reliability
* Backup
* Security
* High availability

---

## 17. etcd Is Not an Application Database

A common misunderstanding is:

> "etcd is the database used by my application."

No.

etcd is primarily used by Kubernetes itself for cluster state.

For example:

```text
Kubernetes
    |
    v
   etcd
    |
    +-- Cluster configuration
    +-- Object state
    +-- Metadata
```

Your application might separately use:

```text
PostgreSQL
MongoDB
MySQL
Redis
```

Those are application-level data stores.

---

## 18. Kubernetes API Server + etcd

A simplified flow:

```text
kubectl
   |
   v
API Server
   |
   v
etcd
```

Suppose we create a Deployment:

```bash
kubectl apply -f deployment.yaml
```

The request goes to the API server.

The API server validates and processes the request, and Kubernetes persists the relevant object state in etcd.

Other control-plane components observe the API and act accordingly.

---

## 19. Scheduler

The Kubernetes **Scheduler** decides which worker node should run a newly created Pod.

For example:

```text
Pod needs:
CPU = 1
Memory = 512 MB
```

Suppose:

```text
Node 1 → insufficient resources
Node 2 → enough resources
Node 3 → enough resources
```

The scheduler evaluates available nodes and selects a suitable node.

Conceptually:

```text
                 New Pod
                    |
                    v
                Scheduler
                    |
          +---------+---------+
          |         |         |
          v         v         v
        Node 1    Node 2    Node 3
          X          ✓         ✓
                    |
                    v
               Selected Node
```

---

## 20. What Does the Scheduler Consider?

Scheduling decisions can consider:

* CPU requirements
* Memory requirements
* Resource availability
* Node constraints
* Node labels
* Affinity/anti-affinity
* Taints and tolerations
* Other scheduling rules

At the introductory level, remember:

> **Scheduler decides where a Pod should run.**

---

## 21. Controller Manager

The Kubernetes **Controller Manager** runs various controllers.

Controllers continuously observe the cluster and attempt to make the actual state match the desired state.

This is a core Kubernetes concept.

---

## 22. Desired State vs Actual State

Suppose we declare:

```text
replicas: 3
```

This means:

```text
Desired State = 3 Pods
```

If currently:

```text
Actual State = 2 Pods
```

the appropriate controller notices the difference.

It takes action to create another Pod.

```text
Desired = 3
Actual  = 2

Controller
    |
    v
Create Pod
    |
    v
Actual = 3
```

This is called **reconciliation**.

---

## 23. Kubernetes Controllers

There are many controllers in Kubernetes.

Examples include:

* Deployment/ReplicaSet-related controllers
* Node Controller
* Job Controller
* Namespace Controller
* Service-related controllers
* EndpointSlice-related controllers
* StatefulSet Controller

You do not need to memorize every controller immediately.

The important idea is:

> Controllers continuously watch Kubernetes resources and take actions to move the cluster toward the desired state.

---

## 24. Node Controller

The Node Controller monitors the state of nodes.

If a node becomes unavailable, Kubernetes can detect the problem and take appropriate actions.

For example:

```text
Node 1
   |
   X
Failure
```

Kubernetes can detect that the node is unhealthy.

Depending on the workload and configuration, Pods can eventually be recreated or rescheduled on healthy nodes.

---

## 25. Worker Node

A worker node is a machine that runs Kubernetes workloads.

A cluster might look like:

```text
Control Plane
      |
      +---------------------------+
      |            |              |
      v            v              v
 Worker Node 1  Worker Node 2  Worker Node 3
      |            |              |
     Pods         Pods           Pods
```

Worker nodes can be:

* Virtual machines
* Physical machines
* Cloud instances

depending on the Kubernetes environment.

---

## 26. Kubelet

The **kubelet** is the primary agent running on each worker node.

Its responsibility is to ensure that the Pods assigned to its node are running and healthy according to the Pod specifications.

The kubelet communicates with the API server.

Conceptually:

```text
API Server
     |
     v
  Kubelet
     |
     v
  Pod
     |
     v
Containers
```

---

## 27. Responsibilities of Kubelet

The kubelet:

* Watches for Pods assigned to its node
* Works with the container runtime
* Starts containers
* Monitors containers
* Reports node/pod status
* Performs health-related management
* Sends node heartbeats/status information to the control plane

A simple way to remember:

> **Kubelet is the agent that makes sure the Pods assigned to its node are actually running.**

---

## 28. Kubelet and Heartbeats

The kubelet communicates node status to the Kubernetes control plane.

This helps Kubernetes determine whether a node is healthy.

Conceptually:

```text
Worker Node
     |
  Kubelet
     |
     | status/heartbeats
     v
API Server
```

If communication is lost for long enough, Kubernetes can determine that the node may be unavailable.

---

## 29. Container Runtime

Kubernetes needs a container runtime to actually run containers.

The container runtime is responsible for operations such as:

* Pulling images
* Creating containers
* Starting containers
* Stopping containers
* Managing container execution

Kubernetes communicates with the runtime through the **Container Runtime Interface (CRI)**.

---

## 30. Container Runtime Interface (CRI)

CRI is an interface that allows Kubernetes to communicate with container runtimes.

Conceptually:

```text
Kubelet
   |
   v
CRI
   |
   v
Container Runtime
   |
   v
Containers
```

This architecture allows Kubernetes to work with compatible container runtimes rather than being tightly coupled to one particular runtime.

---

## 31. containerd

`containerd` is a widely used container runtime in Kubernetes environments.

Modern Kubernetes does not use the old built-in Docker Engine integration (`dockershim`).

Docker Engine itself is not the Kubernetes runtime interface.

Instead, Kubernetes commonly uses runtimes such as:

```text
containerd
CRI-O
```

through CRI-compatible integration.

---

## 32. Docker and Kubernetes Runtime Relationship

A common misconception is:

```text
Kubernetes → Docker Engine → Containers
```

as the standard modern architecture.

A more accurate simplified model is:

```text
Kubelet
   |
   v
CRI
   |
   +--------+
   |        |
containerd  CRI-O
   |
   v
Containers
```

Docker remains very useful for:

* Building images
* Local container development
* Running containers
* Testing

But Kubernetes does not require Docker Engine as its container runtime.

---

## 33. kube-proxy

`kube-proxy` is a node-level networking component traditionally used to implement Kubernetes Service networking.

It helps direct network traffic toward the appropriate backend Pods.

Conceptually:

```text
Client
   |
   v
Service
   |
   v
kube-proxy / networking implementation
   |
   +----> Pod 1
   +----> Pod 2
   +----> Pod 3
```

Modern Kubernetes networking can also use other implementations, and kube-proxy is not an absolute requirement for every cluster networking design.

For foundational learning, remember:

> **kube-proxy is commonly associated with implementing Service networking on nodes.**

---

## 34. Worker Node Architecture

A simplified worker node looks like:

```text
             Worker Node
                  |
       +----------+----------+
       |          |          |
       v          v          v
   Kubelet   kube-proxy   Runtime
                              |
                              v
                            Pods
                              |
                              v
                         Containers
```

---

## 35. Complete Kubernetes Architecture

Now combine everything:

```text
                         Kubernetes Cluster
                                  |
             +--------------------+--------------------+
             |                                         |
             v                                         v
       CONTROL PLANE                              WORKER NODES
             |                                  /       |       \
             |                                 /        |        \
       +-----+------+                         v         v         v
       |     |      |                      Node 1    Node 2    Node 3
       |     |      |                        |         |         |
       v     v      v                        |         |         |
     etcd Scheduler Controller               |         |         |
             |       Manager                 |         |         |
             |                               |         |         |
             +-------------+----------------+---------+---------+
                           |
                           v
                      API Server
                           |
                           v
                        Kubelet
                           |
                           v
                         Pods
                           |
                           v
                      Containers
```

A cleaner conceptual model is:

```text
                         CONTROL PLANE
              +-----------------------------------+
              |                                   |
              |  API Server                        |
              |      |                            |
              |      +----> etcd                  |
              |      |                            |
              |      +----> Scheduler             |
              |      |                            |
              |      +----> Controller Manager    |
              |                                   |
              +----------------+------------------+
                               |
                               |
                 +-------------+-------------+
                 |             |             |
                 v             v             v
             Worker 1      Worker 2      Worker 3
                 |             |             |
             +---+---+     +---+---+     +---+---+
             |       |     |       |     |       |
          Kubelet Runtime Kubelet Runtime Kubelet Runtime
             |       |     |       |     |       |
             +---+---+     +---+---+     +---+---+
                 |             |             |
                Pods          Pods          Pods
```

---

## 36. Kubernetes Objects

Kubernetes is an **API-driven system**.

Resources that Kubernetes manages are represented as API objects/resources.

Examples include:

* Pods
* Services
* Deployments
* ReplicaSets
* ConfigMaps
* Secrets
* Namespaces
* Jobs
* CronJobs
* StatefulSets
* DaemonSets

These objects describe the desired state of applications and infrastructure managed by Kubernetes.

---

## 37. What Is a Kubernetes Object?

A Kubernetes object is a persistent representation of an intended state in the Kubernetes API.

For example:

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: nginx-deployment

spec:
  replicas: 3
```

This tells Kubernetes:

```text
I want:
3 replicas of this Deployment
```

Kubernetes then works to make reality match that specification.

---

## 38. `apiVersion`

A Kubernetes manifest commonly contains:

```yaml
apiVersion: apps/v1
```

This specifies which version of the Kubernetes API should be used for the object.

Different object types use different API groups and versions.

Examples:

```yaml
apiVersion: v1
```

```yaml
apiVersion: apps/v1
```

---

## 39. `kind`

`kind` specifies the type of Kubernetes object.

Example:

```yaml
kind: Pod
```

or:

```yaml
kind: Deployment
```

or:

```yaml
kind: Service
```

---

## 40. `metadata`

Metadata identifies and describes the object.

Example:

```yaml
metadata:
  name: my-app
```

Metadata can also include:

* Labels
* Annotations
* Namespace

Example:

```yaml
metadata:
  name: my-app
  labels:
    app: my-app
```

---

## 41. `spec`

`spec` describes the desired configuration/state of the object.

Example:

```yaml
spec:
  replicas: 3
```

This means the desired number of replicas is three.

---

## 42. Kubernetes Manifest

A Kubernetes YAML configuration is often called a **manifest**.

Example:

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: nginx

spec:
  replicas: 3

  selector:
    matchLabels:
      app: nginx

  template:
    metadata:
      labels:
        app: nginx

    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80
```

This describes a Deployment that should maintain three replicas of an Nginx Pod.

---

## 43. Desired State

Desired state is one of the most important Kubernetes concepts.

Suppose:

```yaml
replicas: 3
```

Kubernetes interprets this as:

```text
Desired State:
3 Pods
```

If one Pod crashes:

```text
Desired = 3
Actual = 2
```

Kubernetes attempts to create another Pod.

Eventually:

```text
Desired = 3
Actual = 3
```

This continuous process is called **reconciliation**.

---

## 44. Declarative vs Imperative Management

Kubernetes strongly supports a **declarative approach**.

### Imperative approach

You tell the system exactly what action to perform.

Example:

```bash
kubectl create deployment nginx --image=nginx
```

### Declarative approach

You describe the desired state:

```yaml
replicas: 3
image: nginx
```

Then apply it:

```bash
kubectl apply -f deployment.yaml
```

Kubernetes determines the actions required to reach that state.

Declarative management is particularly powerful for DevOps and Infrastructure as Code workflows.

---

## 45. Kubernetes Core Objects to Learn

As Kubernetes learning progresses, some objects are especially important.

### Pod

Smallest deployable unit in Kubernetes.

### Deployment

Manages stateless application Pods and supports features such as rolling updates.

### ReplicaSet

Maintains a specified number of Pod replicas.

### Service

Provides stable networking and service discovery for Pods.

### ConfigMap

Stores non-sensitive configuration data.

### Secret

Stores sensitive configuration data, although additional secret-management/security practices are often needed in production.

### Namespace

Provides logical isolation/grouping within a cluster.

These will be covered in greater detail in later chapters.

---

## 46. Pod — First Introduction

A **Pod** is the smallest deployable unit in Kubernetes.

A Pod usually contains one application container.

Example:

```text
Pod
 |
 +-- Container
       |
       +-- nginx
```

However, a Pod can contain multiple tightly coupled containers.

Example:

```text
Pod
 |
 +-- Application Container
 |
 +-- Sidecar Container
```

Containers in the same Pod share certain resources, including:

* Network namespace
* Pod IP address
* Volumes mounted into the Pod

---

## 47. Why Kubernetes Uses Pods

Kubernetes does not directly manage individual containers as its primary workload unit.

Instead:

```text
Kubernetes
    |
    v
   Pod
    |
    v
Container(s)
```

This allows Kubernetes to manage tightly coupled containers as a single unit.

---

## 48. Kubernetes Learning Environment — Minikube

For learning Kubernetes locally, **Minikube** is a popular option.

Minikube allows you to run a small Kubernetes cluster locally.

It is useful for:

* Learning Kubernetes
* Testing manifests
* Practicing `kubectl`
* Running Pods
* Testing Services
* Learning Deployments

---

## 49. Minikube Architecture

Conceptually:

```text
Your Mac
   |
   v
Minikube
   |
   v
Local Kubernetes Cluster
   |
   +-- Control Plane
   |
   +-- Worker Node(s)
```

The exact internal implementation depends on the Minikube driver and configuration.

---

## 50. Installing Minikube

Minikube needs:

* A supported operating system
* A container/VM driver
* `kubectl`

On macOS, a common approach is to use a container driver such as Docker if Docker Desktop is already installed.

After installation, verify:

```bash
minikube version
```

Start a cluster:

```bash
minikube start
```

Check cluster status:

```bash
minikube status
```

---

## 51. Verify Kubernetes Using kubectl

Check cluster information:

```bash
kubectl cluster-info
```

Check nodes:

```bash
kubectl get nodes
```

Example:

```text
NAME       STATUS   ROLES           AGE
minikube   Ready    control-plane   ...
```

The exact output can vary depending on your Minikube version and configuration.

---

## 52. Basic Kubernetes Commands

### Check nodes

```bash
kubectl get nodes
```

### Check Pods

```bash
kubectl get pods
```

### Check all namespaces

```bash
kubectl get pods -A
```

### Get deployments

```bash
kubectl get deployments
```

### Get services

```bash
kubectl get services
```

### Get detailed information

```bash
kubectl describe pod <pod-name>
```

---

## 53. First Kubernetes Deployment

A simple way to create a Deployment:

```bash
kubectl create deployment nginx --image=nginx
```

Check:

```bash
kubectl get deployments
```

Check Pods:

```bash
kubectl get pods
```

You should see an Nginx Pod created by the Deployment.

Conceptually:

```text
Deployment
    |
    v
ReplicaSet
    |
    v
Pod
    |
    v
Nginx Container
```

---

## 54. Scaling a Deployment

Suppose we want three replicas:

```bash
kubectl scale deployment nginx --replicas=3
```

Check:

```bash
kubectl get pods
```

You should now have multiple Pods.

Conceptually:

```text
Deployment
     |
     v
ReplicaSet
  /   |   \
 /    |    \
v     v     v
Pod  Pod   Pod
```

---

## 55. Kubernetes Self-Healing Concept

Suppose:

```text
Desired:
3 Pods
```

Current:

```text
Pod 1
Pod 2
Pod 3
```

If Pod 2 fails:

```text
Pod 1
Pod 2 ❌
Pod 3
```

The controller notices:

```text
Desired = 3
Actual = 2
```

It creates a replacement.

```text
Pod 1
Pod 3
Pod 4
```

The cluster returns toward:

```text
Desired = 3
Actual = 3
```

This is one of Kubernetes' major advantages over manually managing containers.

---

## 56. Kubernetes Scaling

Kubernetes makes it possible to scale workloads more systematically.

For example:

```text
1 Pod
 ↓
3 Pods
 ↓
10 Pods
 ↓
100 Pods
```

Scaling can be performed manually or automatically depending on the workload and configuration.

Later Kubernetes topics include:

* Horizontal Pod Autoscaler
* Vertical Pod Autoscaler
* Cluster Autoscaler

These are more advanced concepts.

---

## 57. Image Updates in Kubernetes

Suppose an application uses:

```text
myapp:v1
```

A Deployment can be updated to:

```text
myapp:v2
```

Kubernetes can perform a controlled rollout.

Conceptually:

```text
v1 → v1 → v1
```

gradually becomes:

```text
v2 → v1 → v1
```

then:

```text
v2 → v2 → v1
```

and eventually:

```text
v2 → v2 → v2
```

This is called a **rolling update**.

It avoids having to manually update every container individually.

---

## 58. Kubernetes and Desired State

The central Kubernetes philosophy can be summarized as:

```text
You declare what you want.
          ↓
Kubernetes observes actual state.
          ↓
Kubernetes compares actual vs desired state.
          ↓
Controllers take action.
          ↓
Cluster moves toward desired state.
```

This is called the **reconciliation loop**.

---

## 59. Control Plane Component Summary

| Component                | Main Responsibility                            |
| ------------------------ | ---------------------------------------------- |
| API Server               | Entry point and API communication              |
| etcd                     | Persistent cluster state storage               |
| Scheduler                | Selects nodes for Pods                         |
| Controller Manager       | Runs controllers and reconciles state          |
| Cloud Controller Manager | Integrates Kubernetes with cloud-provider APIs |

---

## 60. Worker Node Component Summary

| Component         | Main Responsibility                    |
| ----------------- | -------------------------------------- |
| Kubelet           | Manages Pods assigned to the node      |
| Container Runtime | Runs containers                        |
| CRI               | Interface between kubelet and runtime  |
| kube-proxy        | Commonly implements Service networking |

---

## 61. Kubernetes Architecture — Easy Memory Trick

Remember:

### Control Plane

```text
A E S C
```

Think:

```text
A → API Server
E → etcd
S → Scheduler
C → Controller Manager
```

### Worker Node

```text
K R P
```

Think:

```text
K → Kubelet
R → Runtime
P → kube-proxy
```

CRI connects Kubernetes/kubelet with a compatible container runtime.

---

## 62. Important Flow — Creating a Pod

Consider:

```bash
kubectl create deployment nginx --image=nginx
```

A simplified flow is:

```text
User
 |
 v
kubectl
 |
 v
API Server
 |
 +----> etcd
 |
 v
Controllers
 |
 v
Pod needs scheduling
 |
 v
Scheduler
 |
 v
Worker Node selected
 |
 v
Kubelet
 |
 v
Container Runtime
 |
 v
Nginx Container
 |
 v
Pod Running
```

This is a very important architecture flow to understand.

---

## 63. What Happens When a Node Fails?

Suppose:

```text
Node 1
  |
  +-- Pod A
  +-- Pod B
```

Node 1 becomes unavailable.

The kubelet stops communicating normally with the control plane.

The Kubernetes control plane eventually recognizes the node problem.

Controllers can take appropriate recovery actions for workloads managed by controllers such as Deployments.

Pods may then be recreated on healthy nodes, subject to scheduling constraints and workload configuration.

Conceptually:

```text
Node 1 ❌

       ↓

Control Plane detects problem

       ↓

Workload reconciliation

       ↓

Scheduler selects healthy node

       ↓

Replacement Pod
```

---

## 64. Kubernetes vs Docker Compose

Both can manage multiple containers, but their intended scope is different.

| Docker Compose                  | Kubernetes                               |
| ------------------------------- | ---------------------------------------- |
| Excellent for local development | Designed for cluster-scale orchestration |
| Simple configuration            | More complex                             |
| Usually one host/environment    | Multi-node clusters                      |
| Easy to learn                   | Steeper learning curve                   |
| Great for development/testing   | Common in production/cloud environments  |
| Compose services                | Kubernetes workloads/services            |

A common progression is:

```text
Docker
   ↓
Docker Compose
   ↓
Kubernetes
```

This is not a strict requirement, but it is a useful learning progression.

---

## 65. Why Kubernetes Is Considered Complex

Kubernetes is much larger than simply "running containers."

It includes concepts related to:

* Containers
* Networking
* Storage
* Security
* Scheduling
* Deployments
* Service discovery
* Configuration
* Scaling
* Monitoring
* High availability
* Cluster management
* Cloud integration

The core concepts should therefore be learned gradually.

A good learning order is:

```text
Architecture
   ↓
Pods
   ↓
Deployments
   ↓
ReplicaSets
   ↓
Services
   ↓
ConfigMaps
   ↓
Secrets
   ↓
Volumes
   ↓
Namespaces
   ↓
Ingress
   ↓
Scheduling
   ↓
Autoscaling
   ↓
Security
   ↓
Helm
   ↓
Advanced Kubernetes
```

---

## 66. Common Beginner Misconceptions

### Misconception 1

"Kubernetes is Docker."

Incorrect.

Docker is primarily used for building/running containers, while Kubernetes orchestrates workloads across a cluster.

---

### Misconception 2

"Kubernetes runs Docker containers directly."

Not necessarily.

Modern Kubernetes commonly uses CRI-compatible runtimes such as containerd or CRI-O.

---

### Misconception 3

"Every container is a Pod."

Not exactly.

A Pod is the Kubernetes workload unit that can contain one or more containers.

---

### Misconception 4

"Scheduler creates containers."

No.

The scheduler decides which node should run a Pod.

The kubelet and container runtime are involved in actually starting the containers.

---

### Misconception 5

"etcd stores my application's database."

No.

etcd stores Kubernetes cluster state.

Your application database is separate.

---

### Misconception 6

"`kubectl` directly talks to every worker node."

Normally, `kubectl` communicates with the Kubernetes API server.

The API server acts as the central API endpoint.

---

### Misconception 7

"`depends_on` from Docker Compose is the same as Kubernetes scheduling."

No.

Docker Compose's `depends_on` is a Compose dependency mechanism.

Kubernetes uses controllers, scheduling, readiness/health mechanisms, and other primitives to manage workloads.

---

## 67. Important Kubernetes Terms

### Cluster

The complete Kubernetes environment.

### Control Plane

The components responsible for managing the cluster.

### Worker Node

A machine that runs workloads.

### Pod

The smallest deployable Kubernetes unit.

### Container

The actual application process running inside a Pod.

### API Server

The central Kubernetes API endpoint.

### etcd

Persistent key-value store containing Kubernetes cluster state.

### Scheduler

Chooses a worker node for a Pod.

### Controller

Maintains desired state.

### Kubelet

Node agent responsible for managing Pods on its node.

### Container Runtime

Software that runs containers.

### CRI

Interface used by kubelet to communicate with container runtimes.

### kube-proxy

Common node networking component associated with Service traffic.

### kubectl

Command-line tool used to interact with Kubernetes.

---

## 68. Essential Commands for This Chapter

### Minikube

```bash
minikube version
minikube start
minikube status
minikube stop
minikube delete
```

### Cluster

```bash
kubectl cluster-info
kubectl get nodes
```

### Pods

```bash
kubectl get pods
kubectl get pods -A
kubectl describe pod <pod-name>
```

### Deployments

```bash
kubectl get deployments
kubectl create deployment nginx --image=nginx
kubectl scale deployment nginx --replicas=3
```

### Services

```bash
kubectl get services
```

### General

```bash
kubectl get all
kubectl describe <resource-type> <resource-name>
```

---

## 69. Practical Learning Exercise

Once Minikube is installed and running:

### Step 1 — Start Minikube

```bash
minikube start
```

### Step 2 — Verify

```bash
kubectl get nodes
```

### Step 3 — Create a Deployment

```bash
kubectl create deployment nginx --image=nginx
```

### Step 4 — Check Deployment

```bash
kubectl get deployments
```

### Step 5 — Check Pod

```bash
kubectl get pods
```

### Step 6 — Scale

```bash
kubectl scale deployment nginx --replicas=3
```

### Step 7 — Verify

```bash
kubectl get pods
```

You should see three Pods.

### Step 8 — Delete the Deployment

```bash
kubectl delete deployment nginx
```

### Step 9 — Verify

```bash
kubectl get pods
```

The Pods managed by the Deployment should disappear.

This exercise demonstrates:

```text
Deployment
    ↓
Replica management
    ↓
Pods
    ↓
Scaling
    ↓
Deletion
```

---

## 70. Important Architecture Flow to Memorize

This is one of the most important diagrams from the chapter:

```text
                     kubectl
                        |
                        v
                 +-------------+
                 | API Server  |
                 +------+------+
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
        etcd       Scheduler     Controllers
                                      |
                                      v
                              Desired State
                                      |
                                      v
                              Worker Node
                                      |
                                   Kubelet
                                      |
                                      v
                              Container Runtime
                                      |
                                      v
                                     Pod
                                      |
                                      v
                                  Container
```

Remember the responsibilities:

```text
API Server
    ↓
Communication

etcd
    ↓
State storage

Scheduler
    ↓
Pod placement

Controllers
    ↓
Desired-state reconciliation

Kubelet
    ↓
Node/Pod management

Container Runtime
    ↓
Runs containers
```

---

## 71. Final Mental Model

The simplest way to understand Kubernetes is:

```text
                    KUBERNETES
                         |
                         v
                    CLUSTER
                         |
              +----------+----------+
              |                     |
              v                     v
        CONTROL PLANE          WORKER NODES
              |                     |
              |                     v
              |                    Pods
              |                     |
              |                     v
              |                 Containers
              |
      +-------+-------+
      |       |       |
      v       v       v
   API      etcd   Scheduler
  Server
      |
      v
 Controllers
```

The control plane **makes decisions and maintains cluster state**.

Worker nodes **run the workloads**.

---

## 72. Chapter Summary

Kubernetes is a container orchestration platform designed to manage containerized applications at scale.

The fundamental architecture consists of:

```text
Kubernetes Cluster
       |
       +-- Control Plane
       |
       +-- Worker Nodes
```

The control plane contains important components:

```text
API Server
etcd
Scheduler
Controller Manager
```

Worker nodes contain:

```text
Kubelet
Container Runtime
kube-proxy
```

The Kubernetes API represents workloads and configuration as objects.

Important objects include:

```text
Pod
Deployment
ReplicaSet
Service
ConfigMap
Secret
Namespace
```

The most important Kubernetes philosophy is:

```text
Desired State
      ↓
Actual State
      ↓
Compare
      ↓
Reconcile
      ↓
Desired State
```

Kubernetes continuously works to make the actual cluster state match the desired state.

The most important architecture flow to remember is:

```text
kubectl
   ↓
API Server
   ↓
Control Plane
   ↓
Scheduler / Controllers
   ↓
Worker Node
   ↓
Kubelet
   ↓
Container Runtime
   ↓
Pod
   ↓
Container
```

For local practice, Minikube provides a convenient Kubernetes environment.

The first commands to become comfortable with are:

```bash
minikube start
kubectl get nodes
kubectl get pods
kubectl get deployments
kubectl create deployment nginx --image=nginx
kubectl scale deployment nginx --replicas=3
kubectl describe pod <pod-name>
```

The key takeaway is:

> **Docker gives us containers; Kubernetes gives us a system for managing those containers and workloads reliably across a cluster.**

Understanding the architecture in this chapter is the foundation for everything that follows in Kubernetes.
