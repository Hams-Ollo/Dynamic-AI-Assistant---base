import sqlite3
from pathlib import Path

def setup_sqlite():
    """Setup SQLite database and create necessary tables if they don't exist."""
    db_path = Path(__file__).parent.parent.parent / "data" / "chat_history.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Create messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    return str(db_path)
