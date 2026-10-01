# Hallazgos y dictamen de calidad

| ID | Tipo | Severidad | Estado | Issue |
|----|------|-----------|--------|-------|
| H-01 | Defecto que motiva el PR | Media | **Corregido** en `170802a` | [jesusGoliat/PolitecnicoOpenWorld#1](https://github.com/jesusGoliat/PolitecnicoOpenWorld/issues/1) |
| H-02 | Configuración de build y CI | Media | **Preexistente**, fuera de alcance | Se documenta aquí y en el PR; ya está descrito en `README for IAS/SETUP_PC_NUEVA.md` |
| H-03 | i18n | Baja | **Preexistente**, pendiente | No se abrió issue, para no duplicar el refactor de i18n en curso. Se deja documentado |
| H-04 | Accesibilidad / diseño | Baja | **Preexistente**, pendiente | Documentado. No se corrige para mantener una sola intención en el PR |

No se encontraron defectos introducidos por el cambio.

---

## H-01 — JOIN por LAN acepta direcciones IP mal formadas (corregido)

**Pasos para reproducir (SHA `7ed3253`):**
1. Abrir POW y entrar a «★ Titulación por Combate ★».
2. Ir a «↕ Other modes» → «Multiplayer» y desplazarse a la sección LAN.
3. Escribir `1.2.3.` en «Host IP».
4. Pulsar JOIN.

**Esperado:** JOIN deshabilitado; no se intenta conectar.

**Observado:**
- JOIN habilitado. También pasa con `999.1.1.1` y `a.b.c.d`.
- Al pulsarlo, 3 intentos fallidos (`SF-NET: intento 1 de conectar a 1.2.3.:47645 falló`) y luego el overlay «NO WI-FI CONNECTION».

**Severidad media.** No corrompe datos ni cierra la app. Sí bloquea al jugador con un mensaje engañoso: culpa a la red de un error de captura, en una función (unirse por IP) que se usa justo cuando la detección automática falla.

**Evidencia:**
- Antes: [03](../img/03-base-ip-1.2.3.-join-habilitado.png), [04](../img/04-base-join-1.2.3.-resultado.png), [logcat](../img/logs/04-base-logcat-join-1.2.3.txt).
- Después: [23](../img/23-cp02-rama-ip-1.2.3.-join-deshabilitado.png), [24](../img/24-cp02-rama-tap-join-deshabilitado-sin-efecto.png), [logcat vacío](../img/logs/24-cp02-rama-logcat-tap-deshabilitado.txt).

**Estado:** corregido en el commit `170802a` (PR [#172](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/172)). Verificado por CP-01, CP-02, CP-06 y CP-07.

## H-02 — `MAPS_API_KEY` vacío rompe la compilación (y el CI en forks)

**Pasos:**
1. Clonar el repositorio en `7ed3253`.
2. Crear `PolitecnicoOpenWorld/secrets.properties` con `MAPS_API_KEY=`, que es justo lo que escribe el workflow cuando el secret no existe.
3. Ejecutar `./gradlew :app:compileDebugJavaWithJavac`.

**Esperado:** que compile. El comentario del paso del workflow dice «vacío es válido para tests».

**Observado:** `BuildConfig.java:14: error: illegal start of expression` → `public static final String MAPS_API_KEY = ;` → BUILD FAILED.

**Severidad media.** Para quien contribuye desde un fork es bloqueante: en un PR que viene de un fork, GitHub no entrega los secrets al workflow. El job `unit-tests` cae antes de correr una sola prueba, sin importar el cambio. No afecta la app publicada.

**Evidencia:**
- Local, en la base: [12-base-maps-key-vacia.log](../img/logs/12-base-maps-key-vacia.log).
- CI del fork sobre el SHA del PR, run [36892975028](https://github.com/jesusGoliat/PolitecnicoOpenWorld/actions/runs/36892975028): [extracto](../img/logs/13-ci-fork-unit-tests-run36892975028.txt).

**Estado:** preexistente y fuera del alcance de este PR. La solución local documentada por el proyecto es usar `MAPS_API_KEY=DEFAULT_API_KEY`. Una corrección en el workflow (p. ej. `${{ secrets.MAPS_API_KEY || 'DEFAULT_API_KEY' }}`) sería un PR aparte.

**Relacionado:** `gradle-wrapper.jar` está en `.gitignore`, así que `./gradlew` falla en un clon limpio ([log](../img/logs/00-gradlew-preexistente.log)). También está documentado en `SETUP_PC_NUEVA.md §2.1`.

## H-03 — Mensaje de error LAN en español con la interfaz en inglés

**Pasos:** con la app en inglés, unirse por LAN a una IP sin anfitrión.

**Esperado:** todo el overlay en inglés.

**Observado:** el título sale en inglés («NO WI-FI CONNECTION») pero el detalle en español: «Red local: no se pudo conectar (…)» o «Red local: el servidor no respondió (¿el anfitrión sigue en CREAR SERVIDOR…?)».

**Causa:** los textos están escritos directamente en el código, en `shared/src/androidMain/.../streetfighter/data/SfLanClient.kt:136`, y no se leen de `strings.xml`.

**Severidad baja:** sólo es cosmético o de idioma.

**Evidencia:** [04](../img/04-base-join-1.2.3.-resultado.png), [09](../img/09-base-join-10.0.2.2-resultado.png), [32](../img/32-cp01-rama-join-10.0.2.2-resultado.png).

**Estado:** preexistente y pendiente. No se corrige aquí para mantener una sola intención.

## H-04 — La IP más larga no se ve completa con texto ampliado

**Pasos:** con `font_scale` 1.3, escribir `255.255.255.255` en «Host IP».

**Esperado:** que la IP se vea completa.

**Observado:** el campo tiene un ancho fijo de 180 dp y el texto se desplaza, así que el primer dígito queda oculto. El valor sí está completo y JOIN funciona.

**Severidad baja:** el usuario puede mover el cursor para revisarlo.

**Evidencia:** [52](../img/52-cp05-rama-fuente-1.3-ip-larga.png).

**Estado:** preexistente: el ancho no cambió en este PR. Queda pendiente.

---

## Dictamen de calidad

**Recomiendo integrar el PR.**

**Evidencia a favor:**
1. Los dos criterios de aceptación se observaron en el dispositivo, en inglés y en español (CP-01, CP-02, CP-06). El inicio de la conexión real se demuestra con logcat y con un listener TCP.
2. No hubo regresiones en los flujos cercanos: crear servidor, código de sala, Cancelar, Atrás y ciclo de vida (CP-03, CP-04).
3. La regla quedó aislada en una función pura con 12 pruebas unitarias. Las suites completas pasan: 125 pruebas de `:app` y 229 de `:shared`, 0 fallos.
4. detekt pasa con la configuración y el baseline del repositorio, en local y en el CI del fork.

**Riesgos que permanecen:**
- No se probó una partida LAN completa entre dos dispositivos físicos. Sólo se probó el inicio de la conexión contra un listener.
- La verificación con TalkBack fue parcial: no se pudo grabar la voz en el emulador.
- El job `unit-tests` del CI no tiene una ejecución verde para este PR:
  - En el repositorio original espera la aprobación del mantenedor (`action_required`).
  - En el fork falla por H-02, que es preexistente.
  - La validación equivalente se hizo en local con el mismo comando del workflow.
- Las IPs con ceros a la izquierda (`192.168.000.1`) ahora se rechazan a propósito.
