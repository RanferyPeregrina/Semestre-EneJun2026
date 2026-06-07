import math
import sys
from itertools import combinations
from copy import deepcopy

# Configuracion del limite de recursion
sys.setrecursionlimit(2000)

# --- Clase Nodo del Arbol Ternario ---
class NodoArbolTernario:
    def __init__(self, simbolo, probabilidad, izquierda=None, centro=None, derecha=None, es_hoja=True):
        self.simbolo = simbolo
        self.probabilidad = probabilidad
        self.izquierda = izquierda   # Digito 0
        self.centro = centro         # Digito 1
        self.derecha = derecha       # Digito *
        self.es_hoja = es_hoja
        self.codigo = ""

# --- Funciones de entropia ---
def calcular_he(nodos_hoja):
    HE = 0
    for nodo in nodos_hoja:
        prob = nodo.probabilidad
        if prob > 0:
            HE += -prob * math.log2(prob)
    return HE

def calcular_ht_nodo_ternario(probabilidades):
    """
    Calcula la contribucion de HT para una fusion ternaria.
    La entropia se calcula sobre las tres probabilidades.
    """
    # Filtrar probabilidades cero
    probs = [p for p in probabilidades if p > 0 and not math.isclose(p, 0)]
    
    if len(probs) < 2:
        return 0
    
    ht = 0
    for i, p1 in enumerate(probs):
        for j, p2 in enumerate(probs):
            if i < j:
                diferencia = abs(p1 - p2)
                if diferencia > 0 and not math.isclose(diferencia, 0):
                    ht += -diferencia * math.log2(diferencia) / 2  # Promedio
    
    return ht

def calcular_ht_total_ternario(nodo, ht_acumulado=0):
    """Calcula HT total recursivamente para arbol ternario"""
    if nodo.es_hoja:
        return ht_acumulado
    
    ht_total = ht_acumulado
    
    # Recolectar probabilidades de los hijos no nulos
    probs = []
    if nodo.izquierda:
        probs.append(nodo.izquierda.probabilidad)
    if nodo.centro:
        probs.append(nodo.centro.probabilidad)
    if nodo.derecha:
        probs.append(nodo.derecha.probabilidad)
    
    if len(probs) >= 2:
        ht_total += calcular_ht_nodo_ternario(probs)
    
    # Recursivamente calcular en subarboles
    if nodo.izquierda:
        ht_total = calcular_ht_total_ternario(nodo.izquierda, ht_total)
    if nodo.centro:
        ht_total = calcular_ht_total_ternario(nodo.centro, ht_total)
    if nodo.derecha:
        ht_total = calcular_ht_total_ternario(nodo.derecha, ht_total)
    
    return ht_total

# --- Funcion para generar codigos ternarios ---
def generar_codigos_ternarios(nodo, codigo_actual, diccionario):
    if nodo is None:
        return
    
    nodo.codigo = codigo_actual
    
    if nodo.es_hoja:
        diccionario[nodo.simbolo] = codigo_actual if codigo_actual else '0'
    
    generar_codigos_ternarios(nodo.izquierda, codigo_actual + '0', diccionario)
    generar_codigos_ternarios(nodo.centro, codigo_actual + '1', diccionario)
    generar_codigos_ternarios(nodo.derecha, codigo_actual + '*', diccionario)

# --- Funcion para calcular LMS en base 2 (para comparacion) ---
def calcular_lms_ternario(nodos_hoja, codigos):
    """
    Calcula la longitud media en bits.
    Como los codigos ternarios usan digitos en base 3,
    cada digito ternario equivale a log2(3) ≈ 1.585 bits
    """
    bits_por_digito = math.log2(3)  # ≈ 1.58496
    
    lms_ternario = 0
    for nodo in nodos_hoja:
        if nodo.simbolo in codigos:
            lms_ternario += nodo.probabilidad * len(codigos[nodo.simbolo])
    
    # Convertir a bits
    lms_bits = lms_ternario * bits_por_digito
    return lms_bits, lms_ternario

