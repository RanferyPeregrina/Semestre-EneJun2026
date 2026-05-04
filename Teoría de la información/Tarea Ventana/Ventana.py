from tkinter import Tk
from tkinter.filedialog import askopenfilename

def NormalizarTexto(Texto):
    Texto = Texto.lower()                   #Todo minúsculas
    Texto = Texto.replace("\n", " ")        #Sin saltos de línea
    while "  " in Texto:                    #Sin dobles espacios
        Texto = Texto.replace("  ", " ")       
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


# ==================================== AQUÍ COMIENZA EL FLUJO DEL PROGRAMA ======================================== 
#Agarramos nuestro texto
Texto = LeerArchivo()

#Agarramos el tamño de ventana
TamañoVentana = int(input("¿De qué tamaño es la ventana?:  "))

#Creamos la primer ventana
Inicio = 0
Final = TamañoVentana
Texto_Ventana = Texto[Inicio:Final] 
Historial = Texto_Ventana[Inicio:(int(len(Texto) * 0.7))]
LookAhead = Texto_Ventana[len(Historial):(int(len(Texto) * 0.3))]


print(f"Para el texto de la ventana: {Texto_Ventana}")
print(f"El historial es: {Historial}")
print(f"El Lookahead es: {LookAhead}")

# print(Texto)
