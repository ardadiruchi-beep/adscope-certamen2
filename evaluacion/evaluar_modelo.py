#!/usr/bin/env python3
"""Modelación mediante datos: entrena la cabeza de ADScope con el subconjunto
real LC25000-pulmón y reporta métricas honestas.

AISLAMIENTO: usa códigos de la app (read-only) pero con cachés y modelo
propios en certamen2/evaluacion/ — NO toca data/ ni el servidor de la app.

Flujo: embeddings ViT (caché) → split estratificado 75/25 → cabeza lineal
(3 clases) → exactitud, precisión, sensibilidad, F1, matriz de confusión.

Uso: ../.venv/bin/python evaluacion/evaluar_modelo.py
"""

import json
import sys
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))  # raíz del proyecto
from app.foundation import CLASSES, ViTExtractor  # noqa: E402

BASE = Path(__file__).resolve().parent
DATA = BASE.parent / "dataset"
CACHE = BASE / "embeddings"          # caché AISLADO del certamen
GRAF = BASE / "graficos"
GRAF.mkdir(parents=True, exist_ok=True)

MAPEO = {
    "lung_adeno": "Adenocarcinoma",
    "lung_escamoso": "Carcinoma escamoso",
    "lung_benigno": "Tejido normal",
}


def main():
    t0 = time.time()
    print("Creando extractor ViT (placeholder ImageNet) con caché aislado…")
    ex = ViTExtractor(cache_dir=str(CACHE))
    ex.load_head()  # carga SOLO el head del certamen si existe (no el de la app)

    samples = []
    for carpeta, clase in MAPEO.items():
        for f in sorted((DATA / carpeta).glob("*.jpg")):
            samples.append((f.read_bytes(), clase))
    print(f"{len(samples)} imágenes reales de pulmón cargadas")

    resultado = ex.retrain(samples, epochs=300)
    resultado["tiempo_seg"] = round(time.time() - t0, 1)
    resultado["dataset"] = "LC25000 subconjunto pulmón · 40/40/40"
    resultado["nota"] = ("Backbone placeholder (ImageNet): métricas reales del pipeline, "
                         "no validez clínica del modelo.")

    # matriz de confusión
    ev = resultado.get("evaluacion", {})
    if ev.get("test"):
        cm = np.array(ev["test"]["confusion_matrix"])
        plt.figure(figsize=(5.5, 4.5))
        plt.imshow(cm, cmap="Blues")
        plt.colorbar(label="casos")
        names = ev["test"]["class_names"]
        plt.xticks(range(len(names)), names, rotation=30, ha="right", fontsize=8)
        plt.yticks(range(len(names)), names, fontsize=8)
        plt.title("Matriz de confusión (test, LC25000 pulmón)")
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(j, i, str(cm[i, j]), ha="center", va="center",
                         color="white" if cm[i, j] > cm.max() / 2 else "black")
        plt.ylabel("real")
        plt.xlabel("predicho")
        plt.tight_layout()
        plt.savefig(GRAF / "matriz_confusion.png", dpi=150)
        plt.close()

    with open(BASE / "resultados.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print("→ resultados.json generado")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
