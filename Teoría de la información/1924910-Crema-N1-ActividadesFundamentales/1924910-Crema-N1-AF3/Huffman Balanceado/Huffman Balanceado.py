import math
import sys
from copy import deepcopy

# Configuracion del limite de recursion
sys.setrecursionlimit(2000)

# --- Clase Nodo del Arbol ---
class NodoArbol:
    def __init__(self, simbolo, probabilidad, izquierda=None, derecha=None, es_hoja=True, profundidad=0):
        self.simbolo = simbolo
        self.probabilidad = probabilidad
        self.izquierda = izquierda
        self.derecha = derecha
        self.es_hoja = es_hoja
        self.profundidad = profundidad
        self.codigo = ""

# --- Funciones de entropia ---
def calcular_he(nodos_hoja):
    HE = 0
    for nodo in nodos_hoja:
        prob = nodo.probabilidad
        if prob > 0:
            HE += -prob * math.log2(prob)
    return HE

def calcular_ht_nodo(diferencia):
    if diferencia > 0 and not math.isclose(diferencia, 0):
        return -diferencia * math.log2(diferencia)
    return 0

def calcular_ht_total(nodo, ht_acumulado=0):
    if nodo.es_hoja:
        return ht_acumulado
    
    ht_total = ht_acumulado
    
    if nodo.izquierda and nodo.derecha:
        diferencia = abs(nodo.izquierda.probabilidad - nodo.derecha.probabilidad)
        ht_total += calcular_ht_nodo(diferencia)
    
    if nodo.izquierda:
        ht_total = calcular_ht_total(nodo.izquierda, ht_total)
    if nodo.derecha:
        ht_total = calcular_ht_total(nodo.derecha, ht_total)
    
    return ht_total

# --- Funcion para calcular la profundidad maxima del arbol ---
def calcular_profundidad_maxima(nodo, profundidad_actual=0):
    if nodo.es_hoja:
        return profundidad_actual
    else:
        prof_izq = calcular_profundidad_maxima(nodo.izquierda, profundidad_actual + 1)
        prof_der = calcular_profundidad_maxima(nodo.derecha, profundidad_actual + 1)
        return max(prof_izq, prof_der)

# --- Funcion para calcular el desbalance del arbol ---
def calcular_desbalance(nodo):
    """
    Calcula una metrica de desbalance del arbol.
    Arbol perfectamente balanceado = 0
    Arbol muy desbalanceado = valor alto
    """
    if nodo.es_hoja:
        return 0
    
    desbalance = 0
    
    # Diferencia de profundidades entre subarboles
    prof_izq = calcular_profundidad_maxima(nodo.izquierda) if not nodo.izquierda.es_hoja else 1
    prof_der = calcular_profundidad_maxima(nodo.derecha) if not nodo.derecha.es_hoja else 1
    
    desbalance += abs(prof_izq - prof_der)
    
    # Recursivamente calcular desbalance en subarboles
    if nodo.izquierda:
        desbalance += calcular_desbalance(nodo.izquierda)
    if nodo.derecha:
        desbalance += calcular_desbalance(nodo.derecha)
    
    return desbalance

# --- Funcion para generar codigos ---
def generar_codigos(nodo, codigo_actual, diccionario):
    if nodo is None:
        return
    
    nodo.codigo = codigo_actual
    
    if nodo.es_hoja:
        diccionario[nodo.simbolo] = codigo_actual if codigo_actual else '0'
    
    generar_codigos(nodo.izquierda, codigo_actual + '1', diccionario)
    generar_codigos(nodo.derecha, codigo_actual + '0', diccionario)

# --- Funcion para calcular LMS ---
def calcular_lms(nodos_hoja):
    lms = 0
    for nodo in nodos_hoja:
        lms += nodo.probabilidad * len(nodo.codigo)
    return lms

# --- Funcion para calcular la longitud maxima de codigo ---
def calcular_longitud_maxima(codigos):
    return max(len(codigo) for codigo in codigos.values()) if codigos else 0

