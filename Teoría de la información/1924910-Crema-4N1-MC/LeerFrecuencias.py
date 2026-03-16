from collections import Counter

# nombre del archivo
archivo = "resultado_1924910.txt"

# leer el archivo
with open(archivo, "r", encoding="utf-8") as f:
    texto = f.read()

# convertir a minúsculas
texto = texto.lower()

# eliminar espacios y saltos de línea
texto = texto.replace(" ", "").replace("\n", "")

# contar símbolos
frecuencias = Counter(texto)

# total de símbolos
total = sum(frecuencias.values())

print("Símbolo | Frecuencia | Frecuencia relativa")
print("-------------------------------------------")

for simbolo, freq in sorted(frecuencias.items()):
    freq_rel = freq / total
    print(f"{simbolo:7} {freq:10} {freq_rel:.6f}")

print("\nTotal de símbolos:", total)