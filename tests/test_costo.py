"""Pruebas del comando propio `python tareas.py costo`."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from predictor import entrenar_predictor
from tareas import tabla_costos


def test_tabla_costos_cuenta_bien_un_caso_pequeno():
    # 4 solicitudes: 2 malas (1) y 2 buenas (0). Con umbral 0.5 se aprueba un malo y se rechaza un bueno.
    prob = np.array([0.9, 0.2, 0.7, 0.1])
    y = np.array([1, 1, 0, 0])
    fila = tabla_costos(prob, y, umbrales=[0.5]).loc[0.5]
    assert fila["malos aprobados"] == 1 and fila["buenos rechazados"] == 1
    assert fila["costo"] == 5 * 1 + 1 * 1


def test_predictor_cuesta_menos_que_aprobar_a_todos():
    predictor, X_pru, y_pru = entrenar_predictor()
    tabla = tabla_costos(predictor.predict_proba(X_pru)[:, 1], y_pru.values)
    assert tabla["costo"].min() < 5 * int(y_pru.sum())
