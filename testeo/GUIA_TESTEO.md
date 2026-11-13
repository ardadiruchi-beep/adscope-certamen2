# Guía para correr el testeo (Certamen 2)

Instrumento digital: `testeo/instrumento.html`. Corre 100% offline en la laptop
del moderador; **ningún dato sale del equipo** (exporta JSON por participante).

## Preparación (antes de la sesión)

1. Levanta la app ADScope con el backend real:
   ```bash
   cd ~/Documents/Proyecto
   source .venv/bin/activate
   uvicorn app.main:app --port 8000
   ```
   (alternativa para mostrar solo la interfaz: vínculo Netlify
   https://loquacious-pudding-382389.netlify.app — cortina `adscope2026`).
2. Elige los **3 casos de prueba** (1 benigno, 1 adenocarcinoma, 1 escamoso)
   del subconjunto LC25000 en `dataset/` y tenlos abiertos en ADScope.
3. Abre `testeo/instrumento.html` en el navegador (doble clic).
4. Ten a mano: cronómetro no hace falta (el instrumento lo incluye),
   planilla de observación del moderador (papel o Notas).

## Durante la sesión (por participante, ~15 min)

1. **Consentimiento**: el participante lee el texto y marca la casilla
   (firma digital) + ID (P01…P05). Presiona "Iniciar sesión".
2. **Instrucciones estándar** (leer igual para todos): "En ADScope verás una
   imagen histológica, un heatmap (dónde miró la IA) y 5 focos. Revisa el
   caso a tu ritmo, decide el diagnóstico y di si confirmas o corriges la
   sugerencia de la IA. No hay ayuda durante la tarea."
3. **Tarea**: el participante pulsa "Iniciar revisión" (arranca el
   cronómetro), revisa el caso en ADScope, y al terminar marca diagnóstico
   y confirmó/corrigió. Repite con los 3 casos (el orden está aleatorizado
   por participante).
4. **Encuesta**: 5 ítems Likert (1–5) + 2 preguntas abiertas.
5. **Exportar**: "Descargar JSON" → guardarlo en `testeo/resultados/`
   (nombre sugerido: `P01.json`). Luego "Nueva sesión" para el siguiente.

## Reglas del moderador

- Sin ayuda durante la tarea (solo se responden dudas al final).
- Mismo equipo, misma versión, mismo orden de casos dentro de cada
  participante (aleatorizado por el instrumento).
- Anota en la pauta de observación: errores de interacción, dudas,
  comentarios espontáneos (textuales breves).
- La llave P0X ↔ nombre real se guarda APARTE del repositorio
  (resguardo de información personal).

## Después de la sesión

- Los JSON quedan en `testeo/resultados/` (ignorados por git para no
  exponer datos, aunque son anónimos).
- Con los JSON se completan `documentos/REGISTRO_TESTEO.md` (planilla,
  Likert, observaciones) y los espacios de `documentos/CONCLUSIONES.md`
  (tiempos promedio, aciertos, mejoras).
