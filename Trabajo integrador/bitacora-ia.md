================================================================================

BITÁCORA DE CONSULTAS Y DESARROLLO (FORMATO CONVERSACIONAL)

Trabajo Final Integrador — Programación (2026 - 2C)

Tecnicatura Universitaria en Telecomunicaciones — UTN FRBA

================================================================================



INTEGRANTES DEL GRUPO:

- [M] Matías Bonillas (22 años) — Encargado de Ejercicios 1, 3 y 5

- [C] Cliver Cabrera — Encargado de Ejercicios 2, 4 y 6

- [L] Leonel — Encargado de Ejercicios 7, 8 y 9

- [M / C / L] Colaborativo — Integración en Ejercicio 10 y pruebas cruzadas



NOTA SOBRE VALIDACIÓN FÍSICA EN LABORATORIO:

Además de probar el código contra el servidor simulado (`instrumento_virtual.py`), el equipo montó circuitos reales en protoboard generando señales cuadradas y las midió con un osciloscopio físico (Siglent SDS 1022DL, sonda 1X, acoplamiento DC) para contrastar empíricamente la relación Vpp vs. Vrms y comprobar por qué la lógica del Ejercicio 7 excluye las ondas cuadradas al evaluar pureza senoidal.



================================================================================

REGISTRO TEXTUAL DE INTERACCIONES (PREGUNTAS DEL EQUIPO Y RESPUESTAS DE IA)

================================================================================



--------------------------------------------------------------------------------

[ENCUADRE Y ORGANIZACIÓN DEL EQUIPO]

--------------------------------------------------------------------------------

> [M] Matías:

  Planteó la dinámica del chat identificando a cada integrante con su inicial (M, C, L), subió `TUT-PROG-TFI-Consigna.pdf`, `instrumento_virtual.py` y `mediciones.log`, y pidió explícitamente que la IA no resolviera código sin que antes plantearan sus propias teorías.

  Consulta puntual: "¿Del 1 al 9 solamente deben dar resultados de prueba ok sin parámetros que mostrar con print para nosotros, sino que se terminaran volcando en el punto 10 finalmente? Las únicas excepciones las hacen el punto 5, 6 y 10 que necesitan tener la herramienta virtual encendida, y el punto 9 que necesita tener el .log de mediciones. ¿Es esto correcto?"



< IA (Tutor):

  Confirmó que los ejercicios 1 al 9 son módulos puros con bloques `assert` terminados en `print("pruebas OK")`, volcándose la salida en el 10. Aclaró que los ejercicios 5, 6 y 10 requieren `instrumento_virtual.py` activo, mientras que tanto el 8 (lectura) como el 9 (control estadístico) trabajan sobre `mediciones.log`.



> [M] Matías:

  Informó la división de tareas (M: 1-3-5, C: 2-4-6, L: 7-8-9, conjunto: 10) y la metodología de revisión cruzada corriendo cada script en las computadoras de todos los compañeros para evitar código dependiente de una sola máquina y preparar la defensa individual.



--------------------------------------------------------------------------------

[EJERCICIO 1 — 01_identificacion.py]

--------------------------------------------------------------------------------

> [M] Matías:

  Presentó `01_identificacion.py` y consultó: "En el PDF me dice que un instrumento da 4 campos y el otro da 5, pero debo eliminar uno, por tanto probé con el == primeramente y entendí que jamás dará 4, pero después probé con mayor o igual a 3, para que el 4 esté incluido y da errores, ¿tendría que ser mayor o igual a 4? ¿En ciertos casos no se van a excluir valores válidos?"



< IA (Tutor):

  Explicó la diferencia entre cantidad de elementos (`len`) e índice máximo: con `len == 3`, los índices llegan hasta `2`, por lo que al intentar leer `campos[3]` (`version`) salta `IndexError`. Confirmó que `len(campos) < 4` (equivalente a aceptar `>= 4`) es el filtro exacto porque los equipos válidos devuelven 4 o 5 campos y no excluye ningún caso válido.



> [M] Matías:

  "Entiendo según el pdf que hay que usar split en múltiples ocasiones, pero ¿es realmente necesario o se hace por pura prolijidad? Por defecto viene separado por espacios y tabulaciones, ¿no es eso suficiente?"



