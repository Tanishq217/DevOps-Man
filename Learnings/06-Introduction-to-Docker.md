# Chapter 6 — Introduction to Docker

## 1. Introduction to Docker

Docker is a platform used to build, package, distribute, and run applications in containers.

Docker solves many problems that occur when applications are deployed manually on different machines.

The main idea behind Docker is:

Package an application together with everything it needs to run, and run that package consistently in different environments.

Docker is one of the most important technologies in modern DevOps.

## 2. Why Do We Need Docker?

Before Docker, applications were commonly deployed directly onto servers.

Suppose we have a Python application.

To deploy it manually, we might need to:

- Install Python.
- Install the correct Python version.
- Clone the application code.
- Create a virtual environment.
- Install dependencies.
- Configure environment variables.
- Configure networking.
- Start the application.
- Maintain the server.

For example:

```
Server
│
├── Python 3.11
├── Application A
│   ├── Dependency X v1
│   └── Dependency Y v2
│
└── Application B
    ├── Dependency X v2
    └── Dependency Y v3
```

Now imagine hundreds of applications.

Managing these dependencies manually becomes difficult.

This is one of the problems Docker helps solve.

## 3. The "Works on My Machine" Problem

A common problem in software development is:

**"It works on my machine!"**

For example:

```
Developer Machine
Python 3.11
Library X 2.0
Application works
```

But the production server might have:

```
Production Server
Python 3.9
Library X 1.5
Application fails
```

Docker helps create a consistent environment.

```
Application
    +
Dependencies
    +
Runtime
    +
Configuration
       ↓
   Docker Image
       ↓
    Container
```

The same image can then be used in different environments.

## 4. Dependency Hell

Dependency hell occurs when different applications require incompatible versions of the same software or libraries.

Example:

```
Application A → Python 3.9
Application B → Python 3.11
Application C → Python 3.12
```

Or:

```
Application A → Library X v1
Application B → Library X v2
```

Installing everything directly onto one server can become complicated.

Docker allows applications to run in isolated containers.

```
Server
│
├── Container A
│   └── Python 3.9
│
├── Container B
│   └── Python 3.11
│
└── Container C
    └── Python 3.12
```

Each application can have its own environment.

## 5. Docker and Containerization

The process of packaging applications into containers is called:

**Containerization**

A container packages an application with the environment and dependencies required to run it.

Conceptually:

```
Application
     +
Libraries
     +
Dependencies
     +
Configuration
     ↓
   Container
```

Containers provide isolation between applications while being much lighter than traditional virtual machines in many scenarios.

## 6. Docker in DevOps

Docker is heavily used in DevOps because it supports:

- Consistent environments
- Faster deployments
- Application isolation
- Easy scaling
- CI/CD
- Microservices
- Cloud deployment
- Automated testing
- Reproducible deployments

A common DevOps pipeline might look like:

```
Developer
    ↓
GitHub
    ↓
CI/CD
    ↓
Build Application
    ↓
Build Docker Image
    ↓
Push Image to Registry
    ↓
Deploy Container
```

## 7. Important Docker Concepts

Four important Docker concepts are:

- Docker Images
- Docker Containers
- Docker Volumes
- Docker Networks

They can be remembered as:

```
Images     → Application blueprint
Containers → Running application
Volumes    → Persistent storage
Networks   → Communication
```

Images and containers are the main concepts introduced first.

Volumes and networking will be studied in greater detail later.

## 8. Docker Image

A Docker image is a read-only template used to create containers.

An image contains the components required to run an application.

It can contain:

- Application code
- Runtime
- Libraries
- Dependencies
- Configuration
- Files
- Commands required to start the application

For example:

```
Python Application
      +
Python Runtime
      +
Dependencies
      +
Application Code
      ↓
Docker Image
```

## 9. Docker Container

A Docker container is an instance of a Docker image.

The relationship is:

```
Docker Image
     ↓
docker run
     ↓
Docker Container
```

Think of:

```
Image     = Blueprint
Container = Instance
```

One image can be used to create multiple containers.

```
           Docker Image
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
 Container  Container  Container
    A          B          C
```

## 10. Image vs Container

| Docker Image                  | Docker Container                    |
|-------------------------------|-------------------------------------|
| Blueprint/template            | Instance of image                   |
| Read-only                     | Has a writable container layer      |
| Used to create containers     | Runs the application                |
| Can be stored in registry     | Runs on Docker host                 |
| Immutable by design           | Has runtime state                   |

