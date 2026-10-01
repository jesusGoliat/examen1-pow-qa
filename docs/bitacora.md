# Bitácora — jesusGoliat (Jesús Ángel González Arellano)

## Línea de tiempo (2026-10-01)

| Hora | Actividad | Resultado / enlace |
|------|-----------|--------------------|
| 09:45 | Lectura del enunciado y de mis lecciones aprendidas. Revisión de los PRs e issues abiertos en POW para no duplicar trabajo. | Ningún PR o issue sobre la IP de LAN. |
| 09:50 | Fork, issues habilitadas en el fork y sincronización con `main`. | SHA base `7ed3253` |
| 09:52 | Issue creada con los criterios de aceptación. | [jesusGoliat/PolitecnicoOpenWorld#1](https://github.com/jesusGoliat/PolitecnicoOpenWorld/issues/1) |
| 09:55 | Plan de pruebas, riesgos y criterios escritos **antes** de ejecutar. | commit `f0b4457` del repo de entrega |
| 10:00–10:09 | Preparación local: wrapper y `MAPS_API_KEY`. Compilación y pruebas de la base. | H-02; base 125 + 217 pruebas en verde |
| 10:12–10:23 | Ejecución de referencia en la base (B-1 a B-6). | Defecto reproducido |
| 10:26 | Commits de implementación y push. | `16330bf`, `170802a` |
| 10:28 | Build, pruebas y detekt locales de la rama. | Todo en verde |
| 10:33 | Draft PR al repositorio original. | [#172](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/172) |
| 10:33 | El CI del original queda en `action_required`; abro el PR espejo en el fork. | [fork #2](https://github.com/jesusGoliat/PolitecnicoOpenWorld/pull/2) |
| 10:37–10:55 | Ejecución de CP-01 a CP-06 en el emulador. | 6/6 aprobados |
| 10:56–10:59 | Análisis del fallo del CI en el fork y reproducción en la base. | H-02 confirmado como preexistente |
| 11:00–11:05 | Documentación de fichas, hallazgos, CI y dictamen. QA evidence actualizado en el PR, que pasa a Ready for review. | — |

## Mis commits

**En el PR (`fix/sf-lan-ip-validation`):**

| SHA | Mensaje | Tipo de aporte |
|-----|---------|----------------|
| [`16330bf`](https://github.com/jesusGoliat/PolitecnicoOpenWorld/commit/16330bf) | feat: add pure IPv4 validation for LAN join address | Implementación + 12 pruebas unitarias |
| [`170802a`](https://github.com/jesusGoliat/PolitecnicoOpenWorld/commit/170802a) | fix: validate LAN IP before enabling join | Implementación (UI) |

Los commits del repositorio de entrega son de documentación de QA y evidencias. Ver su
[historial](https://github.com/jesusGoliat/examen1-pow-qa/commits/main).

## Casos que ejecuté

- B-1 a B-6: referencia sobre la base.
- CP-01 a CP-07 sobre `170802a`. Ver [pruebas.md](pruebas.md).

## Revisión técnica

- **Revisión recibida en mi PR:** pendiente de solicitar a un compañero de equipo. La conversación y
  mis respuestas se registran en el [PR #172](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/172).
- **Revisión que di:** observación técnica en el PR de un compañero de equipo. El enlace se
  agrega en el [README](../README.md#revisión) al publicarla.

## Herramientas de IA utilizadas

| Herramienta | Para qué la usé |
|-------------|-----------------|
| Claude Code (Anthropic) | Explorar el código de POW para elegir un cambio acotado. Redactar la función de validación y sus pruebas. Automatizar con ADB los recorridos y las capturas del emulador. Redactar los borradores de la issue, el PR y esta documentación. |

Revisé el diff, los resultados de cada caso y la documentación. Puedo explicar:
- la regla de validación (por qué se rechazan los ceros a la izquierda y los octetos mayores a 255),
- cómo se reproduce el defecto,
- por qué el fallo del CI en el fork es preexistente.

Las capturas, los logs y las ejecuciones de Gradle y detekt son reales, sobre los SHA indicados.
