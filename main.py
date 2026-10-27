# main.py — ensamblaje y punto de entrada del asistente del pet shop
from strands import Agent
from config import get_model


from herramientas import (
    buscar_cliente,
    consultar_pedidos,
    consultar_producto,
    listar_productos,
    procesar_devolucion,
)

SYSTEM_PROMPT = """Eres el asistente virtual de un pet shop (tienda de mascotas).
Atiendes a clientes en español, de forma clara y amable.
Antes de consultar pedidos o procesar devoluciones, identifica al cliente por su correo electrónico."""


def crear_agente() -> Agent:
    """Crea y configura el asistente del pet shop."""
    return Agent(
        model= get_model(),
        system_prompt=SYSTEM_PROMPT,
        tools=[
            listar_productos,
            consultar_producto,
            buscar_cliente,
            consultar_pedidos,
            procesar_devolucion,
        ],
    )


if __name__ == "__main__":
    agente = crear_agente()
    agente("Soy maria@example.com. Quiero la devolución de mi último pedido.")