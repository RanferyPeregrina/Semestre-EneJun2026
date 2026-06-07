import math
import sys
from itertools import combinations
from copy import deepcopy

# Configuracion del limite de recursion para arboles profundos
sys.setrecursionlimit(2000)

# --- Clase Nodo del Arbol ---
class NodoArbol:
    def __init__(self, simbolo, probabilidad, izquierda=None, derecha=None, es_hoja=True):
        self.simbolo = simbolo
        self.probabilidad = probabilidad
        self.izquierda = izquierda
        self.derecha = derecha
        self.es_hoja = es_hoja
        self.codigo = ""

# --- Funcion para calcular HE (Entropia de la Fuente) ---
def calcular_he(nodos_hoja):
    HE = 0
    for nodo in nodos_hoja:
        prob = nodo.probabilidad
        if prob > 0:
            HE += -prob * math.log2(prob)
    return HE

# --- Funcion para calcular HT (Entropia del Arbol) - OPTIMIZADA ---
def calcular_ht_nodo(diferencia):
    """Calcula la contribucion de HT para una diferencia de probabilidades"""
    if diferencia > 0 and not math.isclose(diferencia, 0):
        return -diferencia * math.log2(diferencia)
    return 0

def calcular_ht_total(nodo, ht_acumulado=0):
    """Calcula HT total recursivamente con acumulador para mejor rendimiento"""
    if nodo.es_hoja:
        return ht_acumulado
    
    ht_total = ht_acumulado
    
    # Calcula la diferencia en este nodo
    if nodo.izquierda and nodo.derecha:
        diferencia = abs(nodo.izquierda.probabilidad - nodo.derecha.probabilidad)
        ht_total += calcular_ht_nodo(diferencia)
    
    # Recursivamente calcular en subarboles
    if nodo.izquierda:
        ht_total = calcular_ht_total(nodo.izquierda, ht_total)
    if nodo.derecha:
        ht_total = calcular_ht_total(nodo.derecha, ht_total)
    
    return ht_total

# --- Funcion para generar codigos ---
def generar_codigos(nodo, codigo_actual, diccionario):
    if nodo is None:
        return
    
    nodo.codigo = codigo_actual
    
    if nodo.es_hoja:
        diccionario[nodo.simbolo] = codigo_actual if codigo_actual else '0'
    
    generar_codigos(nodo.izquierda, codigo_actual + '1', diccionario)
    generar_codigos(nodo.derecha, codigo_actual + '0', diccionario)

# --- Funcion para calcular LMS (Longitud Media de Simbolo) ---
def calcular_lms(nodos_hoja):
    lms = 0
    for nodo in nodos_hoja:
        lms += nodo.probabilidad * len(nodo.codigo)
    return lms

# --- CONSTRUCCION JERARQUICA CON DETECCION DE MEJORA ---
class BusquedaJerarquica:
    def __init__(self, max_sin_mejora=3):
        self.mejor_ht = float('inf')
        self.mejor_arbol = None
        self.contador_sin_mejora = 0
        self.max_sin_mejora = max_sin_mejora
        self.arboles_evaluados = 0
        self.ht_anterior = None
    
    def registrar_intento(self, ht):
        """Registra un intento y determina si se debe continuar"""
        self.arboles_evaluados += 1
        
        # Si encontramos un arbol con HT menor
        if ht < self.mejor_ht:
            mejora = True
            self.mejor_ht = ht
            self.contador_sin_mejora = 0
            print(f"   [NUEVO MEJOR HT: {ht:.6f} - arbol #{self.arboles_evaluados}]")
        else:
            mejora = False
            self.contador_sin_mejora += 1
            print(f"   [sin mejora: {ht:.6f} - contador: {self.contador_sin_mejora}/{self.max_sin_mejora}]")
        
        self.ht_anterior = ht
        
        # Verificar si debemos detener la busqueda
        if self.contador_sin_mejora >= self.max_sin_mejora:
            print(f"\n   >>> DETENCION: {self.max_sin_mejora} arboles consecutivos sin mejora")
            return True  # True = detener busqueda
        return False  # False = continuar
    
    def deberia_detener(self):
        return self.contador_sin_mejora >= self.max_sin_mejora

