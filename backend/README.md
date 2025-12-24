# Todo API with FastAPI, SQLModel and SQLite

This is a simple Todo API application built with FastAPI, SQLModel, and SQLite database. It provides basic CRUD operations for managing todo items along with a health check endpoint.

## Features

- Health check endpoint
- Create, Read, Update, and Delete operations for Todo items
- SQLite database with SQLModel for ORM
- Automatic database table creation on startup

## Endpoints

- `GET /health` - Health check endpoint
- `POST /todos/` - Create a new todo
- `GET /todos/` - Get all todos
- `GET /todos/{todo_id}` - Get a specific todo
- `PUT /todos/{todo_id}` - Update a specific todo
- `DELETE /todos/{todo_id}` - Delete a specific todo

## Setup

1. Make sure you have Python 3.12+ installed
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the development server:

```bash
uvicorn main:app --reload
```

By default, the server will run on `http://localhost:8000`

## Example Usage

### Create a Todo

```bash
curl -X POST http://localhost:8081/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My Todo", "description": "This is my todo item", "completed": false}'
```

### Get all Todos

```bash
curl http://localhost:8081/todos/
```

### Get a specific Todo

```bash
curl http://localhost:8081/todos/1
```

### Update a Todo

```bash
curl -X PUT http://localhost:8081/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Todo", "description": "This is my updated todo item", "completed": true}'
```

### Delete a Todo

```bash
curl -X DELETE http://localhost:8081/todos/1
```

### Health Check

```bash
curl http://localhost:8081/health
```

## Database

The application uses SQLite as the database, which creates a `todos.db` file in the project directory. SQLModel is used for ORM operations, providing type safety and automatic schema generation.

## Project Structure

- `main.py` - The main application file with all endpoints
- `requirements.txt` - Project dependencies
- `todos.db` - SQLite database file (generated automatically)