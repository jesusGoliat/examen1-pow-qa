@Javier-Gamez thanks for the review, and for checking the `&&` ordering in `esOctetoValido`. Answering your note:

> `onClick = { if (SfLanIp.esIpv4Valida(lanIp)) onLanJoin(lanIp) }` re-checks validity that `enabled` already guarantees

**Agreed, it is redundant today.** I checked `PowButton` (`shared/src/commonMain/kotlin/ovh/gabrielhuav/pow/ui/components/PowButton.kt:29-31`): it forwards `enabled` straight to Material3 `Button(onClick = onClick, enabled = enabled, …)`, so a disabled button never invokes `onClick`. This was also observed on device in CP-02: tapping the disabled JOIN with `1.2.3.` produced **0** `SF-NET` log lines ([logcat](https://github.com/jesusGoliat/examen1-pow-qa/blob/9c80bed/img/logs/24-cp02-rama-logcat-tap-deshabilitado.txt)).

**Decision: keep it, no code change.** Three reasons:
1. **It preserves the original structure.** Before this PR, `onClick` already had its own guard (`if (lanIp.contains('.'))`). I only made it consistent with `enabled`, so the button stays safe if someone later changes `PowButton` (e.g. a custom clickable).
2. **It costs nothing.** It is one pure call on a string of at most 15 characters.
3. **It keeps the QA valid.** Removing it would change the tested code after QA was completed on `170802a`, and every manual case would have to be re-run for a purely cosmetic change.

The head stays at `170802a`, so the tested SHA is still the delivered SHA.
