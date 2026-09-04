# Chapter 8 — Docker Architecture, Networking, Volumes & Docker Compose

## 1. Chapter Overview

Docker is a containerization platform that allows applications and their dependencies to be packaged and run consistently across different environments.

In the previous chapter, we learned about:

* Docker images
* Docker containers
* Dockerfiles
* Container lifecycle
* Docker networking
* Docker volumes
* Multi-stage builds

This chapter goes deeper into Docker's architecture and focuses heavily on:

* Docker architecture
* Docker objects
* Docker commands
* Docker networking
* Network drivers
* Docker volumes
* Bind mounts
* Docker Compose
* Multi-container applications
* Service-to-service communication
* Persistent data
* Docker Compose networking and volumes
* Practical Docker workflows
* Docker best practices

---

## 2. Docker Architecture

Docker follows a **client-server architecture**.

The main components are:

```text
+----------------------+
|    Docker Client     |
|       (CLI)          |
+----------+-----------+
           |
           | Docker API
           v
+----------------------+
|    Docker Daemon     |
|       dockerd        |
+----------+-----------+
           |
           +-------------------+
           |                   |
           v                   v
      Docker Objects      Docker Registry
                           (Docker Hub etc.)
```

### 2.1 Docker Client

The Docker Client is the interface through which we interact with Docker.

The most common client is the Docker CLI:

```bash
docker
```

Examples:

```bash
docker ps
docker images
docker run nginx
docker build -t myapp .
```

When we execute a Docker command, the Docker CLI communicates with the Docker daemon through the Docker API.

---

### 2.2 Docker Daemon

The Docker daemon is the background service responsible for performing Docker operations.

The daemon is commonly called:

```text
dockerd
```

It manages:

* Images
* Containers
* Networks
* Volumes
* Container lifecycle
* Image builds
* Networking
* Storage

For example, when we run:

```bash
docker run nginx
```

the Docker client sends the request to the Docker daemon.

The daemon then:

1. Finds the requested image.
2. Downloads it if necessary.
3. Creates a container.
4. Creates/configures its networking.
5. Creates/configures its filesystem.
6. Starts the container.

---

### 2.3 Docker Registry

A Docker registry stores Docker images.

The most commonly used public registry is Docker Hub.

Examples of images available from registries:

```text
nginx
ubuntu
python
node
redis
mysql
```

When we execute:

```bash
docker pull nginx
```

Docker downloads the image from a registry.

Private organizations can also run or use private registries.

---

## 3. Main Docker Objects

Four important Docker objects are:

1. Images
2. Containers
3. Networks
4. Volumes

```text
                 Docker
                   |
       +-----------+-----------+
       |           |           |
    Images     Containers   Networks
                               |
                            Volumes
```

---

## 4. Docker Images

A Docker image is a read-only template used to create containers.

Examples:

```text
nginx
ubuntu
python:3.12
node:22
```

List images:

```bash
docker images
```

Modern equivalent:

```bash
docker image ls
```

Example:

```text
REPOSITORY   TAG       IMAGE ID       SIZE
nginx        latest    abc123         192MB
python       3.12      def456         1GB
```

An image can be used to create multiple containers.

```text
             nginx image
                 |
       +---------+---------+
       |         |         |
       v         v         v
   Container  Container  Container
      1           2          3
```

---

## 5. Docker Containers

A container is a running or stopped instance of a Docker image.

For example:

```bash
docker run -d nginx
```

creates a container from the `nginx` image.

List running containers:

```bash
docker ps
```

List all containers:

```bash
docker ps -a
```

This includes:

* Running containers
* Stopped containers
* Exited containers
* Created containers

---

## 6. Docker Networks

Docker networks allow containers to communicate with:

* Other containers
* The host
* External networks
* The internet

List networks:

```bash
docker network ls
```

Example:

```text
NETWORK ID     NAME      DRIVER
abc123         bridge    bridge
def456         host      host
ghi789         none      null
```

---

## 7. Docker Volumes

Volumes provide persistent storage for containers.

Normally, container writable data is tied to the container lifecycle.

If a container is removed, data stored only inside its writable layer can be lost.

Volumes solve this problem.

```text
Container
    |
    | mounts
    v
Volume
    |
    v
Persistent Data
```

Volumes are particularly important for databases.

Examples:

* MySQL
* PostgreSQL
* MongoDB
* Redis
* Elasticsearch

---

## 8. Important Docker Commands

### 8.1 List Images

```bash
docker images
```

or:

```bash
docker image ls
```

