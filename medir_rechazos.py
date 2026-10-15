"""Tarea 7.2 · Vuelve a verificar los textos guardados con y sin las reglas nuevas, y busca falsos positivos.

Uso:  python medir_rechazos.py            (lee resultados/explicaciones.json, que genera main.py)
No regenera los textos: compara las reglas sobre exactamente las mismas explicaciones.
"""
import json
from collections import Counter

from datos import datos_legibles
from predictor import entrenar_predictor, probabilidad_malo
from verificador import explicacion_segura, verificar_explicacion


def motivo(problema):
    """Agrupa cada problema en la regla que lo produjo."""
    if problema.startswith("número"):
        return "números (clase)"
    if problema.startswith("dice que el riesgo") or problema.startswith("afirmación absoluta"):
        return "tono bajo/alto (clase)"
    if problema.startswith("la probabilidad es media"):
        return "tono medio (nueva)"
    return "texto contra datos (nueva)"


registros = json.load(open("resultados/explicaciones.json", encoding="utf-8"))
antes_total = despues_total = 0
motivos_antes, motivos_despues = Counter(), Counter()
print(f"{'Sol.':<5}{'Prob.':>6}  {'Antes':<9}{'Después':<9}Motivos nuevos")
for r in registros:
    antes = verificar_explicacion(r["texto"], r["datos"], r["prob"], reglas_nuevas=False)
    despues = verificar_explicacion(r["texto"], r["datos"], r["prob"])
    antes_total += bool(antes)
    despues_total += bool(despues)
    motivos_antes.update({motivo(p) for p in antes})
    motivos_despues.update({motivo(p) for p in despues})
    nuevos = sorted({motivo(p) for p in despues} - {motivo(p) for p in antes})
    print(f"{r['solicitud']:<5}{r['prob']:>6.0%}  {'rechaza' if antes else 'pasa':<9}{'rechaza' if despues else 'pasa':<9}"
          + ", ".join(nuevos))
n = len(registros)
print(f"\nRechazadas: antes {antes_total} de {n}; después {despues_total} de {n}")
print("Solicitudes rechazadas por cada regla (una solicitud puede tener varios motivos):")
for m in ("números (clase)", "tono bajo/alto (clase)", "texto contra datos (nueva)", "tono medio (nueva)"):
    print(f"  {m:<28} antes {motivos_antes[m]:>2}   después {motivos_despues[m]:>2}")

# Falsos positivos: el texto de respaldo solo usa datos y la probabilidad, así que es correcto por construcción.
predictor, X_pru, _ = entrenar_predictor()
fp = 0
for i in range(len(X_pru)):
    datos, prob = datos_legibles(X_pru.iloc[i]), probabilidad_malo(predictor, X_pru, i)
    fp += bool(verificar_explicacion(explicacion_segura(datos, prob), datos, prob))
print(f"\nFalsos positivos sobre los 200 textos de respaldo (correctos por construcción): {fp}")
