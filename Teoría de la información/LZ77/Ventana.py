from tkinter import Tk
from tkinter.filedialog import askopenfilename
import sys

Matricula = input(f"Ingrese su matrícula: ")

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
log_file = open(f"Resultado{Matricula}.txt", "w", encoding="utf-8")
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

def NormalizarTexto(Texto):
    Texto = Texto.lower()                   #Todo minúsculas
    Texto = Texto.replace("\n", " ")        #Sin saltos de línea
    while "  " in Texto:                    #Sin dobles espacios
        Texto = Texto.replace("  ", " ")       
    while " " in Texto:
        Texto = Texto.replace(" ", "◻")

    return Texto

def LeerArchivo():
    root = Tk()
    root.withdraw()

    Archivo = askopenfilename(title = "Elige el archivo de texto")
    if Archivo:
        with open(Archivo, "r", encoding="utf-8") as Archivo:
            Texto = Archivo.read()
            Texto = NormalizarTexto(Texto)

    return Texto

def DividirTexto(Porcentaje, Texto):
    Texto = Texto[0: int(len(Texto) * Porcentaje)]
    return Texto

def CrearContador(Tamaño, EspacioPrevio):
    Contador = "".join(str((Tamaño - i) % 10) for i in range(Tamaño))
    Contador = (" " * EspacioPrevio) + Contador
    return Contador

def CalcularRadioCompresion():
    Original = len(Texto)
    print(f"Tamaño original: {Original} caracteres")
    Comprimido = sum(Tamaño for Tamaño, _, _ in Resultados) + len(Resultados) * 2
    Radio = Original / Comprimido
    print(f"Radio de compresión: {Radio:.2f}")





# ==================================== AQUÍ COMIENZA EL FLUJO DEL PROGRAMA ======================================== 
#Agarramos nuestro texto
Texto = LeerArchivo()
DistanciaRestante = len(Texto)
TamañoVentana = 0

#Agarramos el tamño de ventana

for Digito in Matricula:
    print(f"+ {Digito}", end=" ")
    TamañoVentana += int(Digito)
print(f"\nTamaño de ventana calculado: {TamañoVentana}\n")
# TamañoVentana = int(input("¿De qué tamaño es la ventana?:  "))
DistanciaRestante -= TamañoVentana
VentanaRecorrida = 0
Resultados = []

#Creamos la primer ventana
Inicio = 0
Final = TamañoVentana


while DistanciaRestante >= 0:
    VentanaRecorrida += 1
    # print(f'Quedan {DistanciaRestante} espacios para terminar\n---------------------------------------------------')

    Texto_Ventana = Texto[Inicio:Final] 
    limite = round(len(Texto_Ventana) * 0.7)
    Historial = Texto_Ventana[0:limite]
    LookAhead = Texto_Ventana[limite:]
    #Esta es impresión por motivos de depuración --------------------
    print(f"Para el texto de la ventana: {Texto_Ventana}")
    Contador = CrearContador(TamañoVentana, 29)
    print(Contador)
    print(f"El historial es:{Historial}")
    Contador = CrearContador(len(Historial), 16)
    print(Contador)
    print(f"El Lookahead es:{LookAhead}")
    Contador = CrearContador(len(LookAhead), 16)
    print(Contador)
    # -----------------------------------------------------------------

    LookAheadCorrecto = ''
    Tamaño = 0

    for Letra in LookAhead:
        LookAheadCorrecto += Letra
      
        if LookAheadCorrecto in Historial:                                  #Si encuentra encuentra del Lookahead
            print(f'\nTermino: {LookAheadCorrecto} encontrado.')            #Avisa
            Offset = len(Historial) - (Historial.find(LookAheadCorrecto))   #Calcula cosas
            Tamaño += 1
        else:
            if len(LookAheadCorrecto) <= 1:                                 #Si no encuentra NADA
                Tamaño = len(LookAhead)                                     #Calcula cosas
                Offset = 0
                Letra = "Vacío..."
            break
        if len(LookAheadCorrecto) == len(LookAhead):                        #Si encuentra completo el LookAhead
            Tamaño = len(LookAheadCorrecto)                                 #Calcula cosas
            Offset = len(Historial) - (Historial.find(LookAheadCorrecto))   #Calcula cosas
            Letra = "Vacío..."
            break
    
    Resultados.append((Tamaño, Offset, Letra))                                     #Guarda los resultados
    print(f'Tamaño = {Tamaño}')                                             #Imprime los resultados de cada iteración
    print(f'Offset = {Offset}')
    print(f'Letra que rompió: {Letra}')



    if Tamaño > DistanciaRestante:
        Tamaño = DistanciaRestante

    Inicio += Tamaño
    Final += Tamaño
    if DistanciaRestante <= 0:
        break
    else: DistanciaRestante -= Tamaño

print("=" * 30)
print(f"Ventanas recorrida: {VentanaRecorrida} veces")
for i, (Tamaño, Offset, Letra) in enumerate(Resultados, 1):
    print(f"Ventana {i}: Tamaño={Tamaño}, Offset={Offset}, Letra='{Letra}'")
print()
CalcularRadioCompresion()