Example:

```bash
docker pull nginx
```

downloads an image.

Then:

```bash
docker run nginx
```

creates a container from that image.

## 11. Docker Volumes

Containers are generally considered ephemeral.

Data written inside a container can be lost when the container is removed.

For persistent data, Docker provides volumes.

Conceptually:

```
Container
    ↓
Docker Volume
    ↓
Persistent Data
```

Volumes are commonly used for:

- Databases
- Application data
- Uploaded files
- Persistent configuration

Volumes will be covered in detail in a later chapter.

## 12. Docker Networking

Docker containers can communicate with:

- Other containers
- The host
- External networks
- The internet

Docker provides networking features that allow containers to communicate.

For example:

```
Frontend Container
       ↓
Backend Container
       ↓
Database Container
```

Docker networking becomes especially important when working with microservices.

## 13. Docker and Kubernetes

Docker and Kubernetes are related but are not the same thing.

### Docker

Primarily provides:

- Container creation
- Container execution
- Image building
- Image management
- Container networking
- Container storage

### Kubernetes

Kubernetes is a container orchestration platform.

It manages containers across clusters of machines.

Kubernetes can handle:

- Deployment
- Scaling
- Service discovery
- Load balancing
- Self-healing
- Rolling updates

Simplified relationship:

```
Docker
   ↓
Creates/Runs Containers

Kubernetes
   ↓
Manages Containers at Scale
```

Modern Kubernetes environments commonly use container runtimes such as containerd or CRI-O rather than Docker Engine directly, but Docker remains highly important for building and working with container images.

## 14. Traditional Deployment vs Docker Deployment

### Traditional Deployment

Suppose we want to deploy a Python application.

We may need:

```
Install Linux
      ↓
Install Python
      ↓
Install correct Python version
      ↓
Clone Git repository
      ↓
Create virtual environment
      ↓
Install dependencies
      ↓
Configure environment variables
      ↓
Start application
```

This can be time-consuming and error-prone.

## 15. Docker-Based Deployment

With Docker:

```
Application
     ↓
Dockerfile
     ↓
docker build
     ↓
Docker Image
     ↓
docker run
     ↓
Container
```

The Dockerfile describes the environment required by the application.

This makes deployment more reproducible.

## 16. Example: Python Application

Without Docker:

```bash
git clone <repository>
cd application
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

With Docker, the required setup can be described in a Dockerfile.

Example:

```dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

Then:

```bash
docker build -t my-python-app .
```

and:

```bash
docker run my-python-app
```

The deployment process becomes much more consistent.

## 17. Docker Architecture

Docker follows a client-server architecture.

The major components are:

- Docker Client
- Docker Host
- Docker Registry

Conceptually:

```
              Docker Client
                    │
                    ↓
              Docker Host
                    │
              Docker Daemon
                    │
          ┌─────────┼─────────┐
          ↓         ↓         ↓
       Images   Containers  Networks
                    │
                    ↓
                 Volumes


Docker Registry
       ↕
 Docker Images
```

## 18. Docker Client

The Docker client is the command-line interface used to interact with Docker.

Examples:

```bash
docker images
docker ps
docker pull nginx
docker run nginx
```

The client sends requests to the Docker daemon.

## 19. Docker Host

The Docker host is the machine/environment where Docker Engine runs and where Docker objects are managed.

It can contain:

- Docker daemon
- Images
- Containers
- Networks
- Volumes

On a Linux server, Docker Engine runs directly on the Linux host.

On macOS, Docker Desktop provides the Linux environment in which Linux containers run.

## 20. Docker Daemon

The Docker daemon is a background service responsible for managing Docker resources.

It manages:

- Images
- Containers
- Networks
- Volumes

For example:

```bash
docker run nginx
```

The Docker client sends the request to the daemon.

The daemon performs the necessary operations.

## 21. Docker Registry

A Docker registry stores Docker images.

The most common public registry is:

**Docker Hub**

Other registries include:

- Amazon ECR
- Azure Container Registry
- Google Artifact Registry
- GitHub Container Registry
- Private organizational registries

Conceptually:

```
Developer
    ↓
Docker Image
    ↓
Registry
    ↓
Other Server
    ↓
Docker Container
```

## 22. Docker Hub

Docker Hub is a public container registry.

It contains images for many technologies, including:

