import os
from tkinter import Tk, filedialog

class GenomicData:

    def __init__(self):
        self.sequence = ""
        self.header = ""
        self.length = 0

    def load_fna(self, filepath):
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
        data.load_fna(ruta)
        print(data.info_memoria())
    except Exception as e:
        print(f"Error en Fase 1: {e}")