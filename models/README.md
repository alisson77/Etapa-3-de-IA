# Artefactos del modelo predictivo

Esta carpeta contiene los artefactos generados durante el desarrollo del modelo predictivo en un notebook ejecutado en Google Colab. Estos archivos corresponden a los componentes serializados necesarios para que el agente local pueda consumir el modelo previamente entrenado.

Los artefactos generados son:

* `preprocessor.joblib`: contiene el preprocesador utilizado para transformar las variables numéricas y categóricas antes de la predicción.
* `label_encoder.joblib`: almacena la codificación de las clases de la variable objetivo.
* `logreg_optimized.joblib`: corresponde al modelo de regresión logística optimizado.
* `metadata.joblib`: contiene información auxiliar del modelo, como las variables utilizadas, los nombres de características y parámetros relevantes.

Durante el desarrollo en Google Colab, estos archivos fueron generados en la carpeta:

```text
model_artifacts/
```

En la implementación local del agente, estos artefactos se ubican en:

```text
Etapa-3-de-IA/models/
```

De esta forma, el agente puede cargar el pipeline entrenado, aplicar el mismo preprocesamiento utilizado en el notebook y ejecutar predicciones de riesgo académico a partir de nuevos datos de entrada.
