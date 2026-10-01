# Bitácora — jesusGoliat (Jesús Ángel González Arellano)

## Commits

| SHA | Mensaje | Aporte |
|-----|---------|--------|
| [`16330bf`](https://github.com/jesusGoliat/PolitecnicoOpenWorld/commit/16330bf) | feat: add pure IPv4 validation for LAN join address | Implementación y 12 pruebas unitarias |
| [`170802a`](https://github.com/jesusGoliat/PolitecnicoOpenWorld/commit/170802a) | fix: validate LAN IP before enabling join | Implementación (UI) |

Los commits de documentación de QA están en el
[historial de este repositorio](https://github.com/jesusGoliat/examen1-pow-qa/commits/main).

## Casos ejecutados

- Ejecución de referencia en la base `7ed3253`.
- CP-01 a CP-07 sobre `170802a`, el 2026-10-01. Ver [pruebas.md](pruebas.md).

## Revisión

**Recibida.** [Javier-Gamez](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/172#pullrequestreview-5382926923) señaló que el `if` en `onClick` es redundante con `enabled`.
- [Respondí](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/172#issuecomment-5936751948) con evidencia: `PowButton` pasa `enabled` al `Button` de Material3, y en CP-02 hubo 0 intentos de conexión.
- Lo mantengo para no cambiar código ya probado. Sin commits nuevos.

**Dada a [PR #170](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/170#pullrequestreview-5382923375) (`b33b0db`).**
- Compilé el SHA y lo probé en el dispositivo.
- Señalé que regenera el wrapper de Gradle y que `./gradlew` sigue fallando.
- Señalé los 7.6 MB de videos dentro del APK y los MP3 duplicados.
- Pedí confirmar si el efecto suena al terminar cada ronda o solo al terminar el combate.

**Dada a [PR #148](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/148#pullrequestreview-5383208475) (`92dddec`).**
- Reproduje su TC-02 (escenario bloqueado).
- Probé la actualización de una partida guardada que ya había vencido a la Granadera.
- Recomendé sacar `docs/` del diff y actualizar los conteos «16 mapas».

## Herramientas de IA

| Herramienta | Uso |
|-------------|-----|
| Claude Code (Anthropic) | Explorar el código de POW. Redactar la validación y sus pruebas. Automatizar con ADB los recorridos y las capturas. Redactar borradores de la issue, el PR, las revisiones y esta documentación. |

Revisé el diff, los resultados y la documentación, y puedo explicar el cambio.
Las capturas, los logs y las ejecuciones son reales, sobre los SHA indicados.
