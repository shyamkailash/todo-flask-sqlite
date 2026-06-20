import sqlite3


DB_NAME = "todo.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending'
        )
    """)

    conn.commit()
    conn.close()


def add_task(task):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (task, status) VALUES (?, ?)",
        (task, "Pending")
    )

    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return task_id


def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()

    conn.close()

    return [dict(task) for task in tasks]


def get_task_by_id(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    conn.close()

    if task:
        return dict(task)

    return None


def update_task(task_id, task_text=None, status=None):
    conn = get_connection()
    cursor = conn.cursor()

    if task_text is not None and status is not None:
        cursor.execute(
            "UPDATE tasks SET task = ?, status = ? WHERE id = ?",
            (task_text, status, task_id)
        )
    elif task_text is not None:
        cursor.execute(
            "UPDATE tasks SET task = ? WHERE id = ?",
            (task_text, task_id)
        )
    elif status is not None:
        cursor.execute(
            "UPDATE tasks SET status = ? WHERE id = ?",
            (status, task_id)
        )

    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()

    return updated_rows > 0


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()

    return deleted_rows > 0