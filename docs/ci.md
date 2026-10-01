# Verificaciones automáticas (CI)

Workflow consultado: `.github/workflows/pr-quality-gate.yml` en el commit base `7ed3253`.

Se activa en `pull_request` hacia `main` (`opened`, `synchronize`, `reopened`) cuando el PR toca `PolitecnicoOpenWorld/**`.

## Qué comprueba cada job

| Job / paso | Qué verifica | Qué queda fuera |
|------------|--------------|-----------------|
| `unit-tests` → «Nombres de test compatibles con Kotlin/Native» (`tools/check_kmp_test_names.sh`) | Que ningún nombre de test entre backticks tenga `(`, `)` o `,`, porque esos nombres rompen la compilación de iOS. | No compila iOS: sólo es un `grep`. |
| `unit-tests` → `gradle :app:assembleDebug` | Que la app compile, el grafo de Hilt y el merge de manifest y recursos. | Firma, AAB, release y el comportamiento en un dispositivo. |
| `unit-tests` → `:app:testDebugUnitTest :shared:testAndroidHostTest` | La lógica pura en JVM. | La UI de Compose, la red real, los permisos, Firebase y Maps. Corre sin `google-services.json` y con `MAPS_API_KEY` del secret, así que no demuestra que mapas o servicios externos funcionen. |
| `detekt` (CLI 1.23.8, `detekt.yml` + `baseline.xml`, `maxIssues: 0`) | Análisis estático de `app/src/main/java` y `shared/src/commonMain/kotlin`. Bloquea cualquier issue nuevo. | El código de pruebas, `androidMain` e `iosMain`. La deuda anterior queda en el baseline. |

El CI complementa el QA manual pero no lo reemplaza: ninguno de los jobs ejecuta la
app ni toca la pantalla modificada.

## Resultados

| Verificación | Dónde | SHA | Estado | Liga |
|--------------|-------|-----|--------|------|
| PR Quality Gate (PR #172 al original) | `gabrielhuav/PolitecnicoOpenWorld` | `170802a` | ⏸️ **`action_required`**: GitHub exige que el mantenedor apruebe los workflows de contribuidores nuevos. No se ejecutó ningún job. | [run 36892877520](https://github.com/gabrielhuav/PolitecnicoOpenWorld/actions/runs/36892877520) |
| `detekt` (espejo en el fork) | `jesusGoliat/PolitecnicoOpenWorld` PR #2 | `170802a` | ✅ success (1 m) | [job 110472892791](https://github.com/jesusGoliat/PolitecnicoOpenWorld/actions/runs/36892975028/job/110472892791) · [extracto](../img/logs/14-ci-fork-detekt-run36892975028.txt) |
| `unit-tests` → nombres KMP (espejo) | fork PR #2 | `170802a` | ✅ success | [job 110472893154](https://github.com/jesusGoliat/PolitecnicoOpenWorld/actions/runs/36892975028/job/110472893154) |
| `unit-tests` → build + tests (espejo) | fork PR #2 | `170802a` | ❌ failure en `:app:compileDebugJavaWithJavac`: `MAPS_API_KEY = ;` | mismo job · [extracto](../img/logs/13-ci-fork-unit-tests-run36892975028.txt) |
| Build + tests local (mismo comando del workflow) | Laptop, JDK 21, Gradle 9.5.0 | `170802a` | ✅ BUILD SUCCESSFUL. `:app` 125/125, `:shared` 229/229 | [log](../img/logs/10-gradle-rama-170802a.log) |
| detekt local (misma CLI, config y baseline) | Laptop | `170802a` | ✅ exit 0, sin issues nuevos | [log](../img/logs/11-detekt-rama-170802a.log) |
| Nombres KMP local | Laptop | `170802a` | ✅ | ver CP-07 en [pruebas.md](pruebas.md) |

## Interpretación

1. **El PR al repositorio original está bloqueado por una causa externa.** Como es la primera contribución de esta cuenta, GitHub pide la aprobación del mantenedor para correr el workflow, y no puedo darla yo. Lo registro como bloqueo externo, **no** como prueba aprobada.
2. **CI espejo en el fork.**
   - Para tener al menos una ejecución real del workflow, abrí un PR **sólo dentro del fork** ([jesusGoliat/PolitecnicoOpenWorld#2](https://github.com/jesusGoliat/PolitecnicoOpenWorld/pull/2), marcado «CI mirror – do not merge»). Corre el mismo `pr-quality-gate.yml` sobre el mismo SHA.
   - Este PR **no** sustituye al PR del examen.
3. **El fallo de `unit-tests` en el fork es preexistente y no lo causa el cambio.**
   - El fork no tiene el secret `MAPS_API_KEY`, así que el workflow escribe `MAPS_API_KEY=` vacío y la compilación de `BuildConfig` falla antes de correr cualquier prueba.
   - El mismo fallo se reproduce en el commit base `7ed3253` sin ninguno de mis cambios ([log](../img/logs/12-base-maps-key-vacia.log)). Ver [H-02](hallazgos.md#h-02--maps_api_key-vacío-rompe-la-compilación-y-el-ci-en-forks).
   - No desactivé el check ni cambié el workflow: corregirlo es otro alcance.
4. **Validación posible.** El mismo comando del job (`assembleDebug` + las dos tareas de pruebas) y la misma CLI de detekt pasan en local con `MAPS_API_KEY=DEFAULT_API_KEY`, que es el marcador que documenta el propio proyecto.
5. **Prueba automatizada agregada.** La lógica modificada se pudo aislar en `SfLanIp`, así que se agregó `SfLanIpTest` con 12 casos. Corre dentro de `:shared:testAndroidHostTest`, la tarea que ejecuta el gate.