# --- CONSTRUCCION DE HUFFMAN BALANCEADO ---
class BusquedaBalanceada:
    def __init__(self, max_sin_mejora=3, penalizacion_desbalance=0.5):
        self.mejor_puntaje = float('inf')
        self.mejor_arbol = None
        self.contador_sin_mejora = 0
        self.max_sin_mejora = max_sin_mejora
        self.arboles_evaluados = 0
        self.penalizacion_desbalance = penalizacion_desbalance  # Que tanto penaliza el desbalance
    
    def calcular_puntaje(self, arbol, nodos_hoja):
        """
        Calcula un puntaje combinado que considera:
        - LMS (Longitud Media de Simbolo) - menor es mejor
        - Desbalance del arbol - menor es mejor
        - HT (Entropia del Arbol) - opcional
        """
        # Calcular LMS
        codigos_temp = {}
        generar_codigos(arbol, "", codigos_temp)
        
        lms = 0
        for nodo in nodos_hoja:
            if nodo.simbolo in codigos_temp:
                lms += nodo.probabilidad * len(codigos_temp[nodo.simbolo])
        
        # Calcular desbalance
        desbalance = calcular_desbalance(arbol)
        
        # Puntaje combinado (menor es mejor)
        # LMS normalizado + penalizacion por desbalance
        puntaje = lms + (self.penalizacion_desbalance * desbalance / 100)
        
        return puntaje, lms, desbalance
    
    def registrar_intento(self, arbol, nodos_hoja):
        """Registra un intento y determina si se debe continuar"""
        self.arboles_evaluados += 1
        
        puntaje, lms, desbalance = self.calcular_puntaje(arbol, nodos_hoja)
        
        # Si encontramos un arbol con mejor puntaje
        if puntaje < self.mejor_puntaje:
            self.mejor_puntaje = puntaje
            self.mejor_arbol = deepcopy(arbol)
            self.contador_sin_mejora = 0
            print(f"   [NUEVO MEJOR - Puntaje: {puntaje:.6f} | LMS: {lms:.4f} | Desbalance: {desbalance} | arbol #{self.arboles_evaluados}]")
            return False  # No detener
        else:
            self.contador_sin_mejora += 1
            print(f"   [sin mejora: puntaje={puntaje:.6f} | contador: {self.contador_sin_mejora}/{self.max_sin_mejora}]")
            
            if self.contador_sin_mejora >= self.max_sin_mejora:
                print(f"\n   >>> DETENCION: {self.max_sin_mejora} arboles consecutivos sin mejora")
                return True  # Detener
        
        return False
    
    def deberia_detener(self):
        return self.contador_sin_mejora >= self.max_sin_mejora

