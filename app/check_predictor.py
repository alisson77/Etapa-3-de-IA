"""Prueba directa sin LLM para verificar que los artefactos de Persona A funcionan."""

from app.predictor import predict_student_risk


sample_student = {
    "Hours_Studied": 12,
    "Attendance": 78,
    "Previous_Scores": 65,
    "Tutoring_Sessions": 1,
    "Teacher_Quality": "Medium",
    "Family_Income": "Low",
    "Access_to_Resources": "Medium",
    "Internet_Access": "Yes",
    "Distance_from_Home": "Moderate",
    "Motivation_Level": "Medium",
    "Parental_Involvement": "Low",
    "Peer_Influence": "Neutral",
    "Learning_Disabilities": "No",
    "Sleep_Hours": 6,
}


if __name__ == "__main__":
    print("Probando predictor directo con un estudiante de ejemplo...\n")
    result = predict_student_risk(sample_student)
    print(result)