---

### 8.2 List Running Containers

```bash
docker ps
```

---

### 8.3 List All Containers

```bash
docker ps -a
```

---

## 9. Cleaning Docker Resources

Docker can accumulate unused:

* Containers
* Images
* Networks
* Volumes

This can consume significant disk space.

Docker provides pruning commands.

---

### 9.1 Remove Stopped Containers

```bash
docker container prune
```

Docker asks for confirmation.

This removes stopped containers.

---

### 9.2 Remove Unused Images

```bash
docker image prune
```

By default, this primarily removes dangling images.

To remove all unused images:

```bash
docker image prune -a
```

Be careful with `-a`.

It can remove images that are not currently associated with any container but may still be useful later.

---

### 9.3 Remove Unused Volumes

```bash
docker volume prune
```

Be careful because deleting a volume can permanently delete its data.

---

### 9.4 Remove Unused Networks

```bash
docker network prune
```

This removes networks that are not currently used by containers.

---

### 9.5 Docker System Prune

```bash
docker system prune
```

This removes unused Docker resources such as:

* Stopped containers
* Unused networks
* Dangling images
* Build cache

It does **not** normally remove volumes unless explicitly requested.

To include unused volumes:

```bash
docker system prune --volumes
```

Use prune commands carefully.

---

## 10. Docker Networking

Networking is one of the most important Docker concepts.

Containers often need to communicate with:

* Other containers
* Databases
* Backend services
* Frontend applications
* External APIs
* The internet

Docker provides network drivers to control this communication.

Important network drivers include:

1. Bridge
2. Host
3. None
4. Overlay

---

## 11. Bridge Network

The `bridge` network driver is the most commonly used network driver for standalone Docker containers.

Docker provides a default bridge network.

Check it:

```bash
docker network ls
```

You will usually see:

```text
bridge
host
none
```

---

## 12. Default Bridge Network

Docker automatically creates a default bridge network named:

```text
bridge
```

Containers can be attached to it.

Example:

```bash
docker run -d --name container1 nginx
```

Another:

```bash
docker run -d --name container2 nginx
```

Both containers may be attached to the default bridge network.

However, the default bridge network has limitations.

One important limitation is that automatic container-name DNS resolution is not available in the same convenient way as on user-defined bridge networks.

---

## 13. User-Defined Bridge Network

A user-defined bridge network is generally preferred when multiple standalone containers need to communicate.

Create one:

```bash
docker network create my-network
```

Check:

```bash
docker network ls
```

Example:

```text
NETWORK ID     NAME          DRIVER
abc123         my-network    bridge
```

Run containers on it:

```bash
docker run -d --name app1 --network my-network nginx
```

```bash
docker run -d --name app2 --network my-network nginx
```

Now the containers can communicate using their container names.

For example:

```text
app1 ---> app2
```

`app1` can use:

```text
http://app2
```

instead of needing to manually discover an IP address.

---

## 14. Why User-Defined Bridge Networks Are Better

User-defined bridge networks provide:

* Better isolation
* Automatic DNS resolution
* Easier container-to-container communication
* More control over network membership

Example:

```text
my-network

+----------------------+
|                      |
|   app1 <----------> app2
|                      |
+----------------------+
```

This is extremely useful for multi-container applications.

---

## 15. Docker Network Commands

### List networks

```bash
docker network ls
```

---

### Create network

```bash
docker network create my-network
```

---

### Inspect network

```bash
docker network inspect my-network
```

This provides information such as:

* Network driver
* Subnet
* Gateway
* Connected containers

---

### Connect a container

```bash
docker network connect my-network container1
```

---

### Disconnect a container

```bash
docker network disconnect my-network container1
```

---

### Remove network

```bash
docker network rm my-network
```

The network generally must not have containers attached to it.

---

## 16. Host Network

The `host` network driver allows a container to use the host's network namespace rather than having its own normal isolated network namespace.

Example:

```bash
docker run --network host nginx
```

With host networking, Docker does not provide the normal container-to-host port publishing mechanism.

For example, you generally don't use:

```bash
-p 8080:80
```

with host networking.

The application listens directly through the host network namespace.

### Important Mac Note

On Linux, host networking closely corresponds to sharing the host's network namespace.

On Docker Desktop for macOS, containers run inside a Linux virtual machine, so `--network host` does **not** behave exactly like sharing the macOS host's network stack.

Therefore, when practicing on a Mac, do not assume Linux host-network behavior maps directly to macOS.

---

## 17. None Network

