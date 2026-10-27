from strands import Agent
# main.py — ensamblaje y punto de entrada del asistente
from strands import Agent
from strands.models import BedrockModel

from herramientas import consultar_producto

SYSTEM_PROMPT = """Eres el asistente virtual de una petshop.
Atiendes a clientes en español, de forma clara y amable."""


def crear_agente() -> Agent:
    """Crea y configura el asistente de la petshop."""
    modelo = BedrockModel(
        model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",   # ← el que te dio el diagnóstico del Módulo 1
        region_name="us-east-2",  # ← región siempre explícita, como acordamos
        temperature=0.3,
        max_tokens=1024,
    )
    return Agent(
        model=modelo,
        system_prompt=SYSTEM_PROMPT,
        tools=[consultar_producto],
    )


if __name__ == "__main__":
    agente = crear_agente()
    agente("¿Cuánto cuesta el producto Alimento Premium para Perros y cuánto cuesta?")

    import json
    print(json.dumps(agente.messages, indent=2, ensure_ascii=False, default=str))