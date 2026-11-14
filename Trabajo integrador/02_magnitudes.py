import math

def a_numero(texto):                #Esta funcion entera sirve para verificar que lo que metimos es un string, en caso contrario devuelve none
    if not isinstance(texto, str):
        return None

    texto_limpio = texto.strip()    #Si es efectivamente un string le limpia los espacios
    if texto_limpio == "":
        return None

    try:                            #Luego, el texto intenta volverlo un float, como nos explico usted un string puede al mismo tiempo contener numero intentamos quedarnos solo con eso.
        valor = float(texto_limpio)   
    except ValueError:                #Si la conversion no se puede hacer porque tiene letras o comas en vez de punto es None
        return None

    if math.isnan(valor) or math.isinf(valor):  #Esto se lleva a cabo siempre y cuando sea NaN o infinito lo que nos dio el osciloscopio, y como no, devuelve None como la mitad de cosas aca
        return None

    return valor


def con_unidad(valor, unidad):
    if valor == 0:
        return f"0 {unidad}"
                                         #Aca fijamos los rangos para los prefijos, como pico, nano, micro, mili, medida normal, kilo, mega, giga
    signo = "-" if valor < 0 else ""
    absoluto = abs(valor)                #Y fijamos que tiene que tener un valor absoluto

    prefijos = [
        (1e-12, "p"),
        (1e-9, "n"),
        (1e-6, "u"),
        (1e-3, "m"),
        (1.0, ""),
        (1e3, "k"),
        (1e6, "M"),
        (1e9, "G"),
    ]

    indice_elegido = 0                         #Aca I va a recorrer la tabla que creamos arriba, y va a elejir el prefijo que le corrresponda segun la magnitud
    for i, (factor, _) in enumerate(prefijos):
        if absoluto / factor >= 1:
            indice_elegido = i

    factor, prefijo = prefijos[indice_elegido]
    escalado = round(absoluto / factor, 3)          #Y una vez asignado su prefijo lo dividimos para quedarnos con un par de decimales, como dijo usted en el PDF al menos 3 decimales

   
    if escalado >= 1000 and indice_elegido < len(prefijos) - 1:     #Esto sirve para evitar los casos bordes como nos advirtio que 999.999 no sea 1000Hz, primero redondeamos para arriba, y luego subimos la escala
        indice_elegido += 1
        factor, prefijo = prefijos[indice_elegido]
        escalado = round(absoluto / factor, 3)

    if escalado.is_integer():                                  #Si ya es entero y no hace falta redondear obviamos los 5498394 cantidad de 0 que a veces suelen tener estas cosas horribles
        numero_formateado = str(int(escalado))
    else:
        numero_formateado = str(escalado)

    return f"{signo}{numero_formateado} {prefijo}{unidad}"  #Armamos la cadena final uniendo el signo, el número, el prefijo de ingeniería y la unidad


# --- Pruebas ---
assert a_numero("1.000000E+03") == 1000.0
assert a_numero("  7.090821E-01 \n") == 0.7090821
assert a_numero("ERROR: comando desconocido") is None
assert a_numero("NaN") is None
assert a_numero("") is None

assert con_unidad(1000.0, "Hz") == "1 kHz"
assert con_unidad(2500.0, "Hz") == "2.5 kHz"
assert con_unidad(2.0, "V") == "2 V"
assert con_unidad(0.707, "V") == "707 mV"
assert con_unidad(0.0005, "s") == "500 us"
assert con_unidad(0.0, "V") == "0 V"
assert con_unidad(999.9999, "Hz") == "1 kHz"

print("pruebas OK")