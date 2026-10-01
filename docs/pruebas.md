# Plan y matriz de pruebas — Validación de IP en «Unirse por LAN»

- **Issue:** [jesusGoliat/PolitecnicoOpenWorld#1](https://github.com/jesusGoliat/PolitecnicoOpenWorld/issues/1)
- **SHA base:** `7ed325393f82872c2be94ff2ada46948efa19152` (main de `gabrielhuav/PolitecnicoOpenWorld`)
- **Rama:** `fix/sf-lan-ip-validation`
- **Autor del plan y de la ejecución:** jesusGoliat (Jesús Ángel González Arellano)

> El plan (secciones 1 a 4) se escribió **antes** de ejecutar. Los campos
> «Resultado real», «Estado» y «Evidencia» se llenan sólo después de ejecutar
> cada caso (sección 5).

---

## 1. Criterios de aceptación

| ID | Tipo | Criterio observable |
|----|------|---------------------|
| CA1 | Éxito | Con una IPv4 válida (p. ej. `192.168.0.10`) el botón **Unirse** se habilita y al pulsarlo se inicia la conexión a esa dirección. |
| CA2 | Límite / alterno | Con un valor que no es IPv4 válida (vacío, `1.2.3.`, `256.1.1.1`, `1.2.3.4.5`, `01.2.3.4`, letras) **Unirse** permanece deshabilitado y no se intenta conectar. |

## 2. Riesgos del cambio

| ID | Riesgo | Impacto | Casos que lo cubren |
|----|--------|---------|---------------------|
| R1 | La validación rechaza una IP válida (falso negativo) y el jugador ya no puede unirse por IP. | Alto: bloquea el multijugador LAN manual. | CP-01, CP-06, CP-07 |
| R2 | El filtro de entrada (sólo dígitos y `.`, máx. 15) impide editar/borrar o corta una IP válida larga (`255.255.255.255`). | Medio: entrada frustrante. | CP-02, CP-07 |
| R3 | Regresión en el resto del overlay multijugador (crear partida LAN, código de sala, Cancelar). | Medio: rompe flujos existentes. | CP-03 |
| R4 | El valor escrito o el estado del botón se pierden o se desincronizan al salir y volver a la app. | Bajo: hay que reescribir la IP. | CP-04 |
| R5 | El botón deshabilitado no se distingue o no se anuncia con texto ampliado / TalkBack. | Bajo–medio: accesibilidad. | CP-05 |

## 3. Relación criterio → casos

| Criterio / riesgo | Casos |
|-------------------|-------|
| CA1 | CP-01, CP-06 |
| CA2 | CP-02, CP-06, CP-07 |
| R3 (regresión) | CP-03 |
| R4 (navegación/estado) | CP-04 |
| R5 (accesibilidad) | CP-05 |

## 4. Entorno común

Ver [entorno.md](entorno.md). Emulador **Pixel 3a, API 33 (Android 13), x86_64**,
APK `debug` compilado desde la rama con `./gradlew :app:assembleDebug`.

**Ruta de navegación común (N):** abrir POW → menú principal → botón
«★ Titulación por Combate ★» → «↕ Otros modos / Other modes» → «Multijugador /
Multiplayer» → desplazar hasta la sección LAN («…o únete tecleando la IP»).
*(Ruta corregida tras la primera ejecución: el botón Multijugador está dentro de
«Otros modos».)*

**Datos de prueba (ficticios):** direcciones privadas o de documentación sin host
real; no se usan cuentas ni credenciales.

---


## 5. Ejecución de referencia en la base (antes del cambio)

**SHA:** `7ed3253`. **APK:** debug compilado desde la base. **Fecha:** 2026-10-01, 10:12–10:23. **Ejecutó:** jesusGoliat.

| # | Entrada | JOIN | Al pulsar | Evidencia |
|---|---------|------|-----------|-----------|
| B-1 | vacío | deshabilitado | — | [02](../img/02-base-overlay-lan-vacio.png) |
| B-2 | `1.2.3.` | **habilitado** ❌ | 3 intentos `SF-NET: intento N de conectar a 1.2.3.:47645 falló` y overlay «NO WI-FI CONNECTION» con título «Red local: no se pudo conectar (1.2.3.)» | [03](../img/03-base-ip-1.2.3.-join-habilitado.png), [04](../img/04-base-join-1.2.3.-resultado.png), [logcat](../img/logs/04-base-logcat-join-1.2.3.txt) |
| B-3 | `999.1.1.1` | **habilitado** ❌ | — | [05](../img/05-base-ip-999.1.1.1-join-habilitado.png) |
| B-4 | `a.b.c.d` | **habilitado** ❌ | — | [06](../img/06-base-ip-letras-join-habilitado.png) |
| B-5 | `10.0.2.2` (listener activo) | habilitado | `conectado a 10.0.2.2:47645 → handshake`, el listener recibe `BT_HELLO` | [08](../img/08-base-ip-10.0.2.2-join-habilitado.png), [09](../img/09-base-join-10.0.2.2-resultado.png), [logcat](../img/logs/09-base-logcat-join-10.0.2.2.txt) |
| B-6 | flujo cercano: CREAR SERVIDOR → Cancelar | — | muestra `10.0.2.16 • 10.0.2.15` y Cancelar regresa a la lista de modos | [07](../img/07-base-crear-servidor.png) |

**Conclusión de la base:**
- El defecto existe (B-2, B-3, B-4).
- La conexión válida funciona (B-5) y es el comportamiento que hay que conservar.
- Se observó un detalle de i18n preexistente: el título del error sale en español con la UI en inglés. Ver [hallazgos.md](hallazgos.md) H-03.

---

## 6. Fichas de casos (ejecución sobre la rama)

**Datos comunes de las fichas CP-01 a CP-06:**

| Campo | Valor |
|-------|-------|
| Autor de la ejecución | jesusGoliat (Jesús Ángel González Arellano) |
| Fecha | 2026-10-01 |
| SHA probado | `170802a5898f0c7b1d7d145df28fc1a035e27d29` (rama `fix/sf-lan-ip-validation`) |
| Versión de la app | `ovh.gabrielhuav.pow` 1.0.0.18 (versionCode 12), debug, compilada desde ese SHA |
| Dispositivo | Emulador Pixel 3a, API 33, x86_64, 1080×2220, 440 dpi |
| Configuración base | Idioma del sistema en inglés, fuente 1.0, sin cuenta («Local mode»), Wi-Fi virtual del emulador |

### CP-01 — Ruta feliz: IP válida habilita JOIN e inicia la conexión

| Campo | Valor |
|-------|-------|
| Cubre | CA1, R1 |
| Hora | 10:40–10:41 |
| Precondiciones / datos | Listener TCP de prueba en la laptop, puerto 47645 ([tools/listener.py](../tools/listener.py)). IPs `192.168.0.10`, `255.255.255.255`, `0.0.0.0`, `10.0.2.2`. |

**Pasos:**
1. Seguir la ruta N.
2. Escribir `192.168.0.10` y observar JOIN.
3. Escribir `255.255.255.2559` (con un dígito extra) y luego `0.0.0.0`.
4. Escribir `10.0.2.2` y pulsar JOIN.
5. Leer `adb logcat -s SF-NET:*` y el log del listener.

**Resultado esperado:**
- JOIN se habilita con cada IP válida.
- El dígito extra se descarta (límite de 15 caracteres).
- Al pulsar JOIN, la app abre la conexión TCP a `10.0.2.2:47645`.

**Resultado real:**
- `192.168.0.10`, `255.255.255.255` y `0.0.0.0` dejan JOIN en `enabled=true`.
- `255.255.255.2559` queda en `255.255.255.255`.
- Al pulsar JOIN: `conectado a 10.0.2.2:47645 → handshake`, `enviando BT_HELLO`. El listener registra `conexion desde ('127.0.0.1', 48828) bytes: b'{"type":"BT_HELLO"}\n'`.
- Después aparece el overlay de error porque el listener no es un anfitrión POW real. Es el mismo comportamiento de la base (B-5).

| Campo | Valor |
|-------|-------|
| Estado | ✅ **Aprobado** |
| Evidencia | [30](../img/30-cp01-rama-ip-192.168.0.10-join-habilitado.png), [31](../img/31-cp01-rama-ip-10.0.2.2-join-habilitado.png), [32](../img/32-cp01-rama-join-10.0.2.2-resultado.png), [logcat](../img/logs/32-cp01-rama-logcat-join-10.0.2.2.txt), [listener](../img/logs/32-cp01-rama-listener.txt) |
| Defecto / decisión | Ninguno. Limitación: no se completó una partida real por falta de un segundo dispositivo con POW. Se demuestra el inicio de la conexión, que es lo que exige CA1. |

### CP-02 — Límite: entradas inválidas dejan JOIN deshabilitado

| Campo | Valor |
|-------|-------|
| Cubre | CA2, R2 |
| Hora | 10:37–10:39 |
| Precondiciones / datos | `""`, `1.2.3.`, `999.1.1.1`, `256.1.1.1`, `1.2.3.4.5`, `01.2.3.4`, `a.b.c.d` |

**Pasos:**
1. Seguir la ruta N.
2. Con el campo vacío, leer el estado de JOIN.
3. Escribir cada valor de la lista (borrando el anterior) y leer el estado de JOIN.
4. Con `1.2.3.`, tocar JOIN y leer logcat `SF-NET`.

**Resultado esperado:**
- JOIN queda deshabilitado en todos los casos.
- Las letras no entran al campo.
- Tocar JOIN no genera ningún intento de conexión.

**Resultado real:**
- JOIN queda en `enabled=false` con los 7 valores.
- `a.b.c.d` queda como `...` porque el filtro retira las letras.
- Al tocar JOIN, **0 líneas** `SF-NET` y ningún overlay de error. Comparación con la base: B-2, B-3 y B-4 sí lo habilitaban.

| Campo | Valor |
|-------|-------|
| Estado | ✅ **Aprobado** |
| Evidencia | [20](../img/20-cp02-rama-campo-vacio-join-deshabilitado.png), [21](../img/21-cp02-rama-ip-01.2.3.4-join-deshabilitado.png), [22](../img/22-cp02-rama-letras-filtradas.png), [23](../img/23-cp02-rama-ip-1.2.3.-join-deshabilitado.png) (antes: [03](../img/03-base-ip-1.2.3.-join-habilitado.png)), [24](../img/24-cp02-rama-tap-join-deshabilitado-sin-efecto.png), [logcat vacío](../img/logs/24-cp02-rama-logcat-tap-deshabilitado.txt) |
| Defecto / decisión | Ninguno. |

### CP-03 — Regresión: el resto del overlay multijugador conserva su comportamiento

| Campo | Valor |
|-------|-------|
| Cubre | R3 |
| Hora | 10:41–10:42 |
| Precondiciones / datos | Código de sala `ab1c` |

**Pasos:**
1. Desde el overlay de error de CP-01, pulsar Cancelar.
2. Seguir la ruta N y pulsar CREAR SERVIDOR.
3. Pulsar Cancelar.
4. Abrir Multijugador y escribir `ab1c` en «Código».

**Resultado esperado:** igual que en la base (B-6):
- Cancelar regresa a la lista de modos.
- CREAR SERVIDOR muestra las IPs locales.
- El código se convierte a mayúsculas y habilita su botón JOIN.

**Resultado real:**
- Cancelar regresa a «Otros modos».
- CREAR SERVIDOR muestra `10.0.2.16 • 10.0.2.15` y Cancelar regresa a «Otros modos».
- El código queda `AB1C` y su JOIN en `enabled=true`.

| Campo | Valor |
|-------|-------|
| Estado | ✅ **Aprobado** |
| Evidencia | [33](../img/33-cp03-rama-cancel-error-vuelve-a-modos.png), [34](../img/34-cp03-rama-crear-servidor.png) (antes: [07](../img/07-base-crear-servidor.png)), [35](../img/35-cp03-rama-codigo-sala-AB1C.png) |
| Defecto / decisión | Ninguno. La partida en línea con código no se completó porque requiere servidor y red externa (fuera de alcance). |

### CP-04 — Navegación y estado: Atrás, salir y volver, recreación

| Campo | Valor |
|-------|-------|
| Cubre | R4 |
| Hora | 10:43–10:45 |
| Precondiciones / datos | IP `192.168.0.10` escrita. La orientación está **fija en horizontal** (`SENSOR_LANDSCAPE` para la ruta `street_fighter`, en `AppNavGraph.kt`), así que no se prueba rotación y en su lugar se prueba el ciclo de vida. |

**Pasos:**
1. Escribir `192.168.0.10`.
2. Pulsar Home y volver a abrir la app desde el launcher.
3. Pulsar Atrás del sistema.
4. Volver a abrir Multijugador.
5. Activar «No conservar actividades» (`always_finish_activities=1`), pulsar Home, volver y desactivarlo al terminar.

**Resultado esperado:**
- Tras Home y regreso se conserva la IP y JOIN sigue habilitado.
- Atrás cierra el overlay.
- La recreación no provoca un cierre inesperado.

**Resultado real:**
- Tras Home y regreso, el campo sigue en `192.168.0.10` con JOIN en `enabled=true`.
- Atrás cierra el overlay y regresa a «Otros modos».
- Al reabrir Multijugador, la IP sigue escrita y válida.
- Con la actividad recreada, la app vuelve a «Titulación por Combate / Otros modos» con el overlay cerrado y sin crash. Es el mismo manejo de estado que en la base: el cambio no tocó `remember`.

| Campo | Valor |
|-------|-------|
| Estado | ✅ **Aprobado** |
| Evidencia | [40](../img/40-cp04-rama-home.png), [41](../img/41-cp04-rama-regreso-conserva-ip.png), [42](../img/42-cp04-rama-atras.png), [43](../img/43-cp04-rama-reabrir-conserva-ip.png), [44](../img/44-cp04-rama-recreacion-actividad.png) |
| Defecto / decisión | Ninguno. |

### CP-05 — Accesibilidad: texto ampliado y TalkBack

| Campo | Valor |
|-------|-------|
| Cubre | R5 |
| Hora | 10:45–10:48 |
| Precondiciones / datos | `font_scale` = 1.3 (máximo de Android 13); TalkBack 13 activado por `adb`. IPs `1.2.3.`, `192.168.0.10`, `255.255.255.255`. |

**Pasos:**
1. `adb shell settings put system font_scale 1.3` y seguir la ruta N.
2. Escribir una IP inválida, una válida y la más larga, y observar.
3. Volver a fuente 1.0 y volcar el árbol de accesibilidad con `uiautomator dump`.
4. Activar TalkBack y tocar el campo y JOIN.

**Resultado esperado:**
- Con fuente 1.3 la etiqueta, la IP y JOIN se leen sin cortes.
- El estado deshabilitado de JOIN se expone a los servicios de accesibilidad.

**Resultado real:**
- Con fuente 1.3 la etiqueta «Host IP», la IP y JOIN se leen bien y el botón deshabilitado se ve atenuado.
- Con `255.255.255.255` el texto se desplaza dentro del campo de 180 dp y oculta el primer dígito (el valor está completo). Es una observación de diseño preexistente: el ancho del campo no cambió. Ver H-04.
- El árbol de accesibilidad expone el campo como `EditText` enfocable con su texto, y el contenedor de JOIN con `enabled="false"`, que es lo que TalkBack anuncia como «desactivado».
- **Limitación:** en el emulador no se pudo grabar la voz de TalkBack ni se dibujó el recuadro de foco en la captura. La verificación con TalkBack queda parcial: el servicio estaba activo según `dumpsys accessibility`.

| Campo | Valor |
|-------|-------|
| Estado | ✅ **Aprobado**, con la limitación anotada |
| Evidencia | [50](../img/50-cp05-rama-fuente-1.3-ip-invalida.png), [51](../img/51-cp05-rama-fuente-1.3-ip-valida.png), [52](../img/52-cp05-rama-fuente-1.3-ip-larga.png), [nodos de accesibilidad](../img/logs/53-cp05-rama-nodos-accesibilidad.txt), [54](../img/54-cp05-rama-talkback-foco-join-deshabilitado.png) |
| Defecto / decisión | H-04 (preexistente, baja). No se corrige en este PR. |

### CP-06 — Entorno: mismo recorrido con la app en español

| Campo | Valor |
|-------|-------|
| Cubre | CA1, CA2, R1 en otra configuración |
| Hora | 10:49–10:55 |
| Precondiciones / datos | Ajustes → Interfaz → Idioma = **Español**. (Primero se intentó `cmd locale set-app-locales es-MX`, pero la app lo sobrescribe con su ajuste propio `APP_LANGUAGE` al arrancar.) Listener activo. |

**Pasos:**
1. Cambiar el idioma en Ajustes de la app.
2. Seguir la ruta N.
3. Escribir `1.2.3.`, `256.1.1.1`, `a.b.c.d` y `192.168.0.10`.
4. Escribir `10.0.2.2` y pulsar UNIRSE.

**Resultado esperado:**
- La UI aparece en español («IP del anfitrión», «UNIRSE»).
- La validación se comporta igual que en inglés.

**Resultado real:**
- La etiqueta es «IP del anfitrión», el botón «UNIRSE» y el texto «…o únete tecleando la IP:».
- Los tres valores inválidos dejan UNIRSE en `enabled=false` y `a.b.c.d` queda como `...`.
- `192.168.0.10` lo habilita.
- Con `10.0.2.2`, logcat registra `conectado a 10.0.2.2:47645 → handshake` y el listener recibe `BT_HELLO`.

| Campo | Valor |
|-------|-------|
| Estado | ✅ **Aprobado** |
| Evidencia | [62](../img/62-cp06-rama-ajustes-idioma-espanol.png), [60](../img/60-cp06-rama-es-ip-valida.png), [61](../img/61-cp06-rama-es-ip-invalida.png), [63](../img/63-cp06-rama-es-join-resultado.png), [logcat](../img/logs/63-cp06-rama-logcat-join-es.txt) |
| Defecto / decisión | Ninguno. |

### CP-07 — Pruebas unitarias de la regla (`SfLanIpTest`)

| Campo | Valor |
|-------|-------|
| Cubre | CA1, CA2, R1, R2 |
| Hora | 10:28 |
| Configuración | JVM local, JDK 21; tarea `:shared:testAndroidHostTest` |

**Pasos:**
1. `./gradlew :app:assembleDebug :app:testDebugUnitTest :shared:testAndroidHostTest --stacktrace`
2. `bash tools/check_kmp_test_names.sh`

**Resultado esperado:** 12 pruebas nuevas en verde, ninguna regresión y nombres compatibles con Kotlin/Native.

**Resultado real:**
- BUILD SUCCESSFUL.
- `SfLanIpTest`: 12/12. `:shared`: 229 pruebas (217 de la base + 12), 0 fallos. `:app`: 125 pruebas, 0 fallos.
- `✅ Nombres de test compatibles con Kotlin/Native`.

| Campo | Valor |
|-------|-------|
| Estado | ✅ **Aprobado** |
| Evidencia | [gradle](../img/logs/10-gradle-rama-170802a.log), [reporte JUnit](../img/logs/10-SfLanIpTest-170802a.xml), base: [gradle](../img/logs/00-gradle-base-7ed3253.log) |
| Defecto / decisión | Ninguno. |

---

## 7. Resumen de la ejecución

| Caso | Categoría | Estado |
|------|-----------|--------|
| CP-01 | Ruta feliz | ✅ Aprobado |
| CP-02 | Límite | ✅ Aprobado |
| CP-03 | Regresión | ✅ Aprobado |
| CP-04 | Navegación y estado | ✅ Aprobado |
| CP-05 | Accesibilidad | ✅ Aprobado (con limitación de TalkBack anotada) |
| CP-06 | Entorno / idioma | ✅ Aprobado |
| CP-07 | Unitaria | ✅ Aprobado |

No hubo fallos atribuibles al cambio, así que no hubo re-ejecuciones por corrección.
El SHA probado (`170802a`) es el último commit con cambios de comportamiento de la
rama. Ver la relación con el SHA final en el [README](../README.md#shas).
