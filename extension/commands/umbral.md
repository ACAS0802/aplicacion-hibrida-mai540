---
description: Calcula el costo de los errores del predictor con cada umbral de rechazo y recomienda uno, con sus límites
allowed-tools: Bash(python tareas.py costo:*)
---

## Contexto

Costo de los errores del predictor sobre los 200 casos de prueba (aprobar un crédito malo cuesta 5, rechazar uno bueno cuesta 1):

!`python tareas.py costo`

## Tu tarea

Responde en cuatro frases cortas, con las cifras de la tabla:

1. ¿Cuánto cuesta el umbral 0.50 que usa `predict` y cuánto el umbral de menor costo?
2. ¿Cuántos créditos buenos de más se rechazan a cambio, y cómo cambia la exactitud?
3. ¿Supera el umbral elegido la referencia «aprobar a todos»?
4. Advierte que el umbral se eligió con los mismos 200 casos con que se mide, así que su costo es optimista, y di qué haría falta para confirmarlo (validación cruzada u otra muestra).

No modifiques ningún archivo.
