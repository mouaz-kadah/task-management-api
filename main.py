from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Task, User
from schemas import TaskCreate, TaskResponse, TaskUpdate, UserCreate, UserResponse
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
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="المهمة ما موجودة")
    
    return db_task

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # نشئ task جديدة
    db_task = Task(title=task.title, description=task.description)
    
    # احفظها في Database
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # ارد البيانات للمستخدم
    return db_task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    # ابحث عن المهمة بـ ID
    db_task = db.query(Task).filter(Task.id == task_id).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="المهمة ما موجودة")
    
    # عدّل البيانات
    if task.title:
        db_task.title = task.title
    if task.description:
        db_task.description = task.description
    if task.completed is not None:
        db_task.completed = task.completed
    
    # احفظ التعديلات
    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    # ابحث عن المهمة
    db_task = db.query(Task).filter(Task.id == task_id).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="المهمة ما موجودة")
    
    # احذفها
    db.delete(db_task)
    db.commit()
    
    return {"message": "المهمة انحذفت بنجاح"}

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username موجود بالفعل")
    
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user