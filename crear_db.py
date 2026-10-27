# crear_db.py — crea la base de datos del pet shop con datos de ejemplo
import sqlite3

conexion = sqlite3.connect("petshop.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    producto_id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio_usd REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")

cursor.executemany(
    "INSERT OR REPLACE INTO productos VALUES (?, ?, ?, ?)",
    [
        ("AL-101", "Alimento Premium para Perros 15kg", 45.99, 25),
        ("JU-201", "Juguete mordillo interactivo", 19.99, 40),
        ("AC-301", "Collar ajustable con correa reflectante", 14.50, 30),
        ("SN-401", "Snacks naturales de pollo 250g", 6.99, 60),
    ],
)

conexion.commit()
conexion.close()
print("Base de datos petshop.db creada con datos de ejemplo del pet shop")