import importlib
import math


def resumir(valores):
    if not valores:
        return None

    n = len(valores)
    ordenados = sorted(valores)

    minimo = ordenados[0]
    maximo = ordenados[-1]
    promedio = sum(ordenados) / n

    mitad = n // 2
    if n % 2 == 1:
        mediana = float(ordenados[mitad])
    else:
        mediana = (ordenados[mitad - 1] + ordenados[mitad]) / 2.0

    if n < 2:
        desvio = 0.0
    else:
        suma_cuadrados = sum((x - promedio) ** 2 for x in ordenados)
        desvio = math.sqrt(suma_cuadrados / (n - 1))

    return {
        "cantidad": n,
        "minimo": minimo,
        "maximo": maximo,
        "promedio": promedio,
        "mediana": mediana,
        "desvio": desvio,
    }


def resumir_series(series):
    resumen = {}
    for equipo, canales in series.items():
        resumen[equipo] = {}
        for canal, magnitudes in canales.items():
            resumen[equipo][canal] = {}
            for magnitud, lista_valores in magnitudes.items():
                resumen[equipo][canal][magnitud] = resumir(lista_valores)
    return resumen


# --- Pruebas ---
# 1. Lista vacía
assert resumir([]) is None

# 2. Un solo elemento (desvío debe ser 0.0)
solo_uno = resumir([1000.0])
assert solo_uno is not None
assert solo_uno["cantidad"] == 1
assert solo_uno["promedio"] == 1000.0
assert solo_uno["mediana"] == 1000.0
assert solo_uno["desvio"] == 0.0

# 3. Cantidad impar y verificación de que NO modifica la lista original
original = [30.0, 10.0, 20.0]
res_impar = resumir(original)
assert original == [30.0, 10.0, 20.0]  # sorted() mantiene intacta la original
assert res_impar["minimo"] == 10.0
assert res_impar["maximo"] == 30.0
assert res_impar["promedio"] == 20.0
assert res_impar["mediana"] == 20.0
assert abs(res_impar["desvio"] - 10.0) < 1e-9

# 4. Cantidad par (mediana es el promedio de los dos del medio)
res_par = resumir([10.0, 20.0, 30.0, 40.0])
assert res_par["mediana"] == 25.0

# 5. Integración con el Ejercicio 8 sobre mediciones.log
ej8 = importlib.import_module("08_log")
series_log, _ = ej8.leer_log("mediciones.log")
estadisticas_log = resumir_series(series_log)

stats_ch1_freq = estadisticas_log["ADS3202"]["CH1"]["FREQ"]
assert stats_ch1_freq["cantidad"] == 21
assert stats_ch1_freq["minimo"] <= stats_ch1_freq["mediana"] <= stats_ch1_freq["maximo"]
assert stats_ch1_freq["desvio"] > 0

print("pruebas OK")