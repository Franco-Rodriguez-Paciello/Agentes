# herramientas.py — las herramientas del asistente del pet shop
from datetime import date, timedelta

from strands import tool

import db

DIAS_VENTANA_DEVOLUCION = 30


@tool
def listar_productos() -> str:
    """Lista el catálogo completo de productos disponibles en el pet shop.

    Returns:
        Un listado con el ID, nombre, precio y stock de cada producto.
    """
    productos = db.obtener_todos("SELECT * FROM productos ORDER BY producto_id")
    lineas = [
        f"{p['producto_id']}: {p['nombre']} — ${p['precio_usd']} USD — Stock: {p['stock']} unidades"
        for p in productos
    ]
    return "\n".join(lineas)


@tool
def consultar_producto(producto_id: str) -> str:
    """Consulta la información detallada de un producto específico por su ID.

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
    return f"{producto['nombre']} — ${producto['precio_usd']} USD — Stock: {producto['stock']} unidades"


@tool
def buscar_cliente(email: str) -> str:
    """Identifica a un cliente del pet shop a partir de su correo electrónico.

    Args:
        email: El correo con el que el cliente se registró, p. ej. "maria@example.com"

    Returns:
        El ID y nombre del cliente, necesarios para consultar sus pedidos.
    """
    cliente = db.obtener_uno(
        "SELECT cliente_id, nombre FROM clientes WHERE email = ?",
        (email.strip().lower(),),
    )
    if cliente is None:
        return f"No hay ningún cliente registrado con el correo {email}."
    return f"Cliente {cliente['cliente_id']}: {cliente['nombre']}"


@tool
def consultar_pedidos(cliente_id: str) -> str:
    """Consulta los pedidos realizados por un cliente, con fechas y estado.

    Args:
        cliente_id: El ID del cliente, p. ej. "C-001" (se obtiene con buscar_cliente)
    """
    pedidos = db.obtener_todos(
        """SELECT p.pedido_id, pr.nombre, p.fecha_pedido, p.estado
           FROM pedidos p JOIN productos pr ON pr.producto_id = p.producto_id
           WHERE p.cliente_id = ?""",
        (cliente_id,),
    )
    if not pedidos:
        return f"El cliente {cliente_id} no tiene pedidos registrados."
    lineas = [
        f"Pedido {p['pedido_id']}: {p['nombre']} — pedido el {p['fecha_pedido']} — estado: {p['estado']}"
        for p in pedidos
    ]
    return "\n".join(lineas)


@tool
def procesar_devolucion(pedido_id: int) -> str:
    """Procesa la devolución de un pedido, si cumple la política del pet shop.

    La política permite devoluciones hasta 30 días después de la fecha del pedido.

    Args:
        pedido_id: El número del pedido a devolver (se obtiene con consultar_pedidos)

    Returns:
        Confirmación con el monto devuelto, o el motivo por el cual no procede.
    """
    # Violación de contrato → raise (el "500"): Strands lo convierte en un resultado de error
    if pedido_id <= 0:
        raise ValueError("El pedido_id debe ser un entero positivo.")

    pedido = db.obtener_uno(
        """SELECT p.pedido_id, p.fecha_pedido, p.estado, pr.nombre, pr.precio_usd
           FROM pedidos p JOIN productos pr ON pr.producto_id = p.producto_id
           WHERE p.pedido_id = ?""",
        (pedido_id,),
    )

    # Resultados de dominio → return informativo (los "404")
    if pedido is None:
        return f"No existe el pedido {pedido_id}."
    if pedido["estado"] == "devuelto":
        return f"El pedido {pedido_id} ya fue devuelto anteriormente."

    # Regla de negocio DETERMINISTA: la fecha se compara en código, no la compara el modelo
    fecha_pedido = date.fromisoformat(pedido["fecha_pedido"])
    fecha_limite = fecha_pedido + timedelta(days=DIAS_VENTANA_DEVOLUCION)
    if date.today() > fecha_limite:
        return (
            f"La devolución no es elegible: el pedido es del {fecha_pedido} "
            f"y la ventana de {DIAS_VENTANA_DEVOLUCION} días venció el {fecha_limite}."
        )

    db.ejecutar(
        "UPDATE pedidos SET estado = 'devuelto' WHERE pedido_id = ?",
        (pedido_id,),
    )
    return (
        f"Devolución procesada: {pedido['nombre']} — "
        f"${pedido['precio_usd']} USD devueltos al cliente."
    )