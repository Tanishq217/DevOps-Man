# Chapter 7 — Docker Images, Containers & Docker Basics

## 1. Introduction to Docker

Docker is a platform used to build, package, ship, and run applications inside containers.

A container packages an application together with the dependencies it needs to run.

### Why Docker?

Without Docker, an application may work on one developer's machine but fail on another because of differences in:

- Operating system
- Runtime versions
- Libraries
- Dependencies
- Environment configuration
- Installed software

Docker helps solve this problem by packaging the application and its environment into a consistent unit called a container.

### Example

Suppose a Java application requires:

- Java 22
- Maven
- Specific libraries
- Environment variables
- Application JAR

Instead of manually installing everything on every server, we can create a Docker image containing everything required to run the application.

That image can then be used to create containers on different machines.

## 2. Docker in DevOps

Docker is extremely important in DevOps because it makes application deployment more consistent and easier to automate.

A typical DevOps flow can look like:

```
Developer
    ↓
Git/GitHub
    ↓
Build Application
    ↓
Create Docker Image
    ↓
Push Image to Registry
    ↓
Deploy Container
    ↓
Monitor Application
```

Docker is commonly used in:

- CI/CD pipelines
- Microservices
- Cloud deployments
- Development environments
- Testing
- Production deployments
- Kubernetes

## 3. Docker Architecture

Docker follows a client-server architecture.

The major components are:

```
Docker Client
     ↓
Docker Daemon
     ↓
Docker Objects
 ┌──────┬──────────┬─────────┐
Images Containers Networks Volumes
```

### 3.1 Docker Client

The Docker client is the interface through which we interact with Docker.

For example:

```bash
docker ps
docker images
docker run nginx
```

When we execute these commands, the Docker client communicates with the Docker daemon.

## 4. Docker Daemon

The Docker daemon is the main background service responsible for managing Docker objects.

It manages:

- Images
- Containers
- Networks
- Volumes

The daemon receives requests from the Docker client and performs the required operation.

For example:

```bash
docker run nginx
```

The client sends the request to the Docker daemon.

The daemon then:

- Checks whether the required image exists locally.
- Downloads it if necessary.
- Creates a container.
- Starts the container.

## 5. Docker Host

The Docker host is the machine on which Docker is running.

It contains components such as:

- Docker daemon
- Docker images
- Docker containers
- Docker networks
- Docker volumes

### On macOS

Docker normally runs through Docker Desktop, because Linux containers require a Linux environment.

Conceptually:

```
MacBook
   ↓
Docker Desktop
   ↓
Linux environment
   ↓
Docker Engine
   ↓
Containers
```

Therefore, the Docker commands you run on your Mac interact with Docker Engine through Docker Desktop.

## 6. Four Important Docker Components

The four major Docker objects are:

- Images
- Containers
- Networks
- Volumes

For this chapter, the primary focus is:

- Docker Images
- Docker Containers

Networks and volumes will be studied in greater detail later.

## 7. Docker Image

A Docker image is a read-only template used to create containers.

It contains everything required to create a container, such as:

- Application code
- Runtime
- Libraries
- Dependencies
- Configuration
- Required filesystem contents

An image is generally considered immutable.

That means we don't normally modify an existing image directly.

Instead:

```
Existing Image
      ↓
Modify Dockerfile
      ↓
Build New Image
```

## 8. Docker Image as a Blueprint

A useful way to remember the relationship:

```
Image = Blueprint
Container = Running instance created from blueprint
```

For example:

```
Nginx Image
     ↓
 ┌───┴────┐
 ↓        ↓
Container Container
   1          2
```

The same image can be used to create multiple containers.

## 9. Docker Container

A container is a running or stopped instance of a Docker image.

For example:

```bash
docker run nginx
```

Docker uses the nginx image to create a container.

Relationship:

```
Docker Image
     ↓
docker run
     ↓
Docker Container
```

### Important

An image is not the same thing as a container.

