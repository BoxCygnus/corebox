import os
import datetime
from typing import List, Dict, Any, Optional, Tuple
import config

try:
    import sqlite3
except (ImportError, ModuleNotFoundError):
    sqlite3 = None

try:
    import requests
except Exception:
    requests = None

import json

def get_browser_storage():
    try:
        import js
        return js.localStorage
    except Exception:
        return None

def load_browser_users() -> Dict[str, Dict[str, Any]]:
    storage = get_browser_storage()
    if storage:
        try:
            val = storage.getItem("corebox_users_store")
            if val:
                return json.loads(str(val))
        except Exception:
            pass
    return {}

def save_browser_users(users_map: Dict[str, Dict[str, Any]]):
    storage = get_browser_storage()
    if storage:
        try:
            storage.setItem("corebox_users_store", json.dumps(users_map, ensure_ascii=False))
        except Exception as e:
            print("Failed to save to localStorage:", e)

# Default seed catalog codes for instant out-of-the-box browsing
DEFAULT_SEED_CODES = [
    {"code": "AB.12300", "raw_code": "AB.123", "name": "Đào móng công trình bằng máy đào 0.8m3, đất cấp II", "unit": "100m3", "source_file": "danh_muc_chuan_2024.xlsx"},
    {"code": "AF.12340", "raw_code": "AF.1234", "name": "Bê tông lót móng đá 4x6 mác 100", "unit": "m3", "source_file": "danh_muc_chuan_2024.xlsx"},
    {"code": "AF.21111", "raw_code": "AF.21111", "name": "Bê tông móng đổ bằng thủ công đá 1x2 mác 200", "unit": "m3", "source_file": "danh_muc_chuan_2024.xlsx"},
    {"code": "AF.22222", "raw_code": "AF.22222", "name": "Bê tông cột vách đá 1x2 mác 250", "unit": "m3", "source_file": "danh_muc_chuan_2024.xlsx"},
    {"code": "AF.33333", "raw_code": "AF.33333", "name": "Bê tông dầm sàn đá 1x2 mác 250", "unit": "m3", "source_file": "danh_muc_chuan_2024.xlsx"},
    {"code": "AF.61111", "raw_code": "AF.61111", "name": "Ván khuôn móng thép", "unit": "100m2", "source_file": "danh_muc_chuan_2024.xlsx"},
    {"code": "AF.62222", "raw_code": "AF.62222", "name": "Ván khuôn cột dầm sàn thép", "unit": "100m2", "source_file": "danh_muc_chuan_2024.xlsx"},
    {"code": "AF.63333", "raw_code": "AF.63333", "name": "Cốt thép dầm sàn đường kính <= 10mm", "unit": "tấn", "source_file": "danh_muc_chuan_2024.xlsx"},
    {"code": "AF.64444", "raw_code": "AF.64444", "name": "Cốt thép dầm sàn đường kính <= 18mm", "unit": "tấn", "source_file": "danh_muc_chuan_2024.xlsx"},
    {"code": "AK.11111", "raw_code": "AK.11111", "name": "Xây tường gạch ống 8x8x18 vữa xi măng mác 75", "unit": "m3", "source_file": "danh_muc_chuan_2024.xlsx"},
    {"code": "AK.22222", "raw_code": "AK.22222", "name": "Trát tường trong vữa xi măng mác 75 dày 1.5cm", "unit": "m2", "source_file": "danh_muc_chuan_2024.xlsx"},
    {"code": "AK.33333", "raw_code": "AK.33333", "name": "Lát gạch granite nhân tạo 600x600", "unit": "m2", "source_file": "danh_muc_chuan_2024.xlsx"},
    {"code": "BA.11100", "raw_code": "BA.111", "name": "Lắp đặt dây dẫn điện đơn ruột đồng", "unit": "100m", "source_file": "danh_muc_chuan_2024.xlsx"},
    {"code": "BA.22220", "raw_code": "BA.2222", "name": "Lắp đặt tủ điện phân phối chiếu sáng", "unit": "cái", "source_file": "danh_muc_chuan_2024.xlsx"},
    {"code": "BA.33333", "raw_code": "BA.33333", "name": "Lắp đặt đèn LED panel 600x600 48W", "unit": "bộ", "source_file": "danh_muc_chuan_2024.xlsx"},
]

