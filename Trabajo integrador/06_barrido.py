import importlib

ej2 = importlib.import_module("02_magnitudes")


def barrer(instrumento, canales):
    magnitudes = [
        ("FREQ", "FREQuency", "Hz"),
        ("PKPK", "PKPK", "V"),
        ("CYCRMS", "CYCRms", "V"),
    ]

    resultados = []

    for canal in canales:
        for nombre_mag, comando_scpi, unidad in magnitudes:
            consulta = f":MEASUrement:{canal}:{comando_scpi}?"
            crudo = instrumento.preguntar(consulta)
            valor = ej2.a_numero(crudo)

            resultados.append({
                "canal": canal,
                "magnitud": nombre_mag,
                "unidad": unidad,
                "crudo": crudo,
                "valor": valor,
            })

    return resultados


# --- Pruebas ---
# 1. Prueba sin red usando un instrumento de mentira (Mock)
class InstrumentoMentira:
    def preguntar(self, comando):
        if "ERR" in comando or "CH9" in comando:
            return "ERROR: comando desconocido"
        return "1.000000E+03"


falso = InstrumentoMentira()
filas_mock = barrer(falso, ["CH1", "CH2"])
assert len(filas_mock) == 6
assert filas_mock[0] == {
    "canal": "CH1",
    "magnitud": "FREQ",
    "unidad": "Hz",
    "crudo": "1.000000E+03",
    "valor": 1000.0,
}

# Caso raro: si el instrumento responde ERROR, guarda el texto crudo y deja valor en None
filas_error = barrer(falso, ["CH9"])
assert len(filas_error) == 3
assert filas_error[0]["crudo"] == "ERROR: comando desconocido"
assert filas_error[0]["valor"] is None

# 2. Prueba real contra el instrumento virtual corriendo en puerto 5555
ej5 = importlib.import_module("05_cliente")
osc = ej5.Instrumento()
filas_reales = barrer(osc, ["CH1", "CH2"])
osc.cerrar()

assert len(filas_reales) == 6
assert filas_reales[0]["canal"] == "CH1"
assert filas_reales[0]["magnitud"] == "FREQ"
assert filas_reales[0]["valor"] is not None

print("pruebas OK")