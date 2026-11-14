def es_consulta(comando):
    if not isinstance(comando, str):           #Igual que antes verificamos que sea un string valido, para que no se rompa si llega algo que no es texto
        return False
    return comando.strip().endswith("?")


def validar(comando):
    if not isinstance(comando, str) or comando.strip() == "":   #Si esta vacio devuelve esto
        return "El comando no puede estar vacío"

    c = comando.strip()

    if not (c.startswith(":") or c.startswith("*")):        #Todas las razones de que el comando haya sido negado, cada una tiene en texto el porque :PPP
        return "El comando debe empezar con : o con *"

    if "  " in c:
        return "No puede haber dos espacios seguidos"

    if c.count("?") > 1:
        return "Hay más de un signo de interrogación"

    if "?" in c and not c.endswith("?"):
        return "El signo de interrogación debe ir al final"

    partes = c.split(" ")                                  #Aca las seperamos por espacios las que hayan pasado todo, porque por espacios si antes las discrimanabamos? para contar cuantas palabras tienen y si es orden, consulta, etc.

    if es_consulta(c):
        if len(partes) > 1:
            return "Una consulta no lleva argumento"
    else:
        if len(partes) != 2:
            return "Una orden lleva un solo argumento"

    return None


# --- Pruebas ---
assert es_consulta(":MEASUrement:CH1:FREQuency?") is True
assert es_consulta("*IDN?") is True
assert es_consulta(":CH1:DISPlay ON") is False

assert validar(":CH1:DISPlay ON") is None
assert validar(":MEASUrement:CH1:PKPK?") is None
assert validar("*IDN?") is None

assert validar("") == "El comando no puede estar vacío"
assert validar("   ") == "El comando no puede estar vacío"
assert validar("CH1:DISPlay ON") == "El comando debe empezar con : o con *"
assert validar(":CH1:DISPlay  ON") == "No puede haber dos espacios seguidos"
assert validar(":CH1:DISPlay??") == "Hay más de un signo de interrogación"
assert validar(":CH1:DIS?Play") == "El signo de interrogación debe ir al final"
assert validar(":CH1:SCALe 1 v") == "Una orden lleva un solo argumento"
assert validar(":CH1:DISPlay") == "Una orden lleva un solo argumento"
assert validar(":CH1:DISPlay ON?") == "Una consulta no lleva argumento"

print("pruebas OK") #En este caso a diferencia de los demas, si devuelve NONE ESTA BIEN PORQUE NO TIRO MENSAJE DE PORQUE FALLO