# ============================================
# GENERADOR DE TRANSMISIÓN
# generar.py
# ============================================

import random


# -------------------------------------------------
# TEXTOS BASE
# -------------------------------------------------
fragmentos = [
    "En un lugar de la Mancha de cuyo nombre no quiero acordarme",
    "La inteligencia artificial transforma la manera de resolver problemas",
    "La teoría de la información estudia la transmisión de datos",
    "El conocimiento se construye mediante observación y experiencia",
    "Las redes neuronales pueden aprender patrones complejos",
    "La comunicación digital requiere mecanismos de detección de errores",
    "La programación permite automatizar procesos repetitivos",
    "Los algoritmos de compresión reducen el tamaño de los archivos"
]


# -------------------------------------------------
# GENERAR TEXTO ALEATORIO
# -------------------------------------------------
def generar_texto():

    cantidad = random.randint(2, 4)

    texto = ". ".join(random.sample(fragmentos, cantidad))

    return texto + "."


# -------------------------------------------------
# CONVERTIR TEXTO A BINARIO
# -------------------------------------------------
def texto_a_binario(texto):

    binario = ""

    for caracter in texto:

        # ord() -> ASCII
        # format(..., '08b') -> binario de 8 bits
        binario += format(ord(caracter), '08b')

    return binario


# -------------------------------------------------
# CÓDIGO DE REPETICIÓN
# -------------------------------------------------
def codificar_repeticion(datos, n):

    resultado = ""

    for bit in datos:
        resultado += bit * n

    return resultado


# -------------------------------------------------
# GENERAR MENSAJE
# -------------------------------------------------
texto_original = generar_texto()

print("TEXTO ORIGINAL:\n")
print(texto_original)

# -------------------------------------------------
# BINARIZAR
# -------------------------------------------------
binario = texto_a_binario(texto_original)

print("\nBINARIO:\n")
print(binario)

# -------------------------------------------------
# CODIFICAR
# -------------------------------------------------
repeticiones = 3

codificado = codificar_repeticion(binario, repeticiones)

print("\nBITS TRANSMITIDOS:\n")
print(codificado)

# -------------------------------------------------
# GUARDAR ARCHIVOS
# -------------------------------------------------
with open("mensaje_original.txt", "w", encoding="utf-8") as archivo:
    archivo.write(texto_original)

with open("binario.txt", "w") as archivo:
    archivo.write(binario)

with open("transmision.txt", "w") as archivo:
    archivo.write(codificado)

print("\nArchivos generados:")
print("- mensaje_original.txt")
print("- binario.txt")
print("- transmision.txt")

print("\nAhora puedes modificar manualmente 'transmision.txt'")
print("para simular errores de transmisión.")