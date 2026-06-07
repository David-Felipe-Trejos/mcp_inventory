import sqlite3

DB_NAME = "inventory.db"


def init_db():
    """Inicializa la base de datos y crea la tabla de productos si no existe."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print(f"Base de datos '{DB_NAME}' inicializada correctamente.")


if __name__ == "__main__":
    init_db()
