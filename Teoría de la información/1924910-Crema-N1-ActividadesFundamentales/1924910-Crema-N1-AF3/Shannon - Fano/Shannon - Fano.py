# -*- coding: utf-8 -*-
"""
Created on Tue May 26 14:22:19 2026

@author: blavi
"""

import math
from collections import Counter

def generar_shannon_fano(simbolos, codigo_actual="", codigos=None):

    if codigos is None:
        codigos = {}

    if len(simbolos) == 1:
        simbolo = simbolos[0][0]
        codigos[simbolo] = codigo_actual if codigo_actual != "" else "0"
        return codigos

    total = sum(freq for _, freq in simbolos)

    acumulado = 0
    mejor_indice = 0
    diferencia_minima = float("inf")

    for i in range(len(simbolos)):
        acumulado += simbolos[i][1]

        diferencia = abs((total / 2) - acumulado)

        if diferencia < diferencia_minima:
            diferencia_minima = diferencia
            mejor_indice = i

    izquierda = simbolos[:mejor_indice + 1]
    derecha = simbolos[mejor_indice + 1:]

    generar_shannon_fano(izquierda, codigo_actual + "0", codigos)

    if derecha:
        generar_shannon_fano(derecha, codigo_actual + "1", codigos)

    return codigos


print("======================================")
print(" METODO DE CODIFICACION SHANNON-FANO")
print("======================================")

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

codigos = generar_shannon_fano(simbolos_ordenados)

resultados = []

entropia_total = 0
longitud_promedio = 0

mensaje_codificado = ""

for simbolo in mensaje:
    mensaje_codificado += codigos[simbolo]

for simbolo, frecuencia in simbolos_ordenados:

    probabilidad = frecuencia / total_simbolos

    informacion = -math.log2(probabilidad)

    entropia_individual = probabilidad * informacion

    entropia_total += entropia_individual

    codigo = codigos[simbolo]

    longitud_codigo = len(codigo)

    longitud_promedio += (
        probabilidad * longitud_codigo
    )

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
        "frecuencia": frecuencia,
        "probabilidad": probabilidad,
        "informacion": informacion,
        "entropia_individual": entropia_individual,
        "longitud_codigo": longitud_codigo,
        "codigo": codigo,
        "binario": binario_ascii
    })

eficiencia = (
    entropia_total / longitud_promedio
) * 100

redundancia = 100 - eficiencia

nombre_archivo = "resultado_shannon_fano.txt"

with open(nombre_archivo, "w", encoding="utf-8") as archivo:

    archivo.write("====================================================\n")
    archivo.write("   REPORTE DEL METODO SHANNON-FANO\n")
    archivo.write("====================================================\n\n")

    archivo.write("MENSAJE ORIGINAL:\n")
    archivo.write("----------------------------------------------------\n")
    archivo.write(mensaje + "\n\n")

    archivo.write("MENSAJE CODIFICADO:\n")
    archivo.write("----------------------------------------------------\n")
    archivo.write(mensaje_codificado + "\n\n")

    archivo.write("TOTAL DE SIMBOLOS:\n")
    archivo.write("----------------------------------------------------\n")
    archivo.write(f"{total_simbolos} simbolos\n\n")

    archivo.write("TABLA DE RESULTADOS:\n")
    archivo.write("----------------------------------------------------------------------------------------------------------------------------\n")

    archivo.write(
        f"{'SIMBOLO':15}"
        f"{'FRECUENCIA':12}"
        f"{'PROBABILIDAD':15}"
        f"{'I(x) bits':15}"
        f"{'H(x) bits':15}"
        f"{'LONGITUD':12}"
        f"{'CODIGO':15}"
        f"{'BINARIO ASCII'}\n"
    )

    archivo.write("----------------------------------------------------------------------------------------------------------------------------\n")

    for r in resultados:

        archivo.write(
            f"{r['simbolo']:15}"
            f"{r['frecuencia']:<12}"
            f"{r['probabilidad']:<15.6f}"
            f"{r['informacion']:<15.6f}"
            f"{r['entropia_individual']:<15.6f}"
            f"{r['longitud_codigo']:<12}"
            f"{r['codigo']:<15}"
            f"{r['binario']}\n"
        )

    archivo.write("----------------------------------------------------------------------------------------------------------------------------\n\n")

    archivo.write("RESULTADOS FINALES:\n")
    archivo.write("----------------------------------------------------\n")

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

print("\n======================================")
print("RESULTADOS OBTENIDOS")
print("======================================")

print(f"\nTotal de simbolos: {total_simbolos}")

print(f"\nEntropia total: {entropia_total:.6f} bits/simbolo")

print(f"Longitud promedio: {longitud_promedio:.6f} bits/simbolo")

print(f"Eficiencia: {eficiencia:.2f} %")

print(f"Redundancia: {redundancia:.2f} %")

print(f"\nReporte generado correctamente:")
print(f"{nombre_archivo}")