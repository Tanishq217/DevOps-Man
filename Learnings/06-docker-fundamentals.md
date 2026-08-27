# DevOps — Chapter 6: Docker Fundamentals and Containerization

> **Goal:** Learn why Docker is used, how it works, and how to build, run, inspect, and troubleshoot containers.

---

## 1. Recap: Git, GitHub, and DevOps

Git tracks changes locally as commits. GitHub hosts Git repositories online and adds collaboration, backup, pull requests, Issues, Projects, and automation.

Important commands from the previous chapter:

- `git init` starts tracking a project folder.
- `git add` stages selected changes.
- `git commit` saves a local snapshot.
- `git push` uploads commits to GitHub.
- `git cherry-pick` applies one selected commit to the current branch.

`git merge` combines histories and keeps the existing commit structure. `git rebase` reapplies commits on a new base, giving a linear history but rewriting commit hashes. Do not rebase shared work without team agreement.

Git and Docker are used together: Git tracks source code, Dockerfiles, CI/CD workflows, and infrastructure configuration. Docker turns that versioned application into a consistent runnable package.

## 2. What Is Docker?

**Docker** is a platform for building, packaging, distributing, and running applications in isolated units called **containers**.

A container packages an application with its runtime, libraries, dependencies, and required operating-system-level files. This helps it behave consistently on a developer laptop, test server, and production environment.

Docker addresses the classic problem:

> “It works on my machine, but not on the server.”

Docker does not eliminate all deployment work. Networking, secrets, data persistence, monitoring, security, and correct configuration still matter.

## 3. Why Docker Is Needed

### Traditional Python deployment

Without Docker, deploying a Python application commonly requires:

1. Set up a server with a suitable operating system, commonly Linux.
2. Install the intended Python version.
3. Install Git.
4. Clone the code repository.
5. Create a Python virtual environment.
6. Install packages from `requirements.txt`.
7. Configure environment variables, users, firewall ports, and process management.
8. Start the app and ensure it remains available.
9. Repeat equivalent setup for development, staging, and production.

Example:

```bash
sudo apt update
sudo apt install -y python3 python3-venv git
git clone https://github.com/USERNAME/my-python-app.git
cd my-python-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

This is manageable for one simple application, but becomes fragile with many services needing different Python, Node.js, Java, system-library, or package versions.

### Dependency hell

**Dependency hell** occurs when applications need conflicting versions of runtimes or libraries. For example, one app needs Python 3.10 and another needs Python 3.12; a shared system upgrade can break an existing service.

Containers isolate each application's user-space dependencies, allowing multiple versions to run on one host more predictably.

### Repeatability and scale

A Dockerfile describes the deployment environment as code. Docker builds that definition into an image and runs the image as a container:

```text
Application code + Dockerfile
              ↓ docker build
         Docker image
              ↓ docker run
       Running container
```

The same tested image can be run in many places. Scaling can mean creating more replicas of that image rather than manually repeating server setup. Kubernetes later automates this across many machines.

## 4. Core Docker Concepts

| Term | Meaning |
| --- | --- |
| Dockerfile | Text instructions that build an image |
| Image | Read-only, immutable template for containers |
| Container | Runnable instance of an image |
| Registry | Service that stores and distributes images |
| Docker Hub | Default public Docker registry |
| Volume | Docker-managed persistent data storage |
| Bind mount | Exact host file/folder mounted into a container |
| Network | Virtual network for container communication |
| Port mapping | Publishing a container port through a host port |
| Docker daemon | Background service that manages Docker objects |

### Image vs. container

An image is a **blueprint**. A container is a **running instance** made from that blueprint. One image can create many containers:

```text
nginx image
  ├── development container
  ├── test container
  └── production container
```

An image should be immutable. A running container has a small writable layer, but its changes disappear when the container is removed unless data is saved in a volume or bind mount.

## 5. Images, Tags, and Layers

Docker images contain layers. Most Dockerfile instructions create a layer; unchanged layers can be cached and shared, speeding builds and saving disk space.

```text
Application image
├── Application code
├── Installed dependencies
├── OS packages
└── Base runtime image
```

Dockerfile order affects cache use. Copy dependency definitions and install them before copying frequently changing application code:

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

Images have names and tags:

```text
nginx:latest
python:3.12-slim
mydockeruser/my-app:1.0.0
```

Tags identify versions, but can change. Prefer explicit, tested versions such as `python:3.12-slim` instead of relying on `latest` in production.

## 6. Docker Architecture

Docker uses client-server architecture.

```text
Docker client (docker command)
          |
          | Docker API
          v
