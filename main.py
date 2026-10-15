"""Ejecuta la aplicación híbrida: predice, explica con el modelo de lenguaje y verifica la explicación.

Uso:  python main.py          (12 solicitudes de prueba)
      python main.py 20       (otro número)
Guarda cada texto generado en resultados/explicaciones.json, para volver a verificarlos sin regenerarlos.
"""
import json
import os
import sys
import time

from datos import datos_legibles
from explicador import cargar_modelo_lenguaje, explicar, recortar_a_oracion
from predictor import entrenar_predictor, probabilidad_malo
from verificador import explicacion_segura, verificar_explicacion

N = int(sys.argv[1]) if len(sys.argv) > 1 else 12                 # Tarea 7.2: al menos 10 solicitudes

print("Entrenando el modelo predictivo...")
predictor, X_pru, y_pru = entrenar_predictor()                    # modelo + casos que nunca vio
print("Cargando el modelo de lenguaje (la primera vez se descarga)...")
tokenizador, modelo = cargar_modelo_lenguaje()

rechazadas, registros = 0, []
for i in range(N):
    datos = datos_legibles(X_pru.iloc[i])                         # datos en español
    prob = probabilidad_malo(predictor, X_pru, i)                 # lo que predice el modelo
    inicio = time.time()
    texto = recortar_a_oracion(explicar(tokenizador, modelo, datos, prob))   # lo que redacta (solo frases completas)
    problemas = verificar_explicacion(texto, datos, prob)         # lo que verificamos
    final = explicacion_segura(datos, prob) if problemas else texto
    rechazadas += bool(problemas)
    print(f"\n--- Solicitud {i + 1} | probabilidad de crédito malo: {prob:.0%} | real: {'malo' if y_pru.iloc[i] else 'bueno'}")
    print("Datos:", datos)
    print("Modelo de lenguaje:", texto)
    print("Verificación:", "OK" if not problemas else "; ".join(problemas))
    print("Se muestra:", final)
    registros.append({"solicitud": i + 1, "indice": int(X_pru.index[i]), "datos": datos, "prob": prob,
                      "real": "malo" if y_pru.iloc[i] else "bueno", "texto": texto, "problemas": problemas,
                      "segundos": round(time.time() - inicio, 1)})
print(f"\nExplicaciones rechazadas por la verificación: {rechazadas} de {N}")

os.makedirs("resultados", exist_ok=True)
with open("resultados/explicaciones.json", "w", encoding="utf-8") as f:
    json.dump(registros, f, ensure_ascii=False, indent=2)
print("Textos guardados en resultados/explicaciones.json")
