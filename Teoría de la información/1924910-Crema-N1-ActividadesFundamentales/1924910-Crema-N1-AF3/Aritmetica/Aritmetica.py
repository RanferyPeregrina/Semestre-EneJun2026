import math
from collections import Counter

print("==============================================")
print("     METODO DE CODIFICACION ARITMETICA")
print("==============================================")

print("\nIngrese el mensaje a codificar:")
print("(Presione ENTER dos veces para finalizar)\n")

lineas = []

while True:
    linea = input()
    if linea == "":
        break
    lineas.append(linea)

mensaje = "\n".join(lineas)

if len(mensaje) == 0:
    print("\nError: No se ingresó ningún mensaje.")
    exit()

total_simbolos = len(mensaje)

frecuencias = Counter(mensaje)

simbolos_ordenados = sorted(
    frecuencias.items(),
    key=lambda x: x[1],
    reverse=True
)

# -------------------------------------------------------
# Tabla de probabilidades con intervalos acumulados [inf, sup)
# -------------------------------------------------------
tabla_probabilidades = {}
acumulada = 0.0

for simbolo, frecuencia in simbolos_ordenados:
    probabilidad = frecuencia / total_simbolos
    limite_inferior = acumulada
    limite_superior = acumulada + probabilidad

    tabla_probabilidades[simbolo] = {
        "frecuencia": frecuencia,
        "probabilidad": probabilidad,
        "inferior": limite_inferior,
        "superior": limite_superior
    }

    acumulada = limite_superior

# -------------------------------------------------------
# Proceso de codificacion aritmetica
# -------------------------------------------------------
inferior = 0.0
superior = 1.0
procesos = []

for simbolo in mensaje:
    rango = superior - inferior

    nuevo_inferior = inferior + rango * tabla_probabilidades[simbolo]["inferior"]
    nuevo_superior = inferior + rango * tabla_probabilidades[simbolo]["superior"]

    procesos.append({
        "simbolo": simbolo,
        "inferior_anterior": inferior,
        "superior_anterior": superior,
        "nuevo_inferior": nuevo_inferior,
        "nuevo_superior": nuevo_superior
    })

    inferior = nuevo_inferior
    superior = nuevo_superior

# Codigo aritmetico: cualquier valor dentro del intervalo final
# Se elige el punto medio del intervalo
codigo_aritmetico = (inferior + superior) / 2

# -------------------------------------------------------
# Calculo correcto de bits necesarios para representar el codigo
#
#   El numero de bits necesarios para codificar el mensaje completo es:
#       bits_necesarios = ceil(-log2(superior - inferior)) + 1
#
#   Esto se deriva de que el intervalo final tiene ancho:
#       ancho = prod( P(si) ) = 2^(- sum( -log2(P(si)) ))
#   Por lo tanto se necesitan al menos ceil(-log2(ancho)) + 1 bits.
# -------------------------------------------------------
ancho_intervalo_final = superior - inferior

if ancho_intervalo_final > 0:
    bits_necesarios = math.ceil(-math.log2(ancho_intervalo_final)) + 1
else:
    bits_necesarios = float('inf')

# -------------------------------------------------------
# Calculo de entropia y longitud promedio CORRECTOS
#
#   Entropia H(X)   = -sum( P(x) * log2(P(x)) )   [bits/simbolo]
#
#   Longitud promedio de codificacion aritmetica (cota superior teorica):
#       L = H(X) + 2/n                              [bits/simbolo]
#   donde n = total de simbolos del mensaje.
#   En la practica se usa:
#       L_total = bits_necesarios / total_simbolos  [bits/simbolo]
# -------------------------------------------------------
entropia_total = 0.0
resultados = []

for simbolo, datos in tabla_probabilidades.items():
    probabilidad = datos["probabilidad"]

    # Informacion propia: I(x) = -log2(P(x))
    informacion = -math.log2(probabilidad)

    # Contribucion a la entropia: P(x) * I(x)
    entropia_individual = probabilidad * informacion

    entropia_total += entropia_individual

    # Representacion visual del simbolo
    if simbolo == " ":
        simbolo_mostrar = "[ESPACIO]"
    elif simbolo == "\n":
        simbolo_mostrar = "[SALTO_LINEA]"
    elif simbolo == "\t":
        simbolo_mostrar = "[TABULACION]"
    else:
        simbolo_mostrar = simbolo

    binario_ascii = format(ord(simbolo), '08b')

    resultados.append({
        "simbolo": simbolo_mostrar,
        "frecuencia": datos["frecuencia"],
        "probabilidad": probabilidad,
        "informacion": informacion,
        "entropia_individual": entropia_individual,
        "inferior": datos["inferior"],
        "superior": datos["superior"],
        "binario": binario_ascii
    })

# Longitud promedio real del codigo aritmetico [bits/simbolo]
longitud_promedio = bits_necesarios / total_simbolos

# Cota superior teorica segun Shannon: H(X) + 2/n
cota_superior_teorica = entropia_total + (2 / total_simbolos)

# Eficiencia: que tan cerca estamos del optimo (entropia)
# Una codificacion perfecta tendria longitud_promedio == entropia_total
eficiencia = (entropia_total / longitud_promedio) * 100

redundancia = 100 - eficiencia

