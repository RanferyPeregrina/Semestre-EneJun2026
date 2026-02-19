#Antes de correr el programa recuerden abrir su CMD y escribir: pip install itertools
from itertools import product #El 'product' es como se llama esa cosa de hacer combinaciones posibles.


def generar_mensajes(Alfabeto, L):

    combinaciones = product(Alfabeto, repeat=L)
    
    mensajes = []
    for c in combinaciones:
        mensaje = ''.join(c)
        mensajes.append(mensaje)
    
    return mensajes


# ----- Ejemplo -----

Alfabeto_A = ['0', '1']
Alfabeto_B = ['0', '1', '*']

L = 3
for i in range(L):
    print(i+1)
    mensajes_A = generar_mensajes(Alfabeto_A, i+1)
    mensajes_B = generar_mensajes(Alfabeto_B, i+1)

    print("Mensajes posibles de entrada:")
    print(mensajes_A)
    print("nA = ", len(mensajes_A))

    print("\nMensajes posibles de salida:")
    print(mensajes_B)
    print("nB = ", len(mensajes_B))
    print('= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = \n')