The `none` network driver provides a highly isolated networking environment.

Example:

```bash
docker run --network none nginx
```

The container does not have normal external network connectivity.

It still has a loopback interface, but it does not have normal external networking.

Useful for:

* Highly isolated workloads
* Security-sensitive processing
* Testing applications that should not communicate externally

---

## 18. Overlay Network

The `overlay` network driver is designed for communication between containers running on different Docker hosts.

Conceptually:

```text
Docker Host 1                 Docker Host 2

+-------------+               +-------------+
| Container A | <------------> | Container B |
+-------------+    Overlay    +-------------+
```

Overlay networks are particularly associated with multi-host Docker environments such as Docker Swarm.

They allow containers on different Docker nodes to communicate as though they were part of the same logical network.

---

## 19. Comparing Docker Network Drivers

| Driver  | Main Purpose                           |
| ------- | -------------------------------------- |
| Bridge  | Normal standalone container networking |
| Host    | Share host network namespace           |
| None    | Disable external networking            |
| Overlay | Multi-host container networking        |

---

## 20. Docker Volumes

Containers are generally considered ephemeral.

This means a container can be:

```text
Created
   ↓
Running
   ↓
Stopped
   ↓
Removed
```

If important data exists only inside the container's writable layer, removing the container can remove that data.

For persistent data, use volumes or bind mounts.

---

## 21. Types of Docker Storage

Two important storage approaches are:

1. Docker-managed volumes
2. Bind mounts

There are also anonymous volumes, which are Docker-managed but not explicitly given a user-defined name.

---

## 22. Named Volumes

A named volume is managed by Docker.

Create one:

```bash
docker volume create my-volume
```

List volumes:

```bash
docker volume ls
```

Inspect:

```bash
docker volume inspect my-volume
```

Remove:

```bash
docker volume rm my-volume
```

---

## 23. Using a Volume with a Container

Example:

```bash
docker run -d \
  --name database \
  -v my-volume:/data \
  some-image
```

Here:

```text
my-volume:/data
```

means:

```text
Docker-managed volume
        |
        v
   /data inside container
```

The data stored in `/data` is kept in the volume rather than being tied only to the container.

---

## 24. Why Volumes Are Important

Volumes are useful when:

* A container stores database data
* Data must survive container replacement
* Multiple containers need access to shared data
* Application state needs persistent storage

For example:

```text
MongoDB Container
       |
       v
MongoDB Volume
       |
       v
Persistent Database Data
```

If the MongoDB container is removed and another container mounts the same volume, the data can remain available.

---

## 25. Bind Mounts

A bind mount directly maps a path on the host machine into a container.

Conceptually:

```text
Host Machine
    |
    | /Users/me/project
    |
    v
Container
    |
    | /app
```

Example:

```bash
docker run -it \
  -v "$(pwd):/app" \
  node:22
```

This maps the current host directory to:

```text
/app
```

inside the container.

---

## 26. Why Bind Mounts Are Useful

Bind mounts are especially useful during development.

Suppose we have:

```text
project/
├── index.js
├── package.json
└── src/
```

We mount:

```text
project/ → /app
```

inside the container.

When we modify:

```text
index.js
```

on the host, the container sees the updated file because both locations refer to the same underlying host files.

This is useful for:

* Development
* Live reload
* Testing
* Editing source code from the host

---

## 27. Volumes vs Bind Mounts

| Feature                                  | Named Volume     | Bind Mount          |
| ---------------------------------------- | ---------------- | ------------------- |
| Managed by Docker                        | Yes              | No                  |
| Host path explicitly selected            | No               | Yes                 |
| Good for databases                       | Yes              | Possible            |
| Good for source-code development         | Less common      | Excellent           |
| Docker manages storage location          | Yes              | No                  |
| Easy to move between Docker environments | Generally easier | Host-path dependent |

---

## 28. Modern `--mount` Syntax

Instead of `-v`, Docker also supports the more explicit `--mount` syntax.

Named volume:

```bash
docker run -d \
  --mount type=volume,source=my-volume,target=/data \
  nginx
```

Bind mount:

```bash
docker run -it \
  --mount type=bind,source="$(pwd)",target=/app \
  node:22
```

`--mount` is often easier to understand because every option is explicitly named.

---

## 29. Docker Compose

Docker Compose is used to define and run **multi-container applications**.

Instead of manually executing many `docker run` commands, we can define the application's configuration in a YAML file.

For example, imagine an application containing:

```text
Frontend
   |
   v
Backend
   |
   v
Database
```

