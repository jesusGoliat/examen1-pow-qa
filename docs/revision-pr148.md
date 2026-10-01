Technical review of `92dddec434e79b5dc687e665865baedab9c9080f` (head of `feature/biblioteca-ipn-stage`). I read the diff of `SfStageCatalog.kt` and `SfTheme.kt` and checked them against the unlock logic in `SfArcadeRepository.kt`. I then built and ran this exact SHA (`./gradlew :app:assembleDebug` → BUILD SUCCESSFUL), with a clean install on an emulator (Pixel 3a, API 33).

**Reproduced your TC-02 ✅**
- Path: Practice → Estudiante vs Estudianta → Basic → stage selector, on fresh app data.
- All three variants show 🔒: `Biblioteca Nacional IPN`, `(Noche)` and `(Noche 2)`.
- Each tile's clickable container reports `enabled="false"` in `uiautomator dump`.

**Extra case: upgrade path for existing saves ✅**
This is the risk I was most worried about. A player who already beat `POLICIA_GRANADERO_MUJER` before this PR has the CU UNAM family stored in `UNLOCKED_MAPS_V2`, but not the new stage, and the PR says "no data migration involved".
- I wrote that save state into `shared_prefs/pow_sf_arcade.xml` with `run-as`: fighters ESCOM ×3 + `POLICIA_GRANADERO_MUJER`, maps ESCOM + `unam_biblioteca_cu` ×3. Then I reopened the selector.
- Result: the 3 Biblioteca variants are **unlocked**, and CU UNAM **stays unlocked**.
- After the run, `UNLOCKED_MAPS_V2` contains `fondo_biblioteca_ipn_anim`, `_noche_1_anim` and `_noche_2_anim`.
- The reason it works: `SfArcadeRepository.unlockedMaps()` → `ensureMapsSyncedFromFighters()` re-derives every unlocked fighter's home family on each read. So no explicit migration is needed. 👍 It might be worth one line in *Risk / rollback* explaining *why* no migration is needed.

Observations:

**1. Course QA documentation is inside the PR diff** (`docs/pruebas.md` + `docs/evidencia/`)
- These are 31 files (~8.6 MB) added at the root of POW, which has no `docs/` folder on `main`.
- Merging them would permanently add the exam report and screenshots to the project history. Our course instructions also ask to keep the academic report out of the PR diff and link it from a delivery repo or branch instead.
- **Recommendation:** move `docs/` to your delivery repo or an academic branch, and link it from *QA evidence*. The `raw.githubusercontent.com` preview images in the description can point there too.

**2. Outdated counts in `SfStageCatalog.kt`**
- Line 42 still says `16 bases × 3 iluminaciones = 48`, and line 77 says `Los 16 mapas base tienen al menos un peleadór hogar`. With `BIBLIOTECA_IPN` it is now 17 × 3 = 51.
- You did correctly remove `CU UNAM: PAPARAZZI_1 + POLICIA_GRANADERO_MUJER` from the "Compartidos" list.

**3. No automated test for the data change**
- The behavior lives in two separate plain-data lists (`SfStageCatalog.ALL_STAGES` and `SF_CLASSIC_THEME.fullBackgrounds`) plus one mapping. All three are pure and easy to pin in `shared/commonTest`. For example:
  - `homeStage(POLICIA_GRANADERO_MUJER) == BIBLIOTECA_IPN`
  - `unlockableMapsForFighter(POLICIA_GRANADERO_MUJER)` returns the 3 `fondo_biblioteca_ipn*` files
  - every file of `filesForStage(stage)` for each stage in `ALL_STAGES` has an entry in `SF_CLASSIC_THEME.fullBackgrounds`
- The last one would catch a stage added to one list but not the other, which the PR description itself notes are separate.
- Remember to use test names without `(`, `)` or `,` (`tools/check_kmp_test_names.sh`).

**4. Minor**
- The description calls the variants "day/night/apocalypse" in *What changed?* and "day/dusk/night" for `nuevoMaterial17JUL/`. The code labels are `(Noche)` / `(Noche 2)`, consistent with the other stages. Just align the wording.
- The PR is still **Draft** while the description says "ready to integrate". If nothing is blocking, consider marking it *Ready for review*.

**Verdict:** the stage works as described. Locked → unlocked, and the upgrade path for old saves both behave correctly on device. I'd recommend fixing **1** (moving `docs/` out of the diff) before integration. **2–3** are quick follow-ups.
