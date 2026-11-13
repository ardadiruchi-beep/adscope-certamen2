# Conclusiones preliminares y proyección de mejoras

## 1. Conclusiones preliminares (fundamentadas en datos y en la experiencia)

### 1.1 Modelación mediante datos (cuantitativo)
- La cabeza lineal de ADScope entrenada sobre 120 imágenes reales de
  pulmón (LC25000, 40/40/40) alcanzó **exactitud de test 96.7% (n=30)**,
  con F1 ≥ 0.95 en las tres clases y una sola confusión (un escamoso
  clasificado como adenocarcinoma). *(evaluacion/resultados.json)*
- **Interpretación honesta:** el pipeline de aprendizaje funciona y es
  reproducible; sin embargo, (a) el backbone es un ViT de ImageNet (no
  entrenado en histología), (b) el dataset está aumentado artificialmente
  (riesgo de fuga entre train/test) y (c) la muestra es pequeña. Por
  tanto, el resultado es **evidencia de funcionamiento del pipeline**, no
  validez clínica.

### 1.2 Análisis exploratorio (DEO/EDA)
- El dataset es balanceado y homogéneo en dimensiones (768×768 RGB), lo
  que valida el preprocesamiento actual.
- Los tumores muestran menor brillo medio (escamoso 164.4 vs benigno
  185.6), coherente con mayor densidad celular y hematoxilina: la señal
  morfológica se refleja en las estadísticas de color, y a la vez se
  identificó el riesgo de sesgo por tinción entre laboratorios.

### 1.3 Testeo con usuarios (completar tras la sesión)
- Tiempo promedio por caso, acierto global y concordancia con la IA: ___.
- Percepción Likert (utilidad del heatmap, claridad de focos, confianza): ___.
- Dificultades recurrentes observadas: ___.

## 2. Hallazgos clave

1. El flujo completo (EDA → modelación → métricas) produce evidencia
   trazable y reproducible.
2. La honestidad metodológica (declarar placeholder, fuga potencial,
   muestra pequeña) es parte del resultado, no un defecto del informe.
3. El primer testeo con usuarios permite separar problemas de interfaz
   de problemas de modelo.

## 3. Mejoras proyectadas (ordenadas por prioridad)

| Prioridad | Mejora | Justificación (dato/observación) |
|---|---|---|
| 1 | Sustituir el backbone por UNI 2 / Virchow 2 (modelos fundacionales de patología) | El ViT de ImageNet no fue entrenado en histología; limitación declarada en DATASET.md |
| 2 | Reducir el riesgo de fuga del dataset (split por tejido original o dataset "limpio") | Limitación de LC25000 documentada en la literatura (MICCAI DEMI 2024) |
| 3 | Normalización de tinción (Macenko/Vahadane) | La variación de brillo/tinción entre clases y fuentes detectada en el EDA |
| 4 | Iterar la interfaz según hallazgos del testeo | Dificultades y comentarios de los usuarios reales (registro) |
| 5 | Ampliar a 200+ imágenes con diagnóstico establecido | El pendiente del proyecto para métricas estadísticamente sólidas |
| 6 | Integración LIS/PACS y despliegue on-premise | Escenario real de uso clínico |

## 4. Coherencia con la pregunta de investigación

La evidencia recopilada responde de forma preliminar a la pregunta:
el pipeline explica visualmente (heatmap/focos), aprende de
confirmaciones/correcciones y es medible (tiempos, acierto, concordancia,
Likert). La validez clínica queda explícitamente fuera del alcance de
esta entrega, como corresponde a una primera aproximación empírica.
