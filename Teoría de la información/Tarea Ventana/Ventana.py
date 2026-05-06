from tkinter import Tk
from tkinter.filedialog import askopenfilename

def NormalizarTexto(Texto):
    Texto = Texto.lower()                   #Todo minúsculas
    Texto = Texto.replace("\n", " ")        #Sin saltos de línea
    while "  " in Texto:                    #Sin dobles espacios
        Texto = Texto.replace("  ", " ")       
    # while " " in Texto:
    #     Texto = Texto.replace(" ", "◻")

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
# ==================================== AQUÍ COMIENZA EL FLUJO DEL PROGRAMA ======================================== 
#Agarramos nuestro texto
Texto = LeerArchivo()
DistanciaRestante = len(Texto)

#Agarramos el tamño de ventana
TamañoVentana = int(input("¿De qué tamaño es la ventana?:  "))
DistanciaRestante -= TamañoVentana

#Creamos la primer ventana
Inicio = 0
Final = TamañoVentana


while DistanciaRestante >= 0:
    print(f'Quedan {DistanciaRestante} espacios para terminar\n---------------------------------------------------')

    Texto_Ventana = Texto[Inicio:Final] 
    Historial = Texto_Ventana[Inicio:(int(len(Texto_Ventana) * 0.7))]
    LookAhead = Texto_Ventana[(int(len(Texto_Ventana) * 0.7)):Final]
    #Esta es impresión por motivos de depuración --------------------
    print(f"Para el texto de la ventana: {Texto_Ventana}")
    Contador = CrearContador(TamañoVentana, 28)
    print(Contador)
    print(f"El historial es:{Historial}")
    Contador = CrearContador(len(Historial), 17)
    print(Contador)
    print(f"El Lookahead es:{LookAhead}")
    Contador = CrearContador(len(LookAhead), 17)
    print(Contador)
    # -----------------------------------------------------------------

    LookAheadCorrecto = ''
    Tamaño = 0

    for Letra in LookAhead:
        LookAheadCorrecto += Letra
      
        if LookAheadCorrecto in Historial:
            print(f'Termino: {LookAheadCorrecto} encontrado.')
            Offset = len(Historial) - (Historial.find(Letra))
            Tamaño += 1
        else:
            if LookAheadCorrecto == '':
                Tamaño = len(LookAhead)
                Offset = 0
            print(f'Tamaño = {Tamaño}')
            print(f'Offset = {Offset}')
            print(f'Letra que rompió: {Letra}')
            break



    
    Inicio += Tamaño
    Final += Tamaño
    DistanciaRestante - Tamaño
    input()
            