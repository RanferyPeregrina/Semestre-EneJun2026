import pandas as pd
from itertools import permutations

# ==========================================
# CONFIGURACIÓN
# ==========================================

ARCHIVO = "Secuencias.xlsx"
HOJA = "Recetas simplificadas"

MIN_SUPPORT = 0.6

# ==========================================
# LEER EXCEL
# ==========================================

df = pd.read_excel(ARCHIVO, sheet_name=HOJA)

id_col = df.columns[0]
step_cols = df.columns[1:]

# ==========================================
# CONSTRUIR SECUENCIAS
# ==========================================

recipes = []

for _, row in df.iterrows():

    seq = []

    for col in step_cols:
        val = row[col]
        if pd.notna(val):
            step = str(val).strip()
            if step != "":
                seq.append(step)
    recipes.append(seq)

# ==========================================
# OBTENER TODOS LOS EVENTOS ÚNICOS
# ==========================================

all_steps = set()

for seq in recipes:
    all_steps.update(seq)

all_steps = sorted(list(all_steps))
n_unique = len(all_steps)

print(f"\nEventos únicos encontrados: {n_unique}")

# ==========================================
# FUNCIÓN:
# VERIFICAR SUBSECUENCIA
# ==========================================

def is_subsequence(pattern, sequence):

    seq_idx = 0

    for item in pattern:
        found = False
        while seq_idx < len(sequence):
            if sequence[seq_idx] == item:
                found = True
                seq_idx += 1
                break
            seq_idx += 1
        if not found:
            return False

    return True

# ==========================================
# GENERAR CANDIDATOS
# ==========================================

candidate_patterns = []

# Desde tamaño 2 hasta n-1
for size in range(2, 6):

    print(f"Generando secuencias de tamaño {size}")
    perms = permutations(all_steps, size)

    for p in perms:
        candidate_patterns.append(p)

print(f"\nTotal de candidatos: {len(candidate_patterns)}")

# ==========================================
# CALCULAR SUPPORT
# ==========================================

total_recipes = len(recipes)
frequent_patterns = []
for pattern in candidate_patterns:
    count = 0
    presence = []

    for recipe in recipes:
        exists = is_subsequence(pattern, recipe)
        presence.append(int(exists))
        if exists:
            count += 1

    support = count / total_recipes

    if support >= MIN_SUPPORT:
        frequent_patterns.append({
            "Pattern": " -> ".join(pattern),
            "Length": len(pattern),
            "Support_Count": count,
            "Support": round(support, 4),
            "Presence": presence
        })

# ==========================================
# CREAR TABLA DE SUPPORT
# ==========================================

support_rows = []

for fp in frequent_patterns:

    row = {
        "Pattern": fp["Pattern"],
        "Length": fp["Length"],
        "Support_Count": fp["Support_Count"],
        "Support": fp["Support"]
    }

    for i, val in enumerate(fp["Presence"]):
        row[f"R{i+1}"] = val

    support_rows.append(row)

support_df = pd.DataFrame(support_rows)

# ==========================================
# CALCULAR REGLAS
# ==========================================

rules = []

for fp in frequent_patterns:

    items = fp["Pattern"].split(" -> ")

    if len(items) < 2:
        continue

    antecedent = tuple(items[:-1])
    consequent = items[-1]
    antecedent_count = 0

    for recipe in recipes:

        if is_subsequence(antecedent, recipe):
            antecedent_count += 1

    if antecedent_count > 0:

        confidence = fp["Support_Count"] / antecedent_count

        rules.append({
            "Rule": f'{" -> ".join(antecedent)} => {consequent}',
            "Support": fp["Support"],
            "Confidence": round(confidence, 4)
        })

rules_df = pd.DataFrame(rules)

# ==========================================
# EXPORTAR AL EXCEL
# ==========================================

output_file = "Resultados_Mineria_Secuencias.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

    # Secuencias frecuentes
    support_df.to_excel(
        writer,
        sheet_name="Frequent_Sequences",
        index=False
    )

    # Reglas
    rules_df.to_excel(
        writer,
        sheet_name="Association_Rules",
        index=False
    )

print("\n====================================")
print("MINERÍA TERMINADA")
print("====================================")

print(f"\nArchivo generado: {output_file}")