< IA (Tutor):

  Explicó que es técnicamente necesario: en `*IDN?` los datos vienen separados por comas sin espacios (`split(",")`), en `mediciones.log` se requiere `split()` sin argumentos para absorber tabulaciones, y en comandos SCPI se necesita detectar dobles espacios explícitos.



> [M] Matías:

  "¿Está bien que toqueteando los valores de pruebas a veces dé AssertionError? En el caso de la línea 36 probé borrarle cosas a ver si seguía dando pruebas OK y no llevarme una sorpresa en la defensa."



< IA (Tutor):

  Confirmó que provocar fallos al alterar entradas sin cambiar el valor esperado demuestra que los `assert` no son decorativos, y que borrar elementos de un caso ya inválido (de 3 a 2 campos) sigue cayendo en la regla `< 4` y devolviendo `None`.



--------------------------------------------------------------------------------

[EJERCICIO 2 — 02_magnitudes.py]

--------------------------------------------------------------------------------

> [C] Cliver:

  Presentó `02_magnitudes.py` y consultó: "¿Cómo hago que al meter texto no dé nada? Se me cierra Visual Studio Code. Si ya estoy filtrando solo strings con isinstance, ¿por qué pareciera que no hiciera nada? Probando valores a veces da simplemente NaN o inf, ¿me falta una función o realmente debería excluir completamente NaN e infinito?"



< IA (Tutor):

  Aclaró que `isinstance(texto, str)` verifica el tipo de dato (`"hola"` es un `str`, por lo que pasa ese filtro y recién cae en `except ValueError` dentro de `float()`), y que la ventana se cierra si se ejecuta el `.py` por doble clic fuera de la terminal integrada. Confirmó que `math.isnan(valor) or math.isinf(valor)` es obligatorio porque en Python `"NaN"` e `"inf"` son floats válidos y, si no se filtran, dejan pasar mediciones corruptas del `.log` y arruinan la estadística del Ejercicio 9.



> [C] Cliver:

  "M dice que `absoluto >= factor` es lo mismo que lo que estoy haciendo (`absoluto / factor >= 1`), ¿entonces hay pasos de más? Si el día de mañana se mete un 0 ¿no explota todo con la división en 0? Los valores límites no se están pasando a la siguiente unidad, ¿debería ser `<=` o `>=` si quiero que salte de unidad sí o sí?"



< IA (Tutor):

  Confirmó que `absoluto >= factor` es más limpio, que el `0` ya está atajado al inicio (`if valor == 0`) y además quedaría en el numerador (`0 / factor`), y que `escalado >= 1000` después de `round(..., 3)` es el operador correcto para que `999.9999 Hz` pase a `1 kHz`.



--------------------------------------------------------------------------------

[EJERCICIO 3 — 03_comandos.py]

--------------------------------------------------------------------------------

> [M] Matías:

  Presentó `03_comandos.py` y preguntó: "No entiendo por qué una orden lleva tantos requisitos, el doble signo de pregunta se puede entender perfectamente, ¿en las telecomunicaciones siempre se es riguroso con el tipeo? Ya van dos pruebas que no da pruebas ok por un punto."



< IA (Tutor):

  Explicó que en instrumentación y telecomunicaciones el firmware de los equipos compara cadenas exactas carácter por carácter y aplica el principio de "fallar rápido" para evitar configuraciones erróneas o tráfico inválido en red.



> [M] Matías:

  "¿Por qué en `len(partes)` mayor de 2 da error? Ya arreglé una parte del código poniéndole un filtro para borrar espacios porque terminaban re largos los textos, ¿o se están filtrando órdenes incorrectas que aunque no sean mayor a 2 sí están mal escritas?"



< IA (Tutor):

  Advirtió que borrar espacios internos rompe las órdenes válidas (porque deja pegado `:CH1:DISPlayON` en 1 sola palabra) y que debe mantenerse `len(partes) != 2` para rechazar tanto órdenes sin argumento (`len == 1`) como órdenes con argumentos de más (`len > 2`).



> [M] Matías:

  "¿El orden de los `if` es importante no? Porque metí una consulta como `':CH1:DIS?Play?'` y da error que tiene más de un signo de pregunta, y si pongo `':CH1:DIS?Play?ON'` no me lo corrige como que debe ir al final sino como que hay más de uno."



