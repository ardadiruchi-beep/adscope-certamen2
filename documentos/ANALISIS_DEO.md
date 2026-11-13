# Análisis de datos exploratorios (DEO/EDA) y mejoras derivadas

## 1. Qué se exploró

Se aplicó análisis exploratorio sobre el subconjunto LC25000-pulmón
(120 imágenes, 40 por clase) con métodos de visualización y estadística
descriptiva. Script: `eda/analisis_eda.py`. Resultados en
`eda/eda_stats.json` y `eda/graficos/`.

## 2. Hallazgos del EDA

### 2.1 Balance de clases
- 40/40/40 → **dataset balanceado**; no se requieren técnicas de
  rebalanceo. (Gráfico: `balance_clases.png`)

### 2.2 Dimensiones y formato
- Todas 768×768 RGB JPEG. Dimensión homogénea → el preprocesamiento de
  ADScope (redimensionado a 224 y normalización ImageNet) aplica sin
  adaptaciones. Las láminas WSI de la clínica NO son homogéneas: la app
  las maneja con tiling (256 px) — coherente con la arquitectura.

### 2.3 Tinción H&E por canal (gráfico `histogramas_rgb.png`)
- Los tres canales muestran distribuciones bimodales: fondo claro
  (eosina) + tinción oscura (hematoxilina).
- El pico oscuro varía entre clases → la señal morfológica se refleja en
  la distribución de color, lo que valida que el clasificador puede
  apoyarse en la tinción, pero también advierte del riesgo de **sesgo de
  color/tinción** entre laboratorios.

### 2.4 Brillo y contraste por clase (gráfico `brillo_contraste.png`)
| Clase | Brillo medio | Contraste (σ) |
|---|---|---|
| Benigno | 185.6 | 32.3 |
| Adenocarcinoma | 172.7 | 34.3 |
| Carcinoma escamoso | 164.4 | 30.0 |

- Los tumores tienden a ser **más oscuros** (mayor densidad celular y
  hematoxilina) — hallazgo coherente con la histología.

## 3. Mejoras implementadas a partir del EDA

| Hallazgo del EDA | Mejora en la aplicación | Justificación |
|---|---|---|
| Variación de tinción/brillo entre clases y fuentes | Umbral por percentil 75 en los heatmaps + normalización ImageNet del pipeline | Evita que el fondo o la tinción dominen el heatmap; hace los focos comparables entre láminas |
| Clases balanceadas aquí, riesgo de desbalance en la clínica | Split **estratificado** en la evaluación (seed fija) y métricas por clase (F1/sensibilidad) | Un split aleatorio puro con clases minoritarias inflaría o sesgaría las métricas |
| Riesgo de sobreajuste detectable (pocas muestras) | Aviso explícito de sobreajuste si el gap train/test > 15 pp | El panel "Evaluación honesta" muestra el gap en lugar de ocultarlo |
| Fuga de datos por aumentación del dataset (limitación identificada) | Documentada como condición de borde; las métricas se presentan como evidencia de pipeline, no clínica | Honestidad metodológica ante el evaluador |
| Láminas reales heterogéneas (768 px aquí; WSI gigantes en la clínica) | Tiling 256 px + lectura por niveles con µm/px (arquitectura WSI ya implementada) | El mismo clasificador opera sobre tiles extraídos a ~20× |

## 4. Cómo fortalece la herramienta

El EDA convirtió suposiciones en decisiones verificables: justificó el
umbral de los heatmaps, la estratificación de la evaluación, el manejo de
WSI por tiles y la declaración explícita de limitaciones. Es decir, las
mejoras de la aplicación quedan fundamentadas en datos, no en intuición.
