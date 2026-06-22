"""Schemas de entrada/salida para la tool del agente."""

from typing import Literal
from pydantic import BaseModel, Field


Nivel = Literal["Low", "Medium", "High"]
SiNo = Literal["Yes", "No"]
Distancia = Literal["Near", "Moderate", "Far"]
InfluenciaPares = Literal["Positive", "Neutral", "Negative"]


class DatosEstudianteInput(BaseModel):
    """Campos obligatorios del modelo entrenado por Persona A."""

    Hours_Studied: float = Field(..., ge=0, description="Horas de estudio del estudiante.")
    Attendance: float = Field(..., ge=0, le=100, description="Porcentaje de asistencia entre 0 y 100.")
    Previous_Scores: float = Field(..., ge=0, le=100, description="Calificaciones previas entre 0 y 100.")
    Tutoring_Sessions: int = Field(..., ge=0, description="Cantidad de sesiones de tutoría.")
    Teacher_Quality: Nivel = Field(..., description="Calidad docente: Low, Medium o High.")
    Family_Income: Nivel = Field(..., description="Ingreso familiar: Low, Medium o High.")
    Access_to_Resources: Nivel = Field(..., description="Acceso a recursos: Low, Medium o High.")
    Internet_Access: SiNo = Field(..., description="Acceso a internet: Yes o No.")
    Distance_from_Home: Distancia = Field(..., description="Distancia desde el hogar: Near, Moderate o Far.")
    Motivation_Level: Nivel = Field(..., description="Nivel de motivación: Low, Medium o High.")
    Parental_Involvement: Nivel = Field(..., description="Involucramiento parental: Low, Medium o High.")
    Peer_Influence: InfluenciaPares = Field(..., description="Influencia de pares: Positive, Neutral o Negative.")
    Learning_Disabilities: SiNo = Field(..., description="Dificultades de aprendizaje: Yes o No.")
    Sleep_Hours: float = Field(..., ge=0, le=24, description="Horas de sueño por día.")


class ResultadoPrediccion(BaseModel):
    """Salida estructurada que produce la tool después de llamar el modelo."""

    clase_modelo: str
    probabilidad_riesgo: float
    probabilidad_no_riesgo: float
    porcentaje_riesgo: str
    nivel_descriptivo: str
    datos_usados: dict
    advertencia: str
