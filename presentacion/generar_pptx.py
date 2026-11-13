#!/usr/bin/env python3
"""Genera la presentación PPTX del Certamen 2 (ADScope).

Uso: ../.venv/bin/python presentacion/generar_pptx.py
Salida: presentacion/Certamen2_ADScope.pptx
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

BASE = Path(__file__).resolve().parent.parent
GRAF_EDA = BASE / "eda" / "graficos"
GRAF_EV = BASE / "evaluacion" / "graficos"
OUT = BASE / "presentacion" / "Certamen2_ADScope.pptx"

NAVY = RGBColor(0x12, 0x1F, 0x33)
NAVY2 = RGBColor(0x1B, 0x2E, 0x4B)
BLUE = RGBColor(0x4B, 0x7D, 0xA3)
LBLUE = RGBColor(0x93, 0xAC, 0xC2)
INDIGO = RGBColor(0x36, 0x35, 0x6F)
GREEN = RGBColor(0x38, 0xA1, 0x69)
AMBER = RGBColor(0xD6, 0x9E, 0x2E)
RED = RGBColor(0xE5, 0x3E, 0x3E)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREY = RGBColor(0x71, 0x80, 0x96)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def slide():
    return prs.slides.add_slide(BLANK)


def bg(s, color=NAVY):
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = color


def text(s, x, y, w, h, t, size=18, color=WHITE, bold=False, align=PP_ALIGN.LEFT, italic=False):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = t
    p.alignment = align
    for r in p.runs:
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
        r.font.name = "Calibri"
        r.font.italic = italic
    return tb


def kicker(s, t):
    text(s, 0.8, 0.45, 8, 0.4, t, size=13, color=BLUE, bold=True)


def title(s, t):
    text(s, 0.8, 0.85, 11.5, 0.8, t, size=30, color=WHITE, bold=True)


def bullets(s, x, y, w, h, items, size=15, gap=6):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    first = True
    for it in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        if isinstance(it, tuple):
            r = p.add_run(); r.text = "▸ "; r.font.color.rgb = BLUE; r.font.size = Pt(size); r.font.bold = True
            r = p.add_run(); r.text = it[0]
            r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = "Calibri"
            r = p.add_run(); r.text = " — " + it[1]
            r.font.size = Pt(size - 2); r.font.color.rgb = GREY; r.font.name = "Calibri"
        else:
            r = p.add_run(); r.text = "▸ "; r.font.color.rgb = BLUE; r.font.size = Pt(size); r.font.bold = True
            r = p.add_run(); r.text = it
            r.font.size = Pt(size); r.font.color.rgb = WHITE; r.font.name = "Calibri"
        p.space_after = Pt(gap)
    return tb


def footer(s, n):
    text(s, 0.8, 7.05, 6, 0.4, "Certamen 2 · ADScope", size=10, color=GREY)
    text(s, 11.5, 7.05, 1.2, 0.4, str(n), size=10, color=GREY, align=PP_ALIGN.RIGHT)


def pic(s, path, x, y, w=None, h=None):
    if not Path(path).is_file():
        return
    if w:
        s.shapes.add_picture(str(path), Inches(x), Inches(y), width=Inches(w))
    else:
        s.shapes.add_picture(str(path), Inches(x), Inches(y), height=Inches(h))


# ============ 1. PORTADA ============
s = slide(); bg(s)
pic(s, BASE.parent / "web" / "logo.jpg", 0.8, 1.0, w=2.4)
text(s, 0.8, 2.3, 11, 1.2, "ADScope", size=54, color=WHITE, bold=True)
text(s, 0.8, 3.5, 11, 0.6, "Certamen 2 · Evolución de la investigación y de la aplicación",
     size=22, color=LBLUE)
text(s, 0.8, 4.15, 11, 0.5, "Análisis exploratorio de datos · modelación con datos reales · primer testeo con usuarios",
     size=16, color=GREY, italic=True)
text(s, 0.8, 5.4, 11, 0.5, "Tecnólogo Médico en formación · Morfofisiopatología y Citodiagnóstico",
     size=14, color=WHITE)
text(s, 0.8, 5.9, 11, 0.5, "Viernes 16 de octubre de 2026", size=13, color=GREY)
footer(s, 1)

# ============ 2. PREGUNTA Y OBJETIVO ============
s = slide(); bg(s)
kicker(s, "INVESTIGACIÓN")
title(s, "Pregunta de investigación y objetivo del testeo")
text(s, 0.8, 1.9, 11.7, 1.5,
     "¿Una herramienta de IA explicable (heatmap + 5 focos de atención) reduce el tiempo de "
     "revisión de imágenes histológicas y aumenta la confianza del revisor, sin sustituir su "
     "criterio, en usuarios sin entrenamiento previo en la herramienta?",
     size=20, color=WHITE, bold=True)
bullets(s, 0.8, 3.8, 11.7, 2.4, [
    ("Objetivo del testeo", "observar el primer uso real por pares: tiempos y concordancia (cuantitativo) + percepciones y dificultades (cualitativo)"),
    ("Objetivo de la entrega", "una primera aproximación empírica: hallazgos + decisiones de desarrollo fundamentadas, no una validación definitiva"),
    ("Alcance declarado", "sin pretensión de validez clínica; la herramienta es un instrumento académico en desarrollo"),
], size=16)
footer(s, 2)

# ============ 3. EVOLUCIÓN DE LA APP ============
s = slide(); bg(s)
kicker(s, "EVOLUCIÓN DE LA APLICACIÓN")
title(s, "Del prototipo HTML a una estación de trabajo real")
bullets(s, 0.8, 1.85, 11.7, 4.8, [
    ("IA real", "backbone ViT + Grad-CAM sobre píxeles; heatmaps y 5 focos calculados, no dibujados"),
    ("Aprendizaje human-in-the-loop", "confirmar/corregir → dataset → cabeza re-entrenable"),
    ("Láminas completas (WSI)", "tiling a ~20× (µm/px), MIL con atención (CLAM-lite), visor piramidal"),
    ("Evaluación honesta", "split estratificado + exactitud/precisión/sensibilidad/F1 + aviso de sobreajuste"),
    ("Datos y seguridad", "SQLite multi-usuario, login con roles, auditoría de acciones, .env no versionado"),
    ("Experiencia y despliegue", "worklist con miniaturas, landing de login, Docker y paquete Netlify"),
], size=15)
text(s, 0.8, 6.55, 11.7, 0.5, "Cada mejora quedó justificada por datos (ver análisis DEO) y verificada de punta a punta.",
     size=13, color=LBLUE, italic=True)
footer(s, 3)

# ============ 4. EDA 1 ============
s = slide(); bg(s)
kicker(s, "ANÁLISIS DEO · EDA")
title(s, "Exploración del dataset: balance y tinción")
pic(s, GRAF_EDA / "balance_clases.png", 0.7, 2.0, w=5.6)
pic(s, GRAF_EDA / "histogramas_rgb.png", 6.9, 2.0, w=6.0)
bullets(s, 0.8, 5.7, 11.7, 1.3, [
    ("Balance 40/40/40", "sin necesidad de rebalanceo; justifica el split estratificado"),
    ("Tinción H&E bimodal", "fondo claro + hematoxilina oscura; el pico oscuro varía entre clases → señal morfológica presente"),
], size=14)
footer(s, 4)

# ============ 5. EDA 2 ============
s = slide(); bg(s)
kicker(s, "ANÁLISIS DEO · EDA")
title(s, "Brillo/contraste y muestras del dataset")
pic(s, GRAF_EDA / "brillo_contraste.png", 0.7, 1.9, w=5.2)
pic(s, GRAF_EDA / "montajes.png", 6.4, 1.9, h=4.6)
text(s, 0.8, 5.4, 5.4, 1.4,
     "Los tumores son más oscuros (escamoso 164.4 vs benigno 185.6): mayor densidad celular. "
     "Hallazgo coherente con la histología y alerta de sesgo de tinción entre laboratorios.",
     size=13, color=WHITE)
footer(s, 5)

# ============ 6. DATASET ============
s = slide(); bg(s)
kicker(s, "MODELACIÓN MEDIANTE DATOS")
title(s, "Dataset: LC25000 (pulmón) — origen y criterios")
bullets(s, 0.8, 1.85, 11.7, 3.6, [
    ("Origen", "Borkowski et al. 2019 (arXiv:1912.12142); espejo HuggingFace 1aurent/LC25000 · licencia UNLICENSE"),
    ("Subconjunto", "120 imágenes reales de pulmón: 40 benignas, 40 adenocarcinoma, 40 escamosas · JPEG 768×768"),
    ("Criterios de selección", "solo pulmón (dominio de la app); 40/clase para split con test informativo; selección determinística registrada en manifest.csv"),
    ("Condiciones de borde y limitaciones", "imágenes aumentadas desde 750 originales (riesgo de fuga train/test) · backbone placeholder · muestra pequeña"),
], size=15)
text(s, 0.8, 5.6, 11.7, 1.2,
     "Todo se declara: los datos son reales (no simulados), la licencia permite su uso y las "
     "limitaciones están documentadas en el informe.",
     size=14, color=LBLUE, italic=True)
footer(s, 6)

# ============ 7. RESULTADOS ============
s = slide(); bg(s)
kicker(s, "MODELACIÓN MEDIANTE DATOS")
title(s, "Cabeza de ADScope entrenada con datos reales")
text(s, 0.8, 1.9, 11, 1.0, "Exactitud de test: 96.7% (n=30) · F1 ≥ 0.95 en las tres clases",
     size=28, color=GREEN, bold=True)
pic(s, GRAF_EV / "matriz_confusion.png", 0.8, 3.0, h=3.9)
bullets(s, 7.3, 3.1, 5.6, 3.4, [
    ("Una sola confusión", "escamoso clasificado como adenocarcinoma"),
    ("Interpretación honesta", "evidencia del pipeline, no validez clínica: backbone ImageNet + riesgo de fuga por aumentación"),
    ("Reproducible", "script con split estratificado seed 42 y caché de embeddings aislado"),
], size=15)
footer(s, 7)

# ============ 8. PROTOCOLO ============
s = slide(); bg(s)
kicker(s, "PREPARACIÓN DEL TESTEO")
title(s, "Protocolo: de la pregunta a la evidencia")
bullets(s, 0.8, 1.85, 11.7, 4.9, [
    ("Participantes", "3–5 compañeros de curso (formación en histología, sin experiencia con ADScope), anonimizados P01…P05, con consentimiento informado"),
    ("Actividades", "instrucciones mínimas (2 min) → revisar 3 casos reales sin etiqueta → confirmar/corregir → encuesta Likert + preguntas abiertas"),
    ("Condiciones", "mismo equipo y versión, orden aleatorizado, sin ayuda durante la tarea, ~15 min por participante"),
    ("Indicadores cuantitativos", "tiempo por caso, acierto, concordancia con la IA, puntajes Likert 1–5"),
    ("Indicadores cualitativos", "dificultades observadas, comentarios libres, errores de interacción"),
    ("Instrumentos", "ficha de consentimiento · planilla de tarea · encuesta Likert · pauta de observación"),
], size=14)
footer(s, 8)

# ============ 9. REGISTRO ============
s = slide(); bg(s)
kicker(s, "PRIMER TESTEO CON USUARIOS")
title(s, "Registro formal del testeo")
bullets(s, 0.8, 1.85, 11.7, 4.9, [
    ("Identificación anonimizada", "P01…P05 con llave guardada aparte (resguardo de datos personales)"),
    ("Consentimiento", "texto explícito: voluntario, anónimo, revocable, sin evaluación de desempeño"),
    ("Evidencia", "planillas, encuestas, capturas sin datos personales, bitácora de auditoría de la app"),
    ("Registro", "condiciones, mediciones (tiempos, aciertos, Likert), observaciones y dificultades"),
    ("Análisis preliminar", "descriptivos + categorización de comentarios → mejoras proyectadas priorizadas"),
], size=15)
text(s, 0.8, 6.4, 11.7, 0.6,
     "Completar tras la sesión real: el documento REGISTRO_TESTEO.md es la plantilla oficial.",
     size=13, color=AMBER, italic=True)
footer(s, 9)

# ============ 10. CONCLUSIONES ============
s = slide(); bg(s)
kicker(s, "CONCLUSIONES PRELIMINARES")
title(s, "Hallazgos y mejoras proyectadas")
bullets(s, 0.8, 1.85, 11.7, 3.4, [
    ("El pipeline funciona y es medible", "96.7% test sobre datos reales; EDA reproducible; testeo con métricas cuali-cuantitativas"),
    ("La honestidad metodológica es parte del resultado", "placeholder, fuga potencial y muestra pequeña declarados explícitamente"),
    ("Testeo separa problemas de interfaz vs de modelo", "los hallazgos de usuarios priorizan el desarrollo"),
], size=15)
text(s, 0.8, 5.2, 11.7, 0.5, "Mejoras proyectadas (priorizadas):", size=16, color=LBLUE, bold=True)
bullets(s, 0.8, 5.7, 11.7, 1.4, [
    ("1", "backbone real de patología (UNI 2 / Virchow 2)"),
    ("2", "mitigar fuga del dataset (split por tejido original)"),
    ("3", "normalización de tinción + iteración de interfaz según testeo"),
    ("4", "ampliar a 200+ imágenes y preparar LIS/PACS"),
], size=13)
footer(s, 10)

# ============ 11. CIERRE ============
s = slide(); bg(s)
kicker(s, "ENTREGA")
title(s, "Vínculo funcional y entregables")
bullets(s, 0.8, 1.9, 11.7, 3.2, [
    ("Aplicación actualizada", "vínculo Netlify de la interfaz + backend documentado (Docker/Render)"),
    ("Análisis DEO", "EDA completo con gráficos y mejoras derivadas"),
    ("Dataset documentado", "origen, variables, criterios, condiciones de borde y limitaciones"),
    ("Protocolo + registro", "cadena pregunta→evidencia y plantilla formal del primer testeo"),
    ("Conclusiones", "preliminares, fundamentadas en datos y experiencia"),
], size=15)
text(s, 0.8, 5.5, 11.7, 0.8, "“La IA explica, el humano decide, los datos fundamentan.”", size=18, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
text(s, 0.8, 6.3, 11.7, 0.5, "ADScope · Certamen 2 · octubre 2026", size=13, color=GREY, align=PP_ALIGN.CENTER)
footer(s, 11)

prs.save(OUT)
print("OK ->", OUT, "· slides:", len(prs.slides._sldIdLst))