# --- CONSTRUCCION DE HUFFMAN TERNARIO ---
class BusquedaTernaria:
    def __init__(self, max_sin_mejora=3):
        self.mejor_ht = float('inf')
        self.mejor_lms = float('inf')
        self.mejor_arbol = None
        self.contador_sin_mejora = 0
        self.max_sin_mejora = max_sin_mejora
        self.arboles_evaluados = 0
    
    def calcular_puntaje(self, arbol, nodos_hoja, codigos):
        """Calcula puntaje combinado (HT + LMS normalizado)"""
        ht = calcular_ht_total_ternario(arbol)
        lms_bits, _ = calcular_lms_ternario(nodos_hoja, codigos)
        
        # Puntaje: menor es mejor
        puntaje = ht + (lms_bits / 10)  # LMS tiene menos peso
        return puntaje, ht, lms_bits
    
    def registrar_intento(self, arbol, nodos_hoja, codigos):
        """Registra un intento y determina si se debe continuar"""
        self.arboles_evaluados += 1
        
        puntaje, ht, lms = self.calcular_puntaje(arbol, nodos_hoja, codigos)
        
        # Criterio de mejora: mejora HT o mejora LMS significativamente
        mejora_ht = ht < (self.mejor_ht - 0.0001)
        mejora_lms = lms < (self.mejor_lms - 0.01)
        
        if mejora_ht or mejora_lms:
            if mejora_ht:
                print(f"   [NUEVO MEJOR HT: {ht:.6f} | arbol #{self.arboles_evaluados}]")
            if mejora_lms:
                print(f"   [NUEVO MEJOR LMS: {lms:.4f} bits | arbol #{self.arboles_evaluados}]")
            
            self.mejor_ht = min(self.mejor_ht, ht)
            self.mejor_lms = min(self.mejor_lms, lms)
            self.mejor_arbol = deepcopy(arbol)
            self.contador_sin_mejora = 0
            return False
        else:
            self.contador_sin_mejora += 1
            print(f"   [sin mejora: HT={ht:.6f} LMS={lms:.4f} | contador: {self.contador_sin_mejora}/{self.max_sin_mejora}]")
            
            if self.contador_sin_mejora >= self.max_sin_mejora:
                print(f"\n   >>> DETENCION: {self.max_sin_mejora} arboles consecutivos sin mejora")
                return True
        
        return False
    
    def deberia_detener(self):
        return self.contador_sin_mejora >= self.max_sin_mejora

