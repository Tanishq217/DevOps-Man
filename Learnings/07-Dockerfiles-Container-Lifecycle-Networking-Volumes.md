# Chapter 7 — Dockerfiles, Container Lifecycle, Networking & Volumes

## 1. Chapter Overview

In the previous chapter, we learned the fundamentals of Docker:

- What Docker is
- Why Docker is used
- Docker images
- Docker containers
- Docker Hub
- docker pull
- docker run
- docker ps
- Port mapping

This chapter goes deeper into Docker.

The major topics are:

- Dockerfile
- Dockerfile instructions
- Building Docker images
- Container lifecycle
- Multi-stage Docker builds
- Docker networking
- Docker network types
- Docker volumes
- Bind mounts
- Containerized application workflow

## 2. Dockerfile

A Dockerfile is a text file containing instructions that Docker uses to build a Docker image.

Instead of manually performing:

```
Install dependencies
Copy application
Configure environment
Set working directory
Start application
```

we can define these instructions inside a Dockerfile.

Example:

```dockerfile
FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
```

Docker reads this file and creates an image.

The basic flow is:

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

## 3. Why Do We Need Dockerfiles?

Without a Dockerfile, we would have to manually configure every environment.

For example:

```
Install Python
     ↓
Install dependencies
     ↓
Copy application
     ↓
Configure environment
     ↓
Configure port
     ↓
Start application
```

With a Dockerfile, these steps can be written as code.

This provides:

- Automation
- Reproducibility
- Consistency
- Version control
- Easier deployment
- Easier CI/CD integration

A Dockerfile can also be stored in Git along with the application source code.

## 4. Dockerfile Naming

The conventional filename is:

```
Dockerfile
```

with no file extension.

Example project:

```
my-app/
│
├── Dockerfile
├── app.py
├── requirements.txt
└── README.md
```

Docker can also use a different filename with the `-f` option:

```bash
docker build -f Dockerfile.dev -t my-app .
```

## 5. Dockerfile Instructions

Important Dockerfile instructions covered in this chapter are:

- FROM
- WORKDIR
- COPY
- RUN
- ENV
- EXPOSE
- ARG
- CMD
- ENTRYPOINT
- USER

Each instruction has a specific purpose.

## 6. FROM

`FROM` specifies the base image used to build the new image.

Syntax:

```dockerfile
FROM image:tag
```

Example:

```dockerfile
FROM python:3.12
```

Another example:

```dockerfile
FROM nginx:latest
```

Another:

```dockerfile
FROM ubuntu:24.04
```

Every Dockerfile normally begins with a `FROM` instruction unless it uses a special empty/base-image construction.

## 7. What Is a Base Image?

A base image provides the starting environment for your application.

For example:

```dockerfile
FROM python:3.12
```

provides a Python environment.

Then we add our application:

```
Python Base Image
       +
Application Code
       +
Dependencies
       ↓
Our Docker Image
```

## 8. WORKDIR

`WORKDIR` sets the working directory inside the image/container.

Example:

```dockerfile
WORKDIR /app
```

After this instruction, subsequent commands operate from:

```
/app
```

Example:

```dockerfile
FROM python:3.12

WORKDIR /app

COPY . .
```

The application files are copied into:

```
/app
```

## 9. Why WORKDIR Is Better Than Repeated cd Commands

Instead of:

```dockerfile
RUN cd /app
RUN something
```

use:

```dockerfile
WORKDIR /app
```

It establishes the working directory for subsequent instructions and when the container starts.

## 10. COPY

`COPY` copies files or directories from the build context on the host into the Docker image.

Syntax:

```dockerfile
COPY source destination
```

Example:

```dockerfile
COPY app.py /app/
```

Copy the entire project:

```dockerfile
COPY . .
```

If:

```dockerfile
WORKDIR /app
```

then:

```dockerfile
COPY . .
```

means:

```
Host build context
       ↓
Container image /app
```

## 11. COPY Example

Suppose we have:

```
project/
│
├── Dockerfile
├── app.py
└── requirements.txt
```

Dockerfile:

```dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .
COPY app.py .
```

The resulting image contains:

```
/app/
├── app.py
└── requirements.txt
```

## 12. RUN

`RUN` executes a command during image building.

Example:

```dockerfile
RUN pip install -r requirements.txt
```

Another example:

```dockerfile
RUN apt-get update
```

Another:

```dockerfile
RUN mkdir /app/data
```

Important:

```
RUN → Build time
```

It is executed when:

```bash
docker build
```

is performed.

## 13. RUN vs CMD

This is extremely important.

**RUN**  
Runs commands while building the image.

```dockerfile
RUN pip install flask
```

