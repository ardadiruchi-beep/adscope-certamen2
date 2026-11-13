#!/usr/bin/env python3
"""Análisis de datos exploratorio (EDA / DEO) del subconjunto LC25000-pulmón.

Explora el dataset con métodos de visualización y estadística descriptiva:
- balance de clases
- dimensiones y formato
- distribución de color por canal RGB por clase (tinción H&E)
- brillo y contraste por clase
- montajes de muestra por clase

Salida: eda/graficos/*.png y eda/eda_stats.json
Uso: ../.venv/bin/python eda/analisis_eda.py
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "dataset"
GRAF = BASE / "eda" / "graficos"
GRAF.mkdir(parents=True, exist_ok=True)

CLASES = {"lung_benigno": "Tejido pulmonar benigno",
          "lung_adeno": "Adenocarcinoma",
          "lung_escamoso": "Carcinoma escamoso"}

stats = {"dataset": "LC25000 (subconjunto pulmón)", "n_total": 0, "clases": {}}
medios = {}


def carga_rgb(path):
    img = Image.open(path).convert("RGB")
    arr = np.asarray(img, dtype=np.float32)
    return arr


def main():
    # 1) balance + dimensiones
    balance, dims = {}, {}
    for carpeta, nombre in CLASES.items():
        files = sorted((DATA / carpeta).glob("*.jpg"))
        balance[nombre] = len(files)
        stats["clases"][nombre] = {"n": len(files)}
        for f in files[:5]:
            arr = carga_rgb(f)
            dims[nombre] = (arr.shape[1], arr.shape[0])
        arr = np.stack([carga_rgb(f) for f in files[:20]])  # muestra de 20/clase
        medios[nombre] = arr
        stats["clases"][nombre]["dimensiones"] = f"{arr.shape[2]}×{arr.shape[1]} px"

    stats["n_total"] = sum(balance.values())

    plt.figure(figsize=(6, 3.5))
    plt.bar(balance.keys(), balance.values(), color=["#38a169", "#4b7da3", "#d69e2e"])
    plt.title("Balance de clases (n por clase)")
    plt.ylabel("imágenes")
    plt.tight_layout()
    plt.savefig(GRAF / "balance_clases.png", dpi=150)
    plt.close()

    # 2) distribución de color por canal y clase (tinción)
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.5), sharey=True)
    colores = {"R": "#e53e3e", "G": "#38a169", "B": "#4b7da3"}
    for ax, (nombre, arr) in zip(axes, medios.items()):
        for canal, color in zip("RGB", ("#e53e3e", "#38a169", "#4b7da3")):
            vals = arr[:, :, :, "RGB".index(canal)].ravel()
            ax.hist(vals, bins=60, alpha=0.45, color=color, label=canal, density=True)
        ax.set_title(nombre, fontsize=9)
        ax.set_xlabel("intensidad de píxel (0-255)")
        ax.legend(fontsize=7)
    axes[0].set_ylabel("densidad")
    fig.suptitle("Distribución de intensidad por canal RGB (tinción H&E)")
    plt.tight_layout()
    plt.savefig(GRAF / "histogramas_rgb.png", dpi=150)
    plt.close()

    # 3) brillo y contraste por clase
    plt.figure(figsize=(6, 3.5))
    for nombre, arr in medios.items():
        gris = arr.mean(axis=3)
        brillo = gris.mean()
        contraste = gris.std()
        stats["clases"][nombre]["brillo_medio"] = round(float(brillo), 1)
        stats["clases"][nombre]["contraste_std"] = round(float(contraste), 1)
        plt.scatter(brillo, contraste, s=120, label=nombre)
    plt.title("Brillo medio vs contraste por clase")
    plt.xlabel("brillo medio (0-255)")
    plt.ylabel("contraste (desv. estándar)")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(GRAF / "brillo_contraste.png", dpi=150)
    plt.close()

    # 4) montajes de muestra por clase
    fig, axes = plt.subplots(3, 4, figsize=(11, 8.5))
    for fila, (nombre, arr) in enumerate(medios.items()):
        for col in range(4):
            axes[fila, col].imshow(arr[col].astype(np.uint8))
            axes[fila, col].axis("off")
        axes[fila, 0].set_ylabel(nombre.split(" ")[-1], fontsize=9)
    fig.suptitle("Muestras del dataset LC25000 (pulmón)")
    plt.tight_layout()
    plt.savefig(GRAF / "montajes.png", dpi=130)
    plt.close()

    with open(BASE / "eda" / "eda_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print("EDA completo · gráficos en eda/graficos/ · stats en eda/eda_stats.json")
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
