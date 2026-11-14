import importlib
import socket


class Instrumento:                                            #Una crea el socket ipv4 a la que se va a conectar, y otra la conexion directa con el instrumento virtual
    def __init__(self, direccion="127.0.0.1", puerto=5555):   #Aca empezamos a usar el instrumento virtual que nos mandaron el Miercoles 11. Nos fija la IP y el puerto en el que se va a quedar escuchando, y para ejecutarlo simplemente en otra consola debemos poner la direccion de la carpeta y el archivo.py
        self.direccion = direccion
        self.puerto = puerto
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.direccion, self.puerto))

    def enviar(self, comando):                             #Limpiamos los espacios sobrantes y la /n al final es obligatoria nos dijo usted en una clase, no se si usted o la seño xD.
        mensaje = comando.strip() + "\n"
        self.sock.sendall(mensaje.encode("utf-8"))

    def preguntar(self, comando):
        self.enviar(comando)
        fragmentos = []
        while True:
            byte = self.sock.recv(1)                     #Y la convierte en bytes porque asi se comunican, si llegase a aparecer un byte vacio dejamos de leer
            if not byte or byte == b"\n":
                break
            fragmentos.append(byte.decode("utf-8"))
        return "".join(fragmentos).strip()

    def cerrar(self):                                    #Cerramos el socket para no dejar conexiones abiertas
        self.sock.close()


# --- Pruebas (Requiere instrumento_virtual.py corriendo en otra terminal) ---
ej1 = importlib.import_module("01_identificacion")

# Prueba con el Osciloscopio ADS3202 (puerto 5555 por defecto)
osc = Instrumento()
respuesta_idn = osc.preguntar("*IDN?")
assert respuesta_idn == "OWON,ADS3202,25470803,V1.2.0"

datos_osc = ej1.parsear_idn(respuesta_idn)
assert datos_osc is not None
assert datos_osc["modelo"] == "ADS3202"

osc.enviar(":CH1:DISPlay ON")
assert osc.preguntar(":CH1:DISPlay?") == "ON"
osc.cerrar()

# Prueba con el Multímetro XDM1041 (puerto 5556)
multimetro = Instrumento("127.0.0.1", 5556)
datos_xdm = ej1.parsear_idn(multimetro.preguntar("*IDN?"))
assert datos_xdm is not None
assert datos_xdm["modelo"] == "XDM1041"
multimetro.cerrar()

print("pruebas OK")