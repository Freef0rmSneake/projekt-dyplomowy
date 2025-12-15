from datetime import datetime
from typing import Any, Dict, List, Optional

from .database import get_db


def _now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def get_all_todos() -> List[Dict[str, Any]]:
    db = get_db()
    rows = db.execute(
        "SELECT id, task, done, created_at, updated_at FROM todos ORDER BY id ASC"
    ).fetchall()
    return [dict(row) for row in rows]


def get_todo(todo_id: int) -> Optional[Dict[str, Any]]:
    db = get_db()
    row = db.execute(
        "SELECT id, task, done, created_at, updated_at FROM todos WHERE id = ?",
        (todo_id,),
    ).fetchone()
    return dict(row) if row else None


def create_todo(task: str) -> int:
    db = get_db()
    now = _now_iso()
    cursor = db.execute(
        """
        INSERT INTO todos (task, done, created_at, updated_at)
        VALUES (?, 0, ?, ?)
        """,
        (task, now, now),
    )
    db.commit()
    return cursor.lastrowid


def update_todo(todo_id: int, task: str) -> bool:
    db = get_db()
    now = _now_iso()
    cursor = db.execute(
        """
        UPDATE todos
        SET task = ?, updated_at = ?
        WHERE id = ?
        """,
        (task, now, todo_id),
    )
    db.commit()
    return cursor.rowcount > 0


def toggle_todo_done(todo_id: int) -> bool:
    db = get_db()
    cursor = db.execute(
        """
        UPDATE todos
        SET done = CASE done WHEN 1 THEN 0 ELSE 1 END,
            updated_at = ?
        WHERE id = ?
        """,
        (_now_iso(), todo_id),
    )
    db.commit()
    return cursor.rowcount > 0


def delete_todo(todo_id: int) -> bool:
    db = get_db()
    cursor = db.execute(
        "DELETE FROM todos WHERE id = ?",
        (todo_id,),
    )
    db.commit()
    return cursor.rowcount > 0


