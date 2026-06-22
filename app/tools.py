"""Tool LangChain que encapsula el modelo predictivo."""

import json
from langchain_core.tools import StructuredTool

from app.predictor import predict_student_risk
from app.schemas import DatosEstudianteInput


def nivel_riesgo_descriptivo(probability_risk: float) -> str:
    """Convierte la probabilidad de riesgo en una etiqueta interpretativa simple."""

    if probability_risk >= 0.80:
        return "riesgo alto"
    if probability_risk >= 0.50:
        return "riesgo moderado"
    if probability_risk >= 0.30:
        return "riesgo bajo-moderado"
    return "riesgo bajo"


def predecir_riesgo_estudiante(
    Hours_Studied: float,
    Attendance: float,
    Previous_Scores: float,
    Tutoring_Sessions: int,
    Teacher_Quality: str,
    Family_Income: str,
    Access_to_Resources: str,
    Internet_Access: str,
    Distance_from_Home: str,
    Motivation_Level: str,
    Parental_Involvement: str,
    Peer_Influence: str,
    Learning_Disabilities: str,
    Sleep_Hours: float,
) -> str:
    """
    Predice riesgo académico con el modelo supervisado de Persona A.

    Devuelve un JSON para que el agente pueda leer clase, probabilidades,
    datos usados y advertencia ética.
    """

    student_data = {
        "Hours_Studied": Hours_Studied,
        "Attendance": Attendance,
        "Previous_Scores": Previous_Scores,
        "Tutoring_Sessions": Tutoring_Sessions,
        "Teacher_Quality": Teacher_Quality,
        "Family_Income": Family_Income,
        "Access_to_Resources": Access_to_Resources,
        "Internet_Access": Internet_Access,
        "Distance_from_Home": Distance_from_Home,
        "Motivation_Level": Motivation_Level,
        "Parental_Involvement": Parental_Involvement,
        "Peer_Influence": Peer_Influence,
        "Learning_Disabilities": Learning_Disabilities,
        "Sleep_Hours": Sleep_Hours,
    }

    model_result = predict_student_risk(student_data)
    probability_risk = float(model_result["probability_risk"])

    output = {
        "clase_modelo": model_result["class_label"],
        "probabilidad_riesgo": probability_risk,
        "probabilidad_no_riesgo": float(model_result["probability_not_risk"]),
        "porcentaje_riesgo": model_result["risk_percentage"],
        "nivel_descriptivo": nivel_riesgo_descriptivo(probability_risk),
        "datos_usados": student_data,
        "advertencia": (
            "La predicción es un apoyo para análisis académico. "
            "No debe usarse como decisión automática única sobre el estudiante."
        ),
    }

    return json.dumps(output, ensure_ascii=False, indent=2)


tool_predecir_riesgo = StructuredTool.from_function(
    func=predecir_riesgo_estudiante,
    name="predecir_riesgo_estudiante",
    description=(
        "Usa el modelo supervisado entrenado para predecir si un estudiante presenta "
        "riesgo académico. Requiere los 14 campos del schema. Devuelve clase del modelo, "
        "probabilidad de riesgo, probabilidad de no riesgo y advertencia ética."
    ),
    args_schema=DatosEstudianteInput,
)

TOOLS = [tool_predecir_riesgo]