Docker daemon on Docker host
  ├── Builds images
  ├── Runs containers
  ├── Creates networks and volumes
  └── Pulls/pushes images
          |
          v
Registry: Docker Hub or private registry
```

### Docker client

The Docker client is normally the `docker` command. Commands like `docker pull`, `docker build`, and `docker run` are sent to the Docker daemon.

### Docker daemon and host

The **Docker daemon** (`dockerd`) does the work: it builds images, starts/stops containers, manages networks and volumes, and connects to registries. The **Docker host** is the machine running the daemon and storing local Docker objects.

### Registry and Docker Hub

A registry stores images. Docker Hub is the default registry and includes:

- **Official images**, maintained or curated for common software such as `nginx`, `python`, `postgres`, and `redis`.
- **Verified publisher images**, published by verified organizations.
- **Community images**, published by users or organizations.

Use reputable images, read their documentation, pin versions, and scan images before production use.

### Pull/run flow

1. The client sends `docker run` to the daemon.
2. The daemon checks whether the image exists locally.
3. If it is missing, Docker pulls its layers from a registry.
4. Docker creates a container, including writable layer, network, mounts, and command.
5. Docker starts the container's main process.

## 7. Docker vs. Virtual Machines

| Containers | Virtual Machines |
| --- | --- |
| Share the host OS kernel | Each VM has a complete guest OS |
| Usually smaller and faster to start | Heavier and slower to boot |
| Package application dependencies | Package a full operating environment |
| High workload density | More resource overhead |
| OS-process-level isolation | Hardware virtualization isolation |

Containers are not miniature VMs. Linux containers share the Linux kernel. On macOS and Windows, Docker Desktop commonly uses a lightweight Linux VM behind the scenes. Both approaches are useful; VMs may offer stronger isolation or different OS support, while containers excel at fast portable application packaging.

## 8. Installing Docker on Linux

Exact installation steps vary by distribution. Use Docker's official documentation for the target Linux distribution and production setup.

After installation, verify client, daemon, and service:

```bash
docker --version
docker info
sudo systemctl status docker
```

Run the standard verification image:

```bash
sudo docker run hello-world
```

Docker downloads `hello-world` if necessary, runs it, and prints confirmation.

### Docker permissions

The Docker socket has powerful host-level access. The Docker group is effectively root-equivalent. Only add trusted users:

```bash
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
```

Log out and back in if required.

Useful service commands:

```bash
sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl status docker
```

`enable` starts Docker automatically after a reboot.

## 9. Hands-On: Run Nginx

Nginx is a popular web server and reverse proxy.

```bash
docker pull nginx
docker images
```

`docker pull nginx` downloads the image; without a tag it uses the default `latest` tag. `docker images` lists local images.

Run it in the background:

```bash
docker run -d -p 8080:80 nginx
```

Open `http://localhost:8080` in a browser. The Nginx welcome page should appear.

| Part | Meaning |
| --- | --- |
| `docker run` | Create and start a container |
| `-d` | Detached mode: run in background |
| `-p 8080:80` | Map host port 8080 to container port 80 |
| `nginx` | Image to run |

Port syntax is:

```text
-p HOST_PORT:CONTAINER_PORT
```

Nginx listens on port 80 inside its container. Docker accepts traffic at host port 8080 and forwards it to container port 80.

A named container is easier to manage:

```bash
docker run -d --name my-nginx -p 8080:80 nginx
```

### Inspect and manage a container

```bash
docker ps
docker ps -a
docker logs my-nginx
docker logs -f my-nginx
docker exec -it my-nginx sh
docker stop my-nginx
docker start my-nginx
docker rm my-nginx
```

- `docker ps` shows running containers; `docker ps -a` also shows stopped ones.
- `docker logs -f` follows logs.
- `docker exec -it` runs an interactive command inside an already running container. Lightweight images commonly have `sh`, not `bash`.
- Stop a container before removing it. `docker rm -f` forces removal and should be used carefully.

## 10. Port Mapping Troubleshooting

If the Nginx page does not open:

1. Confirm it is running:

```bash
docker ps
```

2. Confirm the `PORTS` column resembles `0.0.0.0:8080->80/tcp`.
3. Review logs:

```bash
docker logs my-nginx
```

4. Test locally:

```bash
curl http://localhost:8080
```

5. Check whether the host port is in use:

