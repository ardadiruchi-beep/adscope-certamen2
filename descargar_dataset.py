#!/usr/bin/env python3
"""Extrae un subconjunto del dataset LC25000 (pulmón) desde el shard parquet.

Fuente: 1aurent/LC25000 en HuggingFace (espejo del dataset original de
Borkowski et al. 2019, arXiv:1912.12142, licencia UNLICENSE / dominio
público). El shard 0 contiene solo imágenes de pulmón (organ=0).

Clases (label):
  0 = benign (tejido pulmonar sano)      → dataset/lung_benigno/
  1 = adenocarcinoma de pulmón           → dataset/lung_adeno/
  2 = carcinoma escamoso de pulmón       → dataset/lung_escamoso/

Uso: ../.venv/bin/python descargar_dataset.py [n_por_clase]
"""

import csv
import sys
from pathlib import Path

import pyarrow.parquet as pq

BASE = Path(__file__).resolve().parent
SHARDS = [
    BASE / "dataset" / "shard0.parquet",  # pulmón: adeno (5000) + benigno (1250)
    BASE / "dataset" / "shard1.parquet",  # pulmón: benigno (3750) + escamoso (2500)
]
OUT = BASE / "dataset"
N_PER_CLASS = int(sys.argv[1]) if len(sys.argv) > 1 else 40

FOLDERS = {0: "lung_benigno", 1: "lung_adeno", 2: "lung_escamoso"}


def main():
    for folder in FOLDERS.values():
        (OUT / folder).mkdir(parents=True, exist_ok=True)

    counts = {k: 0 for k in FOLDERS}
    manifest = []

    for shard in SHARDS:
        if not shard.is_file():
            continue
        table = pq.read_table(shard)
        for i in range(table.num_rows):
            label = int(table["label"][i].as_py())
            if label not in FOLDERS or counts[label] >= N_PER_CLASS:
                continue
            img = table["image"][i].as_py()
            fname = f"{FOLDERS[label]}_{counts[label]:03d}.jpg"
            (OUT / FOLDERS[label] / fname).write_bytes(img["bytes"])
            manifest.append({"archivo": f"{FOLDERS[label]}/{fname}", "clase": FOLDERS[label],
                             "label": label, "shard": shard.name, "fila_origen": i})
            counts[label] += 1
            if all(c >= N_PER_CLASS for c in counts.values()):
                break

    with open(OUT / "manifest.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["archivo", "clase", "label", "shard", "fila_origen"])
        writer.writeheader()
        writer.writerows(manifest)

    print("extraídos:", counts, "· manifest.csv generado")


if __name__ == "__main__":
    main()
