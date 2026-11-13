# Registro formal del primer testeo con usuarios reales

> PLANTILLA OFICIAL. Completar durante/después de la sesión real. Los
> datos personales NO aparecen: cada participante se identifica como
> P01, P02, … y la llave de correspondencia se guarda aparte del
> proyecto (resguardo de información personal).

---

## 0. Datos de la sesión

- Fecha y hora: ________
- Lugar: ________
- Moderador: ________
- Versión de la app probada: ADScope (commits posteriores a Certamen 1; ver `docs/ESTADO_PROYECTO.md`)
- Vínculo funcional de la app: https://loquacious-pudding-382389.netlify.app
  (cortina de acceso estático: `adscope2026`; backend local documentado en el README del proyecto)
- Instrumento digital: `testeo/instrumento.html` (JSON por participante en `testeo/resultados/`)

## 1. Consentimiento informado

**Texto a leer y firmar por cada participante:**

> Acepto participar voluntariamente en una prueba de uso de la aplicación
> ADScope con fines académicos. Entiendo que: (1) no se evaluará mi
> desempeño profesional; (2) mis datos se registrarán de forma
> anonimizada (P01, P02…); (3) no se recopilarán datos personales
> sensibles; (4) puedo retirarme en cualquier momento sin consecuencias;
> (5) los resultados se usarán solo en el contexto del curso y del
> proyecto. La herramienta está en desarrollo y NO es un dispositivo
> médico.

| ID | Firma (o "sí" vía formulario) | Hora inicio | Hora fin |
|---|---|---|---|
| P01 | | | |
| P02 | | | |
| P03 | | | |
| P04 | | | |
| P05 | | | |

## 2. Condiciones de realización (checklist)

- [ ] Mismo equipo y versión de la app para todos
- [ ] Orden de casos aleatorizado por participante
- [ ] Sin ayuda durante la tarea
- [ ] Participantes declararon no haber usado ADScope antes
- [ ] Se declaró a los participantes que la app está en desarrollo

## 3. Instrumento cuantitativo — planilla de tarea

| Participante | Caso (clase real oculta al usuario) | Tiempo (s) | Diagnóstico elegido | ¿Confirmó IA? (sí/no) | ¿Acertó? |
|---|---|---|---|---|---|
| P01 | benigno | | | | |
| P01 | adenocarcinoma | | | | |
| P01 | escamoso | | | | |
| P02 | … | | | | |
| … | | | | | |

## 4. Instrumento cuantitativo — encuesta Likert (1 = muy en desacuerdo, 5 = muy de acuerdo)

| Ítem | P01 | P02 | P03 | P04 | P05 |
|---|---|---|---|---|---|
| El heatmap me ayudó a localizar la zona relevante | | | | | |
| Los 5 focos guiaron mi revisión | | | | | |
| Entendí qué significaban los colores del heatmap | | | | | |
| Confié en mi decisión final | | | | | |
| Usaría la herramienta como apoyo en mi formación | | | | | |

**Preguntas abiertas** (transcribir por participante):
1. ¿Qué fue lo más difícil de usar?
2. ¿Qué mejorarías primero?

## 5. Instrumento cualitativo — pauta de observación del moderador

Por participante, registrar: dudas verbales, clics erróneos, zonas de la
pantalla que ignoró, momento en que miró el heatmap vs la imagen, y
cualquier comentario espontáneo.

## 6. Datos recopilados (resumen)

- Participantes válidos: ___ (se excluyen los que no completaron)
- Tiempo promedio por caso: ___ s (rango ___–___)
- Acierto global: ___ / ___
- Concordancia con la sugerencia de la IA: ___ %
- Promedios Likert por ítem: (completar tabla)

## 7. Evidencia de la experiencia

- [ ] Planillas y encuestas escaneadas/fotografiadas (anónimas)
- [ ] Capturas de pantalla de la app durante la prueba
- [ ] Registro de auditoría de ADScope (etiquetas generadas, con hora)
- [ ] Notas del moderador

## 8. Hallazgos principales

1. ____________
2. ____________
3. ____________

## 9. Dificultades identificadas

| Dificultad | Frecuencia | Causa probable |
|---|---|---|
| | | |

## 10. Análisis preliminar y mejoras proyectadas

| Hallazgo | Mejora proyectada | Prioridad |
|---|---|---|
| | | |

---

## Anexo A — Casos usados en la prueba

| Caso | Clase real | Archivo fuente (subconjunto) |
|---|---|---|
| 1 | benigno | `dataset/lung_benigno/lung_benigno_000.jpg` |
| 2 | adenocarcinoma | `dataset/lung_adeno/lung_adeno_000.jpg` |
| 3 | escamoso | `dataset/lung_escamoso/lung_escamoso_000.jpg` |
