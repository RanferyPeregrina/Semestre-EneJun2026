import math

def PedirAlfabeto():
    Alfabeto = []
    Indice = 0  #No sé cómo hacer esto de forma más profesional.

    #Mientras el usuario no deje de ingresar símbolos, se van agregando al alfabeto. Si deja de ingresar, se termina el proceso.
    print("Ingrese los símbolos del alfabeto")
    while True:
        Indice += 1
        Simbolo = input(f"Letra {Indice} del alfabeto (Dejar vacío para finalizar): ")
        if Simbolo == "":
            break
        else:
            Alfabeto.append(Simbolo)
    return Alfabeto

def PedirFrecuencias(Alfabeto):
    Frecuencias = []
    for Letra in range(len(Alfabeto)):
        Frecuencias.append(float(input(f"Ingrese la frecuencia de {Letra}:  ")))

    return Frecuencias

def NormalizarAlfabeto(Alfabeto, Frecuencias):
#Si las frecuencias no suman todas de salida un 100% (1) de salida, es porque falta un dato.
#Lo agregamos como un caracter difuso: *
    if sum(Frecuencias) != 1:
        print(f"\nLas frecuencias de entrada suman {sum(Frecuencias)}")
        if sum(Frecuencias) > 1:
            print("El programa excede el 1. Esto no puede seguir.")
            exit()
        elif sum(Frecuencias) < 1:
            print(" -" * 30)
            print(f"⚠ Epale, no acompletas una salida entera.")
            print(f"Se agregará el caracter: * con valor {round(1 -sum(Frecuencias), 4)}")
            Alfabeto.append("*")
            Frecuencias.append(round(1 -sum(Frecuencias), 4))
            print(" -" * 30)

    return Alfabeto, Frecuencias

def Calcular_AutoInformacion(Frecuencia):
    AutoInformacion = round((-1) * (math.log2(Frecuencia)), 5)
    print(f"I({Frecuencia}) = -log({Frecuencia})2 = {AutoInformacion}")
    return AutoInformacion

def Calcular_Entropia(Frecuencia):
    Entropia = round((-1) * (Frecuencia) * (math.log2(Frecuencia)), 5)
    print(f"H({Frecuencia}) = -log({Frecuencia})2 = {Entropia}")
    return Entropia


# Alfabeto = PedirAlfabeto()
# Frecuencias = PedirFrecuencias(Alfabeto)
# ProbabilidadAcertar = float(input("Ingrese la probabilidad de acertar la transmisión:  "))

Alfabeto = ["a", "b", "c", "d"]
Frecuencias = [0.17, 0.38, 0.20, 0.05]
ProbabilidadAcertar = 0.95
Alfabeto, Frecuencias = NormalizarAlfabeto(Alfabeto, Frecuencias)
ProbabilidadFallar = round((1 - ProbabilidadAcertar) / (len(Alfabeto) - 1), 4)

print(f"Alfabeto: {Alfabeto}")
print(f"Frecuencias: {Frecuencias}")
print(f"Probabilidad de transmisión exitosa: {ProbabilidadAcertar}")

#Paso 1: Calculamos las frecuencias de salida.
#La probabilidad de que salga una letra específica es: La suma de que cada letra se convierta en esa letra específica.
print("= " * 30)
print("Frecuencias de salida")
for Frecuencia in range(len(Frecuencias)):
    Actual = Frecuencias[Frecuencia]
    Otros = Frecuencias[:Frecuencia] + Frecuencias[Frecuencia +  1:]
    ProbabilidadAparicion = Actual * ProbabilidadAcertar
    print(f"\n({Actual} * {ProbabilidadAcertar})", end="")
    for FrecuenciaO in Otros:
        ProbabilidadAparicion += FrecuenciaO * ProbabilidadFallar
        print(f" + ({FrecuenciaO} * {ProbabilidadFallar})", end="")
    print(f"\nProbabilidad de aparición de {Alfabeto[Frecuencia]} = {round(ProbabilidadAparicion, 4)}")
print("= " * 30)

#Paso 2: Calcular la autoinformación
#Asumiendo que es una matríz simétrica. Cada letra tiene 1 probabilidad fuerte y k-1 débiles repetidas.
print("= " * 30)
print("Autoinformación")
AutoInformacion_Total = 0
AutoInformacion_Total += Calcular_AutoInformacion(ProbabilidadAcertar)
for Frecuencia in range(len(Frecuencias) - 1):
    AutoInformacion_Total += Calcular_AutoInformacion(ProbabilidadFallar)
print(f"\nLa autoinformación total es: {AutoInformacion_Total}")
    

#Paso 3: Calcular la entropía
#Asumiendo que es una matríz simétrica. Cada letra tiene 1 probabilidad fuerte y k-1 débiles repetidas.
print("= " * 30)
print("Entropía")
Entropia_Total = 0
Entropia_Total += Calcular_Entropia(ProbabilidadAcertar)
for Frecuencia in range(len(Frecuencias) - 1):
    Entropia_Total += Calcular_Entropia(ProbabilidadFallar)
print(f"\nLa entropia total es: {round(Entropia_Total, 5)}")

#Paso 4: Calcular la capacidad del canal
#Para calcular la capacidad del canal expandimos todos los canales al máximo donde no "achican" a otros canales.
#Es decir, todos iguales. Entonces la entropía de salida alcanz su valor máximo con log2(m), donde "m" son todos los símbolos.
Entropia_Maxima = round(math.log2(len(Frecuencias)), 5)
#Y a esa entropía máxima le restamos la entropía total obtenida.
Capacidad_Canal = Entropia_Maxima - Entropia_Total
print(f"La entropía máxma es alcanzada con todos los canales al máximo:")
print(f"Son {len(Frecuencias)} canales, entonces: log2({len(Frecuencias)}) = {round(math.log2(len(Frecuencias)), 5)}")
print(f"C = {Entropia_Maxima} - {Entropia_Total}")
print(f"C = {round(Entropia_Maxima - Entropia_Total, 5)}")