def construir_arbol_ternario(nodos, buscador, profundidad_actual=0, max_profundidad=15):
    """
    Construye arbol Huffman Ternario explorando combinaciones de 2 o 3 nodos
    """
    if buscador.deberia_detener():
        return None
    
    # Si solo queda un nodo, es la raiz
    if len(nodos) == 1:
        hojas = []
        def recolectar_hojas(n):
            if n.es_hoja:
                hojas.append(n)
            else:
                if n.izquierda:
                    recolectar_hojas(n.izquierda)
                if n.centro:
                    recolectar_hojas(n.centro)
                if n.derecha:
                    recolectar_hojas(n.derecha)
        
        recolectar_hojas(nodos[0])
        codigos_temp = {}
        generar_codigos_ternarios(nodos[0], "", codigos_temp)
        detener = buscador.registrar_intento(nodos[0], hojas, codigos_temp)
        return nodos[0]
    
    # Limitar profundidad
    if profundidad_actual >= max_profundidad:
        arbol = construir_huffman_estandar_ternario(nodos)
        hojas = []
        def recolectar_hojas(n):
            if n.es_hoja:
                hojas.append(n)
            else:
                if n.izquierda:
                    recolectar_hojas(n.izquierda)
                if n.centro:
                    recolectar_hojas(n.centro)
                if n.derecha:
                    recolectar_hojas(n.derecha)
        
        recolectar_hojas(arbol)
        codigos_temp = {}
        generar_codigos_ternarios(arbol, "", codigos_temp)
        buscador.registrar_intento(arbol, hojas, codigos_temp)
        return arbol
    
    mejor_arbol_local = None
    mejor_puntaje_local = float('inf')
    
    # Generar combinaciones: fusiones de 2 o 3 nodos
    combinaciones = []
    n = len(nodos)
    
    # Fusiones de 2 nodos
    for i in range(n):
        for j in range(i + 1, n):
            suma_prob = nodos[i].probabilidad + nodos[j].probabilidad
            diff_prob = abs(nodos[i].probabilidad - nodos[j].probabilidad)
            combinaciones.append(('2', [i, j], suma_prob, diff_prob))
    
    # Fusiones de 3 nodos (ternarias puras)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                suma_prob = nodos[i].probabilidad + nodos[j].probabilidad + nodos[k].probabilidad
                probs = [nodos[i].probabilidad, nodos[j].probabilidad, nodos[k].probabilidad]
                probs.sort()
                diff_total = (probs[1] - probs[0]) + (probs[2] - probs[1])
                combinaciones.append(('3', [i, j, k], suma_prob, diff_total))
    
    # Ordenar: priorizar menor diferencia (mas balanceado)
    combinaciones.sort(key=lambda x: (x[3], -x[2]))
    
    # Limitar numero de combinaciones
    max_combinaciones = 25
    if len(combinaciones) > max_combinaciones:
        combinaciones = combinaciones[:max_combinaciones]
    
    for tipo, indices, _, _ in combinaciones:
        if buscador.deberia_detener():
            break
        
        # Crear nueva lista de nodos
        nuevos_nodos = []
        for k in range(len(nodos)):
            if k not in indices:
                nuevos_nodos.append(deepcopy(nodos[k]))
        
        # Crear nodo fusionado segun tipo
        nodos_a_fusionar = [deepcopy(nodos[idx]) for idx in indices]
        
        if tipo == '2':
            # Fusion binaria (crea nodo con dos hijos)
            nodo_izq = nodos_a_fusionar[0]
            nodo_der = nodos_a_fusionar[1]
            
            simbolo_fusion = f"({nodo_izq.simbolo}+{nodo_der.simbolo})"
            prob_fusion = nodo_izq.probabilidad + nodo_der.probabilidad
            
            nodo_padre = NodoArbolTernario(
                simbolo=simbolo_fusion,
                probabilidad=prob_fusion,
                izquierda=nodo_izq,
                derecha=nodo_der,
                es_hoja=False
            )
        
        else:  # tipo '3'
            # Fusion ternaria (crea nodo con tres hijos)
            # Ordenar por probabilidad para asignar posiciones
            nodos_a_fusionar.sort(key=lambda x: x.probabilidad, reverse=True)
            
            nodo_izq = nodos_a_fusionar[0]
            nodo_centro = nodos_a_fusionar[1]
            nodo_der = nodos_a_fusionar[2]
            
            simbolo_fusion = f"({nodo_izq.simbolo}+{nodo_centro.simbolo}+{nodo_der.simbolo})"
            prob_fusion = nodo_izq.probabilidad + nodo_centro.probabilidad + nodo_der.probabilidad
            
            nodo_padre = NodoArbolTernario(
                simbolo=simbolo_fusion,
                probabilidad=prob_fusion,
                izquierda=nodo_izq,
                centro=nodo_centro,
                derecha=nodo_der,
                es_hoja=False
            )
        
        nuevos_nodos.append(nodo_padre)
        
        # Recursion
        arbol_resultante = construir_arbol_ternario(
            nuevos_nodos, buscador, profundidad_actual + 1, max_profundidad
        )
        
        if arbol_resultante is not None:
            # Evaluar este arbol
            hojas = []
            def recolectar_hojas(n):
                if n.es_hoja:
                    hojas.append(n)
                else:
                    if n.izquierda:
                        recolectar_hojas(n.izquierda)
                    if n.centro:
                        recolectar_hojas(n.centro)
                    if n.derecha:
                        recolectar_hojas(n.derecha)
            
            recolectar_hojas(arbol_resultante)
            codigos_temp = {}
            generar_codigos_ternarios(arbol_resultante, "", codigos_temp)
            puntaje, _, _ = buscador.calcular_puntaje(arbol_resultante, hojas, codigos_temp)
            
            if puntaje < mejor_puntaje_local:
                mejor_puntaje_local = puntaje
                mejor_arbol_local = arbol_resultante
    
    return mejor_arbol_local

