"""Tarea 7.2 · Compara la red neuronal con el Random Forest sobre las mismas 200 solicitudes de prueba.

Uso:  python comparar_modelos.py
"""
import time

from sklearn.model_selection import train_test_split

from datos import cargar_datos
from predictor import entrenar_predictor
from red_neuronal import crear_red, describir_red

X, y, cols_cat, cols_num = cargar_datos()
# misma partición que entrenar_predictor: así ambos modelos se miden sobre las mismas 200 solicitudes
X_ent, X_pru, y_ent, y_pru = train_test_split(X, y, test_size=0.20, stratify=y, random_state=42)

inicio = time.time()
red = crear_red(cols_cat, cols_num).fit(X_ent, y_ent)
t_red = time.time() - inicio
inicio = time.time()
bosque, X_pru_rf, y_pru_rf = entrenar_predictor()
t_rf = time.time() - inicio
assert X_pru_rf.index.equals(X_pru.index), "las 200 solicitudes de prueba no coinciden"

capas, pesos = describir_red(red)
print(f"Red neuronal: capas {capas}, {pesos:,} pesos aprendidos")
print(f"{'Modelo':<15}{'Exactitud ent.':>16}{'Exactitud prueba':>18}{'Malos detectados':>18}{'Ajuste (s)':>12}")
for nombre, modelo, t in (("Red neuronal", red, t_red), ("Random Forest", bosque, t_rf)):
    pred = modelo.predict(X_pru)
    acc_ent = float((modelo.predict(X_ent) == y_ent.values).mean())
    acc = float((pred == y_pru.values).mean())
    malos = float(pred[y_pru.values == 1].mean())                   # proporción de malos que detecta
    print(f"{nombre:<15}{acc_ent:>16.3f}{acc:>18.3f}{malos:>18.3f}{t:>12.2f}")
coinciden = float((red.predict(X_pru) == bosque.predict(X_pru)).mean())
print(f"Las dos predicen lo mismo en {coinciden:.0%} de las 200 solicitudes. Referencia «siempre bueno»: 0.700")
