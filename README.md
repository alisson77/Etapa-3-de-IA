# Integración del agente con LangChain y Ollama

Este módulo corresponde a la integración local del modelo predictivo dentro de un agente inteligente construido con LangChain y Ollama. El modelo fue desarrollado previamente en un notebook ejecutado en Google Colab, donde se realizó el entrenamiento, la evaluación, la optimización y la serialización de los artefactos necesarios para su uso posterior.

La implementación local separa la lógica conversacional del agente y la lógica predictiva del modelo. De esta manera, el agente no realiza predicciones por sí mismo, sino que consume el modelo serializado mediante una herramienta estructurada de LangChain.

## Estructura del proyecto

```text
Etapa-3-de-IA/
│
├── app/
│   ├── config.py              # Configuración de rutas, modelo Ollama y variables de entorno
│   ├── schemas.py             # Definición del schema de entrada con los 14 campos requeridos
│   ├── predictor.py           # Carga los artefactos serializados y ejecuta el modelo predictivo
│   ├── tools.py               # Define la herramienta LangChain predecir_riesgo_estudiante
│   ├── prompts.py             # Contiene el prompt del sistema del agente
│   ├── agent.py               # Crea el LLM local y el agente con acceso a la herramienta
│   ├── main.py                # Permite interactuar con el agente desde consola
│   ├── check_predictor.py     # Verifica la carga y ejecución directa del modelo
│   └── check_tool.py          # Verifica la ejecución directa de la herramienta LangChain
│
├── models/                    # Carpeta donde se ubican los artefactos .joblib del modelo
├── logs/                      # Carpeta donde se guarda evidencia de ejecución del agente
├── scripts/
├── requirements.txt
└── .env.example
```

## Artefactos del modelo

El modelo predictivo fue entrenado y serializado desde un notebook en Google Colab. Como resultado, se generaron los siguientes archivos:

```text
model_artifacts/preprocessor.joblib
model_artifacts/label_encoder.joblib
model_artifacts/logreg_optimized.joblib
model_artifacts/metadata.joblib
```

Estos artefactos permiten reproducir el mismo flujo de predicción utilizado durante el entrenamiento. El preprocesador transforma las variables de entrada, el codificador interpreta las clases del modelo, el archivo del modelo contiene la regresión logística optimizada y los metadatos almacenan información auxiliar sobre las variables utilizadas.

En la implementación local, estos archivos se ubican en:

```text
Etapa-3-de-IA/models/
```

La carpeta `models/` debe contener los siguientes archivos para que el agente pueda ejecutar predicciones correctamente:

```text
preprocessor.joblib
label_encoder.joblib
logreg_optimized.joblib
metadata.joblib
```

## Entorno local

El proyecto utiliza un entorno virtual de Python para mantener aisladas las dependencias necesarias. Las principales librerías utilizadas son LangChain, LangChain Ollama, pandas, scikit-learn, joblib y pydantic.

La ejecución puede realizarse tanto en Windows como en macOS, siempre que Python y Ollama estén instalados correctamente en el sistema.

## Ejecución en Windows

Desde PowerShell, dentro de la carpeta `Etapa-3-de-IA`, se crea y activa el entorno virtual con los siguientes comandos:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

En caso de que PowerShell bloquee la activación del entorno virtual, se puede habilitar la ejecución de scripts para el usuario actual con:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Posteriormente, se activa nuevamente el entorno virtual:

```powershell
.\venv\Scripts\Activate.ps1
```

Cuando el entorno virtual se encuentra activo, aparece el prefijo `(venv)` al inicio de la línea de comandos.

## Ejecución en macOS

Desde la terminal de macOS, dentro de la carpeta `Etapa-3-de-IA`, se crea y activa el entorno virtual con los siguientes comandos:

