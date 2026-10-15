# Demo Clase 7 · Aplicación híbrida: un modelo predictivo y un modelo de lenguaje

Un Random Forest (el de la Clase 6) predice la probabilidad de que un crédito sea malo. Un modelo de lenguaje
pequeño redacta la explicación. Una capa de verificación comprueba que el texto no afirme nada que el modelo no
sustente, y si falla, se muestra un texto de respaldo armado solo con datos. Los bloques `TODO` 1 a 11 ya están completos según el instructivo de la Clase 7.

## Instalación

Requiere Python 3.10 a 3.12 (en Mac con chip Intel, Python 3.12). Con el entorno virtual activo:

```bash
pip install -r requirements.txt
python probar_modelo.py      # comprueba que el modelo de lenguaje descarga y responde
```

## Qué hay en cada archivo

| Archivo | Qué hace |
|---|---|
| `datos.py` | Lee German Credit y traduce una solicitud a datos legibles |
| `predictor.py` | El modelo predictivo (Random Forest) y la probabilidad de crédito malo |
| `red_neuronal.py` | Una red neuronal sencilla: capas y pesos |
| `explicador.py` | El modelo de lenguaje que redacta la explicación |
| `verificador.py` | Las verificaciones y el texto de respaldo |
| `main.py` | Ejecuta la aplicación completa sobre seis solicitudes |
| `tareas.py` | Comandos reutilizables: `evaluar`, `auditar`, `probar` y `costo` (propio) |
| `hooks/pre-commit` y `instalar_hook.py` | La automatización: pruebas y revisión de la extensión antes de cada commit |
| `tests/test_hibrido.py`, `tests/test_costo.py` | Pruebas automáticas (7) |
| `verificar.py` | Comprueba un bloque: `python verificar.py <número de TODO>` |
| `verificar_extension.py` | Comprueba la estructura de la extensión: `python verificar_extension.py` |

## Tarea 7.1 · Lo que agregué

**Comando propio: `python tareas.py costo`.** Traduce los errores del predictor a costo con la matriz original de
German Credit (aprobar un malo = 5, rechazar un bueno = 1) para nueve umbrales de rechazo, y compara con
«aprobar a todos». Lo repito cada vez que cambio el modelo, porque la exactitud sola no dice cuánto cuesta.

**Hook ampliado (`hooks/pre-commit`).** Además de `pytest`, ejecuta `python verificar_extension.py` y cancela el
commit si la extensión pierde su estructura.

**Extensión `extension/` (plugin `costo-de-riesgo`).**

| Archivo | Qué hace |
|---|---|
| `.claude-plugin/plugin.json` | Manifiesto |
| `commands/umbral.md` | `/costo-de-riesgo:umbral`: ejecuta `tareas.py costo` y recomienda un umbral, con su límite |
| `agents/revisor-de-commits.md` | Revisa el `git diff` antes de un commit y señala lo que el hook no comprueba |

Para reproducir desde cero:

```bash
python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
pytest -q                     # 7 passed
python tareas.py costo
python verificar_extension.py
python instalar_hook.py
```

La evidencia (commits aceptados y cancelados, salida de `verificar_extension.py`) está en `evidencia/`.

## Cómo se completa

Cada `TODO n` marca un bloque que se escribe en clase. Para verificar cada paso:

```bash
python verificar.py 1     # cambia el número para cada bloque
python main.py            # cuando estén todos los bloques
pytest -v                 # con los TODO 10 y 11
```

## La extensión (plugin)

Un plugin es una carpeta que empaqueta comandos y agentes para reutilizarlos en otro proyecto. Se arma en el paso 23 del instructivo y se comprueba con `python verificar_extension.py`. Con Claude Code se carga con `claude --plugin-dir extension` y sus comandos aparecen como `/auditoria-hibrida:auditar` y `/auditoria-hibrida:probar`.
