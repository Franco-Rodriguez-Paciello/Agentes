# crear_db.py — crea la base de datos del pet shop con datos de ejemplo
import sqlite3
from datetime import date, timedelta

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

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    cliente_id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    pedido_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id TEXT NOT NULL REFERENCES clientes(cliente_id),
    producto_id TEXT NOT NULL REFERENCES productos(producto_id),
    fecha_pedido TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'completado'    -- 'completado' | 'devuelto'
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

cursor.executemany(
    "INSERT OR REPLACE INTO clientes VALUES (?, ?, ?)",
    [
        ("C-001", "María Gómez", "maria@example.com"),
        ("C-002", "Carlos Ruiz", "carlos@example.com"),
    ],
)

# Fechas RELATIVAS a hoy, para que las demos funcionen siempre (ej. política de devolución de 30 días):
hace_10_dias = (date.today() - timedelta(days=10)).isoformat()    # elegible para devolución
hace_45_dias = (date.today() - timedelta(days=45)).isoformat()    # fuera de la ventana de 30 días

cursor.execute("DELETE FROM pedidos")
cursor.executemany(
    "INSERT INTO pedidos (cliente_id, producto_id, fecha_pedido, estado) VALUES (?, ?, ?, ?)",
    [
        ("C-001", "JU-201", hace_10_dias, "completado"),    # id 1: devolución ELEGIBLE
        ("C-001", "AL-101", hace_45_dias, "completado"),    # id 2: devolución NO elegible (ventana de 30 días)
        ("C-002", "AC-301", hace_10_dias, "devuelto"),      # id 3: ya devuelto
    ],
)

conexion.commit()
conexion.close()
print("Base de datos petshop.db creada con datos de ejemplo y fechas relativas")