| Image                      | Container                         |
| -------------------------- | --------------------------------- |
| Blueprint/template         | Instance created from image       |
| Read-only                  | Has a writable layer              |
| Used to create containers  | Runs the application              |
| Can create many containers | Represents one container instance |

## 10. Docker Image vs Container

Suppose we have:

```
nginx:latest
```

This is an image.

Running:

```bash
docker run nginx:latest
```

creates a container based on that image.

We could create multiple containers:

```
nginx image
    ↓
 ┌──┼──┐
 ↓  ↓  ↓
C1 C2 C3
```

All three containers can originate from the same image.

## 11. Checking Docker Installation

Before working with Docker, verify that Docker is installed and running.

```bash
docker --version
```

Example:

```
Docker version 28.x.x
```

You can also run:

```bash
docker info
```

This provides information about the Docker installation and Docker Engine.

If using macOS, make sure Docker Desktop is running.

## 12. Docker Images Command

To list locally available Docker images:

```bash
docker images
```

Modern equivalent:

```bash
docker image ls
```

Example output:

```
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
nginx        latest    abc123456      2 days ago    192MB
ubuntu       latest    def789012      3 days ago    78MB
```

Important columns:

**REPOSITORY**  
Image name.  
Example: `nginx`

**TAG**  
Version or identifier of the image.  
Example: `latest`

**IMAGE ID**  
Unique identifier for the image.

**CREATED**  
When the image was created.

**SIZE**  
Size of the image.

## 13. Docker Image Tags

Images commonly use tags.

Format:

```
repository:tag
```

Example:

```
nginx:latest
nginx:1.27
ubuntu:24.04
node:22
```

The tag helps identify a particular version or variant of an image.

## 14. The latest Tag

If no tag is specified:

```bash
docker pull nginx
```

Docker interprets it as:

```bash
docker pull nginx:latest
```

Similarly:

```bash
docker run nginx
```

generally means:

```bash
docker run nginx:latest
```

### Important

`latest` does not necessarily mean newest version.

It is simply a tag named `latest`.

For production environments, explicitly specifying versions is often safer.

Example:

```bash
docker pull nginx:1.27
```

instead of:

```bash
docker pull nginx:latest
```

## 15. Docker Registry

A Docker registry is a place where Docker images are stored and distributed.

The default public registry commonly used by Docker is:

**Docker Hub**

Conceptually:

```
Local Computer
      ↓
Docker Pull
      ↓
Docker Registry
      ↓
Docker Image
```

## 16. Docker Hub

Docker Hub is a public registry containing Docker images.

Examples include images for:

- Nginx
- Ubuntu
- Redis
- MySQL
- PostgreSQL
- Node.js
- Python

When you execute:

```bash
docker pull nginx
```

Docker normally searches the configured registry, with Docker Hub being the default public registry.

## 17. Private Container Registries

Organizations often use private registries to store internal Docker images.

Examples include:

- Amazon Elastic Container Registry (ECR)
- Azure Container Registry (ACR)
- Google Artifact Registry
- Private Docker registries

Example architecture:

```
Developer
   ↓
Build Docker Image
   ↓
Private Registry
   ↓
Production Server
   ↓
Pull Image
   ↓
Run Container
```

## 18. Pulling Docker Images

To download an image:

```bash
docker pull IMAGE
```

Example:

```bash
docker pull nginx
```

To pull a specific tag:

```bash
docker pull nginx:1.27
```

## 19. What Happens During docker pull?

Suppose you run:

```bash
docker pull nginx
```

Docker checks whether the required image/version is already available locally.

If it isn't available, Docker contacts the configured registry and downloads the required image layers.

Conceptually:

```
docker pull nginx
       ↓
Check local images
       ↓
Image available?
   ↙          ↘
 Yes           No
  ↓             ↓
Use it       Contact Registry
                ↓
             Download
                ↓
             Store locally
```

## 20. Docker Image Layers

Docker images are composed of multiple layers.

For example:

```
Application Layer
      ↓
Dependency Layer
      ↓
Runtime Layer
      ↓
Base OS Layer
```

Layers provide several advantages:

- Reuse
- Efficient storage
- Faster builds
- Faster downloads when layers already exist