**CMD**  
Defines the default command when a container starts.

```dockerfile
CMD ["python", "app.py"]
```

Remember:

```
RUN → Build image
CMD → Run container
```

## 14. ENV

`ENV` defines an environment variable inside the image/container.

Syntax:

```dockerfile
ENV VARIABLE=value
```

Example:

```dockerfile
ENV APP_ENV=production
```

Another example:

```dockerfile
ENV PORT=8080
```

The variable can be accessed by the application.

For example, inside a Linux shell:

```bash
echo $PORT
```

## 15. Environment Variables

Environment variables allow configuration to be separated from application code.

Example:

```
APP_ENV=production
PORT=8080
DATABASE_HOST=db
```

Applications can read these values at runtime.

This is especially useful for:

- Database configuration
- Application environment
- Ports
- Feature flags
- Service URLs

### Important Security Note

Do not put passwords, API keys, private keys, or other secrets directly into a Dockerfile using `ENV`.

Secrets should be handled using appropriate secret-management mechanisms.

## 16. EXPOSE

`EXPOSE` documents the port that the application inside the container is expected to listen on.

Example:

```dockerfile
EXPOSE 80
```

For a Python application:

```dockerfile
EXPOSE 5000
```

Important:

`EXPOSE` does not publish the port to the host by itself.

To actually publish a port, use `docker run -p`.

Example:

```bash
docker run -p 8080:5000 my-app
```

Meaning:

```
Host port 8080
       ↓
Container port 5000
```

## 17. EXPOSE vs -p

This is an important exam question.

**Dockerfile**

```dockerfile
EXPOSE 80
```

Documents that the containerized application listens on port 80.

**Docker command**

```bash
docker run -p 8080:80 nginx
```

Actually publishes/maps the container's port 80 to host port 8080.

Remember:

```
EXPOSE → Documentation/metadata
-p     → Port publishing/mapping
```

## 18. ARG

`ARG` defines a build-time variable.

Example:

```dockerfile
ARG VERSION=1.0
```

It can be used while building the image.

Example:

```dockerfile
ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}
```

A value can be supplied during the build:

```bash
docker build --build-arg VERSION=2.0 -t my-app .
```

## 19. ARG vs ENV

Important difference:

| ARG                                 | ENV                                     |
| ----------------------------------- | --------------------------------------- |
| Build-time variable                 | Environment variable                    |
| Mainly available during image build | Available to processes in the container |
| Set using `--build-arg`             | Can be overridden using `docker run -e` |
| Useful for build configuration      | Useful for runtime configuration        |

Example:

```dockerfile
ARG APP_VERSION=1.0
ENV APP_ENV=production
```

## 20. CMD

`CMD` specifies the default command to execute when a container starts.

Example:

```dockerfile
CMD ["python", "app.py"]
```

For Nginx:

```dockerfile
CMD ["nginx", "-g", "daemon off;"]
```

A Dockerfile can contain only one effective `CMD`; if multiple `CMD` instructions are written, the last one takes effect.

## 21. CMD Can Be Overridden

Suppose the Dockerfile contains:

```dockerfile
CMD ["python", "app.py"]
```

You can provide another command when running the container:

```bash
docker run my-app python test.py
```

The supplied command replaces the default `CMD`.

## 22. ENTRYPOINT

`ENTRYPOINT` configures the container to behave like a specific executable.

Example:

```dockerfile
ENTRYPOINT ["python"]
```

Then:

```bash
docker run my-image app.py
```

effectively runs:

```
python app.py
```

## 23. CMD vs ENTRYPOINT

This is a very important Docker concept.

**CMD**  
Provides a default command or arguments.

```dockerfile
CMD ["python", "app.py"]
```

**ENTRYPOINT**  
Defines the main executable.

```dockerfile
ENTRYPOINT ["python"]
```

Combined example:

```dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]
```

Running:

```bash
docker run my-image
```

results conceptually in:

```
python app.py
```

Running:

```bash
docker run my-image test.py
```

results conceptually in:

```
python test.py
```

## 24. USER

`USER` specifies which user should run subsequent Dockerfile commands and/or the container's default process, depending on where it appears.

Example:

```dockerfile
USER appuser
```

Or:

```dockerfile
USER 1000
```

Running applications as a non-root user is generally preferred when root privileges are not required.

This improves security by reducing the privileges available to the application.

## 25. Example Dockerfile

A simple Python application:

```dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV APP_ENV=production

EXPOSE 5000

CMD ["python", "app.py"]
```

Flow:

```
FROM
 ↓
WORKDIR
 ↓
COPY requirements.txt
 ↓
RUN dependencies
 ↓
COPY application
 ↓
ENV
 ↓
EXPOSE
 ↓
CMD
```

