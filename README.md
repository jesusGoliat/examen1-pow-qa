# Primer examen parcial — Pull Request con QA en PolitecnicoOpenWorld

## Portada

- **Nombre:** Jesús Ángel González Arellano
- **Usuario de GitHub:** [jesusGoliat](https://github.com/jesusGoliat)
- **Grupo:** 7CV4
- **Asignatura:** Desarrollo de aplicaciones móviles nativas
- **Profesor:** Gabriel Hurtado Avilés
- **Periodo:** 2027-1
- **Fecha de entrega:** jueves 1 de octubre de 2026

*(La boleta y los datos de identificación escolar quedan en Classroom, como pide el enunciado.)*

---

## Enlaces principales

| Elemento | Enlace |
|----------|--------|
| **Pull Request** (Draft → Ready for review) | [gabrielhuav/PolitecnicoOpenWorld#172](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/172) |
| Issue | [jesusGoliat/PolitecnicoOpenWorld#1](https://github.com/jesusGoliat/PolitecnicoOpenWorld/issues/1) |
| Rama de trabajo | [`jesusGoliat:fix/sf-lan-ip-validation`](https://github.com/jesusGoliat/PolitecnicoOpenWorld/tree/fix/sf-lan-ip-validation) |
| Matriz y fichas de pruebas | [docs/pruebas.md](docs/pruebas.md) |
| Hallazgos y dictamen | [docs/hallazgos.md](docs/hallazgos.md) |
| Checks de CI | [docs/ci.md](docs/ci.md) |
| Entorno y preparación | [docs/entorno.md](docs/entorno.md) |
| Bitácora y uso de IA | [docs/bitacora.md](docs/bitacora.md) |
| Evidencias (capturas y logs) | [img/](img) |

---

## Estructura del repositorio

```text
README.md          Índice de la entrega (este archivo)
docs/pruebas.md    Criterios, riesgos, matriz, referencia en la base y fichas CP-01..CP-07
docs/hallazgos.md  Defectos encontrados (H-01..H-04) y dictamen de calidad
docs/ci.md         Checks del workflow PR Quality Gate, resultados e interpretación
docs/entorno.md    SO, JDK, SDK, AVD, pasos de preparación y datos de prueba
docs/bitacora.md   Línea de tiempo, commits, casos ejecutados, revisión y uso de IA
img/               Capturas NN-cpXX-*.png (00–09 = base, 20+ = rama)
img/logs/          Salidas de Gradle, detekt, logcat, listener y extractos de CI
tools/             Scripts ADB usados para ejecutar los casos (nav.sh, ip.py, ui.py, listener.py)
```

---

## Equipo

| Integrante | Usuario de GitHub | PR | Bitácora |
|------------|-------------------|----|----------|
| Jesús Ángel González Arellano | [jesusGoliat](https://github.com/jesusGoliat) | [#172](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/172) | [bitacora.md](docs/bitacora.md) |

El examen es individual: cada integrante del equipo entrega su propio PR.

---

## Objetivo y alcance

**Objetivo.** Corregir un defecto pequeño y comprobable de POW y llevarlo a revisión
con un QA reproducible.

**Defecto.**
- **Dónde:** en «★ Titulación por Combate ★ → Otros modos → Multijugador → Servidor local», el campo «IP del anfitrión».
- **Qué pasaba:** el botón **UNIRSE / JOIN** se habilitaba con sólo contar tres puntos. Valores como `1.2.3.`, `999.1.1.1` o `a.b.c.d` lanzaban tres intentos de conexión imposibles y terminaban en un error de red engañoso.

**Cambio** (3 archivos, una sola intención):
- `SfLanIp.kt` (nuevo, `shared/commonMain`). Contiene `esIpv4Valida`: 4 octetos decimales entre 0 y 255, sin ceros a la izquierda. También contiene `filtrarEntrada`: sólo dígitos y puntos, máximo 15 caracteres.
- `SfLanIpTest.kt` (nuevo, `shared/commonTest`): 12 pruebas unitarias.
- `SfOnlineOverlays.kt`: el campo usa el filtro, y el botón usa la validación en `enabled` y en `onClick`.

**Fuera de alcance:**
- el campo de código de sala,
- la lógica de descubrimiento y conexión LAN/WebRTC,
- IPv6,
- los defectos preexistentes H-02 a H-04.

| Criterio | Descripción | Resultado |
|----------|-------------|-----------|
| CA1 (éxito) | Una IPv4 válida habilita UNIRSE y se inicia la conexión | ✅ CP-01, CP-06 |
| CA2 (límite) | Un valor inválido deja UNIRSE deshabilitado y no se intenta conectar | ✅ CP-02, CP-06, CP-07 |

---

## SHAs

| Qué | SHA |
|-----|-----|
| Base (`gabrielhuav/PolitecnicoOpenWorld@main`) | [`7ed325393f82872c2be94ff2ada46948efa19152`](https://github.com/gabrielhuav/PolitecnicoOpenWorld/commit/7ed325393f82872c2be94ff2ada46948efa19152) |
| Probado (QA manual y local) | [`170802a5898f0c7b1d7d145df28fc1a035e27d29`](https://github.com/jesusGoliat/PolitecnicoOpenWorld/commit/170802a5898f0c7b1d7d145df28fc1a035e27d29) |
| **Final entregado del PR** | **`170802a5898f0c7b1d7d145df28fc1a035e27d29`**: el mismo SHA que se probó. No hay commits posteriores en la rama del PR. |

Los commits posteriores al QA están **sólo en este repositorio de entrega** y **sólo
cambian documentación**. El comportamiento de la app que se entrega es exactamente el
del SHA probado.

---

## Matriz de pruebas (resumen)

| ID | Categoría | Qué se verificó | Estado | Evidencia |
|----|-----------|-----------------|--------|-----------|
| CP-01 | Ruta feliz | `192.168.0.10`, `255.255.255.255`, `0.0.0.0` y `10.0.2.2` habilitan JOIN; conexión TCP real a `10.0.2.2:47645` (`BT_HELLO` recibido) | ✅ | [32](img/32-cp01-rama-join-10.0.2.2-resultado.png), [logcat](img/logs/32-cp01-rama-logcat-join-10.0.2.2.txt) |
| CP-02 | Límite | Vacío, `1.2.3.`, `999.1.1.1`, `256.1.1.1`, `1.2.3.4.5`, `01.2.3.4`, letras: JOIN deshabilitado y 0 intentos de conexión | ✅ | antes [03](img/03-base-ip-1.2.3.-join-habilitado.png) / después [23](img/23-cp02-rama-ip-1.2.3.-join-deshabilitado.png) |
| CP-03 | Regresión | Crear servidor, Cancelar, código de sala | ✅ | [34](img/34-cp03-rama-crear-servidor.png), [35](img/35-cp03-rama-codigo-sala-AB1C.png) |
| CP-04 | Navegación y estado | Home → volver, Atrás, reabrir, recreación de la actividad (la orientación está fija en horizontal) | ✅ | [41](img/41-cp04-rama-regreso-conserva-ip.png), [44](img/44-cp04-rama-recreacion-actividad.png) |
| CP-05 | Accesibilidad | Fuente 1.3, árbol de accesibilidad, TalkBack (con limitación) | ✅ | [51](img/51-cp05-rama-fuente-1.3-ip-valida.png), [nodos](img/logs/53-cp05-rama-nodos-accesibilidad.txt) |
| CP-06 | Entorno | Mismo recorrido con la app en español | ✅ | [60](img/60-cp06-rama-es-ip-valida.png), [61](img/61-cp06-rama-es-ip-invalida.png) |
| CP-07 | Unitaria | `SfLanIpTest` 12/12; `:app` 125 y `:shared` 229 pruebas, 0 fallos | ✅ | [reporte](img/logs/10-SfLanIpTest-170802a.xml) |

El detalle de cada caso (autor, fecha, SHA, dispositivo, precondiciones, pasos,
esperado, real, estado, evidencia y decisión) está en [docs/pruebas.md](docs/pruebas.md).

---

## Checks

| Check | Estado | Nota |
|-------|--------|------|
| PR Quality Gate en el PR #172 | ⏸️ `action_required` | Requiere la aprobación del mantenedor (bloqueo externo, [run](https://github.com/gabrielhuav/PolitecnicoOpenWorld/actions/runs/36892877520)). |
| detekt (espejo en el fork) | ✅ | [run 36892975028](https://github.com/jesusGoliat/PolitecnicoOpenWorld/actions/runs/36892975028) |
| unit-tests (espejo en el fork) | ❌ preexistente | Falla al compilar porque el fork no tiene `MAPS_API_KEY`. Se reproduce igual en la base sin mis cambios (H-02). |
| Build + pruebas + detekt locales | ✅ | Mismo comando y misma CLI que el workflow. |

La interpretación completa está en [docs/ci.md](docs/ci.md).

---

## Revisión

| Rol | Enlace | Estado |
|-----|--------|--------|
| Revisión recibida en mi PR (compañero de equipo) | [conversación del PR #172](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/172) | Pendiente de solicitar al compañero |
| Observación técnica que hice al [PR #170](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/170) de luisAgt (SHA revisado `b33b0db`) | [mi revisión](https://github.com/gabrielhuav/PolitecnicoOpenWorld/pull/170#pullrequestreview-5382923375) · [copia](docs/revision-pr170.md) · [evidencias](img/revision-pr170) | ✅ Publicada |

---

## Hallazgos y dictamen

| ID | Hallazgo | Estado |
|----|----------|--------|
| H-01 | JOIN por LAN acepta IPs mal formadas | ✅ Corregido |
| H-02 | `MAPS_API_KEY` vacío rompe el build y el CI en forks; `gradle-wrapper.jar` no está versionado | Preexistente |
| H-03 | Mensaje de error LAN en español con la UI en inglés | Preexistente, pendiente |
| H-04 | La IP más larga no se ve completa con fuente 1.3 | Preexistente, pendiente |

**Dictamen:** recomiendo integrar el PR. Los dos criterios se observaron en el
dispositivo, no hubo regresiones en los flujos cercanos y la regla tiene pruebas
unitarias.

**Riesgos que quedan:**
- no se jugó una partida LAN completa entre dos teléfonos,
- la prueba con TalkBack fue parcial,
- el CI del repositorio original no ha corrido por falta de aprobación.

Ver [docs/hallazgos.md](docs/hallazgos.md).

---

## Conclusiones

Antes de este examen pensaba en el QA como «probar que funciona» al final. Lo que
más me sirvió fue escribir los criterios y los riesgos **antes** de tocar el código.
Así supe exactamente qué capturar en la versión base, y la comparación antes/después
salió casi sola.

Lo que más me sorprendió fue que los dos problemas más difíciles no estaban en mi
cambio sino en el entorno:
- `./gradlew` no funciona en un clon limpio.
- Una `MAPS_API_KEY` vacía rompe la compilación, aunque el propio workflow dice que es válida.

Eso me obligó a separar con evidencia lo que es preexistente de lo que introduce el PR.
Por ejemplo, reproduje el fallo del CI en el commit base para no culpar a mi cambio
ni ocultar el check.

También aprendí que un caso de «ruta feliz» de red se puede demostrar sin dos
teléfonos: con un listener TCP en la laptop y la IP `10.0.2.2` del emulador. Además,
mover la regla a una función pura hizo que las pruebas unitarias fueran triviales.

---

## Referencias (APA)

- Android Developers. (s.f.). *Android Debug Bridge (adb)*. https://developer.android.com/tools/adb
- Android Developers. (s.f.). *Logcat command-line tool*. https://developer.android.com/tools/logcat
- Android Developers. (s.f.). *Make apps more accessible*. https://developer.android.com/guide/topics/ui/accessibility/apps
- detekt. (s.f.). *detekt – Static code analysis for Kotlin*. https://detekt.dev/
- GitHub. (s.f.). *Approving workflow runs from public forks*. https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/approving-workflow-runs-from-public-forks
- Hurtado Avilés, G. (2026). *PolitecnicoOpenWorld* [Repositorio de código]. GitHub. https://github.com/gabrielhuav/PolitecnicoOpenWorld
- Postel, J. (Ed.). (1981). *Internet Protocol* (RFC 791). IETF. https://www.rfc-editor.org/rfc/rfc791
