import sqlite3
from typing import Optional, List, Dict

class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS task (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done BOOLEAN
            )
            """
        )
        self.connection.commit()

    def create_task(self, title: str, done: Optional[bool] = None) -> Dict:
        self.cursor.execute("INSERT INTO task (title,done) VALUES (?,?)", (title, done))
        self.connection.commit()
        task_id = self.cursor.lastrowid
        return {"id": task_id, "title": title, "done": done}

    def get_task(self, task_id: int) -> Optional[Dict]:
        self.cursor.execute("SELECT id, title, done FROM task WHERE id = ?", (task_id,))
        row = self.cursor.fetchone()
        if row:
            return {"id": row[0], "title": row[1], "done": row[2]}
        return None

    def get_all_tasks(self) -> List[Dict]:
        self.cursor.execute("SELECT id, title, done FROM task")
        rows = self.cursor.fetchall()
        return [{"id": row[0], "title": row[1], "done": row[2]} for row in rows]

    def update_task(self, task_id: int, title: str, done: Optional[bool] = None) -> Optional[Dict]:
        self.cursor.execute("UPDATE task SET title = ?, done = ? WHERE id = ?", (title, done, task_id))
        self.connection.commit()
        return self.get_task(task_id)

    def delete_task(self, task_id: int) -> bool:
        self.cursor.execute("DELETE FROM task WHERE id = ?", (task_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def close(self):
        self.connection.close()
