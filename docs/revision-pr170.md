Technical review of `b33b0dbf66e387db1c5ac0c282f44fada7ddcb6b` (head of `fix-audio`). I read the full diff and **built and ran this exact SHA**:
- Built locally with `./gradlew :app:assembleDebug :app:testDebugUnitTest :shared:testAndroidHostTest`: **BUILD SUCCESSFUL**, no test failures.
- Installed the debug APK on an emulator (Pixel 3a, API 33) and played *Titulación por Combate → Other modes → AI vs AI* (Estudiante vs Estudianta) with audio on.
- **Reproduced AC:** the victory/lose effect was heard when the match ended (end menu shown), and not at the end of round 1. 👍

Observations, from most to least important:

**1. The Gradle wrapper commit is out of scope and doesn't fix the wrapper** (`gradlew`, `gradlew.bat`, `gradle/wrapper/gradle-wrapper.properties`)
- `gradlew` and `gradlew.bat` are fully regenerated: +150/−235 lines, from an older template (e.g. it adds `--add-opens java.base/java.lang=ALL-UNNAMED` and drops `DEFAULT_JVM_OPTS='"-Xmx64m" "-Xms64m"'`).
- `networkTimeout=10000` and `validateDistributionUrl=true` are removed from `gradle-wrapper.properties`.
- `gradle-wrapper.jar` is still git-ignored, so on a clean clone of this SHA `./gradlew --version` still fails with `Could not find or load main class org.gradle.wrapper.GradleWrapperMain`.
- `README for IAS/SETUP_PC_NUEVA.md §2.1` documents exactly this case: regenerate the wrapper locally, then `git checkout -- gradlew gradlew.bat gradle/wrapper/gradle-wrapper.properties`.
- The `//noinspection WrongGradleMethod` line in `app/build.gradle.kts` is also unrelated to the audio fix.

**Recommendation:** revert these files in a new commit, so the PR keeps a single intention (audio).

**2. QA videos are shipped inside the APK** (`app/src/main/assets/DOCS/*.mp4`)
Everything under `src/main/assets` is packaged.
- The four `old_*/new_*` recordings add 7.6 MB.
- The debug APK grows from 400,101,003 to 408,756,146 bytes (+8.65 MB) compared with base `7ed3253`.
- No code references `DOCS/`.

**Recommendation:** keep the videos only as PR attachments (they already are) and remove them from `assets/`.

**3. Duplicate, unused sound files** (`assets/STREETFIGHTER/SOUNDS/{lose,victory,start_round}_effect.mp3`)
`SoundManager` loads only the `AUDIO/` copies, and no code references the `STREETFIGHTER/SOUNDS/` ones. That is ~350 KB of dead assets. **Recommendation:** remove them.

**4. Round-end vs match-end trigger, please confirm** (`StreetFighterScreenAndroid.kt`, `LaunchedEffect(state.battleEnded, state.winnerIndex)`)
- The comment says "Sonido al finalizar el combate completo". However, `StreetFighterState.battleEnded` is documented as *"fin de RONDA … el combate sigue si nadie llegó a 2"*, and `endRound()` sets `battleEnded = true` + `winner` on **every** round. `resetRound()` puts them back to `false`/`null`.
- In my run it was only heard at match end, but from the code the effect could fire after round 1 as well.
- **Recommendation:** key the effect on `state.showEndMenu`, which is only true once the match is decided. Alternatively, explain why the round-end case can't happen.
- Relatedly, `winnerIndex == 0` is assumed to be "the player". In *AI vs AI* that is just CPU #1, and as an online guest the local player may not be index 0.

**5. Minor**
- `previousRoundNumber` is written but never read. It can be dropped together with the `rememberSaveable`/`setValue` imports.
- The description says the PR *"Removed strict `loadedSounds` guard"*, and Risk/rollback says to *"Revert the modified methods … back to checking `soundId in loadedSounds`"*. In fact, the three `play*` methods are **new** and no existing guard was modified.
- Because the new sounds are never in `loadedSounds`, a `play()` issued before the async load completes will still be silently dropped. That is fine in practice, because `SoundManager` is created long before a fight starts, but the description should say so.

**Verdict:** the audio behavior works in my test (✅ match-end effect). I'd recommend addressing 1–3 before merging (scope and APK size), and confirming 4.
