# Entorno y preparación

## Entorno de ejecución

| Elemento | Valor |
|----------|-------|
| Sistema operativo | Ubuntu 24.04.5 LTS (kernel 6.17.0-40-generic), x86_64, 4 núcleos, 7.6 GiB RAM |
| Android Studio | Ladybug 2024.2.1 (build AI-242.23339.11.2421.12550806) — **sólo como referencia**: no soporta AGP 9.3, por eso se compiló por consola |
| JDK | Amazon Corretto 21.0.12.1 (el workflow de CI usa Temurin 21) |
| Gradle | 9.5.0 (wrapper del proyecto) |
| AGP / Kotlin | 9.3.0 / 2.3.21 (sin cambios, tal como vienen en `libs.versions.toml`) |
| Android SDK | platforms 34, 35, 36; build-tools 36.0.0; platform-tools 37.0.1; emulator 37.1.11 |
| `compileSdk` / `minSdk` / `targetSdk` | 36 / 24 / 36 |
| Dispositivo | Emulador AVD **Pixel_3a_API_33**: Android 13 (API 33), imagen `google_apis_playstore` x86_64 rev. 9, 1080×2220 px, 440 dpi, 2 GB RAM |
| Idioma del dispositivo | Inglés (en-US) por defecto; CP-06 se ejecuta en español (es-MX) |
| Red | Wi-Fi virtual del emulador (`10.0.2.15/16`); la laptop es `10.0.2.2` |
| App | `ovh.gabrielhuav.pow`, `versionName 1.0.0.18`, `versionCode 12`, variante `debug` |

## Pasos de preparación (reproducibles)

```bash
# 1. Fork y clon (blobless: el repo pesa >1 GB con assets)
gh repo fork gabrielhuav/PolitecnicoOpenWorld --clone=false
git clone --filter=blob:none https://github.com/jesusGoliat/PolitecnicoOpenWorld.git POW-fork
cd POW-fork && git remote add upstream https://github.com/gabrielhuav/PolitecnicoOpenWorld.git
git log --oneline -1          # 7ed3253 = SHA base

# 2. Archivos que NO vienen en git (están en .gitignore a propósito)
cd PolitecnicoOpenWorld
echo "MAPS_API_KEY=DEFAULT_API_KEY" > secrets.properties   # marcador no secreto
echo "sdk.dir=$HOME/Android/Sdk"    > local.properties
#    gradle-wrapper.jar: regenerarlo y revertir los archivos versionados
gradle wrapper --gradle-version 9.5.0
git checkout -- gradlew gradlew.bat gradle/wrapper/gradle-wrapper.properties

# 3. Compilar y probar (mismo comando que el CI)
./gradlew :app:assembleDebug :app:testDebugUnitTest :shared:testAndroidHostTest --stacktrace

# 4. Emulador e instalación
emulator -avd Pixel_3a_API_33 -no-snapshot-load -no-boot-anim -no-audio &
adb wait-for-device
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

`google-services.json` no se crea: sin él, el plugin de Firebase no se aplica y
la app corre en «Local mode (no account)», igual que en el CI.

### Problemas de preparación encontrados (preexistentes, no del cambio)

1. **`./gradlew` falla en un clon limpio** con
   `Could not find or load main class org.gradle.wrapper.GradleWrapperMain`,
   porque `gradle/wrapper/gradle-wrapper.jar` está en `.gitignore`. El CI no lo nota
   porque llama a `gradle` directamente. La solución está documentada en
   `README for IAS/SETUP_PC_NUEVA.md §2.1`. Evidencia:
   [00-gradlew-preexistente.log](../img/logs/00-gradlew-preexistente.log).
2. **`MAPS_API_KEY=` vacío rompe la compilación** con
   `BuildConfig.java:14: error: illegal start of expression`
   (`MAPS_API_KEY = ;`), aunque el comentario del workflow dice que «vacío es
   válido». También está documentado en `SETUP_PC_NUEVA.md §2.2`; se usa el
   marcador `DEFAULT_API_KEY`.

Ninguno de los dos se corrige en este PR: están fuera de su alcance. Se registran en
[hallazgos.md](hallazgos.md).

## Datos de prueba

- Las direcciones IP son ficticias, privadas o de la red virtual del emulador:
  `192.168.0.10`, `10.0.2.2`, `1.2.3.`, `999.1.1.1`, `256.1.1.1`, `a.b.c.d`,
  `01.2.3.4`, `1.2.3.4.5`.
- **Anfitrión simulado para la ruta feliz:** un *listener* TCP en la laptop, en el
  puerto LAN del juego (47645), que sólo registra las conexiones entrantes
  ([listener.py](../tools/listener.py)). Desde el emulador, `10.0.2.2` apunta a la
  laptop. Esto demuestra que **se inicia la conexión** a la IP tecleada (CA1). No
  demuestra una partida completa, que requiere otro dispositivo con POW.
- No se usan cuentas, contraseñas ni claves. `secrets.properties`,
  `local.properties` y el APK no se suben.

## Automatización de la ejecución

Los recorridos se ejecutaron con ADB desde scripts sencillos, guardados en
[`tools/`](../tools):

- `nav.sh`: abre la app y llega al campo de IP.
- `ip.py`: escribe en el campo y lee el estado `enabled` del botón JOIN con `uiautomator dump`.
- `ui.py`: toca elementos por su texto.

Las capturas se tomaron con `adb exec-out screencap -p` y los logs con
`adb logcat -s SF-NET:*`.
