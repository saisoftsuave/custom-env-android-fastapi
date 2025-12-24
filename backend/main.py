from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager
from typing import Optional
import os

# Define the Todo model
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str = Field(default="")
    completed: bool = Field(default=False)

# Create database engine
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todos.db")
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    # Any cleanup can go here

app = FastAPI(lifespan=lifespan)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Create Todo
@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo):
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

# Read all Todos
@app.get("/todos/", response_model=list[Todo])
def read_todos():
    with Session(engine) as session:
        todos = session.exec(select(Todo)).all()
        return todos

# Read a specific Todo
@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo

# Update a Todo
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: Todo):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        # Update fields
        todo.title = todo_update.title
        todo.description = todo_update.description
        todo.completed = todo_update.completed
        
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

# Delete a Todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        session.delete(todo)
        session.commit()
        return {"message": "Todo deleted successfully"}