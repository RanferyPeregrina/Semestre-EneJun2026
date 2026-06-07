# ============================================
# DETECCIÓN Y CORRECCIÓN DE ERRORES
# receptor.py
# ============================================

# -------------------------------------------------
# CONFIGURACIÓN
# -------------------------------------------------

# Número de repeticiones usadas al transmitir
repeticiones = 3

# Archivo recibido
archivo_entrada = "transmision_con_errores.txt"


# -------------------------------------------------
# DETECCIÓN DE ERRORES
# -------------------------------------------------
def detectar_errores(datos, n):

    errores = []

    for i in range(0, len(datos), n):

        bloque = datos[i:i+n]

        # Si los bits no son iguales, hubo error
        if len(set(bloque)) > 1:
            errores.append((i // n, bloque))

    return errores


# -------------------------------------------------
# CORRECCIÓN POR MAYORÍA
# -------------------------------------------------
def corregir_y_decodificar(datos, n):

    resultado = ""

    for i in range(0, len(datos), n):

        bloque = datos[i:i+n]

        unos = bloque.count("1")
        ceros = bloque.count("0")

        # Votación mayoritaria
        if unos > ceros:
            resultado += "1"
        else:
            resultado += "0"

    return resultado


# -------------------------------------------------
# CONVERTIR BINARIO A TEXTO
# -------------------------------------------------
def binario_a_texto(binario):

    texto = ""

    # Tomar bloques de 8 bits
    for i in range(0, len(binario), 8):

        byte = binario[i:i+8]

        # Verificar tamaño correcto
        if len(byte) == 8:

            numero = int(byte, 2)

            texto += chr(numero)

    return texto


# -------------------------------------------------
# LEER ARCHIVO RECIBIDO
# -------------------------------------------------
with open(archivo_entrada, "r") as archivo:

    recibido = archivo.read().strip()

print("BITS RECIBIDOS:\n")
print(recibido)


# -------------------------------------------------
# DETECTAR ERRORES
# -------------------------------------------------
errores = detectar_errores(recibido, repeticiones)

print("\n===================================")
print("ERRORES DETECTADOS")
print("===================================")

if errores:

    print(f"\nCantidad de bloques con error: {len(errores)}\n")

    for posicion, bloque in errores:

        print(f"Bloque {posicion}: {bloque}")

else:

    print("\nNo se detectaron errores")


# -------------------------------------------------
# CORREGIR Y DECODIFICAR
# -------------------------------------------------
binario_recuperado = corregir_y_decodificar(
    recibido,
    repeticiones
)

print("\n===================================")
print("BINARIO RECUPERADO")
print("===================================\n")

print(binario_recuperado)


# -------------------------------------------------
# RECUPERAR TEXTO
# -------------------------------------------------
texto_recuperado = binario_a_texto(binario_recuperado)

print("\n===================================")
print("TEXTO RECUPERADO")
print("===================================\n")

print(texto_recuperado)


# -------------------------------------------------
# GUARDAR RESULTADO
# -------------------------------------------------
with open("texto_recuperado.txt", "w", encoding="utf-8") as archivo:

    archivo.write(texto_recuperado)

print("\nArchivo generado:")
print("texto_recuperado.txt")