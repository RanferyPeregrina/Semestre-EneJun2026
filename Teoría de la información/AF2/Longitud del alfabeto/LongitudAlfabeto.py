from itertools import product #El 'product' es como se llama esa cosa de hacer combinaciones posibles.
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


def PedirAlfabeto(NombreAlfabeto):
    Alfabeto = []
    Indice = 0  #No sé cómo hacer esto de forma más profesional.

    #Mientras el usuario no deje de ingresar símbolos, se van agregando al alfabeto. Si deja de ingresar, se termina el proceso.
    print("Ingrese los símbolos del alfabeto", NombreAlfabeto)
    while True:
        Indice += 1
        Simbolo = input(f"Letra {Indice} del alfabeto (Dejar vacío para finalizar): ")
        if Simbolo == "":
            break
        else:
            Alfabeto.append(Simbolo)
    return Alfabeto

def Generar_Mensajes(Alfabeto, L):
    
    mensajes = []

    def construir(actual, longitud_actual):
        
        # Si ya llegamos exactamente a L → guardamos
        if longitud_actual == L:
            mensajes.append(actual)
            return
        
        # Si nos pasamos → cancelamos este camino
        if longitud_actual > L:
            return
        
        # Intentamos agregar cada símbolo
        for simbolo in Alfabeto:
            nueva_longitud = longitud_actual + len(simbolo)
            construir(actual + simbolo, nueva_longitud)

    # Empezamos desde vacío
    construir("", 0)

    return mensajes


# ----- Aquí vive todo el programa -----


# ---------------------------------------------------------------------------------------
# Para usar un archivo como entrada, comenta esta parte
Alfabeto_A = PedirAlfabeto("A")
Alfabeto_B = PedirAlfabeto("B")
L = int(input("Ingrese la longitud de los mensajes (L): "))
# ---------------------------------------------------------------------------------------
# Para usar un archivo como entrada, descomenta esta parte
# Alfabeto_A = LeerTexto()
# Alfabeto_B = LeerTexto()
# ---------------------------------------------------------------------------------------

for i in range(L):
    print("Para L = ",i+1)
    mensajes_A = Generar_Mensajes(Alfabeto_A, i+1)
    mensajes_B = Generar_Mensajes(Alfabeto_B, i+1)

    print("Mensajes posibles de entrada:")
    print("A = ", mensajes_A)
    print("nA = ", len(mensajes_A))

    print("\nMensajes posibles de salida:")
    print("B = ", mensajes_B)
    print("nB = ", len(mensajes_B),"\n")
    print('= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = \n')