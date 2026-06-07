# ============================================
# COMPARACIÓN SIDE BY SIDE
# comparacion.py
# ============================================

# -------------------------------------------------
# LEER ARCHIVOS
# -------------------------------------------------

with open("mensaje_original.txt", "r", encoding="utf-8") as archivo:
    original = archivo.read()

with open("texto_recuperado.txt", "r", encoding="utf-8") as archivo:
    recuperado = archivo.read()


# -------------------------------------------------
# FUNCIÓN PARA COMPARAR
# -------------------------------------------------
def comparar_textos(texto1, texto2):

    longitud_maxima = max(len(texto1), len(texto2))

    print("\n" + "=" * 90)
    print("COMPARACIÓN SIDE BY SIDE")
    print("=" * 90)

    encabezado1 = "ORIGINAL"
    encabezado2 = "RECUPERADO"

    print(f"{encabezado1:<40} | {encabezado2:<40}")
    print("-" * 90)

    diferencias = 0

    for i in range(longitud_maxima):

        c1 = texto1[i] if i < len(texto1) else " "
        c2 = texto2[i] if i < len(texto2) else " "

        marca = "OK"

        if c1 != c2:
            marca = "ERROR"
            diferencias += 1

        print(f"{c1:<40} | {c2:<40} [{marca}]")

    print("\n" + "=" * 90)

    print(f"Total de diferencias: {diferencias}")

    if diferencias == 0:
        print("Recuperación exitosa")
    else:
        print("Existen diferencias entre el mensaje original y el recuperado")


# -------------------------------------------------
# EJECUTAR COMPARACIÓN
# -------------------------------------------------
comparar_textos(original, recuperado)