# herramientas.py — las herramientas del asistente de la petshop
from strands import tool
import db


@tool
def consultar_producto(producto_id: str) -> str:
    """Consulta la información de un producto por su ID.

    Args:
        producto_id: El identificador del producto, p. ej. "AL-101"
    """
    producto = db.obtener_uno(
        "SELECT nombre, precio_usd, stock FROM productos WHERE producto_id = ?",
        (producto_id,),
    )
    if producto is None:
        validos = [p["producto_id"] for p in db.obtener_todos("SELECT producto_id FROM productos")]
        return f"No existe el producto {producto_id}. IDs válidos: {validos}"
    return f"{producto['nombre']} — ${producto['precio_usd']} USD — Stock: {producto['stock']}"