def construir_arbol_jerarquico_con_detencion(nodos, buscador, nivel=0, profundidad_actual=0, max_profundidad=20):
    """
    Construye arbol Huffman Jerarquico con deteccion de mejora.
    Se detiene si no hay mejora en HT despues de N arboles consecutivos.
    """
    # Verificar si debemos detener la busqueda global
    if buscador.deberia_detener():
        return None, None
    
    # Si solo queda un nodo, es la raiz de un arbol completo
    if len(nodos) == 1:
        ht_total = calcular_ht_total(nodos[0])
        detener = buscador.registrar_intento(ht_total)
        return nodos[0], ht_total
    
    # Limitar profundidad para evitar explosion combinatoria
    if profundidad_actual >= max_profundidad:
        # Usar estrategia greedy para este subarbol
        arbol, ht = construir_huffman_estandar(nodos, calcular_ht=True)
        detener = buscador.registrar_intento(ht)
        return arbol, ht
    
    mejor_arbol_local = None
    mejor_ht_local = float('inf')
    
    # Obtener todas las combinaciones posibles de pares
    indices = list(range(len(nodos)))
    combinaciones_a_explorar = list(combinations(indices, 2))
    
    # Ordenar combinaciones por probabilidad total (mayor a menor)
    # Esto ayuda a encontrar buenos arboles mas rapido
    combinaciones_a_explorar.sort(
        key=lambda idx: nodos[idx[0]].probabilidad + nodos[idx[1]].probabilidad, 
        reverse=True
    )
    
    # Limitar numero de combinaciones si son muchas
    max_combinaciones = 25
    if len(combinaciones_a_explorar) > max_combinaciones:
        combinaciones_a_explorar = combinaciones_a_explorar[:max_combinaciones]
    
    for i, j in combinaciones_a_explorar:
        # Verificar detencion antes de cada iteracion
        if buscador.deberia_detener():
            break
        
        # Crear nueva lista de nodos sin los fusionados
        nuevos_nodos = []
        for k in range(len(nodos)):
            if k != i and k != j:
                nuevos_nodos.append(deepcopy(nodos[k]))
        
        # Crear nodo fusionado
        nodo_izq = deepcopy(nodos[i])
        nodo_der = deepcopy(nodos[j])
        
        # El simbolo del nodo fusionado indica su historia
        if len(nodo_izq.simbolo) > 30 and len(nodo_der.simbolo) > 30:
            # Acortar simbolos para nodos muy profundos
            simbolo_fusion = f"({nodo_izq.simbolo[:15]}...+{nodo_der.simbolo[:15]}...)"
        else:
            simbolo_fusion = f"({nodo_izq.simbolo}+{nodo_der.simbolo})"
        
        prob_fusion = nodo_izq.probabilidad + nodo_der.probabilidad
        
        nodo_padre = NodoArbol(
            simbolo=simbolo_fusion,
            probabilidad=prob_fusion,
            izquierda=nodo_izq,
            derecha=nodo_der,
            es_hoja=False
        )
        
        nuevos_nodos.append(nodo_padre)
        
        # Recursion: construir arboles con esta fusion
        arbol_resultante, ht_parcial = construir_arbol_jerarquico_con_detencion(
            nuevos_nodos, buscador, nivel+1, profundidad_actual+1, max_profundidad
        )
        
        # Si la busqueda se detuvo globalmente, salir
        if buscador.deberia_detener() and arbol_resultante is None:
            break
        
        # Evaluar este arbol
        if arbol_resultante is not None:
            # Calcular diferencia en este nodo
            diferencia = abs(nodo_izq.probabilidad - nodo_der.probabilidad)
            contribucion_nodo = calcular_ht_nodo(diferencia)
            ht_total = ht_parcial + contribucion_nodo if ht_parcial is not None else float('inf')
            
            if ht_total < mejor_ht_local:
                mejor_ht_local = ht_total
                mejor_arbol_local = arbol_resultante
    
    return mejor_arbol_local, mejor_ht_local if mejor_arbol_local else None

def construir_huffman_estandar(nodos, calcular_ht=False):
    """
    Construye arbol Huffman estandar (greedy)
    Si calcular_ht es True, retorna el arbol y su HT
    """
    nodos_temp = deepcopy(nodos)
    contador = 1
    
    while len(nodos_temp) > 1:
        nodos_temp.sort(key=lambda n: n.probabilidad)
        
        izquierdo = nodos_temp.pop(0)
        derecho = nodos_temp.pop(0)
        
        simbolo_padre = f"e{contador}"
        prob_padre = izquierdo.probabilidad + derecho.probabilidad
        
        nodo_padre = NodoArbol(simbolo_padre, prob_padre, izquierdo, derecho, es_hoja=False)
        nodos_temp.append(nodo_padre)
        contador += 1
    
    if calcular_ht:
        ht_total = calcular_ht_total(nodos_temp[0])
        return nodos_temp[0], ht_total
    
    return nodos_temp[0]