## 26. Building a Docker Image

Once the Dockerfile is created, build the image:

```bash
docker build -t my-app .
```

Explanation:

```
docker build → Build image
-t my-app    → Give image a tag/name
.            → Build context is current directory
```

## 27. What Is the Build Context?

The final `.` in:

```bash
docker build -t my-app .
```

represents the build context.

It tells Docker which directory's files are available to `COPY` and `ADD` instructions during the build.

For example:

```
project/
│
├── Dockerfile
├── app.py
└── requirements.txt
```

Running:

```bash
cd project
docker build -t my-app .
```

uses `project/` as the build context.

## 28. .dockerignore

A `.dockerignore` file specifies files/directories that should not be sent as part of the build context.

Example:

```
.git
.gitignore
node_modules
__pycache__
*.log
.env
```

This is important because it:

- Reduces build context size
- Speeds up builds
- Prevents unnecessary files from being copied
- Helps avoid accidentally including sensitive/local files

## 29. Checking the Built Image

After building:

```bash
docker images
```

Example:

```
REPOSITORY   TAG       IMAGE ID
my-app       latest    abc123
```

You can then run it:

```bash
docker run my-app
```

## 30. Container Lifecycle

A container goes through different states during its lifetime.

A simplified lifecycle is:

```
Created
   ↓
Running
   ↓
Stopped
   ↓
Deleted
```

It can also be:

```
Running
   ↓
Paused
   ↓
Running
```

Important states:

- Created
- Running
- Paused
- Stopped/Exited
- Deleted

## 31. Creating a Container Without Starting It

Use:

```bash
docker container create nginx
```

This creates a container but does not start it.

Conceptually:

```
Image
 ↓
docker container create
 ↓
Created Container
```

## 32. Starting a Created Container

Use:

```bash
docker container start CONTAINER
```

Example:

```bash
docker container start my-nginx
```

Now the container starts running.

## 33. Pausing a Container

Use:

```bash
docker container pause CONTAINER
```

A paused container remains present, but its processes are temporarily suspended.

Resume it using:

```bash
docker container unpause CONTAINER
```

Flow:

```
Running
   ↓
pause
   ↓
Paused
   ↓
unpause
   ↓
Running
```

## 34. Stopping a Container

Use:

```bash
docker container stop CONTAINER
```

This gracefully asks the main process to stop and, if necessary, terminates it after the configured timeout.

A stopped container still exists.

Check:

```bash
docker ps -a
```

## 35. Starting a Stopped Container

A stopped container can be started again:

```bash
docker container start CONTAINER
```

Important difference:

```bash
docker run
```

creates a new container from an image.

Whereas:

```bash
docker start
```

starts an existing container.

## 36. Removing a Container

Use:

```bash
docker rm CONTAINER
```

A container generally must be stopped before it can be removed.

You can force removal using:

```bash
docker rm -f CONTAINER
```

Lifecycle:

```
Image
 ↓
Create
 ↓
Container
 ↓
Start
 ↓
Running
 ↓
Stop
 ↓
Stopped
 ↓
Remove
 ↓
Deleted
```

## 37. Container Lifecycle Commands

| Lifecycle Operation | Command                  |
| ------------------- | ------------------------ |
| Create              | docker container create  |
| Start               | docker container start   |
| Pause               | docker container pause   |
| Unpause             | docker container unpause |
| Stop                | docker container stop    |
| Remove              | docker container rm      |

## 38. docker run vs docker create

**docker create**  
Creates a container but does not start it.

```bash
docker create nginx
```

**docker run**  
Creates and starts a container.

```bash
docker run nginx
```

Conceptually:

```
docker run
   =
docker create
   +
docker start
```

## 39. Multi-Stage Docker Builds

A multi-stage build uses multiple `FROM` instructions in one Dockerfile.

It is commonly used to:

- Reduce final image size
- Separate build dependencies from runtime dependencies
- Improve security
- Keep production images clean

Typical structure:

```
Builder Stage
     ↓
Build Application
     ↓
Runtime Stage
     ↓
Copy Required Output
     ↓
Final Image
```

## 40. Why Multi-Stage Builds Are Needed

Suppose we build a Node.js application.

During development/building, we might need:

- Node.js
- npm
- Development dependencies
- Build tools
- Source code

But the final application may need only:

- Node.js runtime
- Production dependencies
- Built application files

There is no reason to keep all build tools in the final image.

## 41. Multi-Stage Example

