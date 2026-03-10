def boyer_moore_explicito(texto, patron):
    m = len(patron)
    n = len(texto)
    
    # Pre-procesamiento: Regla del Carácter Malo
    # Guardamos la última posición de cada letra en el patrón
    tabla_saltos = {letra: m for letra in set(patron)}
    for i in range(m - 1):
        tabla_saltos[patron[i]] = m - 1 - i
        
    print(f"--- Iniciando Boyer-Moore ---")
    print(f"Texto: {texto}")
    print(f"Patrón: {patron}")
    print(f"Tabla de saltos (carácter malo): {tabla_saltos}\n")

    i = 0
    while i <= n - m:
        j = m - 1
        print(f"Alineación actual: {texto}")
        print(f"{' ' * i}{patron} (comparando desde el final...)")
        
        while j >= 0 and patron[j] == texto[i + j]:
            print(f"  ¡Coincidencia! '{patron[j]}' en pos {i+j}")
            j -= 1
        
        if j < 0:
            print(f"--> ¡ENCONTRADO en la posición {i}!")
            return i
        else:
            char_malo = texto[i + j]
            salto = tabla_saltos.get(char_malo, m)
            print(f"  Fallo: '{char_malo}' no coincide con '{patron[j]}'")
            print(f"  Saltando {salto} espacios...\n")
            i += salto
    return -1

# Prueba
#Hola hola
#Programa hecho para la clase de Teoría de la Información y Métodos de Codificación
#1924910

TextoGrande = input("Ingresa el texto enorme (Cadena original):  ")
TextoBuscado = input("Ingresa el texto que buscas (Cadena buscada):  ")

boyer_moore_explicito(TextoGrande, TextoBuscado)

input()