If two images share the same layer, Docker can reuse that layer instead of downloading it again.

## 21. Inspecting an Image

To see detailed information about an image:

```bash
docker inspect IMAGE
```

Example:

```bash
docker inspect nginx
```

This can show information such as:

- Image ID
- Architecture
- OS
- Environment
- Entrypoint
- Commands
- Configuration
- Root filesystem information
- Metadata

## 22. Docker Containers

List currently running containers:

```bash
docker ps
```

Example:

```
CONTAINER ID   IMAGE   STATUS    PORTS
abc123         nginx   Up 2 min   0.0.0.0:8080->80/tcp
```

## 23. docker ps vs docker ps -a

### Running containers

```bash
docker ps
```

Shows only currently running containers.

### All containers

```bash
docker ps -a
```

Shows:

- Running containers
- Stopped containers
- Exited containers

This distinction is extremely important.

## 24. Running a Container

Basic syntax:

```bash
docker run IMAGE
```

Example:

```bash
docker run nginx
```

Docker will create and start a container using the Nginx image.

## 25. docker run Options

A commonly used form is:

```bash
docker run -it -d -p HOST_PORT:CONTAINER_PORT --name CONTAINER_NAME IMAGE
```

Example:

```bash
docker run -it -d -p 8080:80 --name my-nginx nginx
```

Let's understand every part.

## 26. -d — Detached Mode

```
-d
```

means detached mode.

The container runs in the background.

Example:

```bash
docker run -d nginx
```

Your terminal remains available while the container continues running.

## 27. -i — Interactive

```
-i
```

means interactive.

It keeps standard input open.

## 28. -t — TTY

```
-t
```

allocates a pseudo-terminal.

Together:

```
-it
```

is commonly used when you want to interact with a shell inside a container.

Example:

```bash
docker run -it ubuntu /bin/bash
```

## 29. -p — Port Mapping

The `-p` option maps a host port to a container port.

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
Mac Host Port 8080
        ↓
Container Port 80
```

If Nginx is listening on port 80 inside the container, you can access it through port 8080 on your Mac.

Example:

```bash
docker run -d -p 8080:80 nginx
```

Then open:

```
http://localhost:8080
```

## 30. Why Port Mapping Is Required

Containers have their own networking environment.

Suppose Nginx listens on:

```
Container: 80
```

Your Mac does not automatically expose that port to the outside.

Port mapping creates the connection:

```
Mac
localhost:8080
      ↓
Docker
      ↓
Container:80
      ↓
Nginx
```

## 31. --name

The `--name` option gives a container a human-readable name.

Example:

```bash
docker run -d --name my-nginx nginx
```

Now instead of referring to a generated container ID, you can use:

```bash
docker stop my-nginx
```

## 32. Container Lifecycle

A container can move through different states.

A simplified lifecycle:

```
Created
   ↓
Running
   ↓
Stopped / Exited
   ↓
Started again
   ↓
Running
```

A container can also be removed.

```
Running
   ↓
Stopped
   ↓
Removed
```

## 33. Stopping a Container

Use:

```bash
docker stop CONTAINER
```

Example:

```bash
docker stop my-nginx
```

Docker sends a graceful stop request to the container.

## 34. Starting a Stopped Container

If the container already exists but is stopped:

```bash
docker start CONTAINER
```

Example:

```bash
docker start my-nginx
```

This starts the existing container again.

It does not create a new container.

## 35. Restarting a Container

Use:

```bash
docker restart CONTAINER
```

Example:

```bash
docker restart my-nginx
```

This stops and starts the container.

## 36. docker run vs docker start

This is an important exam/interview concept.

### docker run

Creates a new container from an image and starts it.

```bash
docker run nginx
```

### docker start

Starts an existing stopped container.

```bash
docker start my-nginx
```

Remember:

```
Image
 ↓
docker run
 ↓
New Container
```

while:

```
Existing stopped Container
 ↓
docker start
 ↓