```bash
sudo ss -ltnp | grep :8080
```

6. Try a different host port:

```bash
docker run -d --name my-nginx-2 -p 8081:80 nginx
```

Use `http://localhost:8081`. Multiple containers may use port 80 internally, but only one can publish a particular host port at a time.

A frequent error is reversed port order. `-p 8080:80` is host 8080 to container 80. `-p 80:8080` incorrectly assumes Nginx listens on 8080 inside the container.

## 11. Serve a Static Website

Create an `index.html` inside a local folder, then mount that folder into Nginx:

```bash
docker run -d \
  --name static-site \
  -p 8080:80 \
  -v "$(pwd)":/usr/share/nginx/html:ro \
  nginx
```

- `-v HOST_PATH:CONTAINER_PATH:ro` is a bind mount.
- `$(pwd)` is the current host directory.
- `:ro` makes the mount read-only in the container.
- Nginx serves `/usr/share/nginx/html` by default.

For a production-style static-site image, copy content during the build:

```dockerfile
FROM nginx:1.27-alpine
COPY . /usr/share/nginx/html
```

```bash
docker build -t my-static-site:1.0 .
docker run -d --name static-site -p 8080:80 my-static-site:1.0
```

## 12. Dockerfile Fundamentals

A Dockerfile is a plain-text build recipe.

| Instruction | Purpose |
| --- | --- |
| `FROM` | Choose base image |
| `WORKDIR` | Set working folder |
| `COPY` | Copy files to image |
| `RUN` | Execute command at build time |
| `ENV` | Define environment variables |
| `EXPOSE` | Document application port |
| `CMD` | Provide default start command |
| `ENTRYPOINT` | Define fixed main executable |

Important differences:

- `RUN` happens while the image is built, for example installing packages.
- `CMD` provides the default container command and can be overridden at `docker run`.
- `ENTRYPOINT` sets the main executable; `CMD` can supply default arguments.
- `EXPOSE` does not publish a port. `docker run -p` publishes it.

## 13. Containerize a Simple Python Application

Example `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.get("/")
def home():
    return "Hello from Docker!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Example `requirements.txt`:

```text
Flask==3.0.3
```

Dockerfile:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

Explanation:

1. `FROM` starts with a Python runtime image.
2. `WORKDIR /app` sets the application folder.
3. Copy/install requirements first, enabling dependency-layer caching.
4. Copy source code.
5. `EXPOSE 5000` documents the listening port.
6. `CMD` starts the app.

The Flask application binds to `0.0.0.0`, not `127.0.0.1`. Inside a container, `127.0.0.1` accepts only connections from that container; `0.0.0.0` accepts traffic forwarded through Docker networking.

Build and run from the folder containing the Dockerfile:

```bash
docker build -t my-python-app:1.0 .
docker run -d --name python-app -p 5000:5000 my-python-app:1.0
curl http://localhost:5000
```

The final `.` is the **build context**: files Docker can send to its builder. Keep it small.

### `.dockerignore`

`.dockerignore` prevents unnecessary or sensitive files from entering the build context/image:

```gitignore
.git
.venv
__pycache__
*.pyc
.env
*.log
```

It is similar to `.gitignore`, but applies to Docker builds.

## 14. Volumes and Persistent Data

Containers are disposable. Removing a container removes data from its writable layer. Use a **volume** when data must survive replacement.

```bash
docker volume create postgres-data
docker volume ls
docker volume inspect postgres-data
```

Example with PostgreSQL:

```bash
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=change-me \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:16
```

The named volume remains if the `postgres` container is removed.

| Named volume | Bind mount |
| --- | --- |
| Docker manages location | Maps exact host location |
| Good for database/app data | Good for local source-code development |
| Portable with Docker tools | Depends on host filesystem |
| Safer abstraction for data | Host changes immediately appear in container |

Do not store important database data only inside the writable container layer.

## 15. Docker Networking

Networks let containers communicate without publishing every service to the host or internet. For multi-container applications, use a user-defined bridge network:

```bash
docker network create app-network
docker run -d --name database --network app-network postgres:16
docker run -d --name web --network app-network my-python-app:1.0
```

On a user-defined network, containers can usually use each other's names as hostnames. The web app can connect to database host `database`.

Network types to recognize:

- **bridge:** default local, single-host networking.
- **host:** shares host networking directly (mainly Linux; less isolation).
- **none:** no network.
- **overlay:** multi-host network often used with orchestration.

Keep databases/private services on internal networks unless they truly need a public host port.

## 16. Docker and Kubernetes

Docker builds/runs containers. **Kubernetes** is a container orchestrator that deploys, schedules, scales, heals, networks, and updates containers across a cluster.

```text
Docker image
    ↓
