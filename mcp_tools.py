
from typing import Any, Dict
import sqlite3
from pathlib import Path

DB_PATH = Path("data.db")

class ToolResult(Dict[str, Any]):
    pass

class MCPRegistry:
    def __init__(self):
        self.tools = {
            "get_balance": self.get_balance,
            "send_email": self.send_email,
        }
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            customer TEXT UNIQUE,
            balance REAL
        );
        """ )
        cur.execute("INSERT OR IGNORE INTO accounts(id, customer, balance) VALUES (1,'alice', -230.50);")
        conn.commit()
        conn.close()

    def call(self, name: str, **kwargs):
        fn = self.tools.get(name)
        if not fn:
            return {"ok": False, "error": f"unknown_tool:{name}"}
        try:
            return fn(**kwargs)
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_balance(self, customer: str):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT balance FROM accounts WHERE customer=?", (customer,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return {"ok": False, "error": "not_found"}
        return {"ok": True, "balance": row[0]}

    def send_email(self, to: str, subject: str, body: str):
        return {"ok": True, "to": to, "subject": subject, "body_preview": body[:80]}