Without Compose, we might need several Docker commands.

With Compose, these services can be defined together.

---

## 30. Why Docker Compose?

Consider an application containing:

* React frontend
* Node.js backend
* MongoDB database

We need:

```text
Frontend Container
        |
        v
Backend Container
        |
        v
MongoDB Container
```

We could manually create all three containers and configure:

* Networks
* Ports
* Environment variables
* Volumes
* Dependencies

This becomes inconvenient.

Docker Compose lets us define these requirements in one configuration file.

---

## 31. Compose File

A common file name is:

```text
compose.yaml
```

or:

```text
docker-compose.yml
```

Modern Docker Compose uses the Compose Specification, and `docker compose` is the preferred command syntax.

---

## 32. Basic Docker Compose Structure

Example:

```yaml
services:

  backend:
    image: node:22
    ports:
      - "3000:3000"

  database:
    image: mongo
```

This defines two services:

```text
backend
database
```

Each service normally corresponds to a container created by Compose.

---

## 33. Services

A service represents a container configuration in the Compose application.

Example:

```yaml
services:
  backend:
    image: node:22

  database:
    image: mongo
```

Here:

```text
backend → Node.js container
database → MongoDB container
```

---

## 34. Ports in Compose

Example:

```yaml
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

This means:

```text
Host Port 8080
       |
       v
Container Port 80
```

We can access the application through:

```text
localhost:8080
```

Remember:

`EXPOSE` in a Dockerfile does not publish a port.

Publishing is done using:

```bash
-p 8080:80
```

or Compose:

```yaml
ports:
  - "8080:80"
```

---

## 35. Compose Networks

Compose automatically creates a default network for an application unless configured otherwise.

Services connected to the same Compose network can communicate using service names.

Example:

```yaml
services:

  backend:
    image: my-backend

  database:
    image: mongo
```

The backend can communicate with MongoDB using:

```text
database
```

as the hostname.

Conceptually:

```text
backend
   |
   | http://database:27017
   v
database
```

We do not normally need to hard-code the database container's IP address.

---

## 36. Compose Volumes

Volumes can also be defined in Compose.

Example:

```yaml
services:

  database:
    image: mongo
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```

This creates a named volume:

```text
mongo-data
```

and mounts it into:

```text
/data/db
```

inside the MongoDB container.

---

## 37. Complete Compose Example

A simple application can contain:

* Backend
* Database

Example:

```yaml
services:

  backend:
    image: node:22
    ports:
      - "3000:3000"
    depends_on:
      - database

  database:
    image: mongo
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```

Architecture:

```text
                    Docker Compose
                         |
              +----------+----------+
              |                     |
              v                     v
        Backend Service       Database Service
              |                     |
              |                     |
              +------ Network ------+
                                    |
                                    v
                              mongo-data
                                volume
```

---

## 38. Docker Compose Commands

### Start services

Modern syntax:

```bash
docker compose up
```

Run in the background:

```bash
docker compose up -d
```

The older syntax:

```bash
docker-compose up
```

may still exist on some systems, but modern Docker installations generally use:

```bash
docker compose
```

---

## 39. Stop and Remove Services

```bash
docker compose down
```

This normally:

* Stops containers
* Removes containers
* Removes the Compose-created network

It does **not** automatically remove named volumes unless explicitly requested.

To also remove Compose-managed volumes:

```bash
docker compose down -v
```

Be careful because this can delete persistent data stored in those volumes.

---

## 40. List Compose Services

```bash
docker compose ps
```

This shows containers associated with the Compose project.

---

## 41. View Compose Logs

```bash
docker compose logs
```

Follow logs:

```bash
docker compose logs -f
```

Logs for a specific service:

```bash
docker compose logs backend
```

---

## 42. Rebuild Compose Services

If an application has a Dockerfile and the Dockerfile or source configuration changes, we can rebuild:

```bash
docker compose build
```

Then start:

```bash
docker compose up -d
```

Or combine the workflow:

```bash
docker compose up -d --build
```

---

## 43. `depends_on`

`depends_on` specifies service dependency relationships.

Example:

```yaml
services:

  backend:
    image: my-backend
    depends_on:
      - database

  database:
    image: mongo