Running Container
```

## 37. Accessing a Running Container

To execute a command inside a running container:

```bash
docker exec -it CONTAINER /bin/bash
```

Example:

```bash
docker exec -it my-nginx /bin/bash
```

This opens a shell inside the container if `/bin/bash` exists.

## 38. /bin/bash

`/bin/bash` starts the Bash shell.

For images that do not contain Bash, you may need:

```
/bin/sh
```

Example:

```bash
docker exec -it my-container /bin/sh
```

This is common with lightweight images such as Alpine-based images.

## 39. docker exec vs docker run

### docker run

Creates a new container.

### docker exec

Runs a command inside an already running container.

Example:

```bash
docker exec -it my-nginx /bin/bash
```

does not create another container.

## 40. Removing Containers

To remove a stopped container:

```bash
docker rm CONTAINER
```

Example:

```bash
docker rm my-nginx
```

You normally need to stop a running container before removing it.

## 41. Force Removing a Container

To forcefully remove a container:

```bash
docker rm -f my-nginx
```

This can remove a running container by stopping/removing it as necessary.

Use force carefully.

## 42. Removing Docker Images

To remove an image:

```bash
docker rmi IMAGE
```

Example:

```bash
docker rmi nginx
```

Modern equivalent:

```bash
docker image rm nginx
```

An image generally cannot be removed if it is still required by existing containers unless those containers are removed or the removal is forced.

## 43. Force Removing an Image

```bash
docker rmi -f IMAGE
```

Example:

```bash
docker rmi -f nginx
```

Use force carefully because it can remove an image that is still referenced.

## 44. Docker Prune

Docker can accumulate unused objects over time.

For example:

- Stopped containers
- Unused images
- Unused networks
- Build cache

Docker provides prune commands to clean them.

## 45. Container Prune

Remove stopped containers:

```bash
docker container prune
```

Docker will ask for confirmation.

This does not remove running containers.

## 46. Image Prune

To remove dangling images:

```bash
docker image prune
```

A dangling image is typically an untagged image that is no longer associated with a useful repository/tag.

## 47. System Prune

To clean several types of unused Docker resources:

```bash
docker system prune
```

Depending on options and Docker's current behavior, this can remove unused:

- Stopped containers
- Unused networks
- Dangling images
- Build cache

Be careful with prune commands.

Always understand what will be removed before confirming.

## 48. Dangling Images

A dangling image is an image that does not have a meaningful repository/tag association.

They can appear after rebuilding images.

You may see something similar to:

```
<none>    <none>
```

These are commonly called dangling images.

To clean them:

```bash
docker image prune
```

## 49. Dockerfile

A Dockerfile is a text file containing instructions used to build a Docker image.

Example:

```dockerfile
FROM nginx

COPY index.html /usr/share/nginx/html/index.html
```

The Dockerfile describes how the image should be constructed.

Conceptually:

```
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

## 50. Building a Docker Image

Basic syntax:

```bash
docker build -t IMAGE_NAME .
```

Example:

```bash
docker build -t my-nginx .
```

Here:

- `docker build` builds the image.
- `-t my-nginx` assigns the image name/tag.
- `.` specifies the build context as the current directory.

## 51. Docker Build Context

The final `.` in:

```bash
docker build -t my-nginx .
```

is important.

It means:

Use the current directory as the build context.

Docker can access files within the build context during the image build.

Example project:

```
my-project/
├── Dockerfile
├── index.html
└── other-files
```

Run:

```bash
cd my-project
docker build -t my-nginx .
```

## 52. Basic Dockerfile Instructions

Common Dockerfile instructions include:

**FROM**  
Defines the base image.

```dockerfile
FROM nginx
```

**COPY**  
Copies files from the build context into the image.

```dockerfile
COPY index.html /usr/share/nginx/html/
```

**RUN**  
Executes commands while building the image.

```dockerfile
RUN apt-get update
```

**WORKDIR**  
Sets the working directory.

```dockerfile
WORKDIR /app
```

**CMD**  
Defines the default command executed when the container starts.

```dockerfile
CMD ["npm", "start"]
```