```dockerfile
# Stage 1: Builder
FROM node:22 AS builder

WORKDIR /app

COPY package*.json .

RUN npm install

COPY . .

RUN npm run build


# Stage 2: Runtime
FROM node:22-alpine

WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

RUN npm install --omit=dev

CMD ["node", "dist/index.js"]
```

The first stage builds the application.

The second stage contains only what is needed to run it.

## 42. Multi-Stage Build Architecture

```
              Dockerfile
                  │
        ┌─────────┴─────────┐
        ↓                   ↓
   Builder Stage        Runtime Stage
        │                   │
 Install tools          Minimal setup
 Build application          │
        │                   │
        └───────┐           │
                ↓           │
        Required files ─────┘
                ↓
          Final Image
```

## 43. Advantages of Multi-Stage Builds

**Smaller Images**  
Build tools do not need to be included in the final image.

**Better Security**  
Fewer unnecessary packages and tools are present.

**Faster Deployment**  
Smaller images can be transferred more efficiently.

**Cleaner Production Environment**  
Only runtime requirements are included.

## 44. Docker Networking

Docker networking allows containers to communicate with:

- Other containers
- The host
- External services
- The internet

Basic command:

```bash
docker network ls
```

This lists Docker networks.

## 45. Docker Network Commands

**List networks**

```bash
docker network ls
```

**Create network**

```bash
docker network create my-network
```

**Connect container**

```bash
docker network connect my-network CONTAINER
```

**Disconnect container**

```bash
docker network disconnect my-network CONTAINER
```

**Remove network**

```bash
docker network rm my-network
```

## 46. Docker Network Types

Important Docker network drivers/types include:

- Bridge
- Host
- None
- Overlay

Each has a different purpose.

## 47. Bridge Network

Bridge is the common/default network driver for containers on a single Docker host.

Example:

```bash
docker network create my-network
```

This creates a user-defined bridge network by default.

Containers connected to the same user-defined bridge network can communicate with one another.

Conceptually:

```
Container A
     │
     │
Bridge Network
     │
     │
Container B
```

## 48. Default Bridge vs User-Defined Bridge

There are important differences.

**Default Bridge**  
Docker provides a default network called:

```
bridge
```

**User-Defined Bridge**  
You can create your own:

```bash
docker network create app-network
```

User-defined bridge networks generally provide better isolation and built-in DNS-based service discovery between containers.

## 49. Example User-Defined Bridge Network

Create network:

```bash
docker network create app-network
```

Run database:

```bash
docker run -d \
  --name database \
  --network app-network \
  postgres
```

Run backend:

```bash
docker run -d \
  --name backend \
  --network app-network \
  my-backend
```

The backend can communicate with the database using its container/service name in an appropriate configuration:

```
database
```

rather than needing to know the container's IP address.

This is extremely useful for multi-container applications.

## 50. Host Network

With host networking, the container shares the host's network namespace.

Example:

```bash
docker run --network host nginx
```

The container does not get the same kind of isolated network stack as a normal bridge-networked container.

Port publishing with `-p` is generally unnecessary with host networking because the application uses the host's network directly.

**Advantage**  
Potentially less network overhead.

**Disadvantage**  
Less network isolation.

Host networking behavior and availability can differ across operating systems, so it is especially important to understand the Linux behavior when studying Docker networking.

## 51. None Network

The `none` network disables normal network connectivity for the container.

Example:

```bash
docker run --network none nginx
```

The container has only its local loopback interface rather than normal external/container networking.

Useful when an application does not require networking or when strict network isolation is desired.

## 52. Overlay Network

Overlay networking is designed for communication across multiple Docker hosts.

Conceptually:

```
Docker Host A                  Docker Host B
      │                              │
Container A                    Container B
      │                              │
      └──────── Overlay Network ─────┘
```

It is commonly associated with Docker Swarm and multi-host container networking.

In modern production environments, Kubernetes uses its own networking model and CNI-based networking rather than simply using Docker's overlay network.

## 53. Docker Network Comparison

| Network | Main Purpose                       |
| ------- | ---------------------------------- |
| Bridge  | Containers on a single Docker host |
| Host    | Share host network stack           |
| None    | Disable normal networking          |
| Overlay | Multi-host Docker networking       |

## 54. Docker Volumes

Containers are generally considered ephemeral.

If a container is deleted, data stored only inside its writable layer may be lost.

For persistent data, Docker provides storage mechanisms such as:

- Volumes
- Bind mounts

## 55. Docker Volume

A Docker volume is storage managed by Docker.

Create a volume:

```bash
docker volume create my-volume
```

List volumes:

```bash
docker volume ls
```

Inspect a volume:

```bash
docker volume inspect my-volume
```

Remove a volume:

```bash
docker volume rm my-volume
```