```

This tells Compose that the backend service depends on the database service.

However, an important distinction must be understood:

> `depends_on` controls service startup/shutdown ordering; it does not automatically guarantee that the database is fully ready to accept connections.

For robust applications, health checks and application-level retry logic may be required.

---

## 44. Health Checks

A health check allows Docker to determine whether a containerized application is healthy.

Example:

```yaml
services:

  database:
    image: mongo
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5
```

Compose can then use health information when configuring dependencies.

---

## 45. Environment Variables in Compose

Environment variables can be defined using:

```yaml
environment:
  NODE_ENV: production
  PORT: 3000
```

Or:

```yaml
environment:
  - NODE_ENV=production
  - PORT=3000
```

For sensitive values, avoid committing secrets directly into Git.

Use appropriate secret-management mechanisms for production environments.

---

## 46. Building an Application with Compose

Suppose we have:

```text
project/
├── compose.yaml
├── backend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
└── frontend/
    ├── Dockerfile
    ├── package.json
    └── src/
```

Compose can build both applications.

Example:

```yaml
services:

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"

  backend:
    build: ./backend
    ports:
      - "8080:8080"
```

Here:

```text
build: ./frontend
```

means Compose uses the Dockerfile and build context in the `frontend` directory.

Similarly:

```text
build: ./backend
```

builds the backend image.

---

## 47. Compose Application Architecture

A realistic application might look like:

```text
                    Internet
                       |
                       v
                  Frontend
                       |
                       v
                  Backend API
                       |
                       v
                    Database
                       |
                       v
                  Persistent
                    Volume
```

Docker Compose can define all of these components.

---

## 48. Example: React + Node.js + MongoDB

Example architecture:

```text
+----------------------+
| React Frontend       |
| Port 3000            |
+----------+-----------+
           |
           v
+----------------------+
| Node.js Backend      |
| Port 8080            |
+----------+-----------+
           |
           v
+----------------------+
| MongoDB              |
| Port 27017           |
+----------+-----------+
           |
           v
+----------------------+
| MongoDB Volume       |
+----------------------+
```

A Compose file could conceptually define:

```yaml
services:

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"

  backend:
    build: ./backend
    ports:
      - "8080:8080"
    depends_on:
      - database

  database:
    image: mongo
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```

The services automatically share the Compose application's network.

---

## 49. Container-to-Container Communication

One of the most important Docker concepts is:

> Containers should communicate using service/container names rather than hard-coded IP addresses whenever possible.

Example:

```text
backend → database
```

Instead of:

```text
mongodb://192.168.x.x:27017
```

use:

```text
mongodb://database:27017
```

where `database` is the Compose service name.

This makes the application more portable because container IP addresses can change.

---

## 50. Port Mapping vs Container Networking

These are two different concepts.

### Port Mapping

Used to make a container service accessible from the host.

Example:

```yaml
ports:
  - "8080:80"
```

Means:

```text
Host:8080 → Container:80
```

---

### Container Networking

Used for communication between containers.

Example:

```text
backend → database:27017
```

The backend does not need the database's port published to the host merely for container-to-container communication.

This is an important architectural principle.

---

## 51. Internal vs External Services

Suppose:

```text
Frontend
   |
   v
Backend
   |
   v
Database
```

The database does not necessarily need:

```yaml
ports:
  - "27017:27017"
```

if only the backend needs to access it.

The database can remain accessible only within the Docker network.

This improves isolation.

---

## 52. Multi-Stage Builds — Recap

Multi-stage builds were introduced previously.

They allow multiple stages within one Dockerfile.

Example:

```dockerfile
FROM node:22 AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build


FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
```

There are two stages:

```text
Builder Stage
     |
     | build application
     v
Runtime Stage
     |
     | copy only required files
     v
Final Image
```

The final image does not need all of the tools and dependencies used during the build.

Benefits:

* Smaller images
* Reduced attack surface
* Cleaner production containers
* Separation of build and runtime dependencies

---

## 53. Docker Architecture — Complete Picture

Putting everything together:

```text
                       Docker Client
                            |
                            | Docker API
                            v
                     Docker Daemon
                       /    |    \
                      /     |     \
                     v      v      v
                 Images Containers Networks
                              |
                              v
                           Volumes

                            |
                            v
                       Docker Registry
```

Docker Compose sits above these components and allows us to define an entire multi-container application.

```text
                 Docker Compose
                       |
        +--------------+--------------+
        |              |              |
      Service        Network        Volume
        |                              |
        v                              v
    Containers                    Persistent Data
```

---

## 54. Practical Example 1 — Create a Custom Network

Create a network:

```bash
docker network create app-network
```

Run the first container:

```bash
docker run -d \
  --name web1 \
  --network app-network \
  nginx
