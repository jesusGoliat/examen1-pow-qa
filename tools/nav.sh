#!/bin/bash
# Lleva la app desde cero hasta el campo de IP LAN.
S=$(dirname "$0")
wait_tap(){ for i in $(seq 1 20); do $S/ui.py tap "$1" >/dev/null 2>&1 && return 0; sleep 1.5; done; echo "no apareció: $1"; exit 1; }
wait_find(){ for i in $(seq 1 20); do $S/ui.py find "$1" >/dev/null 2>&1 && return 0; sleep 1.5; done; echo "no apareció: $1"; exit 1; }
adb shell am force-stop ovh.gabrielhuav.pow; sleep 1
adb shell monkey -p ovh.gabrielhuav.pow -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1
wait_tap "TITULACIÓN POR COMBATE ★"
wait_tap "↕"
sleep 1; adb shell input swipe 1110 950 1110 300 400; sleep 1
wait_find "← "
$S/ui.py tap "MULTIPLAYER" >/dev/null 2>&1 || $S/ui.py tap "MULTIJUGADOR" >/dev/null
sleep 2; adb shell input swipe 1110 900 1110 200 500; sleep 1
echo "listo"
