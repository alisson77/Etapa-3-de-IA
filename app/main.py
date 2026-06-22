"""CLI del agente académico local."""

from app.agent import crear_agente, extraer_texto_respuesta
from app.logging_utils import guardar_log


def main() -> None:
    agente = crear_agente()

    print("Agente académico iniciado con Ollama.")
    print("Escribe 'salir' para terminar.\n")

    while True:
        consulta = input("Usuario: ").strip()

        if consulta.lower() in {"salir", "exit", "quit"}:
            print("Listo, cerrando agente.")
            break

        try:
            respuesta = agente.invoke({"messages": [{"role": "user", "content": consulta}]})
            log_path = guardar_log(consulta, respuesta)

            print("\nAgente:")
            print(extraer_texto_respuesta(respuesta))
            print(f"\nLog guardado en: {log_path}\n")

        except Exception as exc:
            print("\nOcurrió un error:")
            print(exc)
            print()


if __name__ == "__main__":
    main()
