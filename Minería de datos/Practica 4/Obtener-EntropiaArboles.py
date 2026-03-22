import pandas as pd
import itertools
import math
import sys

# ========= 1. Cargar datos =========
df = pd.read_csv("eve.csv")

# Renombrar columnas para trabajar más fácil
df.columns = ["M", "T", "E"]

# Total de registros
N = len(df)

# ========= 2. Función de entropía =========
def entropy(p):
    if p == 0:
        return 0
    return -p * math.log10(p)

# ========= 3. Función que construye el árbol =========
def build_tree(order, df):
    print("\n===============================")
    print(f"Orden de variables: {order}")
    print("===============================\n")

    current_cols = []

    for level, var in enumerate(order):
        current_cols.append(var)

        print(f"\n--- Nivel {level+1}: Variables {current_cols} ---")

        # Contar combinaciones
        counts = df.groupby(current_cols).size().reset_index(name='FreqABS')

        # Frecuencia relativa
        counts["FreqRel"] = counts["FreqABS"] / N

        # Entropía por fila
        counts["Entropy"] = counts["FreqRel"].apply(entropy)

        # Mostrar tabla
        print(counts)

        # Entropía total del nivel
        total_entropy = counts["Entropy"].sum()
        print(f"\nEntropía total del nivel: {total_entropy:.6f}\n")

# ========= 4. Generar todas las permutaciones =========
variables = ["M", "T", "E"]
orders = list(itertools.permutations(variables))

# ========= 5. Ejecutar árboles =========
for order in orders:
    build_tree(order, df)

sys.stdout = open('resultado_arboles.txt', 'w', encoding ='utf-8')