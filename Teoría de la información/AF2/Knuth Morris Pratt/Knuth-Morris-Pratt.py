from tkinter import Tk
from tkinter.filedialog import askopenfilename
import sys


class Tee:#Esto es para que las cosas se guarden en un TXT al final jeje.
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()  # Para que se guarde al momento
    def flush(self):
        for f in self.files:
            f.flush()
log_file = open("Salida.txt", "w", encoding="utf-8")
original_stdout = sys.stdout
sys.stdout = Tee(sys.stdout, log_file)

def LeerTexto():
    root = Tk()
    root.withdraw()
    Archivo = askopenfilename(title = "Elige el archivo de texto")
    if Archivo:
        with open(Archivo, "r", encoding="utf-8") as Archivo:
            Texto = Archivo.read()
    return Texto
# Esto lo voy a copiar y pegar en todos los programas. 🦀, hasta aquí -----------------------------


def kmp_explicito(texto, patron):
    n = len(texto)
    m = len(patron)
        

    with open("Salida.txt", "w") as Archivo: 

        # 1. Crear la tabla de fallos (Pi)
        pi = [0] * m
        j = 0
        print(f"--- Pre-procesando patrón para KMP ---", file=Archivo)
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

# ---------------------------------------------------------------------------------------
#Para usar el bloc de notas como entrada, descomenta esto:
# TextoGrande = LeerTexto()
# TextoBuscado = LeerTexto()
# ---------------------------------------------------------------------------------------
#Y comenta esto otro de aquí abajo jeje
TextoGrande = input("Ingrese el texto grande con el que trabajará (Cadena principal)")
TextoBuscado = input("Ingresa el texto que buscas (Cadena buscada):  ")
# ---------------------------------------------------------------------------------------

kmp_explicito(TextoGrande, TextoBuscado)



