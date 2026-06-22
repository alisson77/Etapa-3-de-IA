"""Creación del agente LangChain con Ollama."""

from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from app.config import OLLAMA_MODEL, OLLAMA_BASE_URL, TEMPERATURE
from app.prompts import SYSTEM_PROMPT
from app.tools import TOOLS


def crear_llm() -> ChatOllama:
    """Crea el modelo local de Ollama."""

    return ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=TEMPERATURE,
    )


def crear_agente():
    """Crea un agente con acceso a la tool de predicción."""

    llm = crear_llm()

    return create_agent(
        model=llm,
        tools=TOOLS,
        system_prompt=SYSTEM_PROMPT,
    )


def extraer_texto_respuesta(agent_response: dict) -> str:
    """Extrae texto legible desde la respuesta del agente de LangChain."""

    messages = agent_response.get("messages", [])
    if not messages:
        return str(agent_response)

    last_message = messages[-1]
    content = getattr(last_message, "content", None)
    if isinstance(content, str):
        return content

    return str(content or last_message)