- Nginx
- Ubuntu
- Node.js
- Python
- Redis
- MySQL
- PostgreSQL
- Apache

Docker Hub can be used to:

- Pull existing images
- Push your own images
- Share images
- Discover application images

## 23. Official Images

Docker Hub contains Official Images for many popular technologies.

Examples include:

```
nginx
ubuntu
python
node
redis
```

Official images are maintained under Docker's official-image publishing process and are generally a preferred starting point for common software.

There are also images published by companies, organizations, and individual developers.

When selecting an image, check:

- Publisher
- Official/verified status
- Documentation
- Version/tag
- Update history
- Security considerations

## 24. Pulling a Docker Image

To download an image:

```bash
docker pull nginx
```

Docker downloads the image from the configured registry.

If no tag is specified, Docker generally uses:

```
nginx:latest
```

You can also specify a tag:

```bash
docker pull nginx:1.27
```

## 25. Docker Image Tags

A tag identifies a particular version or variant of an image.

Format:

```
image:tag
```

Examples:

```
nginx:latest
nginx:1.27
python:3.12
ubuntu:24.04
node:22
```

Tags are useful because different versions of an application can coexist.

For production deployments, explicitly versioned tags are generally preferable to relying on a moving `latest` tag.

## 26. latest Does Not Always Mean Newest

This is an important concept.

Consider:

```
nginx:latest
nginx:1.27
nginx:1.26
```

`latest` is simply a tag.

It does not guarantee that it represents the newest release forever.

The tag can be moved to different image contents over time.

Therefore:

```bash
docker pull nginx:latest
```

may give different image contents at different times.

Explicit versioning gives more predictable deployments.

## 27. Docker Images and Layers

Docker images are built using layers.

Conceptually:

```
Application Layer
       ↓
Dependency Layer
       ↓
Runtime Layer
       ↓
Base Image Layer
```

Each Dockerfile instruction can contribute to the image's filesystem layers.

Layers provide:

- Reusability
- Efficient storage
- Faster image transfers
- Faster builds when cache can be reused

For example, if multiple images use the same Ubuntu base image, Docker can reuse the existing layers.

## 28. Docker Image Immutability

Docker images are designed to be immutable.

Once an image has been built, you generally don't modify it directly.

Instead:

```
Modify Dockerfile
       ↓
Build new image
       ↓
Deploy new container
```

This provides consistency and reproducibility.

## 29. Installing Docker

Docker can be installed on different operating systems.

For Linux servers, Docker Engine can be installed using the official Docker installation instructions for the specific distribution.

On macOS, Docker Desktop is commonly used.

After installation, verify Docker:

```bash
docker --version
```

You can also check:

```bash
docker info
```

## 30. Testing Docker Installation

A standard way to test a Docker installation is:

```bash
docker run hello-world
```

Docker will:

- Look for the hello-world image locally.
- Pull it from the registry if necessary.
- Create a container.
- Run the container.
- Display a confirmation message.

Conceptually:

```
docker run hello-world
        ↓
Check local image
        ↓
Not available
        ↓
Pull from registry
        ↓
Create container
        ↓
Run container
        ↓
Display output
```

## 31. Running Nginx

Nginx is commonly used as a web server.

We can run it using:

```bash
docker run -d -p 8080:80 nginx
```

Let's understand this command.

**docker run**  
Create and start a container.

**-d**  
Run in detached/background mode.

**-p 8080:80**  
Map host port 8080 to container port 80.

**nginx**  
Use the Nginx image.

## 32. Port Mapping

Port mapping connects a port on the host to a port inside the container.

Syntax:

```
-p HOST_PORT:CONTAINER_PORT
```

Example:

```
-p 8080:80
```

means:

```
Host
Port 8080
   ↓
Docker
   ↓
Container
Port 80
   ↓
Nginx
```

Therefore, you can access:

```
http://localhost:8080
```

on your Mac.

## 33. Why Does Nginx Use Port 80?

HTTP commonly uses port:

```
80
```

HTTPS commonly uses:

```
443
```

Nginx inside the container listens on port 80 by default.

We map it to port 8080 on our Mac:

```
localhost:8080
        ↓
container:80
```

The host port does not have to be the same as the container port.

For example:

```bash
docker run -d -p 9000:80 nginx
```

means:

```
localhost:9000
      ↓
container:80
```

## 34. Checking Running Containers

Use:

```bash
docker ps
```

This shows currently running containers.

Example:

