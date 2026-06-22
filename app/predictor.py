from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from app.config import MODEL_DIR, ARTIFACT_FILES


class ArtifactLoadError(RuntimeError):
    """Error claro cuando faltan artefactos del modelo."""


@lru_cache(maxsize=1)
def load_artifacts() -> dict[str, Any]:
    """Carga una sola vez el preprocesador, encoder, modelo y metadatos."""

    paths = {name: Path(MODEL_DIR) / filename for name, filename in ARTIFACT_FILES.items()}
    missing = [str(path) for path in paths.values() if not path.exists()]

    if missing:
        raise ArtifactLoadError(
            "Faltan artefactos del modelo. Copia estos archivos desde la parte de Persona A "
            f"hacia la carpeta {MODEL_DIR}:\n- " + "\n- ".join(missing)
        )

    return {
        "preprocessor": joblib.load(paths["preprocessor"]),
        "label_encoder": joblib.load(paths["label_encoder"]),
        "model": joblib.load(paths["model"]),
        "metadata": joblib.load(paths["metadata"]),
    }


def predict_student_risk(student_data: dict) -> dict:
    """
    Recibe datos crudos de un estudiante y devuelve clase + probabilidades.

    Esta función NO entrena nada. Solo carga los artefactos serializados por Persona A,
    aplica el mismo preprocesamiento y ejecuta el modelo optimizado.
    """

    artifacts = load_artifacts()
    preprocessor = artifacts["preprocessor"]
    label_encoder = artifacts["label_encoder"]
    model = artifacts["model"]
    metadata = artifacts["metadata"]

    student_df = pd.DataFrame([student_data])

    expected_cols = metadata["numerical_features"] + metadata["categorical_features"]
    missing = sorted(set(expected_cols) - set(student_df.columns))

    if missing:
        raise ValueError(f"Faltan columnas obligatorias para predecir: {missing}")

    # Reordenar columnas para que coincidan exactamente con entrenamiento.
    student_df = student_df[expected_cols]

    x_processed = preprocessor.transform(student_df)
    proba = model.predict_proba(x_processed)[0]
    pred_class = model.predict(x_processed)[0]
    class_label = label_encoder.inverse_transform([pred_class])[0]

    return {
        "class": int(pred_class),
        "class_label": str(class_label),
        "probability_risk": float(proba[1]),
        "probability_not_risk": float(proba[0]),
        "risk_percentage": f"{proba[1] * 100:.2f}%",
    }
