# Plan y matriz de pruebas — Validación de IP en «Unirse por LAN»

- **Issue:** [jesusGoliat/PolitecnicoOpenWorld#1](https://github.com/jesusGoliat/PolitecnicoOpenWorld/issues/1)
- **PR:** [gabrielhuav/PolitecnicoOpenWorld#172](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/172) (rama `fix/sf-lan-ip-validation`)
- **SHA base:** `7ed3253`
- **SHA probado:** `170802a`

Las secciones 1 a 3 se escribieron **antes** de ejecutar (commit `f0b4457`). Los
resultados reales se llenaron después.

## 1. Criterios de aceptación y riesgos

| ID | Criterio / riesgo | Casos |
|----|-------------------|-------|
| CA1 | **Éxito:** con una IPv4 válida, UNIRSE se habilita y se inicia la conexión | CP-01, CP-06 |
| CA2 | **Límite:** con un valor inválido (vacío, `1.2.3.`, `256.1.1.1`, `1.2.3.4.5`, `01.2.3.4`, letras), UNIRSE queda deshabilitado y no se conecta | CP-02, CP-06, CP-07 |
| R1 | Se rechaza una IP válida y ya no se puede unir por IP (impacto alto) | CP-01, CP-06, CP-07 |
| R2 | El filtro de entrada corta una IP válida larga o impide editar (medio) | CP-02, CP-07 |
| R3 | Regresión en el resto del overlay multijugador (medio) | CP-03 |
| R4 | Se pierde la IP escrita al salir y volver a la app (bajo) | CP-04 |
| R5 | El botón deshabilitado no se distingue con texto ampliado o TalkBack (bajo) | CP-05 |

## 2. Entorno

| Elemento | Valor |
|----------|-------|
| SO / JDK / Gradle | Ubuntu 24.04.5 · Corretto 21.0.12 · Gradle 9.5.0 (wrapper del proyecto) |
| Android Studio | Ladybug 2024.2.1. No soporta AGP 9.3, así que se compiló por consola |
| Dispositivo | Emulador Pixel 3a, **API 33** (Android 13), x86_64, 1080×2220. Idioma del sistema en inglés |
| App | `ovh.gabrielhuav.pow` 1.0.0.18, debug, compilada desde el SHA probado |
| Preparación | `secrets.properties` con `MAPS_API_KEY=DEFAULT_API_KEY`; `gradle-wrapper.jar` regenerado. Ambos están en `.gitignore` y no se suben (ver H-02) |

**Ruta N:** «★ Titulación por Combate ★» → «Otros modos» → «Multijugador» → sección LAN.

**Datos ficticios:**
- IPs privadas o de la red del emulador.
- Para la ruta feliz, un *listener* TCP en la laptop en el puerto 47645 (`10.0.2.2` desde el emulador), que solo registra las conexiones.

## 3. Ejecución de referencia en la base (`7ed3253`)

| Entrada | JOIN | Al pulsar | Evidencia |
|---------|------|-----------|-----------|
| `1.2.3.` | **habilitado** ❌ | 3 intentos `SF-NET … 1.2.3.:47645 falló` y un error de red | [03](../img/03-base-ip-1.2.3.-join-habilitado.png), [04](../img/04-base-join-1.2.3.-resultado.png), [logcat](../img/logs/04-base-logcat-join-1.2.3.txt) |
| `999.1.1.1` / `a.b.c.d` | **habilitado** ❌ | — | [05](../img/05-base-ip-999.1.1.1-join-habilitado.png), [06](../img/06-base-ip-letras-join-habilitado.png) |
| `10.0.2.2` | habilitado | `conectado a 10.0.2.2:47645` (comportamiento a conservar) | [09](../img/09-base-join-10.0.2.2-resultado.png), [logcat](../img/logs/09-base-logcat-join-10.0.2.2.txt) |
| CREAR SERVIDOR → Cancelar | — | Muestra las IPs locales y regresa a la lista de modos | [07](../img/07-base-crear-servidor.png) |

## 4. Fichas de casos

**Datos comunes de las fichas:**
- **Autor:** jesusGoliat.
- **Fecha:** 2026-10-01.
- **SHA:** `170802a`, app 1.0.0.18 debug.
- **Dispositivo:** Pixel 3a, API 33.
- **Precondición:** app abierta en la ruta N, salvo que la ficha indique otra cosa.

**CP-01: Ruta feliz** (CA1, R1). ✅ **Aprobado**.

**Datos:** `192.168.0.10`, `255.255.255.255`, `0.0.0.0`, `10.0.2.2`; listener activo.

**Pasos:**
1. Escribir cada IP y observar JOIN.
2. Con `10.0.2.2`, pulsar JOIN.
3. Revisar `adb logcat -s SF-NET`.

**Esperado:** JOIN habilitado y conexión iniciada.

**Real:** JOIN habilitado con todas. Logcat registra `conectado a 10.0.2.2:47645 → handshake`, y el listener recibe `{"type":"BT_HELLO"}`.

**Evidencia:** [31](../img/31-cp01-rama-ip-10.0.2.2-join-habilitado.png), [32](../img/32-cp01-rama-join-10.0.2.2-resultado.png), [logcat](../img/logs/32-cp01-rama-logcat-join-10.0.2.2.txt).

**Decisión:** sin defecto. No se jugó una partida real porque no había un segundo dispositivo.

---

**CP-02: Límite** (CA2, R2). ✅ **Aprobado**.

**Datos:** vacío, `1.2.3.`, `999.1.1.1`, `256.1.1.1`, `1.2.3.4.5`, `01.2.3.4`, `a.b.c.d`.

**Pasos:**
1. Escribir cada valor y leer el estado de JOIN.
2. Con `1.2.3.`, tocar JOIN.
3. Revisar logcat.

**Esperado:** JOIN deshabilitado, letras filtradas y ningún intento de conexión.

**Real:** `enabled=false` en los 7 casos. `a.b.c.d` queda en `...`. Tocar JOIN produce 0 líneas `SF-NET`.

**Evidencia:** antes [03](../img/03-base-ip-1.2.3.-join-habilitado.png) / después [23](../img/23-cp02-rama-ip-1.2.3.-join-deshabilitado.png), [22](../img/22-cp02-rama-letras-filtradas.png), [logcat vacío](../img/logs/24-cp02-rama-logcat-tap-deshabilitado.txt).

**Decisión:** sin defecto.

---

**CP-03: Regresión** (R3). ✅ **Aprobado**.

**Pasos:**
1. Pulsar CREAR SERVIDOR y luego Cancelar.
2. Escribir `ab1c` en «Código».

**Esperado:** igual que en la base.

**Real:** CREAR SERVIDOR muestra `10.0.2.16 • 10.0.2.15`. Cancelar regresa a «Otros modos». El código queda `AB1C` con su botón habilitado.

**Evidencia:** [34](../img/34-cp03-rama-crear-servidor.png), [35](../img/35-cp03-rama-codigo-sala-AB1C.png).

**Decisión:** sin defecto.

---

**CP-04: Navegación y estado** (R4). ✅ **Aprobado**.

La orientación está fija en horizontal (`SENSOR_LANDSCAPE`), así que en lugar de rotar se prueba el ciclo de vida.

**Pasos:**
1. Escribir `192.168.0.10`.
2. Ir a Home y volver.
3. Pulsar Atrás.
4. Reabrir Multijugador.
5. Repetir con «No conservar actividades» activado.

**Esperado:** se conserva la IP y no hay cierre inesperado.

**Real:**
- La IP y JOIN habilitado se conservan.
- Atrás cierra el overlay.
- Con la actividad recreada, la app vuelve a «Otros modos» sin crash.

**Evidencia:** [41](../img/41-cp04-rama-regreso-conserva-ip.png), [42](../img/42-cp04-rama-atras.png), [44](../img/44-cp04-rama-recreacion-actividad.png).

**Decisión:** sin defecto.

---

**CP-05: Accesibilidad** (R5). ✅ **Aprobado**, con una limitación.

**Pasos:**
1. Poner `font_scale` en 1.3.
2. Escribir una IP inválida, una válida y la más larga.
3. Revisar el árbol de accesibilidad.
4. Activar TalkBack.

**Esperado:** texto legible y el estado deshabilitado expuesto.

**Real:**
- El texto es legible.
- El botón deshabilitado se ve atenuado y el árbol de accesibilidad expone `enabled="false"`.
- Con `255.255.255.255` se oculta el primer dígito (H-03).

**Limitación:** no se pudo grabar la voz de TalkBack en el emulador.

**Evidencia:** [51](../img/51-cp05-rama-fuente-1.3-ip-valida.png), [52](../img/52-cp05-rama-fuente-1.3-ip-larga.png), [nodos](../img/logs/53-cp05-rama-nodos-accesibilidad.txt).

**Decisión:** H-03 queda pendiente; es preexistente.

---

**CP-06: Entorno, app en español** (CA1, CA2). ✅ **Aprobado**.

**Pasos:**
1. Ir a Ajustes → Idioma → Español.
2. Repetir `1.2.3.`, `256.1.1.1`, `a.b.c.d`, `192.168.0.10` y unirse a `10.0.2.2`.

**Esperado:** el mismo comportamiento, con los textos en español.

**Real:** las inválidas dejan UNIRSE deshabilitado. La válida lo habilita y conecta (`BT_HELLO` recibido).

**Evidencia:** [61](../img/61-cp06-rama-es-ip-invalida.png), [60](../img/60-cp06-rama-es-ip-valida.png), [logcat](../img/logs/63-cp06-rama-logcat-join-es.txt).

**Decisión:** sin defecto.

---

**CP-07: Pruebas unitarias** (CA1, CA2, R1, R2). ✅ **Aprobado**.

**Pasos:**
1. Ejecutar `./gradlew :app:assembleDebug :app:testDebugUnitTest :shared:testAndroidHostTest`.
2. Ejecutar `bash tools/check_kmp_test_names.sh`.

**Esperado:** pruebas nuevas en verde y sin regresiones.

**Real:**
- `SfLanIpTest`: 12/12.
- `:shared`: 229 pruebas (217 + 12) con 0 fallos.
- `:app`: 125 pruebas con 0 fallos.
- Los nombres de prueba son compatibles con Kotlin/Native.

**Evidencia:** [reporte JUnit](../img/logs/10-SfLanIpTest-170802a.xml).

**Decisión:** sin defecto.

No hubo fallos atribuibles al cambio, así que tampoco hubo re-ejecuciones. El SHA probado es el SHA final del PR.

## 5. Checks de CI

| Check | Estado |
|-------|--------|
| PR Quality Gate en el PR #172 | ⏸️ `action_required`: requiere la aprobación del mantenedor ([run](https://github.com/gabrielhuav/PolitecnicoOpenWorld/actions/runs/36892877520)). Es un bloqueo externo y **no** cuenta como prueba aprobada |
| Espejo en el fork, mismo SHA ([run](https://github.com/jesusGoliat/PolitecnicoOpenWorld/actions/runs/36892975028)) | detekt ✅; nombres KMP ✅; build + pruebas ❌ por `MAPS_API_KEY = ;` (preexistente, H-02) |
| Local, mismo comando y misma CLI de detekt | ✅ build y pruebas; detekt sin hallazgos nuevos |

**Qué cubre el gate:** compilación, pruebas JVM y análisis estático.

**Qué no cubre:** la UI, la red real ni el dispositivo. Por eso complementa el QA manual pero no lo reemplaza.

## 6. Hallazgos

| ID | Hallazgo | Severidad | Estado |
|----|----------|-----------|--------|
| H-01 | JOIN acepta IPs mal formadas y lanza conexiones imposibles con un error engañoso (sección 3) | Media | **Corregido** en `170802a` |
| H-02 | `MAPS_API_KEY` vacío rompe `compileDebugJavaWithJavac` y el CI en forks. Además, `gradle-wrapper.jar` no está versionado. Se reproduce en la base sin el cambio ([log](../img/logs/12-base-maps-key-vacia.log)) | Media | Preexistente, fuera de alcance |
| H-03 | Con fuente 1.3, el campo de 180 dp oculta el primer dígito de la IP más larga ([52](../img/52-cp05-rama-fuente-1.3-ip-larga.png)) | Baja | Preexistente, pendiente |
| H-04 | El detalle del error LAN sale en español con la UI en inglés (texto fijo en `SfLanClient.kt:136`, [04](../img/04-base-join-1.2.3.-resultado.png)) | Baja | Preexistente, pendiente |

## 7. Dictamen

**Recomiendo integrar el PR.**

**Evidencia a favor:**
- CA1 y CA2 se observaron en el dispositivo, en inglés y en español.
- No hubo regresiones.
- La regla tiene 12 pruebas unitarias y el gate local pasa.

**Riesgos que permanecen:**
- No se jugó una partida LAN con dos teléfonos.
- La prueba con TalkBack fue parcial.
- El CI del repositorio original no ha corrido por falta de aprobación.
- Las IPs con ceros a la izquierda se rechazan a propósito.