**EXPOSE**  
Documents the port the application expects to use.

```dockerfile
EXPOSE 80
```

Important:

`EXPOSE` does not itself publish the port to the host.

Port publishing is done using:

```
-p HOST_PORT:CONTAINER_PORT
```

## 53. Simple Nginx Docker Example

Project:

```
nginx-project/
├── Dockerfile
└── index.html
```

**Dockerfile**

```dockerfile
FROM nginx

COPY index.html /usr/share/nginx/html/index.html
```

**index.html**

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Docker App</title>
</head>
<body>
    <h1>Hello from Docker!</h1>
</body>
</html>
```

## 54. Build the Image

From the project directory:

```bash
docker build -t my-nginx .
```

Check the image:

```bash
docker images
```

You should see:

```
my-nginx
```

## 55. Run the Nginx Container

Run:

```bash
docker run -d -p 8080:80 --name my-nginx-container my-nginx
```

Now the mapping is:

```
Mac
localhost:8080
       ↓
Container
port 80
       ↓
Nginx
       ↓
index.html
```

Open:

```
http://localhost:8080
```

You should see your webpage.

## 56. Checking the Container

Run:

```bash
docker ps
```

You should see:

```
my-nginx-container
```

To see all containers:

```bash
docker ps -a
```

## 57. Viewing Container Logs

A very useful command:

```bash
docker logs CONTAINER
```

Example:

```bash
docker logs my-nginx-container
```

Logs are extremely important for troubleshooting containers.

You can follow logs using:

```bash
docker logs -f my-nginx-container
```

`-f` means follow the log output.

## 58. Container Inspection

To inspect a container:

```bash
docker inspect CONTAINER
```

Example:

```bash
docker inspect my-nginx-container
```

This provides detailed metadata about:

- Container configuration
- Network information
- Mounts
- Environment variables
- IP address
- Image
- State

## 59. Useful Docker Commands

### Images

```bash
docker images
docker image ls
docker pull nginx
docker inspect nginx
docker rmi nginx
docker image prune
```

### Containers

```bash
docker ps
docker ps -a
docker run nginx
docker start container
docker stop container
docker restart container
docker rm container
docker exec -it container /bin/bash
docker logs container
docker inspect container
```

### Building

```bash
docker build -t image-name .
```

### Cleanup

```bash
docker container prune
docker image prune
docker system prune
```

## 60. Important Command Differences

| Command          | Description                                      |
|------------------|--------------------------------------------------|
| `docker images`  | Lists images.                                    |
| `docker ps`      | Lists running containers.                        |
| `docker ps -a`   | Lists all containers.                            |
| `docker pull`    | Downloads an image.                              |
| `docker run`     | Creates and starts a new container.              |
| `docker start`   | Starts an existing container.                    |
| `docker stop`    | Stops a running container.                       |
| `docker restart` | Restarts a container.                            |
| `docker exec`    | Runs a command inside a running container.       |
| `docker rm`      | Removes a container.                             |
| `docker rmi`     | Removes an image.                                |
| `docker build`   | Builds an image from a Dockerfile.               |
| `docker inspect` | Displays detailed information.                   |
| `docker logs`    | Displays container logs.                         |

## 61. Complete Docker Workflow

A typical workflow is:

```
Write Application
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

For a production workflow:

```
Developer
   ↓
GitHub
   ↓
CI/CD Pipeline
   ↓
Docker Build
   ↓
Docker Image
   ↓
Container Registry
   ↓
Server / Cloud
   ↓
Docker Container
```

## 62. Docker Image Naming

A Docker image can be represented as:

```
registry/repository:tag
```

For example:

```
docker.io/library/nginx:latest
```

Short form:

```
nginx:latest
```

For private registries, the registry address may be included.

Example format:

```
registry.example.com/myteam/myapp:1.0
```

## 63. Why Tags Matter

Imagine an application has versions:

```
myapp:1.0
myapp:1.1
myapp:2.0
```

A deployment can explicitly choose a version:

```bash
docker run myapp:1.1
```

This makes deployments more predictable.