def construir_arbol_balanceado(nodos, buscador, profundidad_actual=0, max_profundidad=15):
    """
    Construye arbol Huffman Balanceado explorando combinaciones
    priorizando aquellas que producen arboles mas balanceados
    """
    # Verificar detencion
    if buscador.deberia_detener():
        return None
    
    # Si solo queda un nodo, evaluar el arbol completo
    if len(nodos) == 1:
        # Recolectar hojas para evaluar
        hojas = []
        def recolectar_hojas(n):
            if n.es_hoja:
                hojas.append(n)
            else:
                if n.izquierda:
                    recolectar_hojas(n.izquierda)
                if n.derecha:
                    recolectar_hojas(n.derecha)
        
        recolectar_hojas(nodos[0])
        detener = buscador.registrar_intento(nodos[0], hojas)
        return nodos[0]
    
    # Limitar profundidad
    if profundidad_actual >= max_profundidad:
        arbol = construir_huffman_estandar_balanceado(nodos)
        hojas = []
        def recolectar_hojas(n):
            if n.es_hoja:
                hojas.append(n)
            else:
                if n.izquierda:
                    recolectar_hojas(n.izquierda)
                if n.derecha:
                    recolectar_hojas(n.derecha)
        recolectar_hojas(arbol)
        buscador.registrar_intento(arbol, hojas)
        return arbol
    
    mejor_arbol_local = None
    mejor_puntaje_local = float('inf')
    
    # Generar combinaciones de pares
    combinaciones = []
    for i in range(len(nodos)):
        for j in range(i + 1, len(nodos)):
            # Calcular que tan balanceada seria esta fusion
            diff_prob = abs(nodos[i].probabilidad - nodos[j].probabilidad)
            suma_prob = nodos[i].probabilidad + nodos[j].probabilidad
            
            # Priorizar fusiones con probabilidades similares (mas balanceadas)
            balance_score = diff_prob  # menor es mejor
            combinaciones.append((i, j, balance_score, suma_prob))
    
    # Ordenar: primero las mas balanceadas (menor diferencia), luego mayor suma
    combinaciones.sort(key=lambda x: (x[2], -x[3]))
    
    # Limitar numero de combinaciones
    max_combinaciones = 20
    if len(combinaciones) > max_combinaciones:
        combinaciones = combinaciones[:max_combinaciones]
    
    for i, j, _, _ in combinaciones:
        if buscador.deberia_detener():
            break
        
        # Crear nueva lista de nodos
        nuevos_nodos = []
        for k in range(len(nodos)):
            if k != i and k != j:
                nuevos_nodos.append(deepcopy(nodos[k]))
        
        # Crear nodo fusionado
        nodo_izq = deepcopy(nodos[i])
        nodo_der = deepcopy(nodos[j])
        
        # Ajustar profundidades
        nodo_izq.profundidad = profundidad_actual + 1
        nodo_der.profundidad = profundidad_actual + 1
        
        simbolo_fusion = f"({nodo_izq.simbolo}+{nodo_der.simbolo})"
        prob_fusion = nodo_izq.probabilidad + nodo_der.probabilidad
        
        nodo_padre = NodoArbol(
            simbolo=simbolo_fusion,
            probabilidad=prob_fusion,
            izquierda=nodo_izq,
            derecha=nodo_der,
            es_hoja=False,
            profundidad=profundidad_actual
        )
        
        nuevos_nodos.append(nodo_padre)
        
        # Recursion
        arbol_resultante = construir_arbol_balanceado(
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
                    if n.derecha:
                        recolectar_hojas(n.derecha)
            
            recolectar_hojas(arbol_resultante)
            puntaje, lms, desbalance = buscador.calcular_puntaje(arbol_resultante, hojas)
            
            if puntaje < mejor_puntaje_local:
                mejor_puntaje_local = puntaje
                mejor_arbol_local = arbol_resultante
    
    return mejor_arbol_local

def construir_huffman_estandar_balanceado(nodos):
    """
    Construye arbol Huffman estandar (greedy) pero con criterio de balance
    """
    nodos_temp = deepcopy(nodos)
    contador = 1
    
    while len(nodos_temp) > 1:
        # Ordenar por probabilidad (menor primero) para fusionar los mas pequenos
        # Esto tiende a crear arboles mas balanceados que el Huffman tradicional
        nodos_temp.sort(key=lambda n: n.probabilidad)
        
        izquierdo = nodos_temp.pop(0)
        derecho = nodos_temp.pop(0)
        
        simbolo_padre = f"b{contador}"
        prob_padre = izquierdo.probabilidad + derecho.probabilidad
        
        nodo_padre = NodoArbol(simbolo_padre, prob_padre, izquierdo, derecho, es_hoja=False)
        nodos_temp.append(nodo_padre)
        contador += 1
    
    return nodos_temp[0]

# --- Funcion para mostrar tabla de referencia ---
def mostrar_tabla_referencia():
    print("\n" + "-"*70)
    print("TABLA DE REFERENCIA - HUFFMAN BALANCEADO")
    print("-"*70)
    print("  VALOR  |  VELOCIDAD  |  BALANCE  |  COMPRESION  |  RECOMENDADO PARA")
    print("---------|-------------|-----------|--------------|------------------")
    print("  1-3    |  MUY RAPIDO |  MEDIO    |  BUENA       | Textos largos, velocidad prioritaria")
    print("  4-6    |  RAPIDO     |  BUENO    |  BUENA       | Uso general, buen equilibrio")
    print("  7-10   |  MODERADO   |  MUY BUENO|  MEDIA       | Cuando el balance es importante")
    print("  11-15  |  LENTO      |  EXCELENTE|  MEDIA-BAJA  | Textos pequenos, maximo balance")
    print("  16+    |  MUY LENTO  |  OPTIMO   |  BAJA        | Investigacion academica")
    print("  INF    |  EXTREMO    |  OPTIMO   |  BAJA        | Validacion completa")
    print("-"*70)
    print("\nNOTA: Huffman Balanceado prioriza arboles con profundidades similares")
    print("      a costa de una ligera perdida en la tasa de compresion.")
    print("      Ideal para sistemas con buffers limitados o latencia critica.")
    print("="*70)

# --- Funcion principal ---
def solicitar_mensaje():
    print("="*60)
    print("        HUFFMAN BALANCEADO CONFIGURABLE")
    print("="*60)
    print("\nINSTRUCCIONES:")
    print("   - Escribe o pega el texto que deseas procesar")
    print("   - Presiona ENTER cuando termines")
    print("   - Los espacios seran ignorados automaticamente")
    print("   - NO se diferencia entre mayusculas y minusculas")
    print("\nCARACTERISTICAS DEL ALGORITMO:")
    print("   - Construye arboles de Huffman priorizando el BALANCE")
    print("   - Minimiza la diferencia de profundidades entre ramas")
    print("   - Se detiene despues de X arboles consecutivos SIN MEJORA")
    print("   - Ideal para reducir la longitud maxima de codigo")
    print("-"*60)
    
    texto_ingresado = input("\nTu texto: ").strip()
    
    if not texto_ingresado:
        print("\nERROR: El texto no puede estar vacio.")
        sys.exit(1)
    
    return texto_ingresado

def preguntar_umbral():
    """Pregunta al usuario cuantos arboles sin mejora permitir"""
    print("\n" + "="*60)
    print("CONFIGURACION DE LA BUSQUEDA BALANCEADA")
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

def preguntar_penalizacion():
    """Pregunta la penalizacion por desbalance"""
    print("\n" + "-"*60)
    print("CONFIGURACION DE PENALIZACION POR DESBALANCE")
    print("-"*60)
    print("La penalizacion controla que tan importante es el balance:")
    print("   0.0 - Solo importa la compresion (LMS) - similar a Huffman estandar")
    print("   0.3 - Balance moderado (recomendado)")
    print("   0.5 - Balance fuerte")
    print("   1.0 - Balance extremo (prioriza balance sobre compresion)")
    print("-"*60)
    
    while True:
        try:
            respuesta = input("\nPenalizacion por desbalance (0.0 a 1.0) [default=0.5]: ").strip()
            
            if respuesta == "":
                return 0.5
            
            valor = float(respuesta)
            
            if valor < 0:
                print("   Usando valor minimo 0.0")
                return 0.0
            if valor > 1:
                print("   Usando valor maximo 1.0")
                return 1.0
            
            return valor
            
        except ValueError:
            print("   Por favor, ingrese un numero decimal (ej: 0.5)")

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
    
    # Preguntar configuracion
    umbral = preguntar_umbral()
    penalizacion = preguntar_penalizacion()
    
    if umbral == float('inf'):
        print("\n[MODO EXPLORACION COMPLETA] Se exploraran TODOS los arboles posibles")
        print("Esto puede tomar MUCHO tiempo para textos con mas de 8-10 simbolos...")
    else:
        print(f"\n[MODO CONFIGURADO] Se detendra despues de {umbral} arboles consecutivos SIN mejora")
    
    print(f"[PENALIZACION] Balance vs Compresion: {penalizacion:.1f}")
    
    # Configurar profundidad maxima
    profundidad_max = min(15, num_simbolos * 2)
    
    print(f"Profundidad maxima: {profundidad_max}")
    print(f"\nIniciando busqueda de arbol balanceado...\n")
    
    # Crear buscador con el umbral elegido
    buscador = BusquedaBalanceada(max_sin_mejora=umbral, penalizacion_desbalance=penalizacion)
    
    # Ejecutar busqueda principal
    arbol_final = construir_arbol_balanceado(
        nodos_iniciales, 
        buscador, 
        max_profundidad=profundidad_max
    )
    
    # Fallback
    if arbol_final is None:
        print("\n[FALLBACK] Usando arbol Huffman estandar balanceado...")
        arbol_final = construir_huffman_estandar_balanceado(nodos_iniciales)
    
    # Generar codigos
    codigos_huffman = {}
    generar_codigos(arbol_final, "", codigos_huffman)
    
    # Recolectar nodos hoja
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
    
    # Calcular metricas
    HE = calcular_he(nodos_hoja)
    HT = calcular_ht_total(arbol_final)
    HIT = HE + HT
    LMS = calcular_lms(nodos_hoja)
    LME = 8.0
    RC = LME / LMS if LMS > 0 else 0
    profundidad_max_codigo = calcular_longitud_maxima(codigos_huffman)
    desbalance_total = calcular_desbalance(arbol_final)
    
    # Guardar resultados
    archivo_resultados = "resultados_huffman_balanceado.txt"
    with open(archivo_resultados, "w", encoding="utf-8") as archivo:
        archivo.write("="*60 + "\n")
        archivo.write("     RESULTADOS DE HUFFMAN BALANCEADO\n")
        archivo.write("="*60 + "\n\n")
        
        archivo.write(f"TEXTO ORIGINAL:\n   {texto_usuario}\n\n")
        
        archivo.write("CONFIGURACION:\n")
        if umbral == float('inf'):
            archivo.write("   Modo: EXPLORACION COMPLETA\n")
        else:
            archivo.write(f"   Umbral sin mejora: {umbral} arboles\n")
        archivo.write(f"   Penalizacion por desbalance: {penalizacion}\n")
        archivo.write(f"   Arboles evaluados: {buscador.arboles_evaluados}\n\n")
        
        archivo.write("FRECUENCIAS:\n")
        for simbolo, cant in frecuencias:
            archivo.write(f"   '{simbolo}': {cant} veces ({cant/total_caracteres:.4f})\n")
        
        archivo.write("\nCODIGOS HUFFMAN (arbol balanceado):\n")
        for simbolo, codigo in codigos_huffman.items():
            archivo.write(f"   '{simbolo}' -> {codigo} (longitud: {len(codigo)})\n")
        
        archivo.write("\n" + "-"*60 + "\n")
        archivo.write("METRICAS DE BALANCE:\n")
        archivo.write(f"   Profundidad maxima del codigo: {profundidad_max_codigo} bits\n")
        archivo.write(f"   Desbalance total del arbol: {desbalance_total}\n")
        archivo.write(f"   (menor desbalance = arbol mas equilibrado)\n\n")
        
        archivo.write("ENTROPIAS:\n")
        archivo.write(f"   HE (Fuente):  {HE:.6f} bits\n")
        archivo.write(f"   HT (Arbol):   {HT:.6f} bits\n")
        archivo.write(f"   HIT (Total):  {HIT:.6f} bits\n\n")
        
        archivo.write("METRICAS DE COMPRESION:\n")
        archivo.write(f"   LMS (Longitud Media Simbolo): {LMS:.4f} bits\n")
        archivo.write(f"   LME (Longitud Media Ensamblaje): {LME:.4f} bits\n")
        archivo.write(f"   RC (Relacion de Compresion): {RC:.4f}\n")
        
        archivo.write("\n" + "="*60 + "\n")
        archivo.write("ESTRUCTURA DEL ARBOL SELECCIONADO:\n")
        
        def imprimir_arbol(nodo, nivel=0):
            indent = "  " * nivel
            if nodo.es_hoja:
                archivo.write(f"{indent}hoja: '{nodo.simbolo}' (p={nodo.probabilidad:.4f}, prof={nodo.profundidad})\n")
            else:
                simbolo_limpio = nodo.simbolo[:60] if len(nodo.simbolo) > 60 else nodo.simbolo
                archivo.write(f"{indent}nodo: {simbolo_limpio} (p={nodo.probabilidad:.4f})\n")
                if nodo.izquierda:
                    imprimir_arbol(nodo.izquierda, nivel+1)
                if nodo.derecha:
                    imprimir_arbol(nodo.derecha, nivel+1)
        
        imprimir_arbol(arbol_final)
    
    print("\n" + "="*60)
    print("PROCESO COMPLETADO - HUFFMAN BALANCEADO")
    print("="*60)
    print(f"ARBOLES EVALUADOS: {buscador.arboles_evaluados}")
    print(f"PROFUNDIDAD MAXIMA: {profundidad_max_codigo} bits")
    print(f"DESBALANCE TOTAL: {desbalance_total}")
    print("-"*60)
    print(f"HE (Fuente):  {HE:.6f} bits")
    print(f"HT (Arbol):   {HT:.6f} bits")
    print(f"LMS:          {LMS:.4f} bits")
    print(f"RC:           {RC:.4f}")
    print("\n" + "="*60)
    print(f"Resultados guardados en: {archivo_resultados}")

if __name__ == "__main__":
    main()