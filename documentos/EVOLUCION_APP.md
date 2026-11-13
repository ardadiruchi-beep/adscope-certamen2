# Evolución de la aplicación desde el Certamen 1

Documento que sustenta la dimensión "Evolución de la aplicación":
qué se implementó, por qué (con base en el análisis exploratorio de
datos) y qué aporta a la pertinencia, funcionamiento y potencial de la
herramienta.

## 1. De dónde partimos (Certamen 1)

En el Certamen 1 la aplicación era un **prototipo HTML de una sola
página**: interfaz simulada, heatmaps dibujados a mano (círculos fijos),
sin modelo real, sin datos persistentes (localStorage), sin usuarios.

## 2. Qué se implementó después (evolución)

| Área | Mejora implementada | Pertinencia / funcionamiento / potencial |
|---|---|---|
| **IA real** | Backbone ViT + Grad-CAM real sobre píxeles; heatmaps y 5 focos calculados, no dibujados | La explicación ya sale del modelo, no de un dibujo: credibilidad ante el usuario |
| **Aprendizaje** | Human-in-the-loop: confirmar/corregir → dataset → cabeza lineal re-entrenable | La herramienta aprende del criterio de quien la usa (propuesta de valor central) |
| **WSI** | Lectura de láminas completas (.svs/.ndpi/TIFF piramidal), tiling 256 px a ~20× desde µm/px, MIL con atención (CLAM-lite), visor piramidal | Pasa de "fotos sueltas" a láminas digitales reales (escenario clínico) |
| **Evaluación honesta** | Split estratificado + exactitud/precisión/sensibilidad/F1 + aviso de sobreajuste | Los resultados se pueden defender metodológicamente (dimensión "generar evidencia") |
| **Datos** | SQLite multi-usuario (migración automática) + cachés de análisis/embeddings | Persistencia real, re-análisis instantáneo, soporta volumen |
| **Seguridad** | Login con roles (admin/patólogo), cookies de sesión, PBKDF2, auditoría de acciones, `.env` no versionado | Requisito mínimo para acercarse a datos reales de pacientes |
| **Experiencia** | Worklist con miniaturas, landing de login, panel de evaluación, estado del modelo | Reduce fricción del primer uso (relevante para el testeo) |
| **Despliegue** | Dockerfile + docker-compose (libopenslide) y paquete estático Netlify con pantalla de acceso | La app queda disponible en un vínculo funcional (exigencia de la rúbrica) |
| **Ingesta de láminas grandes** | Guardado por streaming + `POST /api/ingest` por ruta del servidor + guardia de RAM | Soporta archivos de GB sin tumbar el equipo |

## 3. Vínculo con el análisis exploratorio de datos

Las mejoras de visualización (umbral por percentil), evaluación
(estratificación, métricas por clase) y WSI (tiling) se decidieron o
reforzaron a partir del EDA del dataset real (ver `ANALISIS_DEO.md`).

## 4. Evidencia funcional

- Modelación con datos reales: **96.7% de exactitud en test (n=30)** con
  la cabeza entrenada sobre LC25000-pulmón (`evaluacion/resultados.json`).
- Seguridad y flujos verificados de punta a punta en `docs/ESTADO_PROYECTO.md` (raíz del proyecto).
