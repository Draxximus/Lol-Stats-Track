import os
import time
import sqlite3
import threading
from typing import List, Dict, Optional
from storage.conffig import db_path


LOCAL_APPDATA = os.getenv("LOCALAPPDATA")
if LOCAL_APPDATA:
    BASE_DIR = os.path.join(LOCAL_APPDATA, "LolMST")
else:
    BASE_DIR = os.path.join(os.path.expanduser("~"), ".lolmst")

os.makedirs(BASE_DIR, exist_ok=True)
DB_PATH = db_path
print(f"[DB] Usando base de datos SQLite en: {DB_PATH}")

_conn = sqlite3.connect(DB_PATH, check_same_thread=False)
_lock = threading.Lock()

with _conn:
    _conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            started_at REAL
        );
        """
    )

# Tabla de eventos
with _conn:
    _conn.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            type TEXT,
            button TEXT,
            pressed INTEGER,
            x REAL,
            y REAL,
            timestamp REAL
        );
        """
    )

# Migración simple: asegurarnos de que exista la columna session_id
with _conn:
    cur = _conn.execute("PRAGMA table_info(events);")
    cols = [row[1] for row in cur.fetchall()]
    if "session_id" not in cols:
        print("[DB] Agregando columna session_id a events (migración).")
        _conn.execute("ALTER TABLE events ADD COLUMN session_id INTEGER;")

# Sesión actual en memoria
_current_session_id: Optional[int] = None


# ==========================
#  MANEJO DE SESIONES
# ==========================

def start_new_session(name: Optional[str] = None) -> int:
    """
    Crea una nueva sesión (partida) y la marca como sesión actual.
    name: nombre opcional para identificar la sesión (ej: 'Ranked top', 'Normals', etc.)
    """
    global _current_session_id

    started_at = time.time()
    with _lock, _conn:
        cur = _conn.cursor()
        cur.execute(
            "INSERT INTO sessions (name, started_at) VALUES (?, ?)",
            (name, started_at),
        )
        _current_session_id = cur.lastrowid

    print(f"[DB] Nueva sesión iniciada: id={_current_session_id}, name={name}")
    return _current_session_id


def get_current_session_id() -> Optional[int]:
    return _current_session_id


def get_latest_session_id() -> Optional[int]:
    """
    Devuelve el id de la sesión más reciente, o None si no hay.
    """
    with _lock:
        cur = _conn.cursor()
        cur.execute(
            "SELECT id FROM sessions ORDER BY started_at DESC LIMIT 1;"
        )
        row = cur.fetchone()

    return row[0] if row else None


# ==========================
#  EVENTOS
# ==========================

def save_event(event: Dict):
    """
    Guarda un evento en SQLite, asociado a la sesión actual.
    Si no hay sesión actual, crea una nueva automáticamente.
    """
    global _current_session_id

    if _current_session_id is None:
        # Si por cualquier motivo nadie inició sesión, la creamos aquí
        start_new_session(name="auto")

    type_ = event.get("type")
    button = str(event.get("button")) if event.get("button") else None
    pressed = event.get("pressed")
    pressed = int(bool(pressed)) if pressed is not None else None

    x = event.get("x")
    y = event.get("y")
    ts = event.get("timestamp")

    with _lock, _conn:
        _conn.execute(
            """
            INSERT INTO events (session_id, type, button, pressed, x, y, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (_current_session_id, type_, button, pressed, x, y, ts),
        )

def load_events(session_id: int | None = None, event_type: str | None = None):
    query = "SELECT session_id, type, button, pressed, x, y, timestamp FROM events"
    params = []
    conditions = []

    if session_id is not None:
        conditions.append("session_id = ?")
        params.append(session_id)
    if event_type is not None:
        conditions.append("type = ?")
        params.append(event_type)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    with _lock:
        cur = _conn.cursor()
        cur.execute(query, tuple(params))
        rows = cur.fetchall()

    events = []
    for sess_id, type_, button, pressed, x, y, ts in rows:
        events.append({
            "session_id": sess_id,
            "type": type_,
            "button": button,
            "pressed": bool(pressed) if pressed is not None else None,
            "x": x,
            "y": y,
            "timestamp": ts,
        })

    print(f"[DB] Eventos cargados desde SQLite: {len(events)} (session_id={session_id})")
    return events