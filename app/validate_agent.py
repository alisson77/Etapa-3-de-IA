"""Validación automática del agente.

Evalúa:
1. Si el agente llama la herramienta cuando corresponde.
2. Si evita predecir con datos incompletos.
3. Si contradice la salida del modelo.
4. Si alucina predicciones sin datos suficientes.
"""

import json
from datetime import datetime
from pathlib import Path

from app.agent import crear_agente, extraer_texto_respuesta
from app.config import LOG_DIR
from app.test_cases import TEST_CASES


def extraer_tool_outputs(respuesta: dict) -> list[dict]:
    """Extrae salidas JSON de ToolMessage generadas por LangChain."""

    outputs = []

    for message in respuesta.get("messages", []):
        message_type = message.__class__.__name__
        name = getattr(message, "name", None)
        content = getattr(message, "content", None)

        if message_type == "ToolMessage" or name == "predecir_riesgo_estudiante":
            try:
                outputs.append(json.loads(content))
            except Exception:
                outputs.append({"raw_output": str(content)})

    return outputs


def tool_fue_llamada(respuesta: dict) -> bool:
    """Verifica si aparece una llamada a la herramienta del modelo."""

    for message in respuesta.get("messages", []):
        tool_calls = getattr(message, "tool_calls", None)

        if tool_calls:
            for call in tool_calls:
                if call.get("name") == "predecir_riesgo_estudiante":
                    return True

        if getattr(message, "name", None) == "predecir_riesgo_estudiante":
            return True

        if message.__class__.__name__ == "ToolMessage":
            return True

    return False


def detectar_contradiccion(texto_final: str, tool_outputs: list[dict]) -> bool:
    """Detecta si el texto final contradice la clase devuelta por el modelo."""

    if not tool_outputs:
        return False

    salida_modelo = tool_outputs[-1]
    clase_modelo = salida_modelo.get("clase_modelo")

    if not clase_modelo:
        return False

    texto = texto_final.lower()
    clase = clase_modelo.lower()

    if clase == "risk":
        return "clase predicha: not_risk" in texto or "clase predicha: no riesgo" in texto

    if clase == "not_risk":
        return "clase predicha: risk" in texto or "clase predicha: riesgo" in texto

    return False


def detectar_alucinacion_sin_datos(texto_final: str, fue_llamada: bool, debe_generar_prediccion: bool) -> bool:
    """Detecta si el agente genera predicción cuando no debía hacerlo."""

    if debe_generar_prediccion:
        return False

    if fue_llamada:
        return True

    texto = texto_final.lower()

    indicadores_prediccion = [
        "clase predicha",
        "probabilidad de riesgo",
        "porcentaje de riesgo",
        "%",
        "riesgo alto",
        "riesgo moderado",
        "not_risk",
        "risk",
    ]

    return any(indicador in texto for indicador in indicadores_prediccion)


def respuesta_contiene_salida_modelo(texto_final: str, tool_outputs: list[dict]) -> bool:
    """Verifica que la respuesta final incluya clase y porcentaje devueltos por el modelo."""

    if not tool_outputs:
        return False

    salida_modelo = tool_outputs[-1]
    clase = str(salida_modelo.get("clase_modelo", "")).lower()
    porcentaje = str(salida_modelo.get("porcentaje_riesgo", ""))

    texto = texto_final.lower()

    return clase in texto and porcentaje in texto_final


def validar_agente() -> list[dict]:
    agente = crear_agente()
    resultados = []

    for caso in TEST_CASES:
        print(f"Ejecutando {caso['id']} - {caso['tipo']}")

        try:
            respuesta = agente.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": caso["consulta"],
                        }
                    ]
                }
            )

            texto_final = extraer_texto_respuesta(respuesta)
            fue_llamada = tool_fue_llamada(respuesta)
            tool_outputs = extraer_tool_outputs(respuesta)

            contradiccion = detectar_contradiccion(texto_final, tool_outputs)
            alucinacion = detectar_alucinacion_sin_datos(
                texto_final=texto_final,
                fue_llamada=fue_llamada,
                debe_generar_prediccion=caso["debe_generar_prediccion"],
            )

            contiene_salida_modelo = (
                respuesta_contiene_salida_modelo(texto_final, tool_outputs)
                if caso["debe_generar_prediccion"]
                else True
            )

            cumple_tool_call = fue_llamada == caso["debe_llamar_tool"]

            cumple = (
                cumple_tool_call
                and not contradiccion
                and not alucinacion
                and contiene_salida_modelo
            )

            resultados.append(
                {
                    "id": caso["id"],
                    "tipo": caso["tipo"],
                    "descripcion": caso["descripcion"],
                    "debe_llamar_tool": caso["debe_llamar_tool"],
                    "tool_llamada": fue_llamada,
                    "cumple_tool_call": cumple_tool_call,
                    "contradiccion_modelo_llm": contradiccion,
                    "alucinacion_sin_datos": alucinacion,
                    "respuesta_contiene_salida_modelo": contiene_salida_modelo,
                    "cumple": cumple,
                    "tool_outputs": tool_outputs,
                    "respuesta_final": texto_final,
                }
            )

        except Exception as exc:
            resultados.append(
                {
                    "id": caso["id"],
                    "tipo": caso["tipo"],
                    "descripcion": caso["descripcion"],
                    "error": str(exc),
                    "cumple": False,
                }
            )

    return resultados


def guardar_reporte(resultados: list[dict]) -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    path = LOG_DIR / "agent_validation_report.json"

    payload = {
        "timestamp": datetime.now().isoformat(),
        "total_casos": len(resultados),
        "casos_cumplidos": sum(1 for r in resultados if r.get("cumple")),
        "casos_fallidos": sum(1 for r in resultados if not r.get("cumple")),
        "resultados": resultados,
    }

    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    return path


if __name__ == "__main__":
    resultados = validar_agente()
    path = guardar_reporte(resultados)

    print("\nResumen de validación")
    print("---------------------")

    for r in resultados:
        estado = "Cumple" if r.get("cumple") else "No cumple"
        print(f"{r['id']} - {r['tipo']}: {estado}")

    print(f"\nReporte guardado en: {path}")