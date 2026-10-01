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

- **Revisión recibida en mi PR:** [Javier-Gamez](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/172#pullrequestreview-5382926923) revisó `170802a`. Su única nota, no bloqueante, fue que el `if` en `onClick` repite lo que ya garantiza `enabled`.
  - Respondí con evidencia: `PowButton` pasa `enabled` al `Button` de Material3, y en CP-02 hubo 0 líneas `SF-NET` al tocar el botón deshabilitado.
  - Decidí mantenerlo, para no cambiar código ya probado ([respuesta](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/172#issuecomment-5936751948)).
  - No hubo commits nuevos, así que el SHA final sigue siendo `170802a`. La conversación y
  mis respuestas se registran en el [PR #172](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/172).
- **Revisión que di:** [PR #170 de luisAgt](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/170#pullrequestreview-5382923375), sobre el SHA `b33b0db`.
  - Leí el diff y compilé el SHA con el mismo comando del CI ([log](../img/revision-pr170/R2-gradle-b33b0db.log)).
  - Reproduje que `./gradlew` sigue fallando sin el jar ([log](../img/revision-pr170/R1-gradlew-sin-jar-b33b0db.log)).
  - Medí que el APK crece 8.65 MB por los MP4 de QA ([assets](../img/revision-pr170/R3-apk-assets-b33b0db.txt)).
  - Probé en el emulador «IA vs IA» con audio: el efecto de victoria/derrota sonó al terminar el combate y no al terminar la ronda 1.
  - Recomendé revertir el wrapper, quitar los MP4 y los MP3 duplicados, y confirmar el disparo por ronda (`battleEnded`) frente a `showEndMenu`.
  - Copia del texto: [revision-pr170.md](revision-pr170.md).
- **Revisión que di (2):** [PR #148 de Javier-Gamez](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/148#pullrequestreview-5383208475), sobre el SHA `92dddec`.
  - Compilé ese SHA ([log](../img/revision-pr148/R1-assembleDebug-92dddec.log)) y lo instalé limpio en el emulador. Mi celular no estaba disponible, así que la sesión fue mínima y el emulador se apagó al terminar.
  - Reproduje su TC-02: la Biblioteca aparece bloqueada en una instalación limpia ([captura](../img/revision-pr148/R2-tc02-biblioteca-bloqueada-92dddec.png)).
  - Probé un caso extra, la actualización de una partida guardada que ya había vencido a la Granadera ([antes](../img/revision-pr148/R3-partida-simulada-antes.xml), [después](../img/revision-pr148/R3-partida-simulada-despues.xml), [captura](../img/revision-pr148/R3-partida-simulada-biblioteca-desbloqueada-92dddec.png)). Aprobado.
  - Recomendé sacar `docs/` (31 archivos, 8.6 MB) del diff, actualizar los conteos «16 mapas» en `SfStageCatalog.kt` y agregar pruebas unitarias del catálogo.
  - Copia del texto: [revision-pr148.md](revision-pr148.md).

## Herramientas de IA utilizadas

| Herramienta | Para qué la usé |
|-------------|-----------------|
| Claude Code (Anthropic) | Explorar el código de POW para elegir un cambio acotado. Redactar la función de validación y sus pruebas. Automatizar con ADB los recorridos y las capturas del emulador. Redactar los borradores de la issue, el PR y esta documentación. |

Revisé el diff, los resultados de cada caso y la documentación. Puedo explicar:
- la regla de validación (por qué se rechazan los ceros a la izquierda y los octetos mayores a 255),
- cómo se reproduce el defecto,
- por qué el fallo del CI en el fork es preexistente.

Las capturas, los logs y las ejecuciones de Gradle y detekt son reales, sobre los SHA indicados.
