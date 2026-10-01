# Listener TCP de prueba en el puerto LAN de POW: sólo registra conexiones entrantes.
import socket,datetime,sys
s=socket.socket(); s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1); s.bind(("0.0.0.0",47645)); s.listen(5)
print("escuchando 0.0.0.0:47645",flush=True)
while True:
    c,a=s.accept(); c.settimeout(5)
    try: d=c.recv(200)
    except Exception: d=b""
    print(datetime.datetime.now().strftime("%H:%M:%S"),"conexion desde",a,"bytes:",d[:80],flush=True); c.close()