```
CONTAINER ID   IMAGE   STATUS       PORTS
abc123         nginx   Up 2 minutes 0.0.0.0:8080->80/tcp
```

Important information includes:

- Container ID
- Image
- Status
- Port mapping
- Container name

## 35. Checking All Containers

Use:

```bash
docker ps -a
```

This shows:

- Running containers
- Stopped containers
- Exited containers

Remember:

```
docker ps
    ↓
Running containers

docker ps -a
    ↓
All containers
```

## 36. Stopping a Container

First find the container:

```bash
docker ps
```

Then:

```bash
docker stop CONTAINER_ID
```

or:

```bash
docker stop CONTAINER_NAME
```

Example:

```bash
docker stop my-nginx
```

## 37. Docker Container Names

Docker can automatically assign names to containers.

You can provide your own name:

```bash
docker run -d -p 8080:80 --name my-nginx nginx
```

Now you can use:

```bash
docker stop my-nginx
```

instead of remembering the container ID.

## 38. Docker Workflow

A basic Docker workflow is:

```
Find/Create Application
        ↓
Create Dockerfile
        ↓
docker build
        ↓
Docker Image
        ↓
docker run
        ↓
Docker Container
        ↓
Application Running
```

If using Docker Hub:

```
Docker Image
      ↓
docker push
      ↓
Docker Hub
      ↓
docker pull
      ↓
Another Machine
      ↓
docker run
      ↓
Container
```

## 39. Docker in a CI/CD Pipeline

Docker fits naturally into CI/CD.

Example:

```
Developer
    ↓
git push
    ↓
GitHub
    ↓
CI Pipeline
    ↓
Build Application
    ↓
Run Tests
    ↓
Build Docker Image
    ↓
Security Scan
    ↓
Push Image
    ↓
Deploy
```

This is one reason Docker is so important in DevOps.

## 40. Docker and Microservices

Docker is particularly useful with microservices.

Suppose an application has:

- Frontend
- Backend
- Authentication Service
- Payment Service
- Database

Each component can potentially run in its own container:

```
┌───────────────┐
│ Frontend      │
│ Container     │
└───────┬───────┘
        ↓
┌───────────────┐
│ Backend       │
│ Container     │
└───────┬───────┘
        ↓
┌───────────────┐
│ Database      │
│ Container     │
└───────────────┘
```

This allows services to be developed, deployed, and scaled independently.

## 41. Scaling with Docker

Suppose one container is not enough to handle traffic.

We can run multiple instances:

```
             Load Balancer
                  │
        ┌─────────┼─────────┐
        ↓         ↓         ↓
   Container  Container  Container
       1          2          3
```

This makes horizontal scaling easier.

In large environments, orchestration platforms such as Kubernetes can manage this process automatically.

## 42. Docker vs Virtual Machines

Docker containers and virtual machines are different technologies.

### Traditional VM

```
Hardware
   ↓
Host OS
   ↓
Hypervisor
   ↓
Guest OS
   ↓
Application
```

### Containers

```
Hardware
   ↓
Host OS / Linux environment
   ↓
Container Runtime
   ↓
Containers
   ↓
Applications
```

A traditional VM usually includes a complete guest operating system.

Containers share the host kernel and isolate application processes.

As a result, containers are generally lighter and can start faster than full VMs.

## 43. Advantages of Docker

**1. Consistency**  
The same image can be used across environments.

**2. Isolation**  
Applications can run independently.

**3. Portability**  
Containers can be moved between compatible environments.

**4. Faster Deployment**  
Containers can start quickly.

**5. Easy Scaling**  
Multiple container instances can be created.

**6. Dependency Management**  
Applications can package their required dependencies.

**7. CI/CD Integration**  
Docker works well with automated pipelines.

**8. Efficient Resource Usage**  
Containers generally require fewer resources than full virtual machines.

## 44. Limitations and Considerations

Docker is powerful, but it does not solve every problem.

Considerations include:

- Container security
- Persistent storage
- Networking complexity
- Image size
- Secrets management
- Container monitoring
- Logging
- Orchestration
- Resource limits

These become increasingly important in production environments.

## 45. Basic Docker Commands

**Check Docker version**

```bash
docker --version
```

**Display Docker information**

```bash
docker info
```

**Download image**

```bash
docker pull nginx
```

**List images**

```bash
docker images
```

**Run container**

```bash
docker run nginx
```

**Run in background**

