"""Utilidades simples para guardar evidencia de ejecución del agente."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from app.config import LOG_DIR


def serializable_message(message: Any) -> dict:
    """Convierte mensajes de LangChain a diccionarios guardables en JSON."""

    return {
        "type": message.__class__.__name__,
        "content": getattr(message, "content", None),
        "tool_calls": getattr(message, "tool_calls", None),
        "name": getattr(message, "name", None),
    }


def guardar_log(consulta: str, respuesta: dict) -> Path:
    """Guarda consulta, mensajes y tool calls para evidencia."""

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = LOG_DIR / f"agente_{timestamp}.json"

    payload = {
        "timestamp": datetime.now().isoformat(),
        "consulta_usuario": consulta,
        "messages": [serializable_message(m) for m in respuesta.get("messages", [])],
    }

    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    return path