Container runtime
    ↓
Kubernetes manages many containers
    ↓
Scaling, service discovery, self-healing, rollouts, load balancing
```

Kubernetes can run images built with Docker, although current Kubernetes environments commonly use runtimes such as containerd rather than Docker daemon directly. Master Docker images, containers, ports, volumes, networks, and registries first.

## 17. Management and Inspection

```bash
docker images
docker image inspect nginx
docker container ls
docker inspect my-nginx
docker stats
docker system df
```

- `docker inspect` prints detailed JSON configuration/state.
- `docker stats` displays live CPU, memory, network, and disk I/O use.
- `docker system df` shows Docker disk consumption.

Remove only verified unused objects:

```bash
docker rm CONTAINER_NAME
docker rmi IMAGE_NAME
docker image prune
docker container prune
```

Prune commands can remove data/objects; read the prompt carefully and avoid broad cleanup in important environments.

## 18. Security and Production Practices

- Use trusted official or verified images.
- Pin base images to tested versions instead of `latest`.
- Rebuild regularly to include security fixes.
- Scan images for vulnerabilities in CI/CD.
- Never bake passwords, API keys, tokens, or private keys into images.
- Supply secrets at runtime through an approved secret-management mechanism.
- Run applications as a non-root user when possible.
- Use multi-stage builds to remove build tools from final images.
- Add `.dockerignore` to reduce build size and accidental secret inclusion.
- Write logs to standard output/error for collection.
- Set health checks and resource limits in production/orchestration platforms.
- Treat containers as replaceable; persist important state externally or in volumes.

## 19. Common Problems

| Problem | Likely cause | Fix |
| --- | --- | --- |
| Browser cannot open app | Container stopped or wrong port mapping | `docker ps`, `docker logs NAME`, verify `-p host:container` |
| Port already allocated | Host port is in use | Pick another host port, e.g. `-p 8081:80` |
| Container exits | Main process finished or failed | `docker ps -a`, then `docker logs NAME` |
| Image not found | Wrong image/tag or private registry | Check name/tag and login if authorized |
| App inaccessible externally | App bound to `127.0.0.1` | Bind app to `0.0.0.0` |
| Data vanished | Stored only in container layer | Use a volume or bind mount |
| Large/slow build | Large context or cache invalidation | Add `.dockerignore`; order layers well |
| Docker permission denied | User cannot access daemon socket | Use approved `sudo` or securely configure group |

## 20. Practice Checklist

- [ ] Install Docker and run `docker run hello-world`.
- [ ] Pull `nginx` and list images.
- [ ] Run `docker run -d -p 8080:80 nginx`.
- [ ] Take screenshots of `docker ps` and the Nginx welcome page.
- [ ] Stop, start, inspect, and remove the Nginx container.
- [ ] Deploy a static website through Nginx.
- [ ] Build and run the Python application.
- [ ] Create a `.dockerignore`.
- [ ] Create a named volume and explain why it persists data.
- [ ] Create a network and connect two containers.
- [ ] Explore Node.js, Python, Java, Apache, and static-site sample apps.
- [ ] Review the DevOps Heroes repository or other approved sample applications.

## 21. Command Cheat Sheet

| Task | Command |
| --- | --- |
| Verify Docker | `docker run hello-world` |
| Download image | `docker pull nginx` |
| List images | `docker images` |
| Run Nginx | `docker run -d -p 8080:80 nginx` |
| List containers | `docker ps` / `docker ps -a` |
| Logs | `docker logs NAME` / `docker logs -f NAME` |
| Shell in container | `docker exec -it NAME sh` |
| Stop/start | `docker stop NAME` / `docker start NAME` |
| Remove container/image | `docker rm NAME` / `docker rmi IMAGE` |
| Build image | `docker build -t NAME:TAG .` |
| Create volume | `docker volume create NAME` |
| Create network | `docker network create NAME` |
| Inspect object | `docker inspect NAME` |

---

## Key Takeaway

Docker packages an application and its dependencies into a portable image, then runs that image as an isolated container. It replaces fragile manual environment setup with a repeatable deployment process. Images, Dockerfiles, ports, logs, volumes, and networks are the essential foundation for CI/CD, microservices, and Kubernetes.
