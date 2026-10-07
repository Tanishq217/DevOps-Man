from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator

from .config import settings
from .db import Base, engine, get_db
from .models import Task
from .schemas import HealthOut, StatsOut, TaskCreate, TaskOut, TaskUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database tables exist
    Base.metadata.create_all(bind=engine)
    # Seed sample tasks if table is empty
    with Session(bind=engine) as session:
        count = session.scalar(select(func.count(Task.id)))
        if count == 0:
            sample_tasks = [
                Task(
                    title="Implement DevSecOps Pipeline in GitHub Actions",
                    description="Configure Bandit SAST, pip-audit SCA, and Trivy container vulnerability scans.",
                    priority="HIGH",
                    status="DONE",
                    assignee="Tanishq Singh",
                ),
                Task(
                    title="Provision AWS Infrastructure with Terraform",
                    description="Write modular HCL scripts for VPC, Subnets, EC2, and S3 using LocalStack.",
                    priority="HIGH",
                    status="IN_PROGRESS",
                    assignee="Tanishq Singh",
                ),
                Task(
                    title="Package TaskBoard Application with Helm",
                    description="Create Helm templates with configurable replicas, resources, and probes.",
                    priority="MEDIUM",
                    status="TODO",
                    assignee="Tanishq Singh",
                ),
                Task(
                    title="Setup Prometheus & Grafana Observability",
                    description="Export application /metrics and visualize request latencies and error rates.",
                    priority="MEDIUM",
                    status="TODO",
                    assignee="Tanishq Singh",
                ),
            ]
            session.add_all(sample_tasks)
            session.commit()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="TaskBoard SaaS API for DevOps Capstone Project",
    lifespan=lifespan,
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expose Prometheus /metrics endpoint
Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.get("/", summary="API Root")
def root():
    return {
        "service": settings.app_name,
        "version": settings.version,
        "status": "OPERATIONAL",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "ready": "/ready",
            "metrics": "/metrics",
            "tasks": "/api/tasks",
            "stats": "/api/tasks/stats",
        },
    }


@app.get("/health", response_model=HealthOut, summary="Liveness Probe")
def health():
    return HealthOut(
        status="UP",
        service=settings.app_name,
        version=settings.version,
    )


@app.get("/ready", summary="Readiness Probe")
def ready(db: Session = Depends(get_db)):
    try:
        db.execute(select(func.count(Task.id)))
        return {"status": "READY", "database": "CONNECTED"}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connectivity failed: {str(exc)}",
        )


@app.get("/api/tasks", response_model=list[TaskOut], summary="List Tasks")
def list_tasks(
    status_filter: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
):
    stmt = select(Task).order_by(Task.id.desc())
    if status_filter and status_filter.upper() != "ALL":
        stmt = stmt.where(Task.status == status_filter.upper())
    return list(db.scalars(stmt))


@app.get("/api/tasks/stats", response_model=StatsOut, summary="Task KPI Metrics")
def stats(db: Session = Depends(get_db)):
    rows = db.execute(select(Task.status, func.count(Task.id)).group_by(Task.status)).all()
    counts = {row_status: count for row_status, count in rows}
    total = sum(counts.values())
    return StatsOut(
        total=total,
        todo=counts.get("TODO", 0),
        inProgress=counts.get("IN_PROGRESS", 0),
        done=counts.get("DONE", 0),
    )


@app.get("/api/tasks/{task_id}", response_model=TaskOut, summary="Get Single Task")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    return task


@app.post("/api/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED, summary="Create Task")
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.put("/api/tasks/{task_id}", response_model=TaskOut, summary="Update Task")
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Task")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    db.delete(task)
    db.commit()
