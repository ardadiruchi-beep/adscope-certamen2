# Protocolo de testeo con usuarios reales

## Cadena del protocolo (según rúbrica)

### 1. Pregunta de investigación
¿Una herramienta de IA explicable (heatmap + 5 focos de atención) reduce
el tiempo de revisión de imágenes histológicas y aumenta la confianza del
revisor, sin sustituir su criterio, en usuarios sin entrenamiento previo
en la herramienta?

### 2. Objetivo del testeo
Observar el **primer uso real** de ADScope por parte de pares: medir
tiempos y concordancia (cuantitativo) y captar percepciones y
dificultades de uso (cualitativo), para identificar hallazgos y priorizar
mejoras. **No** se busca validar precisión diagnóstica clínica.

### 3. Participantes
- **N:** 3–5 compañeros de curso (Tecnología Médica, morfofisiopatología),
  anonimizados como P01…P05 en el registro.
- **Perfil:** usuarios reales con formación básica en histología, sin
  experiencia previa con ADScope → representa al usuario objetivo en
  formación.
- **Consentimiento:** cada participante firma la sección de consentimiento
  del registro antes de la sesión (uso académico, datos anonimizados,
  revocable).

### 4. Actividades (sesión individual de ~15 min por participante)

| # | Actividad | Instrumento |
|---|---|---|
| 1 | Bienvenida + consentimiento informado | Ficha de consentimiento |
| 2 | Instrucciones mínimas (2 min): qué es el heatmap y qué son los focos | Guion estándar |
| 3 | Revisar **3 casos** en ADScope (imágenes reales LC25000 mostradas sin etiqueta) | Cronómetro + planilla |
| 4 | Decidir diagnóstico por caso (confirmar/corregir) | App + planilla de respuestas |
| 5 | Encuesta de percepción (escala Likert 1–5 + preguntas abiertas) | Encuesta post-test |
| 6 | Entrevista breve de dificultades observadas | Pauta de observación |

### 5. Condiciones de prueba
- Mismo equipo (laptop), misma versión de la app, mismo orden de casos
  (aleatorizado por participante), sin ayuda durante la tarea (solo se
  responde al final).
- Ambiente silencioso, iluminación normal, pantalla 13–15".
- Casos: 3 imágenes (1 benigna, 1 adenocarcinoma, 1 escamosa) del
  subconjunto, presentadas **sin diagnóstico visible**.
- Condición de borde: la predicción mostrada es la del clasificador
  entrenado en el certamen (backbone placeholder); se declara a los
  participantes que es una herramienta en desarrollo.

### 6. Indicadores

**Cuantitativos**
- Tiempo de revisión por caso (segundos)
- Acierto del participante por caso (concordancia con el diagnóstico real)
- Concordancia participante ↔ sugerencia de la IA (confirma vs corrige)
- Puntuaciones Likert (utilidad del heatmap, claridad de focos, confianza
  con la herramienta)

**Cualitativos**
- Observaciones de dificultades (grabadas en pauta)
- Comentarios libres en la encuesta
- Errores de interacción detectados

### 7. Instrumentos de registro
1. **Ficha de consentimiento** (anexo A del registro)
2. **Planilla de tarea** (caso, tiempo, diagnóstico elegido, confirmó/corrigió)
3. **Encuesta Likert** (5 ítems, escala 1–5) + 2 preguntas abiertas
4. **Pauta de observación** del moderador

### 8. Evidencia a recolectar
- Planillas completadas por participante (anónimas: P01…)
- Capturas de pantalla (sin datos personales)
- Registro de auditoría de la app (etiquetas con usuario y fecha)
- Encuestas y notas del moderador

### 9. Análisis preliminar
- Estadística descriptiva de tiempos (promedio, rango) por caso y por fase
- Tasa de acierto y de concordancia con la IA
- Promedio y dispersión de cada ítem Likert
- Categorización de comentarios (temas recurrentes)

### 10. Mejoras proyectadas
Las que surjan del análisis; candidatas esperadas: claridad del heatmap
para no expertos, texto de los focos, instrucciones iniciales, y ritmo de
carga del modelo.
