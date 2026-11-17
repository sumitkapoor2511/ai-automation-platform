import uuid
import json
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException, status, Path, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.database import init_db, get_session
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user
from app.models.automation import AutomationTask
from app.models.user import User
from app.schemas.automation import AutomationTaskCreate, AutomationTaskResponse, AutomationTaskUpdate
from app.schemas.auth import UserCreate, UserResponse, Token

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="AI Automation Backend",
    description="Production-grade secured gateway for multi-tier agentic workflows",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "environment": "development",
        "database": "PostgreSQL Connected",
        "security": "OAuth2 JWT Active"
    }

# --- AUTHENTICATION ENDPOINTS ---

@app.post("/api/v1/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Authentication"])
async def register_user(user_in: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == user_in.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    new_user = User(
        id=str(uuid.uuid4()),
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@app.post("/api/v1/auth/login", response_model=Token, tags=["Authentication"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- PROTECTED AUTOMATION ENGINE ENDPOINTS ---

@app.post("/api/v1/tasks", response_model=AutomationTaskResponse, status_code=status.HTTP_201_CREATED, tags=["Automation Engine"])
async def create_automation_task(
    task_in: AutomationTaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if task_in.agent_type == "Data_Extraction" and task_in.priority < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data_Extraction agents require a baseline priority rating of 3 or above."
        )

    db_task = AutomationTask(
        id=str(uuid.uuid4()),
        title=task_in.title,
        agent_type=task_in.agent_type,
        priority=task_in.priority,
        payload_raw=json.dumps(task_in.payload_data)
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return {
        "id": db_task.id,
        "title": db_task.title,
        "agent_type": db_task.agent_type,
        "priority": db_task.priority,
        "payload_data": json.loads(db_task.payload_raw),
        "status": db_task.status,
        "created_at": db_task.created_at
    }

@app.get("/api/v1/tasks", response_model=List[AutomationTaskResponse], tags=["Automation Engine"])
async def list_automation_tasks(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    tasks = session.exec(select(AutomationTask)).all()
    return [
        {
            "id": t.id,
            "title": t.title,
            "agent_type": t.agent_type,
            "priority": t.priority,
            "payload_data": json.loads(t.payload_raw),
            "status": t.status,
            "created_at": t.created_at
        }
        for t in tasks
    ]

@app.get("/api/v1/tasks/{task_id}", response_model=AutomationTaskResponse, tags=["Automation Engine"])
async def get_automation_task(
    task_id: str = Path(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_task = session.get(AutomationTask, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail=f"Automation task with ID '{task_id}' was not found.")
    return {
        "id": db_task.id,
        "title": db_task.title,
        "agent_type": db_task.agent_type,
        "priority": db_task.priority,
        "payload_data": json.loads(db_task.payload_raw),
        "status": db_task.status,
        "created_at": db_task.created_at
    }

@app.patch("/api/v1/tasks/{task_id}", response_model=AutomationTaskResponse, tags=["Automation Engine"])
async def update_automation_task(
    task_id: str = Path(...),
    task_update: AutomationTaskUpdate = ...,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_task = session.get(AutomationTask, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail=f"Automation task with ID '{task_id}' was not found.")

    if task_update.status is not None:
        db_task.status = task_update.status
    if task_update.priority is not None:
        db_task.priority = task_update.priority

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return {
        "id": db_task.id,
        "title": db_task.title,
        "agent_type": db_task.agent_type,
        "priority": db_task.priority,
        "payload_data": json.loads(db_task.payload_raw),
        "status": db_task.status,
        "created_at": db_task.created_at
    }

@app.delete("/api/v1/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Automation Engine"])
async def delete_automation_task(
    task_id: str = Path(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_task = session.get(AutomationTask, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail=f"Automation task with ID '{task_id}' was not found.")

    session.delete(db_task)
    session.commit()
    return None
