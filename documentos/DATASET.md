# Dataset — origen, variables, criterios y limitaciones

## Identificación

| Campo | Valor |
|---|---|
| **Dataset** | LC25000 — Lung and Colon Histopathological Image Dataset |
| **Referencia** | Borkowski AA, Bui MM, Thomas LB, Wilson CP, DeLand LA, Mastorides SM. *LC25000.* arXiv:1912.12142, 2019 |
| **Fuente usada** | Espejo en Hugging Face: `1aurent/LC25000` (shards parquet 0 y 1) |
| **Licencia** | UNLICENSE (dominio público) |
| **Subconjunto usado** | 120 imágenes de **pulmón**: 40 benignas, 40 adenocarcinoma, 40 carcinoma escamoso |
| **Formato** | JPEG, 768×768 px, color RGB (tinción H&E) |

## Origen y construcción del dataset completo

El dataset original se generó a partir de **750 láminas validadas y
anónimas (cumplimiento HIPAA)**: 250 de tejido pulmonar benigno, 250 de
adenocarcinoma de pulmón y 250 de carcinoma escamoso, digitalizadas y
aumentadas con el paquete *Augmentor* hasta 25.000 imágenes (5.000 por
clase). Nuestro subconjunto toma las primeras 40 imágenes de cada clase
de pulmón desde los shards parquet del espejo.

## Variables

| Variable | Descripción | Tipo |
|---|---|---|
| `image` | Matriz RGB 768×768×3 (la lámina digitalizada) | Imagen |
| `organ` | 0 = pulmón (filtrado), 1 = colon (excluido) | Categórica |
| `label` | 0 = benigno · 1 = adenocarcinoma · 2 = escamoso | Categórica (clase objetivo) |

Mapeo a las 3 clases de ADScope: benigno → *Tejido normal*,
adenocarcinoma → *Adenocarcinoma*, escamoso → *Carcinoma escamoso*.

## Criterios de selección del subconjunto

- **Solo pulmón** (`organ=0`): es el dominio de la herramienta ADScope.
- **40 por clase**: suficiente para un split estratificado con test
  informativo (30 casos de test) y computable en CPU en minutos.
- **Primeras filas de los shards** (criterio determinístico y
  reproducible, declarado en `dataset/manifest.csv` con fila de origen).

## Condiciones de borde

- Las imágenes vienen **aumentadas artificialmente** desde 750 originales:
  dos imágenes de la misma clase pueden ser transformaciones del mismo
  tejido.
- No hay metadatos de paciente ni de magnificación en este espejo.

## Limitaciones (declaradas)

1. **Fuga de datos potencial por aumentación**: el split aleatorio puede
   dejar derivados del mismo tejido original en train y test
   simultáneamente, inflando la exactitud (problema documentado para
   LC25000 en la literatura — MICCAI DEMI 2024). → Las métricas reportadas
   son del **pipeline**, no evidencia clínica.
2. **El backbone es placeholder (ImageNet)**: los embeddings usados no
   fueron entrenados con histología. Que separen bien las clases de
   LC25000 no implica capacidad diagnóstica real.
3. **Subconjunto pequeño (120)**: estimaciones orientativas, no
   estadísticamente concluyentes.

## Uso dentro del proyecto

- EDA: `eda/analisis_eda.py` → estadísticas y gráficos
- Modelación: `evaluacion/evaluar_modelo.py` → entrena la cabeza lineal de
  ADScope en entorno aislado y reporta métricas honestas
- El subconjunto NO se inyecta en la base de datos de la aplicación: la
  separación de entornos evita contaminar la herramienta.