```bash
docker run -d nginx
```

**Run with port mapping**

```bash
docker run -d -p 8080:80 nginx
```

**List running containers**

```bash
docker ps
```

**List all containers**

```bash
docker ps -a
```

**Stop container**

```bash
docker stop CONTAINER
```

**Remove container**

```bash
docker rm CONTAINER
```

**Remove image**

```bash
docker rmi IMAGE
```

## 46. Important Docker Command Concepts

**docker pull**  
Downloads an image.

```bash
docker pull nginx
```

**docker run**  
Creates and starts a new container from an image.

```bash
docker run nginx
```

**docker ps**  
Shows running containers.

```bash
docker ps
```

**docker ps -a**  
Shows all containers.

```bash
docker ps -a
```

**docker images**  
Lists local images.

```bash
docker images
```

## 47. Complete Example

Let's deploy a simple Nginx website.

**Step 1 — Pull Nginx**

```bash
docker pull nginx
```

**Step 2 — Verify Image**

```bash
docker images
```

You should see an Nginx image.

**Step 3 — Run Container**

```bash
docker run -d -p 8080:80 --name my-nginx nginx
```

**Step 4 — Check Container**

```bash
docker ps
```

**Step 5 — Open Browser**

Visit:

```
http://localhost:8080
```

You should see the Nginx welcome page.

**Step 6 — Stop Container**

```bash
docker stop my-nginx
```

**Step 7 — Verify**

```bash
docker ps
```

The container should no longer appear because it is stopped.

To see it:

```bash
docker ps -a
```

## 48. Troubleshooting Port Mapping

Suppose you run:

```bash
docker run -d -p 8080:80 nginx
```

but cannot access the page.

Check:

```bash
docker ps
```

Look for the port mapping.

You should see something similar to:

```
0.0.0.0:8080->80/tcp
```

If port 8080 is already being used, choose another host port:

```bash
docker run -d -p 8081:80 nginx
```

Then access:

```
http://localhost:8081
```

## 49. Docker Image Lifecycle

A simplified image lifecycle:

```
Dockerfile
    ↓
docker build
    ↓
Docker Image
    ↓
docker tag
    ↓
docker push
    ↓
Docker Registry
    ↓
docker pull
```

## 50. Docker Container Lifecycle

A simplified container lifecycle:

```
Image
  ↓
docker run
  ↓
Created
  ↓
Running
  ↓
Stopped/Exited
  ↓
docker start
  ↓
Running
  ↓
docker rm
  ↓
Removed
```

## 51. Important Terminology

**Containerization**  
Packaging and running applications in containers.

**Image**  
Read-only template used to create containers.

**Container**  
Instance of an image.

**Registry**  
Storage/distribution system for container images.

**Docker Hub**  
Popular public Docker registry.

**Dockerfile**  
Text file containing instructions for building an image.

**Docker Engine**  
Core Docker technology responsible for running and managing containers.

**Docker Daemon**  
Background service that manages Docker objects.

**Docker Client**  
Command-line interface used to communicate with Docker.

**Volume**  
Persistent storage mechanism.

**Network**  
Allows containers and other systems to communicate.

## 52. Docker Architecture — Complete Picture

Remember this architecture:

```
                    Docker Client
                         │
                         │ Docker API
                         ↓
                  Docker Daemon
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
       Images        Containers      Networks
          │              │
          │              ↓
          │           Volumes
          │
          ↓
     Docker Registry
       / Docker Hub
```

The client sends commands.

The daemon performs operations.

The registry stores/distributes images.

## 53. Exam Questions

**Q1. What is Docker?**  
Docker is a platform used to build, package, distribute, and run applications using containers.

**Q2. Why is Docker used?**  
Docker helps provide consistent environments, isolate applications, simplify deployment, manage dependencies, and support scaling and CI/CD.

**Q3. What is containerization?**  
Containerization is the process of packaging an application and its dependencies into a container so it can run consistently across environments.

**Q4. What is a Docker image?**  
A Docker image is a read-only template used to create containers.

**Q5. What is a Docker container?**  
A Docker container is an instance of a Docker image running as an isolated process environment.

**Q6. What is Docker Hub?**  
Docker Hub is a public container registry used to store and distribute Docker images.

**Q7. What is a Docker registry?**  
A registry is a service that stores and distributes container images.

**Q8. What does docker pull nginx do?**  
It downloads the Nginx image from the configured registry.

