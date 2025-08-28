import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Session, create_engine, select
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional, List
import os

SECRET_KEY = "supersecretkey"  # Change in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24

DB_URL = "sqlite:///./todo.db"
engine = create_engine(DB_URL, echo=True)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to production domain as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ToDo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    content: str
    priority: str  # 'high', 'medium', 'low'
    status: str    # 'not_started', 'in_progress', 'completed'
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ToDoCreate(BaseModel):
    content: str
    priority: str
    status: str

class ToDoRead(BaseModel):
    id: int
    content: str
    priority: str
    status: str
    created_at: datetime

class ToDoUpdate(BaseModel):
    content: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None

# DB init
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.exec(select(User).where(User.username == username)).first()
    if not user:
        raise credentials_exception
    return user

@app.post("/register", response_model=Token)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.username == user_create.username)).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = hash_password(user_create.password)
    user = User(username=user_create.username, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/todos", response_model=List[ToDoRead])
def list_todos(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    status: Optional[str] = None,
    priority: Optional[str] = None,
    completed: Optional[bool] = False,
):
    query = select(ToDo).where(ToDo.user_id == user.id)
    if status:
        query = query.where(ToDo.status == status)
    if priority:
        query = query.where(ToDo.priority == priority)
    if completed:
        query = query.where(ToDo.status == "completed")
    else:
        query = query.where(ToDo.status != "completed")
    todos = db.exec(query.order_by(ToDo.created_at.desc())).all()
    return todos

@app.post("/todos", response_model=ToDoRead)
def create_todo(todo: ToDoCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    todo_obj = ToDo(user_id=user.id, **todo.dict())
    db.add(todo_obj)
    db.commit()
    db.refresh(todo_obj)
    return todo_obj

@app.patch("/todos/{todo_id}", response_model=ToDoRead)
def update_todo(todo_id: int, update: ToDoUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    todo = db.get(ToDo, todo_id)
    if not todo or todo.user_id != user.id:
        raise HTTPException(status_code=404, detail="ToDo not found")
    data = update.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(todo, key, value)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    todo = db.get(ToDo, todo_id)
    if not todo or todo.user_id != user.id:
        raise HTTPException(status_code=404, detail="ToDo not found")
    db.delete(todo)
    db.commit()
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
