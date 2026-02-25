from itertools import product #El 'product' es como se llama esa cosa de hacer combinaciones posibles.

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

Alfabeto_A = PedirAlfabeto("A")
Alfabeto_B = PedirAlfabeto("B")
L = int(input("Ingrese la longitud de los mensajes (L): "))

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