def construir_huffman_estandar_ternario(nodos):
    """
    Construye arbol Huffman Ternario estandar (greedy)
    Fusiona los 3 nodos de menor probabilidad cuando es posible
    """
    nodos_temp = deepcopy(nodos)
    contador = 1
    
    while len(nodos_temp) > 1:
        nodos_temp.sort(key=lambda n: n.probabilidad)
        
        if len(nodos_temp) >= 3:
            # Fusion ternaria: tomar los 3 menores
            izquierdo = nodos_temp.pop(0)
            centro = nodos_temp.pop(0)
            derecho = nodos_temp.pop(0)
            
            simbolo_padre = f"t{contador}"
            prob_padre = izquierdo.probabilidad + centro.probabilidad + derecho.probabilidad
            
            nodo_padre = NodoArbolTernario(
                simbolo=simbolo_padre,
                probabilidad=prob_padre,
                izquierda=izquierdo,
                centro=centro,
                derecha=derecho,
                es_hoja=False
            )
        else:
            # Fusion binaria: tomar los 2 menores (para el ultimo paso)
            izquierdo = nodos_temp.pop(0)
            derecho = nodos_temp.pop(0)
            
            simbolo_padre = f"t{contador}"
            prob_padre = izquierdo.probabilidad + derecho.probabilidad
            
            nodo_padre = NodoArbolTernario(
                simbolo=simbolo_padre,
                probabilidad=prob_padre,
                izquierda=izquierdo,
                derecha=derecho,
                es_hoja=False
            )
        
        nodos_temp.append(nodo_padre)
        contador += 1
    
    return nodos_temp[0]

# --- Funcion para mostrar tabla de referencia ---
def mostrar_tabla_referencia():
    print("\n" + "-"*70)
    print("TABLA DE REFERENCIA - HUFFMAN TERNARIO")
    print("-"*70)
    print("  VALOR  |  VELOCIDAD  |  CALIDAD  |  DIGITOS  |  RECOMENDADO PARA")
    print("---------|-------------|-----------|-----------|------------------")
    print("  1-3    |  MUY RAPIDO |  BASICA   |  CORTOS   | Pruebas rapidas")
    print("  4-6    |  RAPIDO     |  MEDIA    |  CORTOS   | Uso general")
    print("  7-10   |  MODERADO   |  BUENA    |  CORTOS   | Analisis serios")
    print("  11-15  |  LENTO      |  MUY BUENA|  CORTOS   | Maxima calidad")
    print("  16+    |  MUY LENTO  |  EXCELENTE|  CORTOS   | Investigacion")
    print("  INF    |  EXTREMO    |  OPTIMA   |  CORTOS   | Validacion completa")
    print("-"*70)
    print("\nCARACTERISTICAS DEL HUFFMAN TERNARIO:")
    print("   - Utiliza 3 digitos: '0', '1', y '*'")
    print("   - Cada digito ternario equivale a 1.585 bits")
    print("   - Los codigos resultantes son mas CORTOS en digitos")
    print("   - Ideal para canales con 3 estados (ej: +V, 0, -V)")
    print("="*70)

# --- Funcion principal ---
def solicitar_mensaje():
    print("="*60)
    print("        HUFFMAN TERNARIO CONFIGURABLE")
    print("="*60)
    print("\nINSTRUCCIONES:")
    print("   - Escribe o pega el texto que deseas procesar")
    print("   - Presiona ENTER cuando termines")
    print("   - Los espacios seran ignorados automaticamente")
    print("   - NO se diferencia entre mayusculas y minusculas")
    print("\nCARACTERISTICAS DEL ALGORITMO:")
    print("   - ALFABETO DE SALIDA: {0, 1, *}")
    print("   - Construye arboles de Huffman con hasta 3 hijos por nodo")
    print("   - Los codigos resultantes usan digitos ternarios")
    print("   - Se detiene despues de X arboles consecutivos SIN MEJORA")
    print("-"*60)
    
    texto_ingresado = input("\nTu texto: ").strip()
    
    if not texto_ingresado:
        print("\nERROR: El texto no puede estar vacio.")
        sys.exit(1)
    
    return texto_ingresado

