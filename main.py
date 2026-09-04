from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Task, User
from schemas import TaskCreate, TaskResponse, TaskUpdate, UserCreate, UserResponse , LoginRequest, Token
from security import hash_password
from security import create_access_token, verify_password
from security import get_current_user
# نشئ الجداول تلقائياً
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API")

@app.get("/")
def read_root():
    return {"message": "🚀 مرحباً! النظام يشتغل!"}



# اللي بتفتح connection مع Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    # جيب بس مهام الـ user الحالي
    user = db.query(User).filter(User.username == current_user).first()
    tasks = db.query(Task).filter(Task.user_id == user.id).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="المهمة ما موجودة")
    
    return db_task

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()
    db_task = Task(title=task.title, description=task.description, user_id=user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="المهمة ما موجودة")
    
    if task.title:
        db_task.title = task.title
    if task.description:
        db_task.description = task.description
    if task.completed is not None:
        db_task.completed = task.completed
    
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="المهمة ما موجودة")
    
    db.delete(db_task)
    db.commit()
    
    return {"message": "المهمة انحذفت بنجاح"}

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username موجود بالفعل")

    hashed_pwd = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=Token)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    # ابحث عن المستخدم
    user = db.query(User).filter(User.username == credentials.username).first()
    
    # تحقق من كلمة السر
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Username أو password غلط")
    
    # أنشئ token
    access_token = create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}