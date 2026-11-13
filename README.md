# Certamen 2 — ADScope (entorno aislado del proyecto)

Carpeta independiente para el Certamen 2. **No toca la herramienta ADScope**
(`app/`, `web/`, `data/`): solo reutiliza su código de forma read-only.

## Estructura

```
certamen2/
├── descargar_dataset.py        ← extrae el subconjunto desde los shards parquet
├── dataset/                    ← 120 imágenes reales de pulmón (40/clase) + manifest.csv
│   └── shard0.parquet · shard1.parquet   (fuente cruda, ~760 MB — NO versionar)
├── eda/
│   ├── analisis_eda.py         ← análisis exploratorio (DEO/EDA)
│   ├── eda_stats.json          ← estadísticas calculadas
│   └── graficos/               ← balance, histogramas RGB, brillo/contraste, montajes
├── evaluacion/
│   ├── evaluar_modelo.py       ← entrena la cabeza ADScope con datos reales (aislado)
│   ├── resultados.json         ← exactitud 96.7% (n=30) + métricas por clase
│   ├── embeddings/             ← caché AISLADO (no toca data/ de la app)
│   ├── model/                  ← head entrenado del certamen (aislado)
│   └── graficos/matriz_confusion.png
├── documentos/
│   ├── EVOLUCION_APP.md        ← mejoras desde el Certamen 1 + justificación
│   ├── ANALISIS_DEO.md         ← EDA completo + mejoras derivadas
│   ├── DATASET.md              ← origen, variables, criterios, limitaciones
│   ├── PROTOCOLO_TESTEO.md     ← cadena pregunta→objetivo→…→mejoras
│   ├── REGISTRO_TESTEO.md      ← PLANTILLA del registro formal (completar)
│   └── CONCLUSIONES.md         ← conclusiones preliminares + mejoras proyectadas
├── testeo/
│   ├── GUIA_TESTEO.md          ← cómo correr la sesión de testeo real
│   ├── instrumento.html        ← instrumento digital (consentimiento, cronómetro,
│   │                              planilla, Likert, exporta JSON — offline)
│   └── resultados/             ← JSON por participante (NO versionar)
├── netlify/                    ← copia del paquete estático desplegado
└── presentacion/
    ├── generar_pptx.py         ← regenera la presentación
    └── Certamen2_ADScope.pptx  ← 11 diapositivas listas
```

## Vínculo funcional (entregable)

- **Aplicación (interfaz estática en Netlify):**
  https://loquacious-pudding-382389.netlify.app
  · cortina de acceso: `adscope2026`
- **Aplicación completa (con IA real):** backend FastAPI local — ver
  `README.md` del proyecto ADScope (uvicorn + Docker). El paquete estático
  está documentado en `netlify/LEEME_NETLIFY.txt` (honestidad: Netlify solo
  sirve la interfaz; la IA corre en el backend).

## Resultados clave (evidencia real)

- **EDA:** balance 40/40/40 · tumores más oscuros (escamoso 164.4 vs
  benigno 185.6 de brillo medio) · tinción H&E bimodal.
- **Modelación:** exactitud de test **96.7% (n=30)** con F1 ≥ 0.95/clase;
  una confusión escamoso→adeno. *(Interpretación honesta en DATASET.md:
  backbone placeholder + riesgo de fuga por aumentación.)*

## Reproducir todo

```bash
cd certamen2
../.venv/bin/python descargar_dataset.py 40      # ya ejecutado (shards descargados)
../.venv/bin/python eda/analisis_eda.py          # regenera gráficos + stats
../.venv/bin/python evaluacion/evaluar_modelo.py # re-entrena y re-evalúa (aislado)
../.venv/bin/python presentacion/generar_pptx.py # regenera el PPTX
```

## Correr el testeo con usuarios

1. Abre `testeo/GUIA_TESTEO.md` y sigue sus 3 fases (preparación, sesión, cierre).
2. El instrumento `testeo/instrumento.html` se abre con doble clic (offline).
3. Cada participante exporta su JSON a `testeo/resultados/`.
4. Con los JSON se completan `documentos/REGISTRO_TESTEO.md` y los espacios
   de `documentos/CONCLUSIONES.md`.

## Pendientes tuyos (no automatizables)

1. **Realizar el testeo real** con 3–5 compañeros usando el instrumento y
   completar `documentos/REGISTRO_TESTEO.md` (planillas, Likert, observaciones).
2. Completar los espacios `___` de `CONCLUSIONES.md` con los datos del testeo.
