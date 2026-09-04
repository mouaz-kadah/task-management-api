# Task Management API

## Description
A complete REST API for task management with user authentication and JWT security.

## Features
- ✓ Full CRUD operations for tasks
- ✓ User authentication with JWT tokens
- ✓ Password hashing with Argon2
- ✓ Each user can only view their own tasks
- ✓ Automatic API documentation with Swagger

## Tech Stack
- **Backend:** FastAPI
- **Database:** MySQL
- **Authentication:** JWT (JSON Web Tokens)
- **Password Security:** Argon2

## Installation

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

## Running the Server

```bash
python main.py
```

Then open: `http://127.0.0.1:8000/docs`

## API Endpoints

### Users
- `POST /users` - Create a new user
- `POST /login` - Login and get JWT token

### Tasks
- `GET /tasks` - Get all user's tasks
- `GET /tasks/{task_id}` - Get a specific task
- `POST /tasks` - Create a new task
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

## Authentication

All task endpoints require a JWT token in the Authorization header:


## Database Schema

### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- hashed_password

### Tasks Table
- id (Primary Key)
- title
- description
- completed
- user_id (Foreign Key)
- created_at

## Security Features
- Password hashing with Argon2
- JWT token-based authentication
- User isolation (each user sees only their tasks)
- HTTP exception handling for unauthorized access

## Future Improvements
- Add task categories/tags
- Add task priority levels
- Add due dates
- Add email notifications