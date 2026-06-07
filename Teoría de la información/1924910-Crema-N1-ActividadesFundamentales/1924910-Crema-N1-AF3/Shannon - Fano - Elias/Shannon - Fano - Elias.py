# -*- coding: utf-8 -*-
"""
Created on Tue May 26 14:31:52 2026

@author: blavi
"""

import math
from collections import Counter

def decimal_a_binario(numero):
    return bin(numero)[2:]


def codigo_elias(numero):

    numero += 1

    binario = decimal_a_binario(numero)

    longitud = len(binario) - 1

    prefijo = "0" * longitud

    return prefijo + binario


print("=================================================")
print(" METODO DE CODIFICACION SHANNON-FANO-ELIAS")
print("=================================================")

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

resultados = []

acumulada = 0
entropia_total = 0
longitud_promedio = 0

mensaje_codificado = ""

for simbolo, frecuencia in simbolos_ordenados:

    probabilidad = frecuencia / total_simbolos

    informacion = -math.log2(probabilidad)

    entropia_individual = probabilidad * informacion

    entropia_total += entropia_individual

    valor_fano_elias = acumulada + (probabilidad / 2)

    numero_escalado = int(valor_fano_elias * (2 ** 16))

    codigo = codigo_elias(numero_escalado)

    longitud_codigo = len(codigo)

    longitud_promedio += (
        probabilidad * longitud_codigo
    )

    acumulada += probabilidad

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
        "simbolo_real": simbolo,
        "simbolo": simbolo_mostrar,
        "frecuencia": frecuencia,
        "probabilidad": probabilidad,
        "informacion": informacion,
        "entropia_individual": entropia_individual,
        "longitud_codigo": longitud_codigo,
        "codigo": codigo,
        "binario": binario_ascii
    })

tabla_codigos = {}

for r in resultados:
    tabla_codigos[r["simbolo_real"]] = r["codigo"]

for caracter in mensaje:
    mensaje_codificado += tabla_codigos[caracter]

eficiencia = (
    entropia_total / longitud_promedio
) * 100

redundancia = 100 - eficiencia

nombre_archivo = "resultado_shannon_fano_elias.txt"

with open(nombre_archivo, "w", encoding="utf-8") as archivo:

    archivo.write("============================================================\n")
    archivo.write("   REPORTE DEL METODO SHANNON-FANO-ELIAS\n")
    archivo.write("============================================================\n\n")

    archivo.write("MENSAJE ORIGINAL:\n")
    archivo.write("------------------------------------------------------------\n")
    archivo.write(mensaje + "\n\n")

    archivo.write("MENSAJE CODIFICADO:\n")
    archivo.write("------------------------------------------------------------\n")
    archivo.write(mensaje_codificado + "\n\n")

    archivo.write("TOTAL DE SIMBOLOS:\n")
    archivo.write("------------------------------------------------------------\n")
    archivo.write(f"{total_simbolos} simbolos\n\n")

    archivo.write("TABLA DE RESULTADOS:\n")
    archivo.write("-------------------------------------------------------------------------------------------------------------------------------------------------\n")

    archivo.write(
        f"{'SIMBOLO':15}"
        f"{'FRECUENCIA':12}"
        f"{'PROBABILIDAD':15}"
        f"{'I(x) bits':15}"
        f"{'H(x) bits':15}"
        f"{'LONGITUD':12}"
        f"{'CODIGO':35}"
        f"{'BINARIO ASCII'}\n"
    )

    archivo.write("-------------------------------------------------------------------------------------------------------------------------------------------------\n")

    for r in resultados:

        archivo.write(
            f"{r['simbolo']:15}"
            f"{r['frecuencia']:<12}"
            f"{r['probabilidad']:<15.6f}"
            f"{r['informacion']:<15.6f}"
            f"{r['entropia_individual']:<15.6f}"
            f"{r['longitud_codigo']:<12}"
            f"{r['codigo']:<35}"
            f"{r['binario']}\n"
        )

    archivo.write("-------------------------------------------------------------------------------------------------------------------------------------------------\n\n")

    archivo.write("RESULTADOS FINALES:\n")
    archivo.write("------------------------------------------------------------\n")

    archivo.write(
        f"Entropia total: {entropia_total:.6f} bits/simbolo\n"
    )

    archivo.write(
        f"Longitud promedio: {longitud_promedio:.6f} bits/simbolo\n"
    )

    archivo.write(
        f"Eficiencia: {eficiencia:.2f} %\n"
    )

    archivo.write(
        f"Redundancia: {redundancia:.2f} %\n"
    )

print("\n=================================================")
print("RESULTADOS OBTENIDOS")
print("=================================================")

print(f"\nTotal de simbolos: {total_simbolos}")

print(f"\nEntropia total: {entropia_total:.6f} bits/simbolo")

print(f"Longitud promedio: {longitud_promedio:.6f} bits/simbolo")

print(f"Eficiencia: {eficiencia:.2f} %")

print(f"Redundancia: {redundancia:.2f} %")

print(f"\nReporte generado correctamente:")
print(f"{nombre_archivo}")