# --- Funcion para mostrar tabla de referencia ---
def mostrar_tabla_referencia():
    print("\n" + "-"*60)
    print("TABLA DE REFERENCIA - Numero de arboles sin mejora:")
    print("-"*60)
    print("  VALOR  |  VELOCIDAD  |  CALIDAD  |  RECOMENDADO PARA")
    print("---------|-------------|-----------|------------------")
    print("  1-3    |  MUY RAPIDO |  BASICA   | Textos largos, pruebas rapidas")
    print("  4-6    |  RAPIDO     |  MEDIA    | Uso general, buen equilibrio")
    print("  7-10   |  MODERADO   |  BUENA    | Analisis serios, calidad prioritaria")
    print("  11-15  |  LENTO      |  MUY BUENA| Textos pequenos, max precision")
    print("  16+    |  MUY LENTO  |  EXCELENTE| Investigacion academica")
    print("  INF    |  EXTREMO    |  OPTIMA   | Validacion completa (peligro de tiempo)")
    print("-"*60)
    print("\nSUGERENCIA: Para la mayoria de textos use 6-8")
    print("           Para su texto de 15 simbolos unicos, recomiendo 6")
    print("="*60)

# --- Funcion principal mejorada con pregunta ---
def solicitar_mensaje():
    print("="*60)
    print("        HUFFMAN JERARQUICO CONFIGURABLE")
    print("="*60)
    print("\nINSTRUCCIONES:")
    print("   - Escribe o pega el texto que deseas procesar")
    print("   - Presiona ENTER cuando termines")
    print("   - Los espacios seran ignorados automaticamente")
    print("   - NO se diferencia entre mayusculas y minusculas")
    print("\nCARACTERISTICAS DEL ALGORITMO:")
    print("   - Explora arboles de Huffman buscando minimizar HT")
    print("   - Se detiene despues de X arboles consecutivos SIN MEJORA")
    print("   - Elige el arbol con menor HT encontrado")
    print("-"*60)
    
    texto_ingresado = input("\nTu texto: ").strip()
    
    if not texto_ingresado:
        print("\nERROR: El texto no puede estar vacio.")
        sys.exit(1)
    
    return texto_ingresado

def preguntar_umbral():
    """Pregunta al usuario cuantos arboles sin mejora permitir"""
    print("\n" + "="*60)
    print("CONFIGURACION DE LA BUSQUEDA")
    print("="*60)
    
    mostrar_tabla_referencia()
    
    while True:
        try:
            respuesta = input("\nCuantos arboles sin mejora permitir antes de detenerse? ")
            
            if respuesta.upper() == 'INF':
                return float('inf')
            
            if respuesta.upper() == 'TODO':
                return float('inf')
            
            valor = int(respuesta)
            
            if valor < 1:
                print("   El valor debe ser al menos 1. Usando 1...")
                return 1
            
            if valor > 50:
                print(f"   ADVERTENCIA: {valor} es un valor alto. La busqueda puede ser MUY LENTA.")
                confirmar = input("   ¿Confirmar? (s/n): ").lower()
                if confirmar != 's':
                    continue
            
            return valor
            
        except ValueError:
            print("   Por favor, ingrese un numero entero o 'inf' para exploracion completa")

def calcular_frecuencias(mensaje: str) -> list:
    conteo = {}
    mensaje = mensaje.lower()
    
    for letra in mensaje:
        if letra.isspace():
            continue
        if letra in conteo:
            conteo[letra] += 1
        else:
            conteo[letra] = 1
    
    return sorted(conteo.items(), key=lambda x: (-x[1], x[0]))

