import math     #Lo necesitamos para hacer el cuadrado de un numero o raiz cuadrada de un numero, asi tambien validamos NAN o infinitos que rompen todo no se porque


def vrms_teorico(vpp):
    if vpp is None or isinstance(vpp, bool) or not isinstance(vpp, (int, float)):  #Esto es para verificar que el vpp es un numero real positivo, no puede ir solo bool porque es subclase de int 
        return None
    if math.isnan(vpp) or math.isinf(vpp) or vpp <= 0:
        return None

    vp = vpp / 2.0   #  Fórmula de onda senoidal: primero pasamos de pico-a-pico a pico (vp) y dividimos por raíz de 2
    return vp / math.sqrt(2)


def coincide(medido, teorico, tolerancia=0.02):  # Si alguno de los dos valores vino en None o teorico es 0, devolvemos False para no dividir por cero
    if medido is None or teorico is None:
        return False
    if not isinstance(medido, (int, float)) or not isinstance(teorico, (int, float)):
        return False
    if teorico == 0:
        return False

    error_relativo = abs(medido - teorico) / abs(teorico)  # Calculamos el error relativo porcentual y verificamos que esté dentro del 2% permitido
    return error_relativo <= tolerancia


def verificar_canal(filas, canal):
    vpp = None
    vrms_medido = None

    for fila in filas:                      #Buscamos en la lista del barrido (Ej 6) las filas de este canal para extraer PKPK y CYCRMS
        if fila.get("canal") == canal:
            if fila.get("magnitud") == "PKPK":
                vpp = fila.get("valor")
            elif fila.get("magnitud") == "CYCRMS":
                vrms_medido = fila.get("valor")

    teorico = vrms_teorico(vpp)
    ok = coincide(vrms_medido, teorico)

    return {
        "canal": canal,
        "vpp": vpp,
        "vrms_medido": vrms_medido,
        "vrms_teorico": teorico,
        "coincide": ok,
    }


# --- Pruebas ---
# 1. Cálculo teórico nominal (2 Vpp -> ~0.7071 Vrms)
teorico_2v = vrms_teorico(2.0)
assert teorico_2v is not None
assert abs(teorico_2v - 0.70710678) < 1e-6
assert vrms_teorico(-5.0) is None
assert vrms_teorico(0) is None
assert vrms_teorico(None) is None

# 2. Tolerancia relativa (2% por defecto)
assert coincide(0.709, 0.7071) is True
assert coincide(1.0, 0.7071) is False

# 3. Verificación de canal con señal senoidal real (debe coincidir)
barrido_senoidal = [
    {"canal": "CH1", "magnitud": "FREQ", "unidad": "Hz", "crudo": "1.000E+03", "valor": 1000.0},
    {"canal": "CH1", "magnitud": "PKPK", "unidad": "V", "crudo": "2.005E+00", "valor": 2.005},
    {"canal": "CH1", "magnitud": "CYCRMS", "unidad": "V", "crudo": "7.090E-01", "valor": 0.709},
]
res_seno = verificar_canal(barrido_senoidal, "CH1")
assert res_seno["coincide"] is True

# 4. LA PRUEBA CLAVE DEL PDF: Señal cuadrada de 2 Vpp y 1 Vrms (NO debe coincidir)
barrido_cuadrada = [
    {"canal": "CH1", "magnitud": "PKPK", "unidad": "V", "crudo": "2.000E+00", "valor": 2.0},
    {"canal": "CH1", "magnitud": "CYCRMS", "unidad": "V", "crudo": "1.000E+00", "valor": 1.0},
]
res_cuadrada = verificar_canal(barrido_cuadrada, "CH1")
assert res_cuadrada["coincide"] is False

# 5. Caso raro: canal inexistente en el barrido
res_inexistente = verificar_canal(barrido_senoidal, "CH2")
assert res_inexistente["coincide"] is False
assert res_inexistente["vrms_teorico"] is None

print("pruebas OK")