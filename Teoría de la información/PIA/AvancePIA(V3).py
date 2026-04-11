import os
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