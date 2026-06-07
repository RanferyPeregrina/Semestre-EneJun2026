# ============================================
# SIMULADOR DE ERRORES
# errores.py
# ============================================

import random


# -------------------------------------------------
# CONFIGURACIÓN
# -------------------------------------------------

# Probabilidad de cambiar un bit
probabilidad_error = 0.03   # 3%

# Archivo original
archivo_entrada = "transmision.txt"

# Archivo con errores
archivo_salida = "transmision_con_errores.txt"


# -------------------------------------------------
# LEER TRANSMISIÓN
# -------------------------------------------------
with open(archivo_entrada, "r") as archivo:
    datos = archivo.read().strip()

print("Bits originales cargados.")

# -------------------------------------------------
# INTRODUCIR ERRORES
# -------------------------------------------------
resultado = ""

errores = 0

for bit in datos:

    # Generar número aleatorio
    if random.random() < probabilidad_error:

        # Invertir bit
        if bit == "0":
            resultado += "1"
        else:
            resultado += "0"

        errores += 1

    else:
        resultado += bit


# -------------------------------------------------
# GUARDAR RESULTADO
# -------------------------------------------------
with open(archivo_salida, "w") as archivo:
    archivo.write(resultado)

# -------------------------------------------------
# MOSTRAR RESULTADOS
# -------------------------------------------------
print("\nArchivo generado:")
print(archivo_salida)

print(f"\nCantidad de errores introducidos: {errores}")

print(f"\nProbabilidad de error usada: {probabilidad_error * 100}%")

print("\nAhora usa este archivo en el receptor.")