"""Análisis de sesgos, falsos negativos y privacidad.

Este script evalúa falsos negativos por subgrupos del conjunto de prueba.
No utiliza nombres, cédulas, correos ni identificadores personales.
"""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from app.predictor import predict_student_risk
from app.config import BASE_DIR, LOG_DIR


DATA_PATH = BASE_DIR / "data" / "test_data_for_bias_analysis.csv"

SUBGROUP_COLUMNS = [
    "Family_Income",
    "Access_to_Resources",
    "Internet_Access",
    "Distance_from_Home",
    "Motivation_Level",
    "Parental_Involvement",
    "Peer_Influence",
    "Learning_Disabilities",
]

FORBIDDEN_COLUMNS = [
    "Name",
    "Student_Name",
    "Cedula",
    "ID",
    "Student_ID",
    "Email",
    "Phone",
    "Address",
]


def revisar_privacidad(df: pd.DataFrame) -> dict:
    """Verifica si el dataset contiene identificadores personales evidentes."""

    columnas_presentes = set(df.columns)
    columnas_prohibidas = [
        col for col in FORBIDDEN_COLUMNS
        if col in columnas_presentes
    ]

    return {
        "contiene_identificadores_personales": len(columnas_prohibidas) > 0,
        "columnas_identificadoras_detectadas": columnas_prohibidas,
        "criterio": (
            "El análisis no debe utilizar nombres, cédulas, correos, teléfonos "
            "ni direcciones. Solo se usan variables académicas y contextuales."
        ),
    }


def predecir_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Genera predicciones para cada registro usando el modelo serializado."""

    predicciones = []

    for _, row in df.iterrows():
        student_data = row.drop(labels=["Risk_Performance"]).to_dict()
        result = predict_student_risk(student_data)

        predicciones.append(
            {
                "pred_class": result["class_label"],
                "probability_risk": result["probability_risk"],
                "probability_not_risk": result["probability_not_risk"],
            }
        )

    pred_df = pd.DataFrame(predicciones)

    return pd.concat([df.reset_index(drop=True), pred_df], axis=1)


def calcular_falsos_negativos_por_subgrupo(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula tasa de falsos negativos por subgrupo."""

    resultados = []

    for columna in SUBGROUP_COLUMNS:
        if columna not in df.columns:
            continue

        for valor, grupo in df.groupby(columna):
            reales_risk = grupo[grupo["Risk_Performance"] == "risk"]

            total_risk = len(reales_risk)

            if total_risk == 0:
                false_negative_rate = None
                falsos_negativos = 0
            else:
                falsos_negativos = len(
                    reales_risk[reales_risk["pred_class"] == "not_risk"]
                )
                false_negative_rate = falsos_negativos / total_risk

            resultados.append(
                {
                    "variable_subgrupo": columna,
                    "subgrupo": str(valor),
                    "total_registros_subgrupo": len(grupo),
                    "total_reales_risk": total_risk,
                    "falsos_negativos": falsos_negativos,
                    "false_negative_rate": false_negative_rate,
                }
            )

    return pd.DataFrame(resultados)


def generar_reporte() -> dict:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo {DATA_PATH}. "
            "Primero exportá test_data_for_bias_analysis.csv desde Colab."
        )

    df = pd.read_csv(DATA_PATH)

    privacidad = revisar_privacidad(df)

    if privacidad["contiene_identificadores_personales"]:
        raise ValueError(
            "El archivo contiene columnas con posibles identificadores personales: "
            f"{privacidad['columnas_identificadoras_detectadas']}. "
            "Eliminá esas columnas antes de ejecutar el análisis."
        )

    df_pred = predecir_dataframe(df)
    subgroup_results = calcular_falsos_negativos_por_subgrupo(df_pred)

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    csv_path = LOG_DIR / "bias_false_negative_by_subgroup.csv"
    json_path = LOG_DIR / "bias_privacy_report.json"

    subgroup_results.to_csv(csv_path, index=False)

    resumen = {
        "timestamp": datetime.now().isoformat(),
        "privacidad": privacidad,
        "total_registros": len(df_pred),
        "columnas_analizadas": SUBGROUP_COLUMNS,
        "archivo_resultados_subgrupos": str(csv_path),
        "nota": (
            "El análisis identifica posibles diferencias en falsos negativos "
            "entre subgrupos. Los resultados no prueban causalidad, pero sirven "
            "para detectar riesgos de sesgo antes de un despliegue real."
        ),
    }

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(resumen, file, ensure_ascii=False, indent=2)

    return {
        "json_path": json_path,
        "csv_path": csv_path,
        "subgroup_results": subgroup_results,
        "resumen": resumen,
    }


if __name__ == "__main__":
    reporte = generar_reporte()

    print("Análisis de sesgos y privacidad completado.")
    print(f"Reporte JSON: {reporte['json_path']}")
    print(f"Resultados por subgrupo: {reporte['csv_path']}")

    print("\nPrimeras filas del análisis por subgrupo:")
    print(reporte["subgroup_results"].head(20))