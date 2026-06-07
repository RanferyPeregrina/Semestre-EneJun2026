# BOYER-MOORE: Busca patrones ignorando mayúsculas/minúsculas (todo a MAYÚSCULAS) y eliminando los espacios mostrando el proceso visualmente.
# Soporta texto ASCII (caracteres estándar)

# Tamaño del alfabeto ASCII (256 caracteres)
NO_OF_CHARS = 256


def heuristica_mal_caracter(cadena: str, tamaño: int):
    """Crea la tabla de último desplazamiento para cada carácter"""
    mal_caracter = [-1] * NO_OF_CHARS

    for i in range(tamaño):
        mal_caracter[ord(cadena[i])] = i

    return mal_caracter


def imprimir_alineacion(texto: str, patron: str, desplazamiento: int):
    """Muestra texto y patrón alineados visualmente"""
    t_linea = "T\t"
    p_linea = "P\t"

    for i in range(len(texto)):
        t_linea += texto[i] + " "

    for i in range(desplazamiento):
        p_linea += "  "
    for i in range(len(patron)):
        p_linea += patron[i] + " "

    print(t_linea)
    print(p_linea)


def imprimir_alineacion_detallada(texto: str, patron: str, desplazamiento: int, mc=None, bs=None):
    """Muestra alineación con información adicional de reglas"""
    print("-" * 60)
    t_linea = "T\t"
    p_linea = "P\t"

    for i in range(len(texto)):
        t_linea += texto[i] + " "

    for i in range(desplazamiento):
        p_linea += "  "
    for i in range(len(patron)):
        p_linea += patron[i] + " "

    if mc is not None:
        t_linea += f"\tMC: {mc}"  # MC = Mal Carácter
    if bs is not None:
        p_linea += f"\tBS: {bs}"  # BS = Buen Sufijo

    print(t_linea)
    print(p_linea)
    print("-" * 60)


def buscar(texto: str, patron: str, visualizar=True):
    """Algoritmo Boyer-Moore (solo heurística de mal carácter)"""
    m = len(patron)
    n = len(texto)

    # Preprocesamiento: tabla de mal carácter
    mal_caracter = heuristica_mal_caracter(patron, m)

    s = 0  # desplazamiento actual
    ocurrencias = []

    while s <= n - m:
        j = m - 1  # comparar desde el final del patrón

        if visualizar:
            desplazamiento_mc = 1
            desplazamiento_bs = j + 1
            imprimir_alineacion_detallada(texto, patron, s, desplazamiento_mc, desplazamiento_bs)

        # Comparar patrón con texto desde derecha a izquierda
        while j >= 0 and patron[j] == texto[s + j]:
            j -= 1

        if j < 0:  # Patrón encontrado
            ocurrencias.append(s)
            if visualizar:
                print(f"Patrón encontrado en posición {s}")
            s += 1  # Desplazar para buscar más ocurrencias
        else:
            # Regla del mal carácter
            desplazamiento_mc = max(1, j - mal_caracter[ord(texto[s + j])])
            s += desplazamiento_mc

            if visualizar:
                print(f"Desplazamiento de {desplazamiento_mc} usando regla de Mal Carácter")

    return ocurrencias


def main():
    # Solicitar datos al usuario
    texto_original = input("Ingrese el texto: ")
    patron_original = input("Ingrese el patrón a buscar: ")
    
    # Convertir a mayúsculas y eliminar espacios para la búsqueda
    texto = texto_original.upper().replace(" ", "")
    patron = patron_original.upper().replace(" ", "")
    
    print("\n--- DATOS ORIGINALES ---")
    print("Texto original:", texto_original)
    print("Patrón original:", patron_original)
    
    print("\n--- BÚSQUEDA (sin distinguir mayúsculas/minúsculas y sin espacios) ---")
    print("Texto normalizado:", texto)
    print("Patrón normalizado:", patron)
    print()

    ocurrencias = buscar(texto, patron, visualizar=True)
    
    if ocurrencias:
        print(f"\nPatrón encontrado en posiciones (sobre texto normalizado):", ocurrencias)
    else:
        print("\nPatrón no encontrado")

main()