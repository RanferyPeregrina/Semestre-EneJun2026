import pandas as pd
import itertools
import math
import sys
from pandas import ExcelWriter

# ========= Redirigir stdout al inicio =========
sys.stdout = open('resultado_arboles.txt', 'w', encoding='utf-8')

# ========= 1. Cargar datos =========
df = pd.read_csv("eve.csv")  # Directorio relativo porque soy un cobarde.

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
def build_tree(order, df, writer):
    print("\n===============================")
    print(f"Orden de variables: {order}")
    print("===============================\n")

    current_cols = []
    start_col = 0  # para separar tablas en Excel

    for level, var in enumerate(order):
        current_cols.append(var)

        print(f"\n--- Nivel {level+1}: Variables {current_cols} ---")

        counts = df.groupby(current_cols).size().reset_index(name='FreqABS')
        counts["FreqRel"] = counts["FreqABS"] / N
        counts["Entropy"] = counts["FreqRel"].apply(entropy)

        print(counts)

        total_entropy = counts["Entropy"].sum()
        print(f"\nEntropía total del nivel: {total_entropy:.6f}\n")

        # ===== Exportar a Excel =====
        sheet_name = "".join(order)

        counts.to_excel(
            writer,
            sheet_name=sheet_name,
            startcol=start_col,
            index=False
        )

        start_col += len(counts.columns) + 1  # deja una columna vacía para que se vea más ordenadito.

# ========= 4. Generar todas las permutaciones =========
variables = ["M", "T", "E"]
orders = list(itertools.permutations(variables))

# Puse esto para que haga un Excel a parte.
writer = pd.ExcelWriter("arboles_entropia.xlsx", engine="xlsxwriter")

# ========= 5. Ejecutar árboles =========
for order in orders:
    build_tree(order, df, writer)

writer.close()

sys.stdout.close()
sys.stdout = sys.__stdout__