def main():
    texto_usuario = solicitar_mensaje()
    frecuencias = calcular_frecuencias(texto_usuario)
    
    if not frecuencias:
        print("Error: El texto no contiene caracteres validos.")
        return
    
    total_caracteres = sum(cant for _, cant in frecuencias)
    nodos_iniciales = []
    
    print("\nSIMBOLOS ENCONTRADOS:")
    for simbolo, cantidad in frecuencias:
        prob = cantidad / total_caracteres
        nodos_iniciales.append(NodoArbol(simbolo, prob, es_hoja=True))
        print(f"   '{simbolo}': {cantidad} veces (prob={prob:.4f})")
    
    num_simbolos = len(nodos_iniciales)
    print(f"\nTotal simbolos unicos: {num_simbolos}")
    
    # Preguntar el umbral al usuario
    umbral = preguntar_umbral()
    
    if umbral == float('inf'):
        print("\n[MODO EXPLORACION COMPLETA] Se exploraran TODOS los arboles posibles")
        print("Esto puede tomar MUCHO tiempo para textos con mas de 10 simbolos...")
    else:
        print(f"\n[MODO CONFIGURADO] Se detendra despues de {umbral} arboles consecutivos SIN mejora")
    
    # Configurar profundidad maxima
    profundidad_max = min(20, num_simbolos * 2)
    
    print(f"Profundidad maxima: {profundidad_max}")
    print(f"\nIniciando busqueda jerarquica...\n")
    
    # Crear buscador con el umbral elegido
    buscador = BusquedaJerarquica(max_sin_mejora=umbral)
    
    # Ejecutar busqueda principal
    arbol_final, ht_final = construir_arbol_jerarquico_con_detencion(
        nodos_iniciales, 
        buscador, 
        max_profundidad=profundidad_max
    )
    
    # Si no se encontro arbol por detencion temprana, usar el mejor encontrado
    if arbol_final is None:
        print("\n[FALLBACK] Usando arbol Huffman estandar...")
        arbol_final, ht_estandar = construir_huffman_estandar(nodos_iniciales, calcular_ht=True)
        ht_final = ht_estandar
    
    # Generar codigos
    codigos_huffman = {}
    generar_codigos(arbol_final, "", codigos_huffman)
    
    # Recolectar nodos hoja para calculos
    nodos_hoja = []
    def recolectar_hojas(nodo):
        if nodo.es_hoja:
            nodos_hoja.append(nodo)
        else:
            if nodo.izquierda:
                recolectar_hojas(nodo.izquierda)
            if nodo.derecha:
                recolectar_hojas(nodo.derecha)
    
    recolectar_hojas(arbol_final)
    
    # Calcular metricas finales
    HE = calcular_he(nodos_hoja)
    HT = calcular_ht_total(arbol_final)
    HIT = HE + HT
    LMS = calcular_lms(nodos_hoja)
    LME = 8.0
    RC = LME / LMS if LMS > 0 else 0
    
    # Guardar resultados
    archivo_resultados = "resultados_huffman_jerarquico.txt"
    with open(archivo_resultados, "w", encoding="utf-8") as archivo:
        archivo.write("="*60 + "\n")
        archivo.write("     RESULTADOS DE HUFFMAN JERARQUICO\n")
        archivo.write("="*60 + "\n\n")
        
        archivo.write(f"TEXTO ORIGINAL:\n   {texto_usuario}\n\n")
        
        archivo.write("CONFIGURACION:\n")
        if umbral == float('inf'):
            archivo.write("   Modo: EXPLORACION COMPLETA\n")
        else:
            archivo.write(f"   Umbral sin mejora: {umbral} arboles\n")
        archivo.write(f"   Arboles evaluados: {buscador.arboles_evaluados}\n\n")
        
        archivo.write("FRECUENCIAS:\n")
        for simbolo, cant in frecuencias:
            archivo.write(f"   '{simbolo}': {cant} veces ({cant/total_caracteres:.4f})\n")
        
        archivo.write("\nCODIGOS HUFFMAN:\n")
        for simbolo, codigo in codigos_huffman.items():
            archivo.write(f"   '{simbolo}' -> {codigo}\n")
        
        archivo.write("\n" + "-"*60 + "\n")
        archivo.write("ENTROPIAS:\n")
        archivo.write(f"   HE (Fuente):  {HE:.6f} bits\n")
        archivo.write(f"   HT (Arbol):   {HT:.6f} bits\n")
        archivo.write(f"   HIT (Total):  {HIT:.6f} bits\n\n")
        
        archivo.write("METRICAS DE COMPRESION:\n")
        archivo.write(f"   LMS: {LMS:.4f} bits\n")
        archivo.write(f"   LME: {LME:.4f} bits\n")
        archivo.write(f"   RC:  {RC:.4f}\n")
        
        archivo.write("\n" + "="*60 + "\n")
        archivo.write("ESTRUCTURA DEL ARBOL SELECCIONADO:\n")
        
        def imprimir_arbol(nodo, nivel=0):
            indent = "  " * nivel
            if nodo.es_hoja:
                archivo.write(f"{indent}hoja: '{nodo.simbolo}' (p={nodo.probabilidad:.4f})\n")
            else:
                # Acortar simbolos largos en el archivo
                simbolo_limpio = nodo.simbolo[:60] if len(nodo.simbolo) > 60 else nodo.simbolo
                archivo.write(f"{indent}nodo: {simbolo_limpio} (p={nodo.probabilidad:.4f})\n")
                if nodo.izquierda:
                    imprimir_arbol(nodo.izquierda, nivel+1)
                if nodo.derecha:
                    imprimir_arbol(nodo.derecha, nivel+1)
        
        imprimir_arbol(arbol_final)
    
    print("\n" + "="*60)
    print("PROCESO COMPLETADO")
    print("="*60)
    print(f"ARBOLES EVALUADOS: {buscador.arboles_evaluados}")
    print(f"MEJOR HT ENCONTRADO: {buscador.mejor_ht:.6f}")
    print(f"HT DEL ARBOL FINAL: {HT:.6f}")
    print("-"*60)
    print(f"HE (Fuente):  {HE:.6f} bits")
    print(f"HT (Arbol):   {HT:.6f} bits")
    print(f"HIT (Total):  {HIT:.6f} bits")
    print(f"LMS:          {LMS:.4f} bits")
    print(f"RC:           {RC:.4f}")
    print("\n" + "="*60)
    print(f"Resultados guardados en: {archivo_resultados}")

if __name__ == "__main__":
    main()