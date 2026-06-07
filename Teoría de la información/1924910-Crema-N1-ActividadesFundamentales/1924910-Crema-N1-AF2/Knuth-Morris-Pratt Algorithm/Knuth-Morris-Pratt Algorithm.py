# Algoritmo KMP: No distingue mayúsculas/minúsculas (convierte a MAYÚSCULAS) y omite espacios en blanco

def prefix_function(p: str):
    """Construye la función prefijo (también llamada tabla de fallos) para el patrón"""
    m = len(p)
    a = [0] * m  # Array que almacena la longitud del prefijo propio más largo que también es sufijo

    # Length of the previous longest prefix suffix
    k = 0  # Longitud del prefijo/sufijo actual
    i = 1  # Empezamos desde el segundo carácter

    # Loop calculates a[i] for i = 1 to M-1
    while i < m:
        if p[i] == p[k]:  # Si los caracteres coinciden
            k += 1
            a[i] = k
            i += 1
        else:  # Si no coinciden
            if k != 0:
                k = a[k - 1]  # Retrocedemos usando la tabla
            else:
                a[i] = 0  # No hay prefijo que coincida
                i += 1
    print(f"Prefix function {a}")
    return a


def search(p: str, s: str):
    """Busca todas las ocurrencias del patrón p en el texto s usando KMP"""
    m = len(p)
    n = len(s)

    a = prefix_function(p)  # Obtenemos la tabla de fallos
    result = []  # Lista para almacenar las posiciones donde se encuentra el patrón

    i = 0  # Índice para el texto
    j = 0  # Índice para el patrón
    while (n - i) >= (m - j):  # Mientras queden suficientes caracteres
        if p[j] == s[i]:  # Si hay coincidencia
            j += 1
            i += 1

        if j == m:  # Si encontramos el patrón completo
            result.append(i - j + 1)  # Guardamos la posición (1-indexed)
            j = a[j - 1]  # Retrocedemos para buscar más ocurrencias
        elif i < n and p[j] != s[i]:  # Si hay desajuste
            if j != 0:
                j = a[j - 1]  # Retrocedemos usando la tabla
            else:
                i += 1  # Avanzamos en el texto
    return result


def main():
    # Pedir al usuario el texto y el patrón
    text = input("Ingrese el texto: ")
    pattern = input("Ingrese el patrón a buscar: ")
    
    # Procesamiento: convertir a mayúsculas y eliminar espacios
    text_processed = text.upper().replace(" ", "")  # Texto sin espacios y en mayúsculas
    pattern_processed = pattern.upper().replace(" ", "")  # Patrón sin espacios y en mayúsculas
    
    print(f"\nTexto procesado: {text_processed}")
    print(f"Patrón procesado: {pattern_processed}")
    
    # Buscar el patrón en el texto procesado
    result = search(pattern_processed, text_processed)

    # Mostrar resultados
    if result:
        print(f"\nPatrón encontrado en las posiciones (del texto sin espacios): {result}")
        
        # Información adicional para el usuario
        print("\nNota: Las posiciones mostradas corresponden al texto sin espacios.")
        print(f"Texto original: {text}")
        print(f"Texto sin espacios: {text_processed}")
    else:
        print("\nPatrón no encontrado en el texto.")

main()