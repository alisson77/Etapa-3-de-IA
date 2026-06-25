"""Configuración central del proyecto local."""

from pathlib import Path
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv es opcional; el proyecto también funciona con variables de entorno normales.
    pass

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = Path(os.getenv("MODEL_DIR", BASE_DIR / "models"))
LOG_DIR = Path(os.getenv("LOG_DIR", BASE_DIR / "logs"))

# Modelo local de Ollama. Cambialo si en `ollama list` usás otro nombre.
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:0.6b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))

ARTIFACT_FILES = {
    "preprocessor": "preprocessor.joblib",
    "label_encoder": "label_encoder.joblib",
    "model": "logreg_optimized.joblib",
    "metadata": "metadata.joblib",
}