Using only:

```bash
docker run myapp:latest
```

can result in different image contents at different times if the `latest` tag changes.

## 64. Containers Are Ephemeral

Containers are generally designed to be replaceable.

Instead of manually modifying a running container and treating it like a permanent server, a common Docker approach is:

```
Modify Dockerfile
      ↓
Build new image
      ↓
Remove/replace old container
      ↓
Run new container
```

This supports reproducible deployments.

## 65. Container Writable Layer

Docker images are read-only.

When a container starts from an image, Docker adds a writable layer for that container.

Conceptually:

```
Container
┌───────────────────────┐
│ Writable Layer        │
├───────────────────────┤
│ Image Layer 3         │
├───────────────────────┤
│ Image Layer 2         │
├───────────────────────┤
│ Image Layer 1         │
└───────────────────────┘
```

Changes made inside the container's filesystem generally belong to the container's writable layer.

If the container is deleted, those changes can disappear.

Persistent data should therefore be handled using Docker volumes or other external storage mechanisms.

Volumes will be studied in detail later.

## 66. Docker Container vs Virtual Machine

Docker containers and virtual machines are different.

### Virtual Machine

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

### Docker Container

```
Hardware
   ↓
Host OS / Linux environment
   ↓
Docker Engine
   ↓
Containers
   ↓
Applications
```

Containers generally share the host's kernel, whereas each traditional VM includes its own guest operating system.

This makes containers generally lighter and faster to start than full virtual machines.

## 67. Common Docker Use Cases

Docker is commonly used for:

**Development**  
Create consistent development environments.

**Testing**  
Run applications in isolated environments.

**CI/CD**  
Build and test applications automatically.

**Microservices**  
Run individual services independently.

**Cloud Deployment**  
Package applications for deployment to cloud infrastructure.

**Reproducibility**  
Ensure that an application runs in a consistent environment.

## 68. Common Errors and Troubleshooting

### Error: Docker daemon not running

On macOS, make sure Docker Desktop is running.

Check:

```bash
docker info
```

### Error: Port already in use

If port 8080 is already being used:

```bash
docker run -d -p 8081:80 nginx
```

Now:

```
localhost:8081
      ↓
container:80
```

### Container immediately exits

Check:

```bash
docker ps -a
```

Then:

```bash
docker logs CONTAINER
```

The logs often explain why the application stopped.

### Cannot remove image

Check whether a container is using the image:

```bash
docker ps -a
```

Remove the relevant container first if appropriate.

## 69. Docker Security Basics

Never store sensitive information directly inside a Docker image.

Avoid putting:

- Passwords
- API keys
- Access tokens
- Private keys
- Cloud credentials

inside:

```
ENV PASSWORD=...
```

or hardcoding them into application files that are copied into the image.

Secrets should be handled using appropriate secret-management mechanisms.

This topic will become more important when we study cloud and DevSecOps.

## 70. Important Concepts to Remember

Memorize these relationships:

```
Dockerfile
    ↓ docker build
Docker Image
    ↓ docker run
Docker Container
```

And:

```
Docker Image
    ↓
Read-only template

Docker Container
    ↓
Running/stopped instance of an image

Docker Registry
    ↓
Stores and distributes images

Docker Hub
    ↓
Popular public Docker registry
```

## 71. Exam-Oriented Questions

**Q1. What is Docker?**  
Docker is a platform for packaging and running applications in isolated containers.

**Q2. What is a Docker image?**  
A Docker image is a read-only template containing the files, dependencies, configuration, and instructions required to create a container.

**Q3. What is a Docker container?**  
A Docker container is a running or stopped instance of a Docker image.

**Q4. What is Docker Hub?**  
Docker Hub is a public container image registry used to store and distribute Docker images.

**Q5. What does docker pull do?**  
It downloads an image from a container registry to the local Docker environment.

**Q6. What does docker run do?**  
It creates and starts a new container from an image.

**Q7. Difference between docker run and docker start?**  
`docker run` creates a new container, while `docker start` starts an existing stopped container.

