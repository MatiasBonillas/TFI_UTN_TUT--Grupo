import importlib

ej1 = importlib.import_module("01_identificacion")
ej2 = importlib.import_module("02_magnitudes")
ej3 = importlib.import_module("03_comandos")
ej4 = importlib.import_module("04_configurar")
ej5 = importlib.import_module("05_cliente")
ej6 = importlib.import_module("06_barrido")
ej7 = importlib.import_module("07_verificacion")
ej8 = importlib.import_module("08_log")
ej9 = importlib.import_module("09_estadistica")


def generar_informe(direccion="127.0.0.1", puerto_osc=5555, puerto_dmm=5556, ruta_log="mediciones.log"):
    lineas = []
    lineas.append("=" * 60)  #Es necesario tantos simbolos igual? No pero la usa medio mundo, incluido la IA y hay que admitir que se ve muy bien
    lineas.append("INFORME AUTOMATIZADO DE BANCO DE MEDICIONES")
    lineas.append("=" * 60)

    # 1. Conexión e identificación de instrumentos (Ejercicios 1 y 5)
    osc = ej5.Instrumento(direccion, puerto_osc)
    dmm = ej5.Instrumento(direccion, puerto_dmm)

    try:
        info_osc = ej1.parsear_idn(osc.preguntar("*IDN?"))
        info_dmm = ej1.parsear_idn(dmm.preguntar("*IDN?"))

        lineas.append("\n[1] INSTRUMENTOS CONECTADOS")
        lineas.append(f"  - Osciloscopio: {info_osc['fabricante']} {info_osc['modelo']} (S/N: {info_osc['serie']}, FW: {info_osc['version']})")
        lineas.append(f"  - Multímetro  : {info_dmm['fabricante']} {info_dmm['modelo']} (S/N: {info_dmm['serie']}, FW: {info_dmm['version']})")

        # 2. Configuración validada de canales (Ejercicios 3 y 4)
        configuraciones = [
            ("CH1", "ON", "DC", "10X", "1v"),
            ("CH2", "ON", "AC", "1X", "500mv"),
        ]
        for canal, disp, acop, sonda, esc in configuraciones:
            comandos = ej4.comandos_de_canal(canal, disp, acop, sonda, esc)
            for cmd in comandos:
                error_sintaxis = ej3.validar(cmd)
                if error_sintaxis is not None:
                    raise ValueError(f"Comando inválido '{cmd}': {error_sintaxis}")
                osc.enviar(cmd)

        # 3. Barrido de mediciones en vivo (Ejercicios 2 y 6)
        filas_barrido = ej6.barrer(osc, ["CH1", "CH2"])
        lineas.append("\n[2] MEDICIONES EN VIVO (OSCILOSCOPIO)")
        for fila in filas_barrido:
            val_fmt = ej2.con_unidad(fila["valor"], fila["unidad"]) if fila["valor"] is not None else "ERROR"
            lineas.append(f"  - {fila['canal']} | {fila['magnitud']:<6}: {val_fmt}")

        # 4. Verificación física Vrms teórico vs medido (Ejercicio 7)
        lineas.append("\n[3] VERIFICACIÓN DE FORMA DE ONDA SENOIDAL (Tolerancia 2%)")
        for canal in ("CH1", "CH2"):
            verif = ej7.verificar_canal(filas_barrido, canal)
            estado = "CUMPLE (Senoidal)" if verif["coincide"] else "NO CUMPLE (Distorsionada / No senoidal)"
            teor_fmt = ej2.con_unidad(verif["vrms_teorico"], "V") if verif["vrms_teorico"] is not None else "N/A"
            med_fmt = ej2.con_unidad(verif["vrms_medido"], "V") if verif["vrms_medido"] is not None else "N/A"
            lineas.append(f"  - {canal}: Vrms medido = {med_fmt} | Vrms teórico = {teor_fmt} -> {estado}")

    finally:
        osc.cerrar()
        dmm.cerrar()

    # 5. Análisis histórico del archivo de log (Ejercicios 8 y 9)
    series_log, rechazadas_log = ej8.leer_log(ruta_log)
    resumen_log = ej9.resumir_series(series_log)

    lineas.append(f"\n[4] ESTADÍSTICAS DEL REGISTRO HISTÓRICO ({ruta_log})")
    unidades_mag = {"FREQ": "Hz", "PKPK": "V", "CYCRMS": "V"}

    for equipo, canales in resumen_log.items():
        for canal, magnitudes in canales.items():
            for mag, stats in magnitudes.items():
                u = unidades_mag.get(mag, "")
                prom = ej2.con_unidad(stats["promedio"], u)
                med = ej2.con_unidad(stats["mediana"], u)
                desv = ej2.con_unidad(stats["desvio"], u)
                lineas.append(
                    f"  - {equipo} {canal} {mag:<6} (n={stats['cantidad']}): "
                    f"Promedio={prom}, Mediana={med}, Desvío={desv}"
                )

    lineas.append(f"\n[5] AUDITORÍA DE REGISTROS RECHAZADOS: {len(rechazadas_log)} líneas descartadas")
    for item in rechazadas_log:
        lineas.append(f"  - Línea {item['linea']}: {item['motivo']} -> '{item['contenido']}'")

    lineas.append("=" * 60)
    return "\n".join(lineas)


# --- Pruebas ---
informe_texto = generar_informe()

assert "ADS3202" in informe_texto
assert "XDM1041" in informe_texto
assert "VERIFICACIÓN DE FORMA DE ONDA SENOIDAL" in informe_texto
assert "ESTADÍSTICAS DEL REGISTRO HISTÓRICO" in informe_texto
assert "8 líneas descartadas" in informe_texto

print(informe_texto)
print("\npruebas OK")