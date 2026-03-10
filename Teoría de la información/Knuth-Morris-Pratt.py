def kmp_explicito(texto, patron):
    n = len(texto)
    m = len(patron)
    
    # 1. Crear la tabla de fallos (Pi)
    pi = [0] * m
    j = 0
    print(f"--- Pre-procesando patrón para KMP ---")
    for i in range(1, m):
        while j > 0 and patron[i] != patron[j]:
            j = pi[j-1]
        if patron[i] == patron[j]:
            j += 1
        pi[i] = j
    print(f"Tabla Pi (cheat sheet): {pi}\n")

    # 2. Buscar en el texto
    print(f"--- Buscando en el texto ---")
    q = 0 # caracteres emparejados
    for i in range(n):
        print(f"Texto:  {texto}")
        print(f"Patrón: {' ' * (i-q)}{patron}")
        print(f"Comparando T[{i}]='{texto[i]}' con P[{q}]='{patron[q]}'")
        
        while q > 0 and patron[q] != texto[i]:
            print(f"  ¡Fallo! Usando tabla Pi para saltar a q={pi[q-1]}")
            q = pi[q-1]
        
        if patron[q] == texto[i]:
            print(f"  ¡Coincide!")
            q += 1
        
        if q == m:
            print(f"--> ¡ENCONTRADO en la posición {i - m + 1}!")
            return i - m + 1
        print("-" * 20)
    return -1


TextoGrande = input("Ingresa el texto enorme (Cadena original):  ")
TextoBuscado = input("Ingresa el texto que buscas (Cadena buscada):  ")

kmp_explicito(TextoGrande, TextoBuscado)