# To-Do Flask SQLite Backend

A simple REST API backend for a To-Do application using Flask and SQLite.

## Features

- Add new tasks
- View all tasks
- Mark tasks as completed
- Delete tasks
- Store tasks using SQLite database

## Tech Stack

- Python
- Flask
- SQLite
- Flask-CORS

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| GET | `/api/health` | Health check |
| GET | `/api/tasks` | Get all tasks |
| POST | `/api/tasks` | Add a task |
| PUT | `/api/tasks/<id>` | Update a task |
| PUT | `/api/tasks/<id>/complete` | Mark task as completed |
| DELETE | `/api/tasks/<id>` | Delete a task |

## How to Run

```bash
pip install -r requirements.txt
python app.py