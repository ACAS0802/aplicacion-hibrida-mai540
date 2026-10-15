"""Tarea 7.2 · Pruebas de las dos reglas nuevas del verificador. Cada una falla con el verificador de clase.

Los textos de las pruebas son los que el modelo de lenguaje generó en resultados/explicaciones.json.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from datos import datos_legibles
from predictor import entrenar_predictor, probabilidad_malo
from verificador import explicacion_segura, verificar_explicacion

# Solicitud 8: dice «sin saldo negativo» cuando el dato es saldo negativo.
DATOS_8 = {"edad": 23, "duración (meses)": 6, "monto": 1352, "cuenta corriente": "saldo negativo", "vivienda": "alquilada"}
# Solicitud 4: inventa «una persona sola».
DATOS_4 = {"edad": 31, "duración (meses)": 18, "monto": 3104, "cuenta corriente": "saldo negativo", "vivienda": "propia"}


# --- Regla 1: el texto contra los datos ------------------------------------------------------------------

def test_regla_datos_detecta_cuenta_contradicha():
    texto = ("El modelo de riesgo de crédito sugiere una probabilidad de crédito malo del 43%, para una persona "
             "con una edad de 23 años y una duración de 6 meses en una cuenta corriente sin saldo negativo.")
    assert any("niega el saldo negativo" in p for p in verificar_explicacion(texto, DATOS_8, 0.43))


def test_regla_datos_detecta_rasgo_inventado():
    texto = ("El modelo de riesgo de crédito sugiere una probabilidad de crédito malo del 41%, ya que la cuenta "
             "corriente tiene un saldo negativo y la persona es una persona sola.")
    assert any("persona sola" in p for p in verificar_explicacion(texto, DATOS_4, 0.41))


def test_regla_datos_detecta_vivienda_contradicha():
    texto = "El modelo estima 41% de probabilidad de crédito malo; la persona vive en una vivienda alquilada."
    assert any("vivienda «alquilada»" in p for p in verificar_explicacion(texto, DATOS_4, 0.41))


# --- Regla 2: el tono entre 30% y 60% --------------------------------------------------------------------

def test_regla_tono_medio_detecta_alto():
    # Solicitud 12: 37% y dice «alto».
    texto = "El modelo estima una probabilidad de crédito malo del 37%, lo cual es alto para una persona de 43 años."
    datos = {"edad": 43, "duración (meses)": 12, "monto": 4843, "cuenta corriente": "saldo negativo", "vivienda": "alquilada"}
    assert any("probabilidad es media" in p for p in verificar_explicacion(texto, datos, 0.37))