< IA (Tutor):

  Confirmó que el orden importa porque cada `return` interrumpe la evaluación ante la primera regla violada, y que validar primero la cantidad (`count("?") > 1`) y luego la posición (`endswith("?")`) es la jerarquía más lógica.



--------------------------------------------------------------------------------

[EJERCICIO 4 — 04_configurar.py]

--------------------------------------------------------------------------------

> [C] Cliver:

  Presentó `04_configurar.py` y preguntó: "Si el `import` lo intento poner como `03_comandos` me lo rechaza y tengo que usar `importlib.import_module`, ¿es porque arranca por un número? ¿Si le cambio el nombre al archivo se solucionaría? ¿Este programa se tiene que encargar solo de detectar CH1 y CH2 o debería limpiar espacios en parámetros como `'1 v'`?"



< IA (Tutor):

  Explicó que Python prohíbe identificadores que empiecen con dígitos, por lo que `importlib.import_module("03_comandos")` es la forma correcta sin romper los nombres de archivo exigidos por la cátedra. Indicó no limpiar espacios internos en `comandos_de_canal` para que la prueba cruzada con `ej3.validar` detecte si se armó un comando inválido.



> [C] Cliver:

  "Al iterar tengo problemas, ¿el `assert comandos_ch2 is not None` está medio al pedo? A veces los f-string de canal dan cualquier cosa, ¿los espacios importan? ¿Cuando cambio valores falla el assert porque no coinciden?"



< IA (Tutor):

  Explicó que `assert comandos_ch2 is not None` evita un `TypeError` al iterar si fallara el filtro de canal, que `==` compara carácter por carácter incluyendo espacios, y que al cambiar argumentos de entrada en la prueba también debe actualizarse la lista esperada.



--------------------------------------------------------------------------------

[EJERCICIO 5 — 05_cliente.py]

--------------------------------------------------------------------------------

> [M] Matías:

  Presentó `05_cliente.py` y consultó: "Cuando le doy un `enviar` al osciloscopio es como si se quedase esperando de forma indefinida, no responde, le tiro un `*IDN?` y nada, vi en internet un `/n` que no tengo idea para que podría servir."



< IA (Tutor):

  Aclaró que el carácter es `\n` (barra invertida), obligatorio porque el servidor TCP lee línea por línea y sin `\n` ambos extremos quedan bloqueados esperándose; además explicó que `enviar` solo manda órdenes sin esperar respuesta, mientras que `*IDN?` debe ejecutarse con `preguntar`.



> [M] Matías:

  "En `if not byte or byte == b'\n'` debo hacer lo mismo no? Porque ese `while` no tiene pinta de parar. Probé cortando y conectando la conexión de golpe y a veces `recv(1024)` da la información incompleta, ¿tengo que leer byte por byte o es una aberración programática?"



< IA (Tutor):

  Explicó que `b"\n"` es 1 byte ASCII (mientras que `b"/n"` serían 2 bytes y dejaría el bucle infinito), que `recv(1024)` devuelve los bytes disponibles hasta ese instante pudiendo fragmentar mensajes TCP, y que `recv(1)` es totalmente viable para respuestas SCPI cortas.



--------------------------------------------------------------------------------

[EJERCICIO 6 — 06_barrido.py]

--------------------------------------------------------------------------------

> [C] Cliver:

  Presentó `06_barrido.py` y preguntó: "¿Por qué `barrer` cuando le pongo `CH9` no tira error? ¿Es porque el trabajo real lo hace `a_numero` que tira `None` ante cualquier texto? Si me equivoco en `FREQ`/`FREQuency`/`Hz`, ¿es normal que salte el error recién cuando consulta con el instrumento virtual?"



< IA (Tutor):

  Confirmó que `barrer` guarda intencionalmente el texto crudo de error y deja `valor` en `None` mediante `ej2.a_numero(crudo)` sin frenar el barrido, y que un error de tipeo en el comando SCPI viaja por socket hasta que el instrumento virtual responde `"ERROR: comando desconocido"`.



--------------------------------------------------------------------------------

[EJERCICIO 7 — 07_verificacion.py + VALIDACIÓN FÍSICA EN OSCILOSCOPIO]

--------------------------------------------------------------------------------