## 56. Using a Volume With a Container

Example:

```bash
docker run -d \
  --name my-container \
  -v my-volume:/data \
  nginx
```

Conceptually:

```
Docker Volume
     │
     ↓
/data inside container
```

The data remains available independently of the container's lifecycle.

## 57. Bind Mounts

A bind mount maps a specific directory/file on the host directly into the container.

Example:

```bash
docker run -d \
  -v /Users/me/project:/app \
  my-app
```

Conceptually:

```
Mac Host
/Users/me/project
        │
        ↓
Container
/app
```

Changes made on the host can immediately appear inside the container.

## 58. Volumes vs Bind Mounts

| Docker Volume                              | Bind Mount                               |
| ------------------------------------------ | ---------------------------------------- |
| Managed by Docker                          | Managed by user/host filesystem          |
| Docker controls storage location           | User specifies host path                 |
| Good for persistent application data       | Good for development/source-code sharing |
| Less dependent on host directory structure | Directly tied to host path               |

## 59. Development With Bind Mounts

Suppose you're developing a Node.js application.

Your code is located on your Mac:

```
~/projects/my-app
```

You can mount it into the container:

```bash
docker run -v ~/projects/my-app:/app my-node-app
```

Now:

```
Mac
   ↓
~/projects/my-app
   ↓
Container
   ↓
/app
```

When you modify code on your Mac, the changed files can be visible inside the container immediately.

This can make development much easier.

## 60. Named Volumes vs Bind Mounts

**Named Volume**

```
-v my-volume:/data
```

Docker manages the storage.

**Bind Mount**

```
-v /host/path:/container/path
```

You specify the host path.

Remember:

```
Volume
→ Docker-managed storage

Bind Mount
→ Host directory mapped directly
```

## 61. Containerizing Multiple Applications

A major practical assignment is to containerize:

- Nginx
- Apache
- React
- Java
- Python
- Node.js

The general process is:

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
     ↓
Test Application
```

## 62. Nginx Container

Example:

```bash
docker pull nginx
```

Run:

```bash
docker run -d -p 8080:80 --name nginx-container nginx
```

Check:

```bash
docker ps
```

Open:

```
http://localhost:8080
```

## 63. Apache Container

Apache HTTP Server is another popular web server.

A container can be started from an appropriate Apache image.

The general pattern is:

```bash
docker pull httpd
docker run -d -p 8080:80 --name apache-container httpd
```

If port 8080 is already being used by another container, choose another host port:

```bash
docker run -d -p 8081:80 --name apache-container httpd
```

## 64. Python Application Container

Typical Dockerfile:

```dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Build:

```bash
docker build -t python-app .
```

Run:

```bash
docker run -d -p 5000:5000 python-app
```

## 65. Node.js Application Container

Typical Dockerfile:

```dockerfile
FROM node:22

WORKDIR /app

COPY package*.json .

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

Build:

```bash
docker build -t node-app .
```

Run:

```bash
docker run -d -p 3000:3000 node-app
```

## 66. Java Application Container

A Java application can use a Java runtime/base image.

Example:

```dockerfile
FROM eclipse-temurin:21-jre

WORKDIR /app

COPY target/app.jar app.jar

EXPOSE 8080

CMD ["java", "-jar", "app.jar"]
```

Build:

```bash
docker build -t java-app .
```

Run:

```bash
docker run -d -p 8080:8080 java-app
```

The exact Java version and artifact name depend on the application.

## 67. React Application Container

React applications are commonly built into static files and served using a web server such as Nginx.

A multi-stage build is a good approach:

```dockerfile
FROM node:22 AS builder

WORKDIR /app

COPY package*.json .

RUN npm install

COPY . .

RUN npm run build


FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
```

The first stage builds the React application.

The second stage serves the generated static files.

## 68. Why React Benefits From Multi-Stage Builds

The Node.js environment is required to build the React application.

But after:

```
npm run build
```

we usually need only the generated static files.

Therefore:

```
Node.js + Source Code + Build Tools
             ↓
          Build App
             ↓
         Static Files
             ↓
       Minimal Nginx Image
```

This can significantly reduce the final image compared with keeping the complete Node.js build environment.

## 69. Docker Build Process

When executing:

```bash
docker build -t my-app .
```

Docker:

- Reads the Dockerfile.
- Processes instructions.
- Sends/uses the build context.
- Pulls the base image if necessary.
- Executes build instructions.
- Creates filesystem layers.
- Produces the final image.

Conceptually:

```
Dockerfile
    ↓
Build Context
    ↓
Docker Build Engine
    ↓
Layers
    ↓