**Q9. What does docker run nginx do?**  
It creates and starts a new container from the Nginx image.

**Q10. What does docker ps do?**  
It lists running containers.

**Q11. What does docker ps -a do?**  
It lists all containers, including stopped containers.

**Q12. What does -p 8080:80 mean?**  
It maps port 8080 on the host to port 80 inside the container.

**Q13. Why are Docker images layered?**  
Layers allow Docker to reuse data, reduce storage requirements, and improve build and transfer efficiency.

**Q14. What is Docker's relationship with Kubernetes?**  
Docker is a container platform, while Kubernetes is a container orchestration platform. Kubernetes manages containers across larger environments.

## 54. Interview Questions

**Q: What problem does Docker solve?**  
Docker helps solve environment inconsistency and dependency conflicts by packaging applications with their required environment into portable containers.

**Q: Why are containers lighter than VMs?**  
Containers share the host kernel instead of requiring a complete guest operating system for every application.

**Q: Can one image create multiple containers?**  
Yes.

```
Image
 ├── Container 1
 ├── Container 2
 └── Container 3
```

**Q: What happens if no tag is specified?**  
Docker generally uses the `latest` tag.

```bash
docker pull nginx
```

is generally equivalent to:

```bash
docker pull nginx:latest
```

**Q: Why shouldn't production systems blindly use latest?**  
Because the tag can point to different image contents over time, making deployments less predictable.

## 55. Quick Revision Sheet

```bash
# Docker information
docker --version
docker info

# Images
docker pull nginx
docker images

# Containers
docker run nginx
docker run -d nginx
docker run -d -p 8080:80 nginx

# Container listing
docker ps
docker ps -a

# Container management
docker stop CONTAINER
docker start CONTAINER
docker restart CONTAINER
docker rm CONTAINER

# Image management
docker rmi IMAGE

# Test installation
docker run hello-world
```

## 56. Most Important Mental Model

Remember this:

```
                DOCKER
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
      Image     Container    Registry
        │          │          │
        │          │          │
    Blueprint   Running     Stores &
                Instance    distributes
                              images
```

The most important flow is:

```
Dockerfile
     ↓
docker build
     ↓
Docker Image
     ↓
docker run
     ↓
Docker Container
```

And when a registry is involved:

```
Docker Image
     ↓
docker push
     ↓
Registry
     ↓
docker pull
     ↓
Another Machine
     ↓
docker run
     ↓
Container
```

## 57. Chapter 6 Final Checklist

Before moving forward, make sure you understand:

- What Docker is
- Why Docker is required
- Containerization
- Dependency hell
- "Works on my machine" problem
- Docker's role in DevOps
- Docker images
- Docker containers
- Images vs containers
- Docker volumes
- Docker networking
- Docker and Kubernetes
- Traditional deployment
- Docker-based deployment
- Docker architecture
- Docker client
- Docker host
- Docker daemon
- Docker registry
- Docker Hub
- Official images
- Image tags
- latest tag
- Image layers
- Image immutability
- Installing Docker
- docker run hello-world
- docker pull
- docker images
- docker run
- docker ps
- docker ps -a
- Port mapping
- Host port vs container port
- Running Nginx
- Container lifecycle
- Image lifecycle
- Docker in CI/CD
- Docker with microservices
- Basic Docker troubleshooting

## Chapter Summary

Docker is a containerization platform that allows applications and their dependencies to be packaged and run consistently.

The core relationship is:

```text
Dockerfile → Docker Image → Docker Container
```

Docker images are reusable templates, while containers are instances created from those images.

Docker uses a client-server architecture:

```
Docker Client
      ↓
Docker Daemon
      ↓
Docker Objects
```

Docker images can be stored and distributed through registries such as Docker Hub.

Important commands introduced in this chapter include:

```bash
docker pull
docker images
docker run
docker ps
docker ps -a
docker stop
docker start
docker rm
docker rmi
```

Port mapping allows applications inside containers to be accessed from the host:

```bash
docker run -d -p 8080:80 nginx
```

which creates:

```
localhost:8080
      ↓
container:80
      ↓
Nginx
```

Docker is particularly valuable in DevOps because it supports consistent deployments, CI/CD, microservices, portability, isolation, and scaling.

The concepts from this chapter provide the foundation for the next Docker topics: Docker images in depth, Dockerfiles, image layers, container lifecycle, volumes, networking, and eventually Docker Compose and Kubernetes.
