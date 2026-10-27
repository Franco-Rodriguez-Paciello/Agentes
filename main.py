# main.py — ensamblaje y punto de entrada del asistente del pet shop
from strands import Agent
from strands.models import BedrockModel
from strands_tools import current_time

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
    modelo = BedrockModel(
        model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",   # modelo configurado para las prácticas
        region_name="us-east-2",
        temperature=0.3,
        max_tokens=1024,
    )
    return Agent(
        model=modelo,
        system_prompt=SYSTEM_PROMPT,
        tools=[
            listar_productos,
            consultar_producto,
            buscar_cliente,
            consultar_pedidos,
            procesar_devolucion,
            current_time,
        ],
    )


if __name__ == "__main__":
    agente = crear_agente()
    agente("Soy maria@example.com. Quiero la devolución de mi último pedido.")