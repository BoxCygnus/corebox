import os
import sqlite3
import datetime
try:
    import requests
except Exception:
    requests = None
from typing import List, Dict, Any, Optional, Tuple
import config

class Database:
    def __init__(self):
        self.use_d1 = bool(
            config.CLOUDFLARE_ACCOUNT_ID
            and config.CLOUDFLARE_D1_DATABASE_ID
            and config.CLOUDFLARE_API_TOKEN
            and requests is not None
        )
        if not self.use_d1:
            db_dir = os.path.dirname(config.DB_PATH)
            if db_dir:
                try:
                    os.makedirs(db_dir, exist_ok=True)
                except Exception:
                    pass
        self.init_db()

    def get_backend_name(self) -> str:
        return "Cloudflare D1" if self.use_d1 else "Local SQLite"

    def _execute_sqlite(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(config.DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        try:
            cur.execute(query, params)
            if query.strip().upper().startswith(("SELECT", "PRAGMA")):
                rows = [dict(r) for r in cur.fetchall()]
                conn.commit()
                return rows
            conn.commit()
            return []
        finally:
            conn.close()

    def _execute_d1(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{config.CLOUDFLARE_ACCOUNT_ID}/d1/database/"
            f"{config.CLOUDFLARE_D1_DATABASE_ID}/query"
        )
        headers = {
            "Authorization": f"Bearer {config.CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        # Cloudflare D1 expects query and params
        payload = {
            "sql": query,
            "params": list(params)
        }
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=15)
            data = res.json()
            if not data.get("success"):
                errors = data.get("errors", [])
                raise RuntimeError(f"Cloudflare D1 error: {errors}")
            result_objs = data.get("result", [])
            if result_objs and "results" in result_objs[0]:
                return result_objs[0]["results"]
            return []
        except Exception as e:
            # If D1 call fails, log and fallback to local sqlite
            print(f"[Database] D1 query failed, falling back to SQLite: {e}")
            return self._execute_sqlite(query, params)

    def execute(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        if self.use_d1:
            return self._execute_d1(query, params)
        return self._execute_sqlite(query, params)

    def init_db(self):
        """Create tables if they don't exist and ensure default admin is configured."""
        schema = [
            """
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                full_name TEXT,
                role TEXT DEFAULT 'user',
                status TEXT DEFAULT 'pending',
                created_at TEXT,
                updated_at TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS work_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL,
                raw_code TEXT,
                name TEXT NOT NULL,
                unit TEXT DEFAULT '',
                source_file TEXT NOT NULL,
                created_at TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS uploaded_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE NOT NULL,
                total_records INTEGER DEFAULT 0,
                uploaded_by TEXT NOT NULL,
                uploaded_at TEXT
            );
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_work_codes_code ON work_codes(code);
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_work_codes_file ON work_codes(source_file);
            """
        ]
        
        for statement in schema:
            self.execute(statement)

        # Seed or ensure default official Admin
        admin_email = config.ADMIN_EMAIL
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        existing_admin = self.get_user(admin_email)
        if not existing_admin:
            self.execute(
                "INSERT INTO users (email, full_name, role, status, created_at, updated_at) "
                "VALUES (?, ?, 'admin', 'active', ?, ?)",
                (admin_email, "System Administrator", now_str, now_str)
            )
        else:
            # Ensure always active admin
            if existing_admin.get("role") != "admin" or existing_admin.get("status") != "active":
                self.execute(
                    "UPDATE users SET role = 'admin', status = 'active', updated_at = ? WHERE email = ?",
                    (now_str, admin_email)
                )

    # ================= User Management =================
    def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        if not email:
            return None
        res = self.execute("SELECT * FROM users WHERE email = ? LIMIT 1", (email.strip().lower(),))
        return res[0] if res else None

    def register_or_get_user(self, email: str, full_name: str = "") -> Dict[str, Any]:
        email = email.strip().lower()
        user = self.get_user(email)
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if user:
            return user
        
        # Determine status and role
        if email == config.ADMIN_EMAIL:
            role = "admin"
            status = "active"
        else:
            role = "user"
            status = "pending"  # Needs approval queue
            
        display_name = full_name or email.split("@")[0]
        self.execute(
            "INSERT INTO users (email, full_name, role, status, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (email, display_name, role, status, now_str, now_str)
        )
        return self.get_user(email)

    def get_all_users(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        if status:
            return self.execute("SELECT * FROM users WHERE status = ? ORDER BY created_at DESC", (status,))
        return self.execute("SELECT * FROM users ORDER BY created_at DESC")

    def update_user_status(self, email: str, status: str):
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.execute(
            "UPDATE users SET status = ?, updated_at = ? WHERE email = ?",
            (status, now_str, email.strip().lower())
        )

    def update_user_role(self, email: str, role: str):
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.execute(
            "UPDATE users SET role = ?, updated_at = ? WHERE email = ?",
            (role, now_str, email.strip().lower())
        )

    def delete_user(self, email: str):
        # Do not allow deleting root official admin
        if email.strip().lower() == config.ADMIN_EMAIL:
            return
        self.execute("DELETE FROM users WHERE email = ?", (email.strip().lower(),))

    # ================= Work Codes Repository =================
    def add_work_codes(self, records: List[Dict[str, str]], filename: str, uploaded_by: str) -> int:
        """
        Saves work codes extracted from a file.
        If file already exists, old records from this file are purged first.
        """
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Purge existing if any
        self.execute("DELETE FROM work_codes WHERE source_file = ?", (filename,))
        self.execute("DELETE FROM uploaded_files WHERE filename = ?", (filename,))
        
        # Insert work codes
        inserted_count = 0
        if not self.use_d1:
            conn = sqlite3.connect(config.DB_PATH)
            cur = conn.cursor()
            try:
                for r in records:
                    cur.execute(
                        "INSERT INTO work_codes (code, raw_code, name, unit, source_file, created_at) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (r["code"], r.get("raw_code", r["code"]), r["name"], r.get("unit", ""), filename, now_str)
                    )
                    inserted_count += 1
                conn.commit()
            finally:
                conn.close()
        else:
            # Batch or sequential insert for D1
            for r in records:
                self.execute(
                    "INSERT INTO work_codes (code, raw_code, name, unit, source_file, created_at) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (r["code"], r.get("raw_code", r["code"]), r["name"], r.get("unit", ""), filename, now_str)
                )
                inserted_count += 1
                
        # Record file metadata
        self.execute(
            "INSERT INTO uploaded_files (filename, total_records, uploaded_by, uploaded_at) "
            "VALUES (?, ?, ?, ?)",
            (filename, inserted_count, uploaded_by, now_str)
        )
        return inserted_count

    def get_uploaded_files(self) -> List[Dict[str, Any]]:
        return self.execute("SELECT * FROM uploaded_files ORDER BY uploaded_at DESC")

    def delete_uploaded_file(self, filename: str):
        self.execute("DELETE FROM work_codes WHERE source_file = ?", (filename,))
        self.execute("DELETE FROM uploaded_files WHERE filename = ?", (filename,))

    def get_work_codes(
        self,
        search: Optional[str] = None,
        source_file: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        query = "SELECT * FROM work_codes WHERE 1=1"
        params = []
        if source_file:
            query += " AND source_file = ?"
            params.append(source_file)
        if search:
            query += " AND (code LIKE ? OR name LIKE ? OR raw_code LIKE ?)"
            s_param = f"%{search}%"
            params.extend([s_param, s_param, s_param])
        query += " ORDER BY code ASC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        return self.execute(query, tuple(params))

    def count_work_codes(self, search: Optional[str] = None, source_file: Optional[str] = None) -> int:
        query = "SELECT COUNT(*) as cnt FROM work_codes WHERE 1=1"
        params = []
        if source_file:
            query += " AND source_file = ?"
            params.append(source_file)
        if search:
            query += " AND (code LIKE ? OR name LIKE ? OR raw_code LIKE ?)"
            s_param = f"%{search}%"
            params.extend([s_param, s_param, s_param])
        res = self.execute(query, tuple(params))
        return res[0]["cnt"] if res else 0

    def get_all_codes_lookup(self) -> Dict[str, Dict[str, str]]:
        """
        Loads all work codes into a fast in-memory lookup dictionary:
        {
           'AB.12300': {'name': '...', 'unit': '...', 'source': '...'},
           ...
        }
        Also maps raw_code as fallback.
        """
        rows = self.execute("SELECT code, raw_code, name, unit, source_file FROM work_codes")
        lookup = {}
        for r in rows:
            info = {
                "name": r["name"],
                "unit": r.get("unit", ""),
                "source_file": r.get("source_file", ""),
                "code": r["code"]
            }
            lookup[r["code"].upper()] = info
            if r.get("raw_code"):
                lookup[r["raw_code"].upper()] = info
        return lookup

# Global database instance
db = Database()
