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
«Titulación por Combate» → «Multijugador» → sección LAN («…o únete tecleando la IP»).

**Datos de prueba (ficticios):** direcciones privadas o de documentación sin host
real; no se usan cuentas ni credenciales.

---

## 5. Fichas de casos

Las fichas se completan tras la ejecución.