```

Run another:

```bash
docker run -d \
  --name web2 \
  --network app-network \
  nginx
```

Check:

```bash
docker network inspect app-network
```

You should see both containers attached.

---

## 55. Practical Example 2 — Test Container Communication

Run a container:

```bash
docker run -d \
  --name server \
  --network app-network \
  nginx
```

Run another interactive container:

```bash
docker run -it \
  --name client \
  --network app-network \
  alpine sh
```

Inside the Alpine container:

```bash
wget -qO- http://server
```

The client can resolve:

```text
server
```

through Docker's user-defined bridge network DNS.

---

## 56. Practical Example 3 — Create a Persistent Volume

Create:

```bash
docker volume create app-data
```

Run a container:

```bash
docker run -it \
  --name storage-test \
  -v app-data:/data \
  alpine sh
```

Inside:

```bash
echo "Hello Docker" > /data/message.txt
```

Exit:

```bash
exit
```

Remove the container:

```bash
docker rm storage-test
```

Create another container using the same volume:

```bash
docker run -it \
  -v app-data:/data \
  alpine sh
```

Check:

```bash
cat /data/message.txt
```

The data should still exist.

This demonstrates persistence.

---

## 57. Practical Example 4 — Bind Mount

Create a directory:

```bash
mkdir docker-dev
cd docker-dev
```

Create a file:

```bash
echo "Hello from host" > index.html
```

Run:

```bash
docker run -it \
  --mount type=bind,source="$(pwd)",target=/app \
  alpine sh
```

Inside the container:

```bash
cat /app/index.html
```

You should see:

```text
Hello from host
```

Now modify `index.html` on the host.

The container sees the change because `/app` is a bind mount.

---

## 58. Practical Example 5 — Docker Compose

Create:

```text
compose-demo/
└── compose.yaml
```

Add:

```yaml
services:

  web:
    image: nginx
    ports:
      - "8080:80"

  alpine:
    image: alpine
    command: ["sleep", "3600"]
```

Start:

```bash
docker compose up -d
```

Check:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

Stop and remove:

```bash
docker compose down
```

---

## 59. Docker Compose Development Workflow

A common workflow is:

```bash
docker compose up -d
```

Check:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

Make code/configuration changes.

Rebuild if necessary:

```bash
docker compose up -d --build
```

Stop:

```bash
docker compose down
```

---

## 60. Important Docker Networking Concepts

### Container IP addresses can change

Do not build applications around fixed container IP addresses.

Prefer:

```text
database
backend
redis
```

as hostnames when using a user-defined network or Compose.

---

### Published ports are mainly for host/external access

Example:

```text
8080:80
```

means:

```text
Host port 8080
       ↓
Container port 80
```

It is not required merely because two containers need to communicate.

---

### Containers on the same network can communicate

Example:

```text
frontend
   |
   v
backend
   |
   v
database
```

All can be connected to the same Docker network.

---

## 61. Important Docker Storage Concepts

### Container filesystem

Container writable-layer data is tied to the container.

### Named volume

Docker manages the storage.

```text
volume → container
```

### Bind mount

The host controls the source path.

```text
host path → container path
```

---

## 62. Docker on macOS

Since Docker Desktop on macOS runs Linux containers inside a Linux virtual machine, some Docker behavior differs from native Linux.

Important points:

* Containers are Linux environments.
* Docker storage ultimately resides inside Docker Desktop's Linux VM.
* Bind mounts are specially shared between macOS and the Linux VM.
* Linux-specific commands and networking behavior may not map exactly to macOS.
* `docker` commands themselves work normally from the Mac terminal.
* Docker Desktop manages the Docker engine rather than using Linux `systemctl`.

Check Docker:

```bash
docker info
```

Check version:

```bash
docker version
```

If Docker Desktop is not running, many Docker commands will fail because the Docker daemon is unavailable.

---

## 63. Docker Best Practices

### 63.1 Use User-Defined Networks

Prefer:

```bash
docker network create my-network
```

for applications requiring multiple containers.

This provides better isolation and convenient DNS-based service discovery.

---

### 63.2 Use Volumes for Persistent Data

Do not store important database data only inside the container writable layer.

Use:

```text
Named Volume
```

for persistent application data.

---

### 63.3 Use Bind Mounts for Development

Bind mounts are useful when source code is edited on the host.

Example:

```text
Host source code
       ↓