# -------------------------------------------------------
# Escritura del reporte
# -------------------------------------------------------
nombre_archivo = "resultado_codificacion_aritmetica.txt"

with open(nombre_archivo, "w", encoding="utf-8") as archivo:

    archivo.write("============================================================\n")
    archivo.write("     REPORTE DEL METODO DE CODIFICACION ARITMETICA\n")
    archivo.write("============================================================\n\n")

    archivo.write("MENSAJE ORIGINAL:\n")
    archivo.write("------------------------------------------------------------\n")
    archivo.write(mensaje + "\n\n")

    archivo.write("TOTAL DE SIMBOLOS:\n")
    archivo.write("------------------------------------------------------------\n")
    archivo.write(f"{total_simbolos} simbolos\n\n")

    archivo.write("TABLA DE PROBABILIDADES:\n")
    archivo.write("-" * 130 + "\n")
    archivo.write(
        f"{'SIMBOLO':15}"
        f"{'FRECUENCIA':12}"
        f"{'PROBABILIDAD':15}"
        f"{'I(x) bits':15}"
        f"{'H(x) bits':15}"
        f"{'LIMITE INF':18}"
        f"{'LIMITE SUP':18}"
        f"{'BINARIO ASCII'}\n"
    )
    archivo.write("-" * 130 + "\n")

    for r in resultados:
        archivo.write(
            f"{r['simbolo']:15}"
            f"{r['frecuencia']:<12}"
            f"{r['probabilidad']:<15.6f}"
            f"{r['informacion']:<15.6f}"
            f"{r['entropia_individual']:<15.6f}"
            f"{r['inferior']:<18.10f}"
            f"{r['superior']:<18.10f}"
            f"{r['binario']}\n"
        )
    archivo.write("-" * 130 + "\n\n")

    archivo.write("PROCESO DE CODIFICACION:\n")
    archivo.write("-" * 130 + "\n")
    archivo.write(
        f"{'SIMBOLO':15}"
        f"{'INF. ANTERIOR':20}"
        f"{'SUP. ANTERIOR':20}"
        f"{'NUEVO INF.':20}"
        f"{'NUEVO SUP.'}\n"
    )
    archivo.write("-" * 130 + "\n")

    for p in procesos:
        if p["simbolo"] == " ":
            simbolo_mostrar = "[ESPACIO]"
        elif p["simbolo"] == "\n":
            simbolo_mostrar = "[SALTO_LINEA]"
        elif p["simbolo"] == "\t":
            simbolo_mostrar = "[TABULACION]"
        else:
            simbolo_mostrar = p["simbolo"]

        archivo.write(
            f"{simbolo_mostrar:15}"
            f"{p['inferior_anterior']:<20.10f}"
            f"{p['superior_anterior']:<20.10f}"
            f"{p['nuevo_inferior']:<20.10f}"
            f"{p['nuevo_superior']:.10f}\n"
        )
    archivo.write("-" * 130 + "\n\n")

    archivo.write("RESULTADO FINAL DE LA CODIFICACION:\n")
    archivo.write("------------------------------------------------------------\n")
    archivo.write(f"Intervalo final      : [{inferior:.10f}, {superior:.10f})\n")
    archivo.write(f"Ancho del intervalo  : {ancho_intervalo_final:.10e}\n")
    archivo.write(f"Codigo aritmetico    : {codigo_aritmetico:.10f}  (punto medio del intervalo final)\n")
    archivo.write(f"Bits necesarios      : {bits_necesarios} bits  (ceil(-log2(ancho)) + 1)\n\n")

    archivo.write("RESULTADOS FINALES:\n")
    archivo.write("------------------------------------------------------------\n")
    archivo.write(f"Entropia total H(X)          : {entropia_total:.6f} bits/simbolo\n")
    archivo.write(f"Cota superior teorica H(X)+2/n: {cota_superior_teorica:.6f} bits/simbolo\n")
    archivo.write(f"Longitud promedio real L      : {longitud_promedio:.6f} bits/simbolo  ({bits_necesarios} bits / {total_simbolos} simbolos)\n")
    archivo.write(f"Eficiencia                   : {eficiencia:.2f} %\n")
    archivo.write(f"Redundancia                  : {redundancia:.2f} %\n")

# -------------------------------------------------------
# Salida en consola
# -------------------------------------------------------
print("\n==============================================")
print("RESULTADOS OBTENIDOS")
print("==============================================")
print(f"\nTotal de simbolos            : {total_simbolos}")
print(f"\nIntervalo final              : [{inferior:.10f}, {superior:.10f})")
print(f"Ancho del intervalo          : {ancho_intervalo_final:.10e}")
print(f"Codigo aritmetico            : {codigo_aritmetico:.10f}")
print(f"Bits necesarios              : {bits_necesarios} bits")
print(f"\nEntropia total H(X)          : {entropia_total:.6f} bits/simbolo")
print(f"Cota superior teorica H(X)+2/n: {cota_superior_teorica:.6f} bits/simbolo")
print(f"Longitud promedio real L      : {longitud_promedio:.6f} bits/simbolo")
print(f"Eficiencia                   : {eficiencia:.2f} %")
print(f"Redundancia                  : {redundancia:.2f} %")
print(f"\nReporte generado: {nombre_archivo}")