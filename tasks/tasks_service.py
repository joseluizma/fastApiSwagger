import sqlite3
from .dtos import TaskCreate

class TasksService:
    async def create_task(self, task: TaskCreate, username: str):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if not user:
            conn.close()
            raise ValueError("Usuário não encontrado")
        user_id = user[0]
        c.execute("INSERT INTO tasks (title, description, user_id) VALUES (?, ?, ?)", 
                 (task.title, task.description, user_id))
        task_id = c.lastrowid
        conn.commit()
        conn.close()
        return task_id

    async def get_user_tasks(self, username: str):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if not user:
            conn.close()
            raise ValueError("Usuário não encontrado")
        user_id = user[0]
        c.execute("SELECT id, title, description, user_id FROM tasks WHERE user_id = ?", (user_id,))
        tasks = [{"id": row[0], "title": row[1], "description": row[2], "user_id": row[3]} 
                 for row in c.fetchall()]
        conn.close()
        return tasks

    async def get_task(self, task_id: int, username: str):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if not user:
            conn.close()
            raise ValueError("Usuário não encontrado")
        user_id = user[0]
        c.execute("SELECT id, title, description, user_id FROM tasks WHERE id = ? AND user_id = ?", 
                 (task_id, user_id))
        task = c.fetchone()
        conn.close()
        if task:
            return {"id": task[0], "title": task[1], "description": task[2], "user_id": task[3]}
        return None

    async def update_task(self, task_id: int, task: TaskCreate, username: str):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if not user:
            conn.close()
            raise ValueError("Usuário não encontrado")
        user_id = user[0]
        c.execute("UPDATE tasks SET title = ?, description = ? WHERE id = ? AND user_id = ?", 
                 (task.title, task.description, task_id, user_id))
        if c.rowcount == 0:
            conn.close()
            raise ValueError("Tarefa não encontrada ou não pertence ao usuário")
        conn.commit()
        conn.close()

    async def delete_task(self, task_id: int, username: str):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if not user:
            conn.close()
            raise ValueError("Usuário não encontrado")
        user_id = user[0]
        c.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        if c.rowcount == 0:
            conn.close()
            raise ValueError("Tarefa não encontrada ou não pertence ao usuário")
        conn.commit()
        conn.close()