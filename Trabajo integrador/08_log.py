import importlib

ej2 = importlib.import_module("02_magnitudes")


def _hora_valida(hora_str):
    partes = hora_str.split(":")
    if len(partes) != 3:
        return False
    try:
        horas, minutos, segundos = int(partes[0]), int(partes[1]), int(partes[2])
    except ValueError:
        return False
    return (0 <= horas <= 23) and (0 <= minutos <= 59) and (0 <= segundos <= 59)


def _fecha_valida(fecha_str):
    partes = fecha_str.split("-")
    if len(partes) != 3:
        return False
    try:
        anio, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
    except ValueError:
        return False
    return (anio > 0) and (1 <= mes <= 12) and (1 <= dia <= 31)


def analizar_linea(linea):
    if not isinstance(linea, str):
        return (None, "Línea inválida")

    limpia = linea.strip()

    # Regla 1: Líneas en blanco o comentarios con # se ignoran (ambos None)
    if limpia == "" or limpia.startswith("#"):
        return (None, None)

    # Regla 2: split() sin argumentos separa por espacios Y tabulaciones (\t)
    campos = limpia.split()
    if len(campos) != 6:
        return (None, "Cantidad de campos distinta de 6")

    fecha, hora, equipo, canal, magnitud, valor_texto = campos

    if not _fecha_valida(fecha) or not _hora_valida(hora):
        return (None, "Fecha u hora imposible")

    if canal not in ("CH1", "CH2"):
        return (None, "Canal desconocido")

    if magnitud not in ("FREQ", "PKPK", "CYCRMS"):
        return (None, "Magnitud desconocida")

    valor = ej2.a_numero(valor_texto)
    if valor is None:
        return (None, "Valor no numérico")

    medicion = {
        "fecha": fecha,
        "hora": hora,
        "equipo": equipo,
        "canal": canal,
        "magnitud": magnitud,
        "valor": valor,
    }
    return (medicion, None)


def leer_log(ruta):
    series = {}
    rechazadas = []

    with open(ruta, "r", encoding="utf-8") as archivo:
        for num_linea, linea in enumerate(archivo, start=1):
            medicion, motivo = analizar_linea(linea)

            # Ignorada (blanco o comentario)
            if medicion is None and motivo is None:
                continue

            # Rechazada (tiene un motivo de error)
            if motivo is not None:
                rechazadas.append({
                    "linea": num_linea,
                    "contenido": linea.strip(),
                    "motivo": motivo,
                })
                continue

            # Válida: agrupar por equipo -> canal -> magnitud
            eq = medicion["equipo"]
            can = medicion["canal"]
            mag = medicion["magnitud"]
            val = medicion["valor"]

            if eq not in series:
                series[eq] = {}
            if can not in series[eq]:
                series[eq][can] = {}
            if mag not in series[eq][can]:
                series[eq][can][mag] = []

            series[eq][can][mag].append(val)

    return series, rechazadas


# --- Pruebas ---
# 1. Línea válida normal
med, err = analizar_linea("2026-09-08 09:14:00 ADS3202 CH1 FREQ 9.993761E+02\n")
assert err is None and med is not None
assert med["valor"] == 999.3761

# 2. LA TRAMPA DEL PDF: Línea válida separada por tabulaciones (\t)
med_tab, err_tab = analizar_linea("2026-09-08\t09:17:31\tADS3202\tCH1\tFREQ\t1.001000E+03\n")
assert err_tab is None and med_tab is not None
assert med_tab["valor"] == 1001.0

# 3. Líneas ignoradas (devuelven (None, None))
assert analizar_linea("   \n") == (None, None)
assert analizar_linea("# reconexion del puerto LAN\n") == (None, None)

# 4. Líneas rechazadas (devuelven (None, motivo))
assert analizar_linea("2026-09-08 25:61:00 ADS3202 CH2 FREQ 2.500000E+03")[1] is not None
assert analizar_linea("2026-09-08 09:16:31 ADS3202 CH3 FREQ 1.000000E+03")[1] is not None
assert analizar_linea("2026-09-08 09:17:01 ADS3202 CH1 TEMP 3.150000E+02")[1] is not None
assert analizar_linea("2026-09-08 09:16:01 ADS3202 CH2 CYCRMS NaN")[1] is not None
assert analizar_linea("2026-09-08 09:15:31 ADS3202 CH1 PKPK 2,003812")[1] is not None
assert analizar_linea("2026-09-08 09:15:01 ADS3202 CH2 PKPK")[1] is not None

# 5. Prueba sobre el archivo real mediciones.log
series_log, rechazadas_log = leer_log("mediciones.log")
assert len(series_log["ADS3202"]["CH1"]["FREQ"]) == 21  # 18 con espacios + 1 con tabulaciones
assert len(rechazadas_log) == 8

print("pruebas OK")