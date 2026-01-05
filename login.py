import sqlite3
import hashlib

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# --- Password Hashing ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Register User ---
def register_user(username, password):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, hash_password(password)))
        conn.commit()
        print("✅ User registered successfully!")
    except sqlite3.IntegrityError:
        print("⚠️ Username already exists!")
    conn.close()

# --- Authenticate User ---
def authenticate_user(username, password):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0] == hash_password(password):
        print("✅ Login successful!")
        return True
    else:
        print("❌ Invalid username or password.")
        return False

# --- Example Usage ---
if __name__ == "__main__":
    init_db()

    # Register new users
    register_user("teacher1", "securepass123")
    register_user("student1", "mypassword")

    # Authenticate users
    authenticate_user("teacher1", "securepass123")  # ✅ success
    authenticate_user("student1", "wrongpass")      # ❌ fail