def preguntar_umbral():
    """Pregunta al usuario cuantos arboles sin mejora permitir"""
    print("\n" + "="*60)
    print("CONFIGURACION DE LA BUSQUEDA TERNARIA")
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
        nodos_iniciales.append(NodoArbolTernario(simbolo, prob, es_hoja=True))
        print(f"   '{simbolo}': {cantidad} veces (prob={prob:.4f})")
    
    num_simbolos = len(nodos_iniciales)
    print(f"\nTotal simbolos unicos: {num_simbolos}")
    
    # Preguntar umbral
    umbral = preguntar_umbral()
    
    if umbral == float('inf'):
        print("\n[MODO EXPLORACION COMPLETA] Se exploraran TODOS los arboles posibles")
        print("Esto puede tomar MUCHO tiempo para textos con mas de 6-7 simbolos...")
    else:
        print(f"\n[MODO CONFIGURADO] Se detendra despues de {umbral} arboles consecutivos SIN mejora")
    
    # Configurar profundidad maxima
    profundidad_max = min(12, num_simbolos * 2)
    
    print(f"Profundidad maxima: {profundidad_max}")
    print(f"\nIniciando busqueda de arbol ternario...")
    print(f"Alfabeto de salida: 0, 1, *")
    print(f"1 digito ternario = {math.log2(3):.5f} bits\n")
    
    # Crear buscador
    buscador = BusquedaTernaria(max_sin_mejora=umbral)
    
    # Ejecutar busqueda
    arbol_final = construir_arbol_ternario(
        nodos_iniciales, 
        buscador, 
        max_profundidad=profundidad_max
    )
    
    # Fallback
    if arbol_final is None:
        print("\n[FALLBACK] Usando arbol Huffman ternario estandar...")
        arbol_final = construir_huffman_estandar_ternario(nodos_iniciales)
    
    # Generar codigos
    codigos_huffman = {}
    generar_codigos_ternarios(arbol_final, "", codigos_huffman)
    
    # Recolectar nodos hoja
    nodos_hoja = []
    def recolectar_hojas(nodo):
        if nodo.es_hoja:
            nodos_hoja.append(nodo)
        else:
            if nodo.izquierda:
                recolectar_hojas(nodo.izquierda)
            if nodo.centro:
                recolectar_hojas(nodo.centro)
            if nodo.derecha:
                recolectar_hojas(nodo.derecha)
    
    recolectar_hojas(arbol_final)
    
    # Calcular metricas
    HE = calcular_he(nodos_hoja)
    HT = calcular_ht_total_ternario(arbol_final)
    HIT = HE + HT
    lms_bits, lms_digitos = calcular_lms_ternario(nodos_hoja, codigos_huffman)
    LME = 8.0
    RC = LME / lms_bits if lms_bits > 0 else 0
    
    # Calcular longitud maxima en digitos y bits
    max_digitos = max(len(codigo) for codigo in codigos_huffman.values()) if codigos_huffman else 0
    max_bits = max_digitos * math.log2(3)
    
    # Guardar resultados
    archivo_resultados = "resultados_huffman_ternario.txt"
    with open(archivo_resultados, "w", encoding="utf-8") as archivo:
        archivo.write("="*60 + "\n")
        archivo.write("     RESULTADOS DE HUFFMAN TERNARIO\n")
        archivo.write("="*60 + "\n\n")
        
        archivo.write(f"TEXTO ORIGINAL:\n   {texto_usuario}\n\n")
        
        archivo.write("CONFIGURACION:\n")
        if umbral == float('inf'):
            archivo.write("   Modo: EXPLORACION COMPLETA\n")
        else:
            archivo.write(f"   Umbral sin mejora: {umbral} arboles\n")
        archivo.write(f"   Arboles evaluados: {buscador.arboles_evaluados}\n")
        archivo.write(f"   Alfabeto ternario: {{0, 1, *}}\n")
        archivo.write(f"   Bits por digito ternario: {math.log2(3):.5f}\n\n")
        
        archivo.write("FRECUENCIAS:\n")
        for simbolo, cant in frecuencias:
            archivo.write(f"   '{simbolo}': {cant} veces ({cant/total_caracteres:.4f})\n")
        
        archivo.write("\nCODIGOS TERNARIOS:\n")
        for simbolo, codigo in codigos_huffman.items():
            bits_equiv = len(codigo) * math.log2(3)
            archivo.write(f"   '{simbolo}' -> {codigo}  (digitos: {len(codigo)} | bits: {bits_equiv:.2f})\n")
        
        archivo.write("\n" + "-"*60 + "\n")
        archivo.write("METRICAS TERNARIAS:\n")
        archivo.write(f"   Longitud media en digitos: {lms_digitos:.4f} digitos\n")
        archivo.write(f"   Longitud media en bits:   {lms_bits:.4f} bits\n")
        archivo.write(f"   Longitud maxima en digitos: {max_digitos} digitos\n")
        archivo.write(f"   Longitud maxima en bits:   {max_bits:.2f} bits\n\n")
        
        archivo.write("ENTROPIAS:\n")
        archivo.write(f"   HE (Fuente):  {HE:.6f} bits\n")
        archivo.write(f"   HT (Arbol):   {HT:.6f} bits\n")
        archivo.write(f"   HIT (Total):  {HIT:.6f} bits\n\n")
        
        archivo.write("METRICAS DE COMPRESION:\n")
        archivo.write(f"   LMS (Longitud Media Simbolo): {lms_bits:.4f} bits\n")
        archivo.write(f"   LME (Longitud Media Ensamblaje): {LME:.4f} bits\n")
        archivo.write(f"   RC (Relacion de Compresion): {RC:.4f}\n")
        
        archivo.write("\n" + "="*60 + "\n")
        archivo.write("ESTRUCTURA DEL ARBOL TERNARIO:\n")
        archivo.write("(0 = izquierda, 1 = centro, * = derecha)\n\n")
        
        def imprimir_arbol(nodo, nivel=0):
            indent = "  " * nivel
            if nodo.es_hoja:
                archivo.write(f"{indent}hoja: '{nodo.simbolo}' (p={nodo.probabilidad:.4f})\n")
            else:
                simbolo_limpio = nodo.simbolo[:60] if len(nodo.simbolo) > 60 else nodo.simbolo
                archivo.write(f"{indent}nodo: {simbolo_limpio} (p={nodo.probabilidad:.4f})\n")
                if nodo.izquierda:
                    archivo.write(f"{indent}  [0] ")
                    imprimir_arbol(nodo.izquierda, nivel+1)
                if nodo.centro:
                    archivo.write(f"{indent}  [1] ")
                    imprimir_arbol(nodo.centro, nivel+1)
                if nodo.derecha:
                    archivo.write(f"{indent}  [*] ")
                    imprimir_arbol(nodo.derecha, nivel+1)
        
        imprimir_arbol(arbol_final)
    
    print("\n" + "="*60)
    print("PROCESO COMPLETADO - HUFFMAN TERNARIO")
    print("="*60)
    print(f"ARBOLES EVALUADOS: {buscador.arboles_evaluados}")
    print(f"MEJOR HT: {buscador.mejor_ht:.6f}")
    print(f"MEJOR LMS: {buscador.mejor_lms:.4f} bits")
    print("-"*60)
    print(f"HE (Fuente):     {HE:.6f} bits")
    print(f"HT (Arbol):      {HT:.6f} bits")
    print(f"LMS (bits):      {lms_bits:.4f} bits")
    print(f"LMS (digitos):   {lms_digitos:.4f} digitos ternarios")
    print(f"RC:              {RC:.4f}")
    print("-"*60)
    print(f"EJEMPLO DE CODIGO: '{list(codigos_huffman.keys())[0] if codigos_huffman else ''}' -> {list(codigos_huffman.values())[0] if codigos_huffman else ''}")
    print("\n" + "="*60)
    print(f"Resultados guardados en: {archivo_resultados}")

if __name__ == "__main__":
    main()