```bash
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Cuando el entorno virtual se encuentra activo, aparece el prefijo `(venv)` al inicio de la línea de comandos.

Para salir del entorno virtual, tanto en Windows como en macOS, se utiliza:

```bash
deactivate
```

## Configuración de Ollama

El agente utiliza un modelo local ejecutado mediante Ollama. La configuración del modelo se define en el archivo `.env`, a partir del archivo de ejemplo `.env.example`.

Un ejemplo de configuración es:

```text
OLLAMA_MODEL=qwen3
OLLAMA_BASE_URL=http://localhost:11434
TEMPERATURE=0
```

El modelo disponible en Ollama puede verificarse con el siguiente comando, tanto en Windows como en macOS:

```bash
ollama list
```

En caso de que el modelo no se encuentre instalado, puede descargarse con:

```bash
ollama pull qwen3
```

Si se utiliza otro modelo local, el nombre definido en `OLLAMA_MODEL` debe coincidir exactamente con el nombre mostrado por `ollama list`.

## Verificación del modelo predictivo

El archivo `check_predictor.py` permite comprobar que los artefactos `.joblib` se cargan correctamente y que el modelo puede generar una predicción sin intervención del agente conversacional.

La ejecución se realiza con:

```bash
python -m app.check_predictor
```

Esta verificación confirma que el pipeline serializado puede recibir nuevos datos de entrada, aplicar el preprocesamiento correspondiente y devolver la clase predicha junto con las probabilidades asociadas.

## Verificación de la herramienta LangChain

El archivo `check_tool.py` permite probar la herramienta `predecir_riesgo_estudiante` de forma aislada. Esta herramienta encapsula el modelo predictivo y lo expone como una función consumible por el agente.

La ejecución se realiza con:

```bash
python -m app.check_tool
```

Cuando esta prueba funciona correctamente, se confirma que existe una conexión funcional entre el modelo serializado y la herramienta de LangChain.

## Ejecución del agente

El archivo `main.py` permite ejecutar el agente desde consola. En este flujo, el usuario ingresa los datos de un estudiante, el agente interpreta la solicitud, invoca la herramienta de predicción y genera una respuesta final con la clase predicha, la probabilidad de riesgo, una interpretación y una advertencia ética.

La ejecución se realiza con:

```bash
python -m app.main
```

Un ejemplo de consulta válida es:

```text
Evalúa un estudiante con Hours_Studied 12, Attendance 78, Previous_Scores 65, Tutoring_Sessions 1, Teacher_Quality Medium, Family_Income Low, Access_to_Resources Medium, Internet_Access Yes, Distance_from_Home Moderate, Motivation_Level Medium, Parental_Involvement Low, Peer_Influence Neutral, Learning_Disabilities No y Sleep_Hours 6.
```

## Evidencia generada

Durante la ejecución del agente se generan registros en formato JSON dentro de la carpeta:

```text
logs/
```

Estos registros permiten documentar la interacción del usuario con el agente y sirven como evidencia de la integración. Para efectos de validación, se consideran especialmente relevantes los siguientes casos:

1. Ejecución directa del modelo mediante `check_predictor.py`.
2. Ejecución directa de la herramienta mediante `check_tool.py`.
3. Ejecución del agente mediante `main.py`.
4. Caso completo donde el agente invoca la herramienta de predicción.
5. Caso incompleto donde el agente solicita los datos faltantes.
6. Caso donde el usuario intenta forzar una contradicción y el agente mantiene la salida generada por el modelo.

## Descripción de la integración

La integración del agente se implementó mediante LangChain y Ollama, separando la capacidad conversacional del LLM de la lógica predictiva del modelo supervisado. El agente no realiza predicciones directamente; cuando el usuario solicita evaluar un estudiante, invoca la herramienta `predecir_riesgo_estudiante`, la cual carga el pipeline serializado desde los artefactos generados en Google Colab.

La respuesta final del agente se construye a partir de la clase y las probabilidades devueltas por el modelo. Además, se incluye una interpretación del resultado, una recomendación de apoyo académico y una advertencia ética para evitar que la predicción sea utilizada como una decisión automática única.

## Consideraciones de reproducibilidad

El proyecto incluye un archivo `requirements.txt` con las dependencias necesarias para ejecutar el agente localmente. Además, el uso de archivos `.joblib` permite reutilizar el mismo pipeline entrenado en Google Colab sin volver a ejecutar el proceso de entrenamiento.

Para reproducir correctamente la integración, se deben considerar los siguientes elementos:

```text
1. Tener Python instalado.
2. Tener Ollama instalado y en ejecución.
3. Contar con un modelo local disponible en Ollama.
4. Instalar las dependencias del archivo requirements.txt.
5. Ubicar los artefactos .joblib dentro de la carpeta models/.
6. Ejecutar las pruebas check_predictor.py y check_tool.py antes de usar el agente.
```

## Archivos no versionados

Por razones de tamaño, configuración local y privacidad, algunos archivos no deberían incluirse directamente en el repositorio:

```text
venv/
.env
logs/
models/*.joblib
```

Los artefactos `.joblib` pueden generarse desde el notebook en Google Colab o compartirse por separado cuando sea necesario reproducir la ejecución local del agente.


## Autores
| Nombre  | Carné | Github |
|------|--------|--------|
| Jorge Luis Rodriguez Cruz | 2020010773 | [@JorgeLuisRodriguezCruz](https://github.com/JorgeLuisRodriguezCruz) |
| Alisson Carrillo Selva | 2021032663 | [@alisson77](https://github.com/alisson77) |
| Dayana Xie Li | 2022097967 | [@dayanaxie](https://github.com/dayanaxie) |