class Database:
    def __init__(self):
        self.use_d1 = bool(
            config.CLOUDFLARE_ACCOUNT_ID
            and config.CLOUDFLARE_D1_DATABASE_ID
            and config.CLOUDFLARE_API_TOKEN
            and requests is not None
        )
        self.has_sqlite = (sqlite3 is not None)

        # In-memory store (active in Pyodide / WebAssembly environment where sqlite3 is absent)
        self._users: Dict[str, Dict[str, Any]] = {}
        self._work_codes: List[Dict[str, Any]] = []
        self._uploaded_files: Dict[str, Dict[str, Any]] = {}

        if not self.use_d1 and self.has_sqlite:
            db_dir = os.path.dirname(config.DB_PATH)
            if db_dir:
                try:
                    os.makedirs(db_dir, exist_ok=True)
                except Exception:
                    pass
        self.init_db()

    def get_backend_name(self) -> str:
        if self.use_d1:
            return "Cloudflare D1"
        if self.has_sqlite:
            return "Local SQLite"
        return "WebAssembly Memory Engine (Pyodide)"

    def _execute_sqlite(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        if not self.has_sqlite:
            return []
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
            print(f"[Database] D1 query failed, falling back: {e}")
            if self.has_sqlite:
                return self._execute_sqlite(query, params)
            return []

    def execute(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        if self.use_d1:
            return self._execute_d1(query, params)
        if self.has_sqlite:
            return self._execute_sqlite(query, params)
        return []

    def init_db(self):
        """Create tables if they don't exist and ensure default admin is configured."""
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        admin_email = config.ADMIN_EMAIL.strip().lower()

        if self.use_d1 or self.has_sqlite:
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

            existing_admin = self.get_user(admin_email)
            if not existing_admin:
                self.execute(
                    "INSERT INTO users (email, full_name, role, status, created_at, updated_at) "
                    "VALUES (?, ?, 'admin', 'active', ?, ?)",
                    (admin_email, "System Administrator", now_str, now_str)
                )
            else:
                if existing_admin.get("role") != "admin" or existing_admin.get("status") != "active":
                    self.execute(
                        "UPDATE users SET role = 'admin', status = 'active', updated_at = ? WHERE email = ?",
                        (now_str, admin_email)
                    )
        else:
            # In-memory initialization (Pyodide in browser)
            self._users[admin_email] = {
                "email": admin_email,
                "full_name": "System Administrator",
                "role": "admin",
                "status": "active",
                "created_at": now_str,
                "updated_at": now_str
            }
            # Seed default records if empty
            if not self._work_codes:
                for r in DEFAULT_SEED_CODES:
                    self._work_codes.append({
                        "code": r["code"],
                        "raw_code": r["raw_code"],
                        "name": r["name"],
                        "unit": r["unit"],
                        "source_file": r["source_file"],
                        "created_at": now_str
                    })
                self._uploaded_files["danh_muc_chuan_2024.xlsx"] = {
                    "filename": "danh_muc_chuan_2024.xlsx",
                    "total_records": len(DEFAULT_SEED_CODES),
                    "uploaded_by": admin_email,
                    "uploaded_at": now_str
                }

        # Synchronize with browser localStorage if any stored accounts exist
        browser_users = load_browser_users()
        if browser_users:
            for b_email, b_data in browser_users.items():
                self._users[b_email] = b_data
                if self.use_d1 or self.has_sqlite:
                    existing = self.execute("SELECT email FROM users WHERE email = ?", (b_email,))
                    if not existing:
                        self.execute(
                            "INSERT INTO users (email, full_name, role, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                            (b_email, b_data.get("full_name", ""), b_data.get("role", "user"), b_data.get("status", "pending"), b_data.get("created_at", now_str), b_data.get("updated_at", now_str))
                        )
                    else:
                        self.execute(
                            "UPDATE users SET role = ?, status = ?, updated_at = ? WHERE email = ?",
                            (b_data.get("role", "user"), b_data.get("status", "pending"), b_data.get("updated_at", now_str), b_email)
                        )
        else:
            # Save default state
            save_browser_users({admin_email: {
                "email": admin_email,
                "full_name": "System Administrator",
                "role": "admin",
                "status": "active",
                "created_at": now_str,
                "updated_at": now_str
            }})

    # ================= User Management =================
    def _sync_all_to_browser(self):
        try:
            users_list = self.get_all_users()
            save_browser_users({u["email"]: u for u in users_list})
        except Exception:
            pass

    def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        if not email:
            return None
        norm_email = email.strip().lower()
        if self.use_d1 or self.has_sqlite:
            res = self.execute("SELECT * FROM users WHERE email = ? LIMIT 1", (norm_email,))
            if res:
                return res[0]
        # Check browser storage if not found in db
        b_users = load_browser_users()
        if norm_email in b_users:
            u = b_users[norm_email]
            if self.use_d1 or self.has_sqlite:
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.execute(
                    "INSERT INTO users (email, full_name, role, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (norm_email, u.get("full_name", ""), u.get("role", "user"), u.get("status", "pending"), u.get("created_at", now_str), u.get("updated_at", now_str))
                )
            return u
        return self._users.get(norm_email)

    def register_or_get_user(self, email: str, full_name: str = "") -> Dict[str, Any]:
        norm_email = email.strip().lower()
        user = self.get_user(norm_email)
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if user:
            self._sync_all_to_browser()
            return user

        if norm_email == config.ADMIN_EMAIL.strip().lower():
            role = "admin"
            status = "active"
        else:
            role = "user"
            status = "pending"

        display_name = full_name or norm_email.split("@")[0]

        if self.use_d1 or self.has_sqlite:
            self.execute(
                "INSERT INTO users (email, full_name, role, status, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (norm_email, display_name, role, status, now_str, now_str)
            )
            u = self.get_user(norm_email)
            self._users[norm_email] = u
        else:
            new_u = {
                "email": norm_email,
                "full_name": display_name,
                "role": role,
                "status": status,
                "created_at": now_str,
                "updated_at": now_str
            }
            self._users[norm_email] = new_u
            u = new_u

        self._sync_all_to_browser()
        return u

    def get_all_users(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        # Sync in any browser users first
        b_users = load_browser_users()
        if b_users and (self.use_d1 or self.has_sqlite):
            for b_email, b_data in b_users.items():
                existing = self.execute("SELECT email FROM users WHERE email = ?", (b_email,))
                if not existing:
                    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.execute(
                        "INSERT INTO users (email, full_name, role, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                        (b_email, b_data.get("full_name", ""), b_data.get("role", "user"), b_data.get("status", "pending"), b_data.get("created_at", now_str), b_data.get("updated_at", now_str))
                    )

        if self.use_d1 or self.has_sqlite:
            if status:
                return self.execute("SELECT * FROM users WHERE status = ? ORDER BY created_at DESC", (status,))
            return self.execute("SELECT * FROM users ORDER BY created_at DESC")
        else:
            users = list(self._users.values())
            if status:
                users = [u for u in users if u.get("status") == status]
            users.sort(key=lambda u: u.get("created_at", ""), reverse=True)
            return users

    def update_user_status(self, email: str, status: str):
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        norm_email = email.strip().lower()
        if self.use_d1 or self.has_sqlite:
            self.execute(
                "UPDATE users SET status = ?, updated_at = ? WHERE email = ?",
                (status, now_str, norm_email)
            )
        u = self._users.get(norm_email)
        if u:
            u["status"] = status
            u["updated_at"] = now_str
        self._sync_all_to_browser()

    def update_user_role(self, email: str, role: str):
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        norm_email = email.strip().lower()
        if self.use_d1 or self.has_sqlite:
            self.execute(
                "UPDATE users SET role = ?, updated_at = ? WHERE email = ?",
                (role, now_str, norm_email)
            )
        u = self._users.get(norm_email)
        if u:
            u["role"] = role
            u["updated_at"] = now_str
        self._sync_all_to_browser()

    def delete_user(self, email: str):
        norm_email = email.strip().lower()
        if norm_email == config.ADMIN_EMAIL.strip().lower():
            return
        if self.use_d1 or self.has_sqlite:
            self.execute("DELETE FROM users WHERE email = ?", (norm_email,))
        self._users.pop(norm_email, None)
        self._sync_all_to_browser()

    # ================= Work Codes Repository =================
    def add_work_codes(self, records: List[Dict[str, str]], filename: str, uploaded_by: str) -> int:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if self.use_d1 or self.has_sqlite:
            self.execute("DELETE FROM work_codes WHERE source_file = ?", (filename,))
            self.execute("DELETE FROM uploaded_files WHERE filename = ?", (filename,))

            inserted_count = 0
            if self.has_sqlite and not self.use_d1:
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
                for r in records:
                    self.execute(
                        "INSERT INTO work_codes (code, raw_code, name, unit, source_file, created_at) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (r["code"], r.get("raw_code", r["code"]), r["name"], r.get("unit", ""), filename, now_str)
                    )
                    inserted_count += 1

            self.execute(
                "INSERT INTO uploaded_files (filename, total_records, uploaded_by, uploaded_at) "
                "VALUES (?, ?, ?, ?)",
                (filename, inserted_count, uploaded_by, now_str)
            )
            return inserted_count
        else:
            # In-memory implementation
            self._work_codes = [r for r in self._work_codes if r.get("source_file") != filename]
            for r in records:
                self._work_codes.append({
                    "code": r["code"],
                    "raw_code": r.get("raw_code", r["code"]),
                    "name": r["name"],
                    "unit": r.get("unit", ""),
                    "source_file": filename,
                    "created_at": now_str
                })
            self._uploaded_files[filename] = {
                "filename": filename,
                "total_records": len(records),
                "uploaded_by": uploaded_by,
                "uploaded_at": now_str
            }
            return len(records)

    def get_uploaded_files(self) -> List[Dict[str, Any]]:
        if self.use_d1 or self.has_sqlite:
            return self.execute("SELECT * FROM uploaded_files ORDER BY uploaded_at DESC")
        else:
            files = list(self._uploaded_files.values())
            files.sort(key=lambda f: f.get("uploaded_at", ""), reverse=True)
            return files

    def delete_uploaded_file(self, filename: str):
        if self.use_d1 or self.has_sqlite:
            self.execute("DELETE FROM work_codes WHERE source_file = ?", (filename,))
            self.execute("DELETE FROM uploaded_files WHERE filename = ?", (filename,))
        else:
            self._work_codes = [r for r in self._work_codes if r.get("source_file") != filename]
            self._uploaded_files.pop(filename, None)

    def get_work_codes(
        self,
        search: Optional[str] = None,
        source_file: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        if self.use_d1 or self.has_sqlite:
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
        else:
            res = []
            for r in self._work_codes:
                if source_file and r.get("source_file") != source_file:
                    continue
                if search:
                    s = search.lower()
                    if (s not in r.get("code", "").lower()
                        and s not in r.get("name", "").lower()
                        and s not in r.get("raw_code", "").lower()):
                        continue
                res.append(r)
            res.sort(key=lambda x: x.get("code", ""))
            return res[offset:offset+limit]

    def count_work_codes(self, search: Optional[str] = None, source_file: Optional[str] = None) -> int:
        if self.use_d1 or self.has_sqlite:
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
        else:
            cnt = 0
            for r in self._work_codes:
                if source_file and r.get("source_file") != source_file:
                    continue
                if search:
                    s = search.lower()
                    if (s not in r.get("code", "").lower()
                        and s not in r.get("name", "").lower()
                        and s not in r.get("raw_code", "").lower()):
                        continue
                cnt += 1
            return cnt

    def get_all_codes_lookup(self) -> Dict[str, Dict[str, str]]:
        if self.use_d1 or self.has_sqlite:
            rows = self.execute("SELECT code, raw_code, name, unit, source_file FROM work_codes")
        else:
            rows = self._work_codes

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