> [L] Leonel (y validación física del equipo en laboratorio):

  Presentó `07_verificacion.py` y planteó: "Con `verificar_canal` y `coincide` puedo filtrar las ondas cuadradas que tengan como `vpp` 0, ¿no? Además excluyo `NaN` e infinito porque el PDF pide que solo se analicen senoidales puras. Lo digo porque me pasa lo mismo con `isinstance(vpp, bool)` antes de `isinstance(vpp, (int, float))`, recibo hate en el grupo pero creería que está bien para que no calcule un voltaje ficticio de ~0,35 V."

  *Nota de trabajo experimental:* El equipo armó un oscilador de onda cuadrada en protoboard y lo midió con un osciloscopio digital Siglent SDS 1022DL para verificar físicamente cómo el Vrms medido de una onda cuadrada coincide con su amplitud pico ($V_p = V_{pp}/2$), alejándose ~41,4% del valor teórico senoidal ($V_p / \sqrt{2}$) y confirmando que el algoritmo descarta la onda cuadrada.



< IA (Tutor):

  Validó ambos puntos: `isinstance(vpp, bool)` es necesario porque en Python `bool` hereda de `int` (`True == 1`, lo que produciría $1 / (2\sqrt{2}) \approx 0,3535\text{ V}$), y `coincide` rechaza las ondas cuadradas reales porque su error relativo respecto de la fórmula senoidal (~41,4%) supera ampliamente la tolerancia del 2%.



> [L] Leonel:

  "El `abs(teorico)` lo metí para poder tener una tolerancia normalizada, no sé si está bien. No es lo mismo 0,02 V de tolerancia en 10 V que en 0,4 V."



< IA (Tutor):

  Confirmó que dividir por `abs(teorico)` normaliza el error relativo a una proporción adimensional comparable con `0.02` (2%) independientemente de la amplitud de la señal.



--------------------------------------------------------------------------------

[EJERCICIO 8 — 08_log.py]

--------------------------------------------------------------------------------

> [L] Leonel:

  Presentó `08_log.py` y preguntó: "Quiero ahorrarme un paso, ¿puedo simplemente repetir el `c.split(' ')` del ejercicio 3? Estoy viendo el log por encima y creo que no habría problemas, ¿o sí los habría por las líneas válidas separadas por tabulaciones?"



< IA (Tutor):

  Advirtió que `split(" ")` descartaría la medición válida de las `09:17:31` separada por tabulaciones (`\t`), mientras que `limpia.split()` sin argumentos (como finalmente quedó implementado) conserva ese registro y permite alcanzar las 21 mediciones válidas de `CH1 FREQ` y las 8 rechazadas.



--------------------------------------------------------------------------------

[EJERCICIO 9 — 09_estadistica.py]

--------------------------------------------------------------------------------

> [L] Leonel:

  Presentó `09_estadistica.py` y consultó: "El programa al leer el log da error, si le pongo que empiece por el 1 ya no lo da, ¿está bien o es un error de programación? Los humanos solemos ver el 1 así que no veo problema, empezar del 0 es hasta raro."



< IA (Tutor):

  Distinguió entre numeración de líneas de archivo (`enumerate(archivo, start=1)`, correcto para reportes humanos) e indexación de listas en Python (que siempre inicia en `0` y lanza `IndexError` si se lee `lista[1]` en listas de 1 elemento). Además señaló alinear el nombre `resumen(valores)`, la clave `"n"`, agregar `fuera_de_rango` y los `assert` de control sobre `mediciones.log` (promedio < 0,5% de 1000 Hz y desvío < 5 Hz).



--------------------------------------------------------------------------------

[EJERCICIO 10 — 10_informe.py]

--------------------------------------------------------------------------------

> [M / C / L] Equipo completo:

  Subió `10_informe.py` integrando todos los módulos y pidió revisión general de arquitectura antes de la prueba final con el instrumento virtual.



< IA (Tutor):

  Confirmó que la integración entre módulos funciona, pero señaló dos ajustes para cumplir estrictamente con la consigna: aislar la función pura `armar_informe(idn, series, verificaciones)` (sin abrir sockets ni archivos adentro para poder testearla con `assert` puros) y agregar los valores `minimo` y `maximo` formateados con `con_unidad` en el resumen de cada serie.

================================================================================