"""Paso 4 · Verificar la capa generativa: que el texto no afirme nada que el modelo no sustente."""
import re


def _numeros(texto):
    """Todos los números que aparecen en un texto, como conjunto de floats."""
    return {float(n.replace(",", ".")) for n in re.findall(r"\d+(?:[.,]\d+)?", texto)}


def verificar_numeros(texto, datos, prob):
    """Devuelve una lista de problemas: números del texto que no vienen de los datos ni del modelo."""
    # permitidos: los números de los datos y la probabilidad en porcentaje entero
    permitidos = _numeros(" ".join(str(v) for v in datos.values())) | {float(round(prob * 100))}
    # lo que sobra, el modelo lo inventó
    return [f"número no sustentado: {n:g}" for n in sorted(_numeros(texto) - permitidos)]


def verificar_tono(texto, prob):
    """Devuelve una lista de problemas: el tono no coincide con la probabilidad, o hay afirmaciones absolutas."""
    t = texto.lower()                                        # minúsculas para comparar
    problemas = []
    if prob < 0.30 and any(p in t for p in ("alto", "elevado")):
        problemas.append("dice que el riesgo es alto, pero la probabilidad es baja")
    if prob > 0.60 and any(p in t for p in ("bajo", "mínimo")):
        problemas.append("dice que el riesgo es bajo, pero la probabilidad es alta")
    # certezas que un modelo de probabilidades no puede dar
    for absoluta in ("garantiza", "garantizado", "sin riesgo", "seguro que", "imposible", "nunca", "siempre"):
        if absoluta in t:
            problemas.append(f"afirmación absoluta: '{absoluta}'")
    return problemas


def explicacion_segura(datos, prob):
    """Texto de respaldo, armado solo con datos y la probabilidad. No usa el modelo de lenguaje."""
    nivel = "bajo" if prob < 0.30 else ("medio" if prob <= 0.60 else "alto")   # mismas franjas que verificar_tono
    detalle = ", ".join(f"{k}: {v}" for k, v in datos.items())
    return f"El modelo estima una probabilidad de {prob:.0%} de que el crédito sea malo (riesgo {nivel}). Datos: {detalle}."


# ---------------------------------------------------------------------------------------------------------
# Tarea 7.2 · Dos reglas nuevas. Usan límites de palabra (\b) para que, por ejemplo, «bajo» no coincida
# dentro de «trabajo» ni «alta» dentro de «faltan».

# Qué frase del texto corresponde a cada valor de los datos (los mismos valores que produce datos.py).
CUENTA_EN_TEXTO = {
    "saldo negativo": r"(?<!sin )(?<!no tiene )(?<!no tiene un )saldo negativo|n[uú]meros rojos|sobregir",
    "saldo entre 0 y 200": r"saldo entre 0 y 200",
    "saldo de 200 o más": r"saldo de 200 o m[aá]s|saldo (?:superior|mayor) a 200",
    "sin cuenta corriente": r"sin cuenta corriente|no tiene cuenta corriente",
}
NIEGA_SALDO_NEGATIVO = r"sin saldo negativo|no tiene (?:un )?saldo negativo"
VIVIENDA_EN_TEXTO = {
    "propia": r"\bvivienda propia\b|\bpropiedad propia\b|\bpropietari[oa]\b|\bcasa propia\b",
    "alquilada": r"\balquil\w*",
    "sin costo": r"\bsin costo\b|\bgratuit[oa]\b",
}
# Rasgos de la persona que la solicitud no trae: si el texto los menciona, los inventó.
SIN_DATO = r"\b(?:persona sola|solter[oa]|casad[oa]|divorciad[oa]|viud[oa]|hij[oa]s|familia|desemplead[oa]|empleo|trabajo|salario|sueldo|ingresos?|salud)\b"


def verificar_datos(texto, datos):
    """Regla nueva 1: lo que el texto afirma de la cuenta corriente, la vivienda o la persona debe coincidir con los datos."""
    t = texto.lower()
    problemas = []
    cuenta = datos.get("cuenta corriente")
    for valor, patron in CUENTA_EN_TEXTO.items():
        if valor != cuenta and re.search(patron, t):
            problemas.append(f"el texto dice «{valor}», pero el dato de cuenta corriente es «{cuenta}»")
    if cuenta == "saldo negativo" and re.search(NIEGA_SALDO_NEGATIVO, t):
        problemas.append("el texto niega el saldo negativo, pero el dato de cuenta corriente es «saldo negativo»")
    vivienda = datos.get("vivienda")
    for valor, patron in VIVIENDA_EN_TEXTO.items():
        if valor != vivienda and re.search(patron, t):
            problemas.append(f"el texto dice vivienda «{valor}», pero el dato es «{vivienda}»")
    for rasgo in sorted(set(re.findall(SIN_DATO, t))):
        problemas.append(f"afirmación sin dato que la respalde: «{rasgo}»")
    return problemas


def verificar_tono_medio(texto, prob):
    """Regla nueva 2: con probabilidad entre 30% y 60% (riesgo medio), el texto no debe calificar el riesgo de alto ni de bajo."""
    if not 0.30 <= prob <= 0.60:                             # mismas franjas que verificar_tono y explicacion_segura
        return []
    extremos = sorted(set(re.findall(r"\b(?:alto|alta|elevad[oa]|bajo|baja|m[ií]nim[oa])\b", texto.lower())))
    return [f"la probabilidad es media ({prob:.0%}), pero el texto dice «{p}»" for p in extremos]


def verificar_explicacion(texto, datos, prob, reglas_nuevas=True):
    """Reúne todas las verificaciones. Lista vacía = el texto se puede mostrar.
    Con reglas_nuevas=False aplica solo las reglas de clase (sirve para medir el antes y el después)."""
    problemas = verificar_numeros(texto, datos, prob) + verificar_tono(texto, prob)
    if reglas_nuevas:
        problemas += verificar_datos(texto, datos) + verificar_tono_medio(texto, prob)
    return problemas
