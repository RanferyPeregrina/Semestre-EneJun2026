import os
import numpy as np
from tkinter import Tk, filedialog

class GenomicData:

    def __init__(self):
        self.sequence = ""
        self.header = ""
        self.length = 0

    def cargar_fna(self, filepath):
        """
        Lee archivos .fna o .fasta de forma eficiente.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No se encontró el archivo: {filepath}")

        fragments = []
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                # Manejo del encabezado (Metadata)
                if line.startswith(">"):
                    self.header = line[1:]
                    continue
                
                # Limpieza: Solo letras, todo a mayúsculas
                # El artículo sugiere normalizar para evitar errores de comparación
                fragments.append(line.upper())

        # Unimos todos los fragmentos en una sola cadena en memoria
        # Añadimos el centinela '$' que es muy importante para el SuffixArray
        self.sequence = "".join(fragments) + "$"
        self.length = len(self.sequence)
        
        print(f"--- Fase 1 Completada ---")
        print(f"ID Secuencia: {self.header[:50]}...")
        print(f"Longitud total (n): {self.length} bases (incluyendo '$')")

    def info_memoria(self):
        import sys
        size_mb = sys.getsizeof(self.sequence) / (1024 * 1024)
        return f"Tamaño en RAM de la secuencia: {size_mb:.2f} MB"

def compare_with_lcp(text, idx_a, idx_b, shared_lcp):
    """
    Compara dos sufijos (idx_a y idx_b) sabiendo que ya comparten 
    'shared_lcp' caracteres.
    Retorna: (ganador, nuevo_lcp)
    """
    n = len(text)
    k = shared_lcp
    
    # Comparamos a partir del punto donde sabemos que son iguales
    while idx_a + k < n and idx_b + k < n:
        if text[idx_a + k] != text[idx_b + k]:
            if text[idx_a + k] < text[idx_b + k]:
                return "a", k  # s_a es menor, comparten k letras
            else:
                return "b", k  # s_b es menor, comparten k letras
        k += 1
    
    # Si llegamos al final de la cadena, el más corto es el menor
    if idx_a + k == n:
        return "a", k
    return "b", k


#  ========================================================================================================
#Esta clase es el motor de CAPS.
# Aquí hacemos la comparación que utiliza la información del LCP (Longest Common Prefix) para evitar comparaciones
# de caracteres innecesarias.
# En la sección 3.2 del artículo, los autores explican que el éxito de su algoritmo reside en cómo mezclan (merge)
# dos listas de sufijos ya ordenadas.
#  ========================================================================================================
class CAPS_Engine:

    def __init__(self, text):
        self.text = text
        self.n = len(text)

    def lcp_informed_merge(self, sa_a, lcp_a, sa_b, lcp_b):

        merged_sa = []
        merged_lcp = [0]
        
        i, j = 0, 0
        # l_a y l_b mantienen el LCP entre el último elemento añadido 
        # al merged_sa y el candidato actual de cada lista.
        l_a, l_b = 0, 0 
        
        while i < len(sa_a) and j < len(sa_b):
            s_a, s_b = sa_a[i], sa_b[j]
            
            # CASO 1: l_a > l_b
            if l_a > l_b:
                # s_b es el menor
                merged_sa.append(s_b)
                merged_lcp.append(l_b)
                # Actualizamos: el nuevo s_last es s_b. 
                # El LCP entre s_b y s_a ahora es l_b.
                l_b = lcp_b[j+1] if j+1 < len(lcp_b) else 0
                l_a = l_b # Propiedad transitiva del LCP
                j += 1
                
            # CASO 2: l_a < l_b
            elif l_a < l_b:
                merged_sa.append(s_a)
                merged_lcp.append(l_a)
                l_a = lcp_a[i+1] if i+1 < len(lcp_a) else 0
                l_b = l_a
                i += 1
                
            # CASO 3: l_a == l_b (Incertidumbre)
            else:
                res, match_len = compare_with_lcp(self.text, s_a, s_b, l_a)
                if res == "a":
                    merged_sa.append(s_a)
                    merged_lcp.append(l_a) # El LCP con el anterior ya estaba en l_a
                    l_a = lcp_a[i+1] if i+1 < len(lcp_a) else 0
                    l_b = match_len
                    i += 1
                else:
                    merged_sa.append(s_b)
                    merged_lcp.append(l_b)
                    l_b = lcp_b[j+1] if j+1 < len(lcp_b) else 0
                    l_a = match_len
                    j += 1

        # Agregar sobrantes...
        # (Aquí se requiere una lógica similar para vaciar las listas)
        print(merged_sa)
        return merged_sa, merged_lcp




class LocalSort:
    def __init__(self, text):
        self.text = text
        self.n = len(text)

    def compare_with_lcp(self, idx_a, idx_b, shared_lcp):
        """Motor de comparación (Fase 2 mejorada)"""
        k = shared_lcp
        while idx_a + k < self.n and idx_b + k < self.n:
            if self.text[idx_a + k] != self.text[idx_b + k]:
                if self.text[idx_a + k] < self.text[idx_b + k]:
                    return "a", k
                else:
                    return "b", k
            k += 1
        return ("a", k) if idx_a + k == self.n else ("b", k)

    def merge(self, sa_a, lcp_a, sa_b, lcp_b):
        """Fusión de dos listas usando los 3 casos del paper"""
        merged_sa = []
        merged_lcp = []
        
        i, j = 0, 0
        l_a, l_b = 0, 0 
        
        # El primer elemento de la fusión
        # Necesitamos decidir quién arranca el array
        res, match_len = self.compare_with_lcp(sa_a[0], sa_b[0], 0)
        if res == "a":
            merged_sa.append(sa_a[0])
            merged_lcp.append(0) # El primero siempre es 0
            l_a = lcp_a[1] if 1 < len(lcp_a) else 0
            l_b = match_len
            i += 1
        else:
            merged_sa.append(sa_b[0])
            merged_lcp.append(0)
            l_b = lcp_b[1] if 1 < len(lcp_b) else 0
            l_a = match_len
            j += 1

        while i < len(sa_a) and j < len(sa_b):
            s_a, s_b = sa_a[i], sa_b[j]
            
            if l_a > l_b: # Caso 1
                merged_sa.append(s_b); merged_lcp.append(l_b)
                l_b = lcp_b[j+1] if j+1 < len(lcp_b) else 0
                # l_a se mantiene igual (propiedad transitiva)
                j += 1
            elif l_a < l_b: # Caso 2
                merged_sa.append(s_a); merged_lcp.append(l_a)
                l_a = lcp_a[i+1] if i+1 < len(lcp_a) else 0
                i += 1
            else: # Caso 3: Empate de LCP, comparar letras
                res, match_len = self.compare_with_lcp(s_a, s_b, l_a)
                if res == "a":
                    merged_sa.append(s_a); merged_lcp.append(l_a)
                    l_a = lcp_a[i+1] if i+1 < len(lcp_a) else 0
                    l_b = match_len
                    i += 1
                else:
                    merged_sa.append(s_b); merged_lcp.append(l_b)
                    l_b = lcp_b[j+1] if j+1 < len(lcp_b) else 0
                    l_a = match_len
                    j += 1

        # Vaciar los elementos restantes (muy importante para la robustez)
        while i < len(sa_a):
            merged_sa.append(sa_a[i])
            merged_lcp.append(l_a)
            l_a = lcp_a[i+1] if i+1 < len(lcp_a) else 0
            i += 1
        while j < len(sa_b):
            merged_sa.append(sa_b[j])
            merged_lcp.append(l_b)
            l_b = lcp_b[j+1] if j+1 < len(lcp_b) else 0
            j += 1

        return merged_sa, merged_lcp

    def execute_sort(self, indices):
        """Función recursiva de ordenamiento local"""
        if len(indices) <= 1:
            return indices, [0]
        
        mid = len(indices) // 2
        sa_izq, lcp_izq = self.execute_sort(indices[:mid])
        sa_der, lcp_der = self.execute_sort(indices[mid:])
        
        return self.merge(sa_izq, lcp_izq, sa_der, lcp_der)
    

# Ejemplo de uso para esta fase:
if __name__ == "__main__":
    
    try:

        root = Tk()
        root.withdraw() 
        ruta = filedialog.askopenfilename(
            title="Selecciona tu secuencia",
            # ¡Añadido soporte para .fna y otros formatos (Por si a caso)
            filetypes=[("Secuencias de ADN", "*.fasta *.fa *.fna *.txt")] 
        )

        data = GenomicData()
        data.cargar_fna(ruta)
        print(data.info_memoria())
    except Exception as e:
        print(f"Error en Fase 1: {e}")