Final Docker Image
```

## 70. Docker Image Layers and Caching

Docker can cache previously built layers.

Suppose:

```dockerfile
COPY package*.json .
RUN npm install
COPY . .
```

If application source code changes but `package.json` does not, Docker may reuse the cached dependency-installation layer.

This can make builds faster.

Therefore, Dockerfile instruction order matters.

A common optimization is to copy dependency files before copying the entire source tree.

## 71. Good Dockerfile Practices

**Use an appropriate base image**  
Prefer a suitable official or trusted image.

**Keep images small**  
Avoid unnecessary packages.

**Use .dockerignore**  
Do not send unnecessary files into the build context.

**Use multi-stage builds**  
Especially for compiled/build-based applications.

**Avoid secrets**  
Never hard-code passwords or API keys into Dockerfiles.

**Use non-root users**  
Where practical.

**Use meaningful tags**  
Example:

```bash
docker build -t my-app:1.0 .
```

**Keep instructions logically organized**  
Readable Dockerfiles are easier to maintain.

## 72. Common Docker Mistakes

**Mistake 1 — Confusing RUN and CMD**

Wrong understanding:

```
RUN = command when container starts
```

Correct:

```
RUN → build time
CMD → container runtime
```

**Mistake 2 — Thinking EXPOSE Publishes a Port**

```dockerfile
EXPOSE 8080
```

does not automatically make the application accessible from the host.

Use:

```bash
docker run -p 8080:8080 image
```

**Mistake 3 — Confusing Image and Container**

```
Image     → Template
Container → Running/created instance
```

**Mistake 4 — Using docker start to create a new container**

`docker start` starts an existing container.  
`docker run` creates and starts a new container.

**Mistake 5 — Storing Everything Inside Container**

Containers should not be treated as the best place for important persistent data.

Use volumes or appropriate external storage.

## 73. Practical Docker Workflow

A typical developer workflow:

```
1. Write application
       ↓
2. Create Dockerfile
       ↓
3. Create .dockerignore
       ↓
4. Build image
       ↓
docker build
       ↓
5. Check image
       ↓
docker images
       ↓
6. Run container
       ↓
docker run
       ↓
7. Test application
       ↓
8. Check logs/status
       ↓
9. Stop/remove container
       ↓
10. Improve Dockerfile
```

## 74. Important Commands — Chapter 7

### Images

```bash
docker images
docker pull IMAGE
docker build -t NAME .
docker rmi IMAGE
```

### Containers

```bash
docker ps
docker ps -a
docker run IMAGE
docker create IMAGE
docker start CONTAINER
docker stop CONTAINER
docker restart CONTAINER
docker pause CONTAINER
docker unpause CONTAINER
docker rm CONTAINER
docker rm -f CONTAINER
```

### Container execution

```bash
docker exec -it CONTAINER /bin/bash
```

If Bash isn't installed:

```bash
docker exec -it CONTAINER /bin/sh
```

### Networks

```bash
docker network ls
docker network create NETWORK
docker network connect NETWORK CONTAINER
docker network disconnect NETWORK CONTAINER
docker network rm NETWORK
docker network inspect NETWORK
```

### Volumes

```bash
docker volume ls
docker volume create VOLUME
docker volume inspect VOLUME
docker volume rm VOLUME
```

## 75. docker exec

`docker exec` allows you to execute a command inside an already-running container.

Example:

```bash
docker exec -it my-nginx /bin/bash
```

If Bash isn't available:

```bash
docker exec -it my-nginx /bin/sh
```

Explanation:

```
docker exec
    ↓
Execute command
    ↓
Inside existing container
```

This is useful for troubleshooting and inspecting containers.

## 76. Complete Dockerfile Example

```dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_ENV=production

EXPOSE 5000

CMD ["python", "app.py"]
```

Build:

```bash
docker build -t my-python-app:1.0 .
```

Run:

```bash
docker run -d \
  --name my-python-container \
  -p 5000:5000 \
  my-python-app:1.0
```

Check:

```bash
docker ps
```

## 77. Complete Mental Model

You should now understand the complete relationship:

```
                   Dockerfile
                       │
                       │ docker build
                       ↓
                 Docker Image
                       │
                       │ docker run
                       ↓
                Docker Container
                  /     |      \
                 /      |       \
                ↓       ↓        ↓
            Network   Volume   Application
```

And for image distribution:

```
Dockerfile
    ↓
Docker Image
    ↓
docker push
    ↓
Docker Registry
    ↓
docker pull
    ↓
Another Docker Host
    ↓
