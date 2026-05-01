def lz77_codificar(texto: str, tam_ventana: int = 26) -> list:
    """
    Codifica un texto usando LZ77 con ventana deslizante.
    
    Parámetros:
        texto: cadena de entrada
        tam_ventana: tamaño total de la ventana (histórico + lookahead)
    
    Devuelve:
        lista de tripletas (offset, longitud, caracter)
    """
    # 1. Tamaños de histórico y lookahead (70% aproximado)
    tam_historico = max(1, int(tam_ventana * 0.7))      # 18 para ventana 26
    tam_lookahead = tam_ventana - tam_historico          # 8 para ventana 26

    print(f"Ventana total: {tam_ventana}")
    print(f"Histórico: {tam_historico} caracteres")
    print(f"Lookahead: {tam_lookahead} caracteres\n")

    tripletas = []
    # El lookahead empieza justo después del histórico inicial
    pos = tam_historico                  # índice del primer carácter del lookahead

    # 2. Bucle principal: mientras queden caracteres en el lookahead
    while pos < len(texto):
        # -- Obtener las dos partes de la ventana actual --
        inicio_hist = max(0, pos - tam_historico)
        historico = texto[inicio_hist : pos]
        lookahead = texto[pos : pos + tam_lookahead]

        if not lookahead:
            break   # ya no hay nada que codificar

        # -- Buscar la coincidencia más larga en el histórico --
        mejor_offset = 0
        mejor_long = 0

        # Probamos cada posición del histórico como inicio de coincidencia
        for i in range(len(historico)):
            long_actual = 0
            # Comparar mientras no se acabe el lookahead, el histórico
            # y los caracteres coincidan
            while (long_actual < len(lookahead) and
                   i + long_actual < len(historico) and
                   historico[i + long_actual] == lookahead[long_actual]):
                long_actual += 1

            if long_actual > mejor_long:
                mejor_long = long_actual
                # Offset = distancia desde el borde izquierdo del lookahead
                # hacia atrás, contando de derecha a izquierda (ver PDF).
                mejor_offset = len(historico) - i

        # -- Determinar el carácter de ruptura --
        if mejor_long < len(lookahead):
            # La coincidencia no cubrió todo el lookahead
            caracter_ruptura = lookahead[mejor_long]
        else:
            # Cubrió todo el lookahead; el carácter siguiente está más allá
            if pos + mejor_long < len(texto):
                caracter_ruptura = texto[pos + mejor_long]
            else:
                # Caso especial: final exacto del texto.
                # Emitimos una tripleta con carácter vacío y terminamos.
                tripletas.append((mejor_offset, mejor_long, ''))
                break

        # -- Guardar la tripleta --
        tripletas.append((mejor_offset, mejor_long, caracter_ruptura))

        # -- Mostrar paso actual (opcional, para entender el proceso) --
        print(f"Histórico    : '{historico}'")
        print(f"Lookahead    : '{lookahead}'")
        print(f"→ tripleta   : ({mejor_offset}, {mejor_long}, '{caracter_ruptura}')")
        print(f"  (coincidencia de {mejor_long} caracteres a {mejor_offset} posiciones)\n")

        # -- Deslizar la ventana: avanzar longitud + 1 caracteres --
        pos += mejor_long + 1

    return tripletas


# ============================================================
# EJEMPLO DE USO (con una frase que contenga repeticiones)
# ============================================================
if __name__ == "__main__":
    # Frase de ejemplo (similar a la del PDF, pero ajustada para ventana 18+8)
    frase = "She sells sea shells by the sea shore. The shells she sells are surely seashells."
    print("TEXTO ORIGINAL:")
    print(frase, "\n")

    # Ventana total 26 -> histórico 18, lookahead 8
    resultado = lz77_codificar(frase, tam_ventana=26)

    print("\n--- RESULTADO FINAL ---")
    for i, t in enumerate(resultado):
        print(f"{i+1:3d}: offset={t[0]:2d}, longitud={t[1]:1d}, caracter='{t[2]}'")