#!/usr/bin/env python3
# usage: ui.py dump | ui.py tap "texto" [n] | ui.py find "texto"
import subprocess,sys,re,xml.etree.ElementTree as ET
def dump():
    subprocess.run(["adb","shell","uiautomator","dump","/sdcard/ui.xml"],capture_output=True)
    x=subprocess.run(["adb","shell","cat","/sdcard/ui.xml"],capture_output=True,text=True).stdout
    return ET.fromstring(x[x.index("<"):])
def nodes(root):
    for n in root.iter("node"):
        b=list(map(int,re.findall(r"\d+",n.get("bounds"))))
        yield n,b
cmd=sys.argv[1]; root=dump()
if cmd=="dump":
    for n,b in nodes(root):
        t=n.get("text") or n.get("content-desc")
        if t or n.get("clickable")=="true":
            print(b, repr(t), "click" if n.get("clickable")=="true" else "", "enabled="+n.get("enabled"), n.get("class").split(".")[-1])
else:
    q=sys.argv[2].lower(); idx=int(sys.argv[3]) if len(sys.argv)>3 else 0
    hits=[(n,b) for n,b in nodes(root) if q in ((n.get("text") or "")+" "+(n.get("content-desc") or "")).lower()]
    if not hits: print("NOT FOUND",q); sys.exit(1)
    n,b=hits[idx]; x=(b[0]+b[2])//2; y=(b[1]+b[3])//2
    if cmd=="tap": subprocess.run(["adb","shell","input","tap",str(x),str(y)])
    print(cmd,repr(n.get("text") or n.get("content-desc")),x,y,"enabled="+n.get("enabled"))