Docker Container
```

## 78. Important Exam Questions

**Q1. What is a Dockerfile?**  
A Dockerfile is a text file containing instructions used to build a Docker image.

**Q2. What does FROM do?**  
`FROM` specifies the base image used for building the Docker image.

**Q3. What does WORKDIR do?**  
`WORKDIR` sets the working directory for subsequent Dockerfile instructions and the default working directory for the container.

**Q4. What does COPY do?**  
`COPY` copies files/directories from the build context into the image.

**Q5. What does RUN do?**  
`RUN` executes commands during image construction.

**Q6. What does CMD do?**  
`CMD` specifies the default command/arguments executed when a container starts.

**Q7. What does ENTRYPOINT do?**  
`ENTRYPOINT` configures the container's main executable.

**Q8. What does EXPOSE do?**  
`EXPOSE` documents the port that the containerized application listens on. It does not itself publish the port to the host.

**Q9. What is ARG?**  
`ARG` defines a variable available during image build.

**Q10. What is ENV?**  
`ENV` defines environment variables available to processes in the container.

**Q11. What is a multi-stage Docker build?**  
A multi-stage build uses multiple build stages so that the final image contains only the files and dependencies needed at runtime.

**Q12. Why use multi-stage builds?**  
To:

- Reduce image size
- Remove build dependencies
- Improve security
- Create cleaner production images

**Q13. What is Docker networking?**  
Docker networking provides communication between containers, the host, and external networks.

**Q14. What is a bridge network?**  
A bridge network provides networking for containers on a Docker host and allows connected containers to communicate.

**Q15. What is a host network?**  
Host networking allows the container to share the host's network stack.

**Q16. What is a none network?**  
It provides a container with no normal external/container network connectivity.

**Q17. What is an overlay network?**  
An overlay network enables container networking across multiple Docker hosts.

**Q18. What is a Docker volume?**  
A Docker volume is Docker-managed persistent storage that can exist independently of a container.

**Q19. What is a bind mount?**  
A bind mount maps a specific host filesystem path into a container.

**Q20. Difference between volume and bind mount?**  

**Volume**  
→ Docker manages storage.

**Bind mount**  
→ User specifies the host path.

## 79. Interview Questions

**Q: What is the difference between Docker image and Docker container?**  
An image is a read-only template used to create containers, while a container is an instance of that image.

**Q: What is the difference between docker run and docker start?**  
`docker run` creates and starts a new container from an image.  
`docker start` starts an existing stopped container.

**Q: What is the difference between docker create and docker run?**  
`docker create` creates a container without starting it.  
`docker run` creates and starts a container.

**Q: What is the difference between RUN and CMD?**  

```
RUN → Executes during image build.
CMD → Default command when container starts.
```

**Q: What is the difference between CMD and ENTRYPOINT?**  
`ENTRYPOINT` defines the main executable, while `CMD` provides default command/arguments that can be overridden more easily at runtime.

**Q: Does EXPOSE publish a port?**  
No.

For example:

```dockerfile
EXPOSE 8080
```

does not automatically publish the port.

You need:

```bash
docker run -p 8080:8080 image
```

**Q: Why are Docker images layered?**  
Layers allow Docker to reuse filesystem components and build/cache images efficiently.

**Q: Why are multi-stage builds useful?**  
They allow build environments and runtime environments to be separated, resulting in smaller and cleaner production images.

**Q: Why use Docker volumes?**  
To persist data independently of the container lifecycle.

**Q: Why use bind mounts?**  
They are particularly useful during development when host source files need to be shared with a container.

## 80. Practical Homework Structure

For each application, create a separate directory.

Example:

```
dev-ops/
│
├── Session7-Docker/
│   │
│   ├── Nginx/
│   │   ├── Dockerfile
│   │   ├── index.html
│   │   └── README.md
│   │
│   ├── Apache/
│   │   ├── Dockerfile
│   │   └── README.md
│   │
│   ├── React/
│   │   ├── Dockerfile
│   │   ├── .dockerignore
│   │   └── README.md
│   │
│   ├── Java/
│   │   ├── Dockerfile
│   │   └── README.md
│   │
│   ├── Python/
│   │   ├── Dockerfile
│   │   └── README.md
│   │
│   └── Node/
│       ├── Dockerfile
│       └── README.md
```

The exact folder name should follow the repository/session naming convention being used for the course.

## 81. What to Include in README.md

For each application, document:

**1. Application Name**  
Example:  
Nginx Docker Application

**2. Dockerfile**  
Explain the important instructions.

**3. Build Command**

```bash
docker build -t nginx-custom .
```

**4. Run Command**

```bash
docker run -d -p 8080:80 --name nginx-container nginx-custom
```

**5. Verify Container**

```bash
docker ps
```

**6. Open Application**

```
http://localhost:8080
```

**7. Screenshots**  
Include screenshots showing:

- Dockerfile
- Build command/output
- Running container
- Application in browser

**8. Short Explanation**  
Explain what you did and how the application works.

## 82. Git Workflow for the Assignment

After completing the Docker work:

```bash
git status
```

Then:

```bash
git add .
```

Commit:

```bash
git commit -m "Add Docker application assignments"
```

Push:

```bash
git push
```

If the assignment requires a branch and Pull Request:

```bash
git checkout -b docker-assignment
```

Make changes:

```bash
git add .
git commit -m "Add Docker assignments"
git push -u origin docker-assignment
```

Then create a Pull Request on GitHub.

## 83. Chapter 7 Final Checklist

Before considering this chapter complete, you should understand:

- What a Dockerfile is
- Why Dockerfiles are used
- FROM
- Base images
- WORKDIR
- COPY
- RUN
- ENV
- EXPOSE
- ARG
- CMD
- ENTRYPOINT
- USER
- ARG vs ENV
- RUN vs CMD
- CMD vs ENTRYPOINT
- EXPOSE vs -p
- Docker build context
- .dockerignore
- docker build
- Image layers
- Docker build cache
- Container lifecycle
- Created state
- Running state
- Paused state
- Stopped/exited state
- Deleted state
- docker create
- docker start
- docker pause
- docker unpause
- docker stop
- docker rm
- Multi-stage builds
- Builder stage
- Runtime stage
- Docker networking
- Bridge network
- Default bridge
- User-defined bridge
- Host network
- None network
- Overlay network
- Docker network commands
- Docker volumes
- Named volumes
- Bind mounts
- Volume vs bind mount
- docker exec
- Containerizing Nginx
- Containerizing Apache
- Containerizing Python
- Containerizing Node.js
- Containerizing Java
- Containerizing React
- README documentation
- Git/GitHub submission workflow

## 84. Chapter 7 Quick Revision

The most important concepts to remember:

```
Dockerfile
    ↓
