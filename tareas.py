"""Comandos reutilizables del proyecto.  Uso:  python tareas.py evaluar | auditar | probar | costo"""
import subprocess
import sys

import pandas as pd
from sklearn.model_selection import cross_val_score, StratifiedKFold   # validación cruzada (Clase 6)

from datos import cargar_datos
from predictor import entrenar_predictor


def evaluar():
    """Exactitud del predictor con validación cruzada de 5 pliegues."""
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OrdinalEncoder
    X, y, cols_cat, _ = cargar_datos()
    prep = ColumnTransformer([("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), cols_cat)], remainder="passthrough")
    pipe = Pipeline([("prep", prep), ("modelo", RandomForestClassifier(n_estimators=200, random_state=42))])
    scores = cross_val_score(pipe, X, y, cv=StratifiedKFold(5, shuffle=True, random_state=42))
    print(f"Exactitud: {scores.mean():.3f} ± {scores.std():.3f}")


def auditar():
    """Exactitud por rango de edad, sobre los casos de prueba."""
    predictor, X_pru, y_pru = entrenar_predictor()
    acierto = predictor.predict(X_pru) == y_pru.values
    rango = pd.cut(X_pru["age"], [0, 25, 35, 50, 100], labels=["hasta 25", "26-35", "36-50", "más de 50"])
    print(X_pru.assign(acierto=acierto, edad=rango).groupby("edad", observed=True)["acierto"]
          .agg(exactitud="mean", casos="count").round(2))


def probar():
    """Ejecuta las pruebas automáticas."""
    sys.exit(subprocess.call([sys.executable, "-m", "pytest", "-q"]))


# Costo de cada error, con la matriz original de German Credit: aprobar un crédito malo cuesta 5,
# rechazar uno bueno cuesta 1 (la misma regla que usé en la Tarea 6.2).
COSTO_MALO_APROBADO = 5
COSTO_BUENO_RECHAZADO = 1
UMBRALES = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60]


def tabla_costos(prob, y_real, umbrales=UMBRALES):
    """Para cada umbral (rechazar si prob >= umbral): errores de cada tipo, costo y exactitud."""
    filas = []
    for u in umbrales:
        rechaza = prob >= u
        malos_aprobados = int(((~rechaza) & (y_real == 1)).sum())       # el error caro
        buenos_rechazados = int((rechaza & (y_real == 0)).sum())         # el error barato
        filas.append({"umbral": u, "malos aprobados": malos_aprobados, "buenos rechazados": buenos_rechazados,
                      "costo": COSTO_MALO_APROBADO * malos_aprobados + COSTO_BUENO_RECHAZADO * buenos_rechazados,
                      "exactitud": round(float((rechaza == (y_real == 1)).mean()), 3)})
    return pd.DataFrame(filas).set_index("umbral")


def costo():
    """Costo de los errores del predictor según el umbral de rechazo, sobre los casos de prueba."""
    predictor, X_pru, y_pru = entrenar_predictor()
    prob = predictor.predict_proba(X_pru)[:, 1]
    tabla = tabla_costos(prob, y_pru.values)
    print(tabla)
    siempre_bueno = COSTO_MALO_APROBADO * int(y_pru.sum())               # aprobar a todos
    mejor = tabla["costo"].idxmin()
    print(f"\nReferencia «aprobar a todos»: costo {siempre_bueno}")
    print(f"Umbral 0.50 (el que usa predict): costo {tabla.loc[0.50, 'costo']}")
    print(f"Umbral de menor costo: {mejor:.2f} con costo {tabla.loc[mejor, 'costo']} "
          f"y exactitud {tabla.loc[mejor, 'exactitud']}")


COMANDOS = {"evaluar": evaluar, "auditar": auditar, "probar": probar, "costo": costo}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in COMANDOS:
        sys.exit("Uso: python tareas.py " + " | ".join(COMANDOS))
    COMANDOS[sys.argv[1]]()
