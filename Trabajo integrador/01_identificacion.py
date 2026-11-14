#Definimos la funcion parsear que nos pidio usted, que va a ser la encargada de recibir el texto que venga de IDN? que esta en otro ejercicio
def parsear_idn(respuesta): 
    if not isinstance(respuesta, str):  #Verifica que haya texto y no este vacia
        return None

    texto_limpio = respuesta.strip()     #Limpia espacios
    if texto_limpio == "" or texto_limpio.startswith("ERROR"):   #Si el texto esta vacio o empieza con error, va a ser NONE cuando ejecutemos el ejercicio 10, ademas que ejecutar este no dara pruebas ok
        return None

    campos = texto_limpio.split(",")      #Separa bien el texto con comas, asi cuando se imprima en pantalla sale (espero) algo asi TOYOYA, 2005, PEPE
    if len(campos) < 4:                   #Como un instrumento manda 4 campos y el otro 5 (como dice el pdf) rechazamos cualquier lenght menor a 4, que es lo mismo que mayor o igual a 4 :P
        return None                       #Y dara none con cualquier medida menor a 4

    fabricante = campos[0].strip()       #Como nos enseño en la clase del 30/10, las listas arrancan en 0, asi que a cada dato le asignamos su posicion en el diccionario
    modelo = campos[1].strip()
    serie = campos[2].strip()
    version = campos[3].strip()

    if not fabricante or not modelo or not serie or not version:    #Y si alguno de estos del diccionario no esta devuelve NONE
        return None

    return {                          #Y bueno aca no cambia demasiado pero lo ordeno como pidio en el PDF, primero fabricante, despues modelo etc.
        "fabricante": fabricante,
        "modelo": modelo,
        "serie": serie,
        "version": version
    }

# --- Pruebas ---  Tal cual copiado y pegado del pdf con unos toquecitos, un caso esta con 4 campos, otro con 5 y descarta el ultimo, otro tiene respuestas invalidas con los estandares que puse arriba y el ultimo esta vacio directamente.
assert parsear_idn("OWON, ADS3202, 25470803, V1.2.0") == {  
    "fabricante": "OWON",
    "modelo": "ADS3202",
    "serie": "25470803",
    "version": "V1.2.0"
}
assert parsear_idn("OWON,XDM1041,25470803,V4.4.0,3")["modelo"] == "XDM1041"    #El correcto
assert parsear_idn("OWON, ADS3202, 254") is None  #El de menos de 4
assert parsear_idn("") is None                #El vacio                                  
assert parsear_idn("ERROR: comando desconocido") is None   #El que empieza con errror, osea none
print("pruebas OK")