Container /app
```

---

### 63.4 Avoid Hard-Coding Container IPs

Bad:

```text
192.168.1.25
```

Better:

```text
database
```

---

### 63.5 Do Not Publish Unnecessary Ports

If only the backend needs to access the database, the database does not necessarily need its port published to the host.

Keep internal services internal whenever possible.

---

### 63.6 Use Compose for Multi-Container Applications

Instead of manually managing:

```text
frontend
backend
database
redis
```

use Docker Compose to define them together.

---

### 63.7 Be Careful with Prune Commands

Commands such as:

```bash
docker system prune
```

and especially:

```bash
docker system prune --volumes
```

can remove resources you may still need.

Always understand what will be deleted before confirming.

---

## 64. Common Docker Problems

### Problem 1 — Container cannot communicate with another container

Check:

```bash
docker network ls
```

Then:

```bash
docker network inspect my-network
```

Make sure both containers are connected to the same network.

---

### Problem 2 — Using container IP addresses

Avoid hard-coding IP addresses.

Use container/service names on user-defined networks.

---

### Problem 3 — Port already in use

Example:

```text
Bind for 0.0.0.0:8080 failed: port is already allocated
```

Check what is using the port.

```bash
docker ps
```

Then either stop the existing container or choose another host port:

```bash
docker run -p 8081:80 nginx
```

---

### Problem 4 — Data disappeared after deleting container

If data was stored only inside the container writable layer, removing the container can remove that data.

Use a volume:

```bash
docker volume create my-data
```

and mount it.

---

### Problem 5 — `docker compose down` and data

Remember:

```bash
docker compose down
```

normally does not remove named volumes.

But:

```bash
docker compose down -v
```

removes Compose-managed volumes.

Be careful with the `-v` option.

---

### Problem 6 — `docker exec` cannot find Bash

Some minimal images do not contain Bash.

Instead of:

```bash
docker exec -it container bash
```

try:

```bash
docker exec -it container sh
```

For Alpine-based images, `/bin/sh` is commonly available.

---

## 65. Important Command Cheat Sheet

### Images

```bash
docker images
docker image ls
docker pull nginx
docker build -t myapp:1.0 .
docker image prune
```

### Containers

```bash
docker run nginx
docker ps
docker ps -a
docker start container
docker stop container
docker rm container
docker logs container
docker exec -it container sh
docker inspect container
```

### Networks

```bash
docker network ls
docker network create my-network
docker network inspect my-network
docker network connect my-network container
docker network disconnect my-network container
docker network rm my-network
docker network prune
```

### Volumes

```bash
docker volume create my-volume
docker volume ls
docker volume inspect my-volume
docker volume rm my-volume
docker volume prune
```

### Compose

```bash
docker compose up
docker compose up -d
docker compose down
docker compose ps
docker compose logs
docker compose logs -f
docker compose build
docker compose up -d --build
```

### Cleanup

```bash
docker container prune
docker image prune
docker volume prune
docker network prune
docker system prune
```

---

## 66. Docker Objects Relationship

A useful way to understand Docker is:

```text
                    Docker Image
                         |
                         | creates
                         v
                    Container
                    /        \
                   /          \
                  v            v
              Network       Volume
                  |            |
                  v            v
          Communication    Persistent Data
```

For a real application:

```text
                Docker Compose
                       |
       +---------------+---------------+
       |               |               |
       v               v               v
   Frontend         Backend         Database
       |               |               |
       +---------------+---------------+
                       |
                  Docker Network
                       |
                       v
                Database Volume
```

---

## 67. Key Concepts to Remember

### Docker Architecture

```text
Client → Docker Daemon → Docker Objects
```

### Four Major Objects

```text
Images
Containers
Networks
Volumes
```

### Network Drivers

```text
Bridge → normal container networking
Host → host network namespace
None → network isolation
Overlay → multi-host networking
```

### Storage

```text
Named Volume → Docker-managed persistent storage
Bind Mount → host path mapped into container
```

### Docker Compose

```text
Compose
   |
   +── Services
   |
   +── Networks
   |
   +── Volumes
```

### Service Discovery

Prefer:

```text
database
```

instead of:

```text
192.168.x.x
```

### Port Mapping

```text
Host:Container
8080:80
```

### Persistence

```text
Container + Volume = Persistent Data
```

---

## 68. Interview Questions

### Q1. What is Docker architecture?

Docker uses a client-server architecture in which the Docker CLI communicates with the Docker daemon through the Docker API. The daemon manages Docker objects such as images, containers, networks, and volumes.

---

### Q2. What are the four major Docker objects?

The four major objects are:

1. Images
2. Containers
3. Networks
4. Volumes

---

### Q3. What is a Docker network?

A Docker network provides communication between containers and, depending on configuration, communication with the host and external networks.

---

### Q4. What is the difference between default bridge and user-defined bridge?

A user-defined bridge network provides better isolation and built-in DNS-based service discovery between containers using names. The default bridge network has fewer conveniences and is generally less suitable for multi-container application architectures.

---

### Q5. What is host networking?

Host networking allows a container to use the host's network namespace instead of the usual isolated container network namespace.

---

### Q6. What is the `none` network?

The `none` network provides a highly isolated container networking environment with no normal external network connectivity.

---

### Q7. What is an overlay network?

An overlay network allows containers on different Docker hosts/nodes to communicate over a logical Docker network, commonly in multi-host environments such as Docker Swarm.

---

### Q8. What is a Docker volume?

A Docker volume is Docker-managed storage that can persist independently of a container's lifecycle.

---

### Q9. Volume vs bind mount?

A volume is managed by Docker, while a bind mount maps a specific host filesystem path into a container.

---

### Q10. Why are bind mounts useful in development?

They allow files edited on the host to be immediately visible inside the container, making them useful for development and live-reload workflows.

---

### Q11. What is Docker Compose?

Docker Compose is a tool for defining and running multi-container applications using a declarative YAML configuration.

---

### Q12. What is a service in Docker Compose?

A service defines the configuration for a containerized component of the Compose application.

Examples:

```text
frontend
backend
database
redis
```

---

### Q13. How do containers communicate in Docker Compose?

Services in the same Compose network can communicate using service names as DNS hostnames.

Example:

```text
backend → database:27017
```

---

### Q14. Does `depends_on` guarantee application readiness?

No.

`depends_on` primarily controls dependency startup/shutdown ordering. It does not by itself guarantee that the dependent service is fully ready to accept requests.

Health checks and application-level retry mechanisms may be needed.

---

### Q15. Does `EXPOSE` publish a port?

No.

`EXPOSE` documents the port that an application expects to listen on.

Actual host publishing requires:

```bash
-p 8080:80
```

or Compose:

```yaml
ports:
  - "8080:80"
```

---

## 69. Practical Learning Checklist

Before considering this chapter complete, make sure you can perform these operations yourself.

### Docker Basics

* [ ] List images
* [ ] List running containers
* [ ] List all containers
* [ ] Inspect a container
* [ ] View container logs
* [ ] Enter a running container

### Networking

* [ ] List networks
* [ ] Create a custom bridge network
* [ ] Connect containers to the network
* [ ] Test container-to-container communication
* [ ] Inspect a network
* [ ] Disconnect a container
* [ ] Remove a network

### Volumes

* [ ] Create a named volume
* [ ] List volumes
* [ ] Inspect a volume
* [ ] Mount a volume
* [ ] Delete a container and verify persistent data
* [ ] Understand bind mounts

### Docker Compose

* [ ] Create a `compose.yaml`
* [ ] Define multiple services
* [ ] Start services
* [ ] Run Compose in detached mode
* [ ] Check service status
* [ ] View logs
* [ ] Stop and remove services
* [ ] Rebuild services
* [ ] Configure a volume
* [ ] Configure service dependencies
* [ ] Understand service-name DNS

---

## 70. Final Summary

Docker provides a complete environment for packaging, running, networking, and storing containerized applications.

The most important concepts from this chapter are:

```text
Docker Architecture
        ↓
Client → Daemon → Docker Objects
                    ↓
        +-----------+-----------+
        |           |           |
      Images    Containers   Networks
                                |
                             Volumes
```

Docker networking allows containers to communicate.

The major network drivers are:

```text
Bridge
Host
None
Overlay
```

For application development, **user-defined bridge networks** are especially important because they provide isolation and convenient DNS-based service discovery.

Docker storage allows data to survive container replacement.

The two major approaches are:

```text
Named Volumes
Bind Mounts
```

Docker Compose allows multiple containers to be managed as a single application.

For example:

```text
             Docker Compose
                    |
       +------------+------------+
       |            |            |
       v            v            v
   Frontend      Backend      Database
                                |
                                v
                              Volume
```

The key idea is:

> **Docker handles individual containers, while Docker Compose makes it much easier to define and manage an entire multi-container application.**

Understanding these concepts is an important foundation for later DevOps topics such as:

* CI/CD
* Kubernetes
* Container orchestration
* Microservices
* Cloud deployments
* Infrastructure as Code
* Production monitoring
* Container security
