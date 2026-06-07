# -*- coding: utf-8 -*-
"""
Created on Tue May 26 15:14:50 2026

@author: blavi
"""

from collections import Counter

print("===================================================")
print(" CODIFICACION ARITMETICA ADAPTATIVA")
print("===================================================")

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

frecuencias = {}

for caracter in mensaje:
    if caracter not in frecuencias:
        frecuencias[caracter] = 1

simbolos = sorted(frecuencias.keys())

inferior = 0.0
superior = 1.0

procesos = []

mensaje_codificado = ""

for indice, simbolo_actual in enumerate(mensaje):

    total_frecuencias = sum(frecuencias.values())

    probabilidades = {}
    acumulada = 0.0

    for simbolo in simbolos:

        probabilidad = (
            frecuencias[simbolo] /
            total_frecuencias
        )

        limite_inferior = acumulada
        limite_superior = acumulada + probabilidad

        probabilidades[simbolo] = {
            "probabilidad": probabilidad,
            "inferior": limite_inferior,
            "superior": limite_superior
        }

        acumulada = limite_superior

    rango = superior - inferior

    nuevo_inferior = (
        inferior +
        rango *
        probabilidades[simbolo_actual]["inferior"]
    )

    nuevo_superior = (
        inferior +
        rango *
        probabilidades[simbolo_actual]["superior"]
    )

    procesos.append({
        "paso": indice + 1,
        "simbolo": simbolo_actual,
        "inferior_anterior": inferior,
        "superior_anterior": superior,
        "nuevo_inferior": nuevo_inferior,
        "nuevo_superior": nuevo_superior
    })

    inferior = nuevo_inferior
    superior = nuevo_superior

    frecuencias[simbolo_actual] += 1

codigo_final = (inferior + superior) / 2

binario_codigo = format(
    int(codigo_final * (2 ** 32)),
    '032b'
)

nombre_archivo = "resultado_aritmetica_adaptativa.txt"

with open(nombre_archivo, "w", encoding="utf-8") as archivo:

    archivo.write("=========================================================\n")
    archivo.write("   REPORTE DE CODIFICACION ARITMETICA ADAPTATIVA\n")
    archivo.write("=========================================================\n\n")

    archivo.write("MENSAJE ORIGINAL:\n")
    archivo.write("---------------------------------------------------------\n")
    archivo.write(mensaje + "\n\n")

    archivo.write("TOTAL DE SIMBOLOS:\n")
    archivo.write("---------------------------------------------------------\n")
    archivo.write(f"{len(mensaje)} simbolos\n\n")

    archivo.write("PROCESO DE CODIFICACION:\n")
    archivo.write("----------------------------------------------------------------------------------------------------------------------------\n")

    archivo.write(
        f"{'PASO':8}"
        f"{'SIMBOLO':15}"
        f"{'INF. ANTERIOR':20}"
        f"{'SUP. ANTERIOR':20}"
        f"{'NUEVO INF.':20}"
        f"{'NUEVO SUP.'}\n"
    )

    archivo.write("----------------------------------------------------------------------------------------------------------------------------\n")

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
            f"{p['paso']:<8}"
            f"{simbolo_mostrar:15}"
            f"{p['inferior_anterior']:<20.10f}"
            f"{p['superior_anterior']:<20.10f}"
            f"{p['nuevo_inferior']:<20.10f}"
            f"{p['nuevo_superior']:.10f}\n"
        )

    archivo.write("----------------------------------------------------------------------------------------------------------------------------\n\n")

    archivo.write("RESULTADOS FINALES:\n")
    archivo.write("---------------------------------------------------------\n")

    archivo.write(
        f"Intervalo final: [{inferior}, {superior})\n"
    )

    archivo.write(
        f"Codigo aritmetico final: {codigo_final}\n"
    )

    archivo.write(
        f"Codigo binario final: {binario_codigo}\n"
    )

print("\n===================================================")
print("RESULTADOS OBTENIDOS")
print("===================================================")

print(f"\nIntervalo final: [{inferior}, {superior})")

print(f"\nCodigo aritmetico final: {codigo_final}")

print(f"\nCodigo binario final:")
print(binario_codigo)

print(f"\nReporte generado correctamente:")
print(nombre_archivo)