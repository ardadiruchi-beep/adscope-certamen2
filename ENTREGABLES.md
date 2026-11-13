# Índice de entregables — Certamen 2 (ADScope)

Mapeo de cada entregable pedido con su ubicación en este repositorio.

| # | Entregable pedido | Dónde está | Estado |
|---|---|---|---|
| 1 | Presentación individual (evolución desde el Certamen 1) | [`presentacion/Certamen2_ADScope.pptx`](presentacion/Certamen2_ADScope.pptx) | ✅ |
| 2 | Aplicación actualizada y funcional con vínculo | https://loquacious-pudding-382389.netlify.app (cortina: `adscope2026`) + paquete en [`netlify/`](netlify/) | ✅ |
| 3 | Análisis EDA con mejoras y justificación | [`documentos/ANALISIS_DEO.md`](documentos/ANALISIS_DEO.md) + [`eda/`](eda/) (script, stats, 4 gráficos) | ✅ |
| 4 | Dataset identificado y documentado | [`documentos/DATASET.md`](documentos/DATASET.md) + [`dataset/`](dataset/) (120 imágenes + manifest) | ✅ |
| 5 | Protocolo de testeo (participantes, actividades, condiciones, indicadores, instrumentos) | [`documentos/PROTOCOLO_TESTEO.md`](documentos/PROTOCOLO_TESTEO.md) | ✅ |
| 6 | Registro formal del primer testeo (evidencia cuanti + cuali) | [`documentos/REGISTRO_TESTEO.md`](documentos/REGISTRO_TESTEO.md) + [`testeo/instrumento.html`](testeo/instrumento.html) | ⏳ plantilla e instrumento listos; se completa al correr la sesión |
| 7 | Conclusiones preliminares y proyección de mejoras | [`documentos/CONCLUSIONES.md`](documentos/CONCLUSIONES.md) | ⏳ redactadas con espacios para los datos del testeo |

## Otros documentos de apoyo

- [`documentos/EVOLUCION_APP.md`](documentos/EVOLUCION_APP.md) — mejoras desde el Certamen 1 y su justificación.
- [`testeo/GUIA_TESTEO.md`](testeo/GUIA_TESTEO.md) — cómo correr la sesión de testeo en 3 fases.
- [`README.md`](README.md) — estructura, resultados clave y reproducción.

## Evaluación (criterios del enunciado)

- **Coherencia entre investigación, EDA, modelación y evidencia**: la cadena
  pregunta de investigación → dataset → EDA → modelación → protocolo → testeo
  está documentada extremo a extremo en [`documentos/PROTOCOLO_TESTEO.md`](documentos/PROTOCOLO_TESTEO.md).
- **Honestidad técnica**: el backbone es un placeholder ImageNet (no
  fine-tuneado con H&E real); la exactitud 96.7% es evidencia del pipeline,
  no validez clínica. Declarado en [`documentos/DATASET.md`](documentos/DATASET.md) y [`documentos/ANALISIS_DEO.md`](documentos/ANALISIS_DEO.md).
- **Resguardo de datos**: participantes anonimizados P01–P05, llave guardada
  aparte, JSONs de testeo fuera del repositorio (`.gitignore`).