**Q8. What does docker ps show?**  
It shows currently running containers.

**Q9. What does docker ps -a show?**  
It shows all containers, including stopped/exited containers.

**Q10. What does -p 8080:80 mean?**  
It maps host port 8080 to container port 80.

**Q11. What is a Dockerfile?**  
A Dockerfile is a text file containing instructions used to build a Docker image.

**Q12. What does docker build -t myapp . mean?**  
It builds a Docker image using the Dockerfile in the current directory and tags the resulting image as myapp.

## 72. Quick Revision Sheet

```bash
# Check Docker
docker --version
docker info

# Images
docker images
docker pull nginx
docker inspect nginx
docker rmi nginx

# Containers
docker ps
docker ps -a

# Run
docker run nginx
docker run -d nginx
docker run -d -p 8080:80 --name my-nginx nginx

# Lifecycle
docker stop my-nginx
docker start my-nginx
docker restart my-nginx

# Access container
docker exec -it my-nginx /bin/bash

# Logs
docker logs my-nginx
docker logs -f my-nginx

# Inspect
docker inspect my-nginx

# Remove
docker rm my-nginx
docker rm -f my-nginx

# Build
docker build -t my-nginx .

# Cleanup
docker container prune
docker image prune
docker system prune
```

## 73. The Most Important Mental Model

Always remember this:

```
                 DOCKER
                    │
          ┌─────────┴─────────┐
          │                   │
      Dockerfile          Existing Image
          │                   │
     docker build        docker pull
          │                   │
          └─────────┬─────────┘
                    ↓
               Docker Image
                    │
                docker run
                    ↓
              Docker Container
                    │
          ┌─────────┼─────────┐
          ↓         ↓         ↓
        Logs      Exec      Ports
```

The fundamental flow is:

```
Dockerfile → Image → Container
```

And when using a registry:

```
Dockerfile
    ↓
docker build
    ↓
Image
    ↓
docker push
    ↓
Registry
    ↓
docker pull
    ↓
Image
    ↓
docker run
    ↓
Container
```

## 74. Chapter 7 Checklist

Before considering this chapter complete, you should be able to explain and practically use:

- What Docker is
- Why Docker is used
- Docker architecture
- Docker client
- Docker daemon
- Docker host
- Docker image
- Docker container
- Image vs container
- Docker registry
- Docker Hub
- Private registries
- Image tags
- latest tag
- Image layers
- docker images
- docker pull
- docker inspect
- docker ps
- docker ps -a
- docker run
- -d
- -i
- -t
- -it
- -p
- --name
- Container lifecycle
- docker stop
- docker start
- docker restart
- docker exec
- docker rm
- docker rmi
- Dangling images
- docker image prune
- docker container prune
- docker system prune
- Dockerfile
- docker build
- Build context
- Basic Dockerfile instructions
- Nginx container
- Port mapping
- Container logs
- Container inspection
- Basic troubleshooting
- Docker image lifecycle
- Docker container lifecycle

## 75. Chapter Summary

Docker provides a standardized way to package and run applications.

The most important relationship is:

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

Images are reusable, read-only templates, while containers are instances created from those images.

Docker images can be downloaded from registries such as Docker Hub using:

```bash
docker pull
```

Containers can be created and started using:

```bash
docker run
```

Running containers can be viewed using:

```bash
docker ps
```

All containers can be viewed using:

```bash
docker ps -a
```

Containers can be managed using:

```bash
docker start
docker stop
docker restart
docker rm
```

Images can be managed using:

```bash
docker images
docker pull
docker rmi
docker image prune
```

Applications running inside containers can be exposed to the host using port mapping:

```
-p HOST_PORT:CONTAINER_PORT
```

For example:

```bash
docker run -d -p 8080:80 nginx
```

This maps:

```
localhost:8080 → container:80
```

The concepts introduced in this chapter form the foundation for later Docker topics such as:

- Advanced Dockerfiles
- Volumes
- Container networking
- Docker Compose
- Image optimization
- Docker security
- CI/CD with Docker
- Kubernetes
- Cloud container services
