#!/usr/bin/env python3
# ip.py "<texto>"  -> limpia el campo IP (último EditText), escribe el texto y reporta el campo y JOIN
import subprocess,sys,re,time,xml.etree.ElementTree as ET
def sh(*a): return subprocess.run(["adb","shell",*a],capture_output=True,text=True).stdout
def dump():
    sh("uiautomator","dump","/sdcard/ui.xml"); x=sh("cat","/sdcard/ui.xml"); return ET.fromstring(x[x.index("<"):])
def B(n): return list(map(int,re.findall(r"\d+",n.get("bounds"))))
def estado(root):
    eds=[n for n in root.iter("node") if n.get("class").endswith("EditText")]
    ed=max(eds,key=lambda n:B(n)[1]); eb=B(ed)
    txt=[n for n in root.iter("node") if (n.get("text") or "") in ("JOIN","UNIRSE")]
    tb=max(txt,key=lambda n:B(n)[1]) if txt else None
    btn=None
    if tb is not None:
        cx=(B(tb)[0]+B(tb)[2])//2; cy=(B(tb)[1]+B(tb)[3])//2
        for n in root.iter("node"):
            b=B(n)
            if n.get("clickable")=="true" and b[0]<=cx<=b[2] and b[1]<=cy<=b[3] and not n.get("class").endswith("EditText"): btn=n
    return ed,eb,btn
root=dump(); ed,eb,btn=estado(root)
if len(sys.argv)>1:
    sh("input","tap",str((eb[0]+eb[2])//2),str((eb[1]+eb[3])//2)); time.sleep(0.5)
    sh("input","keyevent","KEYCODE_MOVE_END")
    for _ in range(20): sh("input","keyevent","KEYCODE_DEL")
    t=sys.argv[1]
    if t: sh("input","text",t.replace(" ","%s"))
    time.sleep(0.5); sh("input","keyevent","111"); time.sleep(0.8)
    root=dump(); ed,eb,btn=estado(root)
print(f"campo={ed.get('text')!r} JOIN.enabled={btn.get('enabled') if btn is not None else '?'} join_bounds={B(btn) if btn is not None else None}")