docker build
    ↓
Image
    ↓
docker run
    ↓
Container
```

**Dockerfile**

```
FROM
WORKDIR
COPY
RUN
ENV
EXPOSE
ARG
CMD
ENTRYPOINT
USER
```

**Container lifecycle**

```
Created
   ↓
Running
   ↓
Paused
   ↓
Running
   ↓
Stopped
   ↓
Deleted
```

**Networking**

```
Bridge
Host
None
Overlay
```

**Storage**

```
Docker Volume
     vs
Bind Mount
```

**Multi-stage build**

```
Builder Stage
      ↓
Build Application
      ↓
Copy Required Output
      ↓
Runtime Stage
      ↓
Small Final Image
```

## 85. One-Line Memory Tricks

```
FROM       → Start from this image
WORKDIR    → Work here
COPY       → Bring files here
RUN        → Build-time command
ENV        → Runtime environment variable
EXPOSE     → Document container port
ARG        → Build-time variable
CMD        → Default startup command
ENTRYPOINT → Main executable
USER       → Run as this user
```

And:

```
Image      = Blueprint
Container  = Instance
Registry   = Image storage/distribution
Volume     = Persistent Docker-managed storage
Bind Mount = Host path mapped into container
Network    = Container communication
Dockerfile = Image-building instructions
```

## Chapter 7 — Final Summary

Dockerfiles allow applications to be packaged into reproducible Docker images.

The basic process is:

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
Docker Container
```

Dockerfiles use instructions such as `FROM`, `WORKDIR`, `COPY`, `RUN`, `ENV`, `EXPOSE`, `ARG`, `CMD`, `ENTRYPOINT`, and `USER`.

The container lifecycle includes creation, starting, running, pausing, stopping, and deletion.

Multi-stage builds separate the build environment from the final runtime environment and can produce smaller, cleaner images.

Docker networking allows containers to communicate. The major network types introduced are:

- Bridge
- Host
- None
- Overlay

Docker also provides persistent storage through volumes, while bind mounts allow host directories to be directly shared with containers.

The most important mental model for this chapter is:

```
                 Dockerfile
                     │
                     ↓
                docker build
                     │
                     ↓
                Docker Image
                     │
                     ↓
                 docker run
                     │
                     ↓
              Docker Container
                /          \
               ↓            ↓
           Network        Storage
              │              │
              ↓              ↓
          Containers      Volumes
```

By the end of this chapter, you should be able to create a Dockerfile, build an image, run and manage containers, understand their lifecycle, create Docker networks, attach containers to networks, use persistent storage, and understand why multi-stage builds are useful in production.

These concepts form the foundation for the more advanced Docker topics that follow.
