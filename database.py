"""
database.py – SQLite database setup and user management for FlashMind AI.
Handles user creation and authentication with hashed passwords.
"""

import sqlite3
import hashlib
import os

# Path to the SQLite database file
DB_PATH = os.path.join(os.path.dirname(__file__), "flashmind.db")


def _hash_password(password: str) -> str:
    """Hash a password using SHA-256 for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()


def get_connection() -> sqlite3.Connection:
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    """
    Initialize the database and create the users table if it doesn't exist.
    Call this once at app startup.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Safely add new columns to existing database (won't fail if already exist)
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN full_name TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN age INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()


def create_user(username: str, password: str) -> dict:
    """
    Register a new user in the database.

    Returns:
        dict with 'success' (bool) and 'message' (str)
    """
    if not username.strip() or not password.strip():
        return {"success": False, "message": "Username and password cannot be empty."}

    if len(password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters."}

    conn = get_connection()
    cursor = conn.cursor()
    try:
        password_hash = _hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username.strip(), password_hash),
        )
        conn.commit()
        return {"success": True, "message": "Account created successfully!"}
    except sqlite3.IntegrityError:
        return {"success": False, "message": "Username already exists. Please choose another."}
    finally:
        conn.close()


def login_user(username: str, password: str) -> dict:
    """
    Authenticate a user against the database.

    Returns:
        dict with 'success' (bool) and 'message' (str)
    """
    if not username.strip() or not password.strip():
        return {"success": False, "message": "Please enter your username and password."}

    conn = get_connection()
    cursor = conn.cursor()
    try:
        password_hash = _hash_password(password)
        cursor.execute(
            "SELECT id, username FROM users WHERE username = ? AND password_hash = ?",
            (username.strip(), password_hash),
        )
        row = cursor.fetchone()
        if row:
            return {"success": True, "message": f"Welcome back, {row[1]}!", "username": row[1]}
        else:
            return {"success": False, "message": "Invalid username or password."}
    finally:
        conn.close()


# ══════════════════════════════════════════════════════════════════════════════
#  SETTINGS FEATURES — added below, nothing above is changed
# ══════════════════════════════════════════════════════════════════════════════

def get_user_profile(username: str) -> dict:
    """
    Fetch full profile info for a user.

    Returns:
        dict with 'success', 'username', 'full_name', 'age', 'created_at'
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT username, full_name, age, created_at FROM users WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()
        if row:
            return {
                "success": True,
                "username": row[0],
                "full_name": row[1] or "",
                "age": row[2] or 0,
                "created_at": row[3],
            }
        return {"success": False, "message": "User not found."}
    finally:
        conn.close()


def update_profile(username: str, full_name: str, age: int) -> dict:
    """
    Update a user's full name and age.

    Returns:
        dict with 'success' (bool) and 'message' (str)
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET full_name = ?, age = ? WHERE username = ?",
            (full_name.strip(), int(age) if age else 0, username)
        )
        conn.commit()
        return {"success": True, "message": "Profile updated successfully!"}
    except Exception as e:
        return {"success": False, "message": str(e)}
    finally:
        conn.close()


def update_password(username: str, old_password: str, new_password: str) -> dict:
    """
    Change a user's password after verifying the old one.

    Returns:
        dict with 'success' (bool) and 'message' (str)
    """
    if len(new_password) < 6:
        return {"success": False, "message": "New password must be at least 6 characters."}

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password_hash = ?",
            (username, _hash_password(old_password))
        )
        if not cursor.fetchone():
            return {"success": False, "message": "Current password is incorrect."}
        cursor.execute(
            "UPDATE users SET password_hash = ? WHERE username = ?",
            (_hash_password(new_password), username)
        )
        conn.commit()
        return {"success": True, "message": "Password updated successfully!"}
    finally:
        conn.close()


def delete_account(username: str, password: str) -> dict:
    """
    Permanently delete a user account after verifying password.

    Returns:
        dict with 'success' (bool) and 'message' (str)
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password_hash = ?",
            (username, _hash_password(password))
        )
        if not cursor.fetchone():
            return {"success": False, "message": "Incorrect password. Account not deleted."}
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        return {"success": True, "message": "Account deleted successfully."}
    finally:
        conn.close()