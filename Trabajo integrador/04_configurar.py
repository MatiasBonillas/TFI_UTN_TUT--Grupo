import importlib                                                       #Importo los ejercicios del 3, para que sea mas rapido, no se si en el PDF se permitia :ppp


def comandos_de_canal(canal, display, acoplamiento, sonda, escala):    #Validamos que en el osciloscopio este CH1 y CH2, si aparece un CH3 de la nada le devolvemos NONE
    if canal not in ("CH1", "CH2"):
        return None

    return [                                       #Aca va a estar una lista con un orden prolijo de mostrar, con 4 SCPI como dice el PDF, f-string es para insertar el canal en cada parametro
        f":{canal}:DISPlay {display}",
        f":{canal}:COUPling {acoplamiento}",
        f":{canal}:PROBe {sonda}",
        f":{canal}:SCALe {escala}",
    ]


# --- Pruebas ---
esperado_ch1 = [
    ":CH1:DISPlay ON",
    ":CH1:COUPling DC",
    ":CH1:PROBe 10X",
    ":CH1:SCALe 1v",
]
assert comandos_de_canal("CH1", "ON", "DC", "10X", "1v") == esperado_ch1      #Tendria que rechazar los que no existen o tienen espacios vacios como NONE
assert comandos_de_canal("CH3", "ON", "DC", "10X", "1v") is None
assert comandos_de_canal("", "ON", "DC", "10X", "1v") is None

# Prueba cruzada: verificar que todos los comandos generados pasen validar() del ejercicio 3
ej3 = importlib.import_module("03_comandos")
comandos_ch2 = comandos_de_canal("CH2", "OFF", "AC", "1X", "500mv")
assert comandos_ch2 is not None
for cmd in comandos_ch2:
    assert ej3.validar(cmd) is None

print("pruebas OK")