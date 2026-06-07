import pandas as pd
from itertools import permutations, combinations

# =========================================================
# CONFIGURACIÓN
# =========================================================

ARCHIVO = "Episodios.xlsx"
HOJA = "Input"

# Support mínimo
MIN_SUPPORT = 0.05

# Tamaño máximo de episodio
# (Cantidad de eventos dentro del episodio)
MAX_EPISODE_SIZE = 2

# =========================================================
# LEER EXCEL
# =========================================================

df = pd.read_excel(ARCHIVO, sheet_name=HOJA)

# Segunda columna = eventos
events = df.iloc[:, 1].dropna().astype(str).tolist()

print("\n========================================")
print("SECUENCIA TEMPORAL")
print("========================================")

print(events)

# =========================================================
# EVENTOS ÚNICOS
# =========================================================

unique_events = sorted(list(set(events)))

print("\n========================================")
print("EVENTOS ÚNICOS")
print("========================================")

print(unique_events)

# =========================================================
# FUNCIÓN:
# VERIFICAR SUBSECUENCIA
# =========================================================

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

# =========================================================
# DATAFRAME RESUMEN
# =========================================================

summary_rows = []

# =========================================================
# EXCEL DE SALIDA
# =========================================================

OUTPUT = "Resultados_Episode_Mining.xlsx"

writer = pd.ExcelWriter(OUTPUT, engine="openpyxl")

# =========================================================
# ANALIZAR TODAS LAS VENTANAS
# =========================================================
#
# El maestro pidió:
#
# ventana = 3
# ventana = 4
# ventana = 5
# ...
# ventana = n-1
#
# =========================================================

for WINDOW_SIZE in range(3, 37):

    print("\n========================================")
    print(f"ANALIZANDO VENTANA {WINDOW_SIZE}")
    print("========================================")

    # =====================================================
    # GENERAR VENTANAS DESLIZANTES
    # =====================================================

    windows = []

    for i in range(len(events) - WINDOW_SIZE + 1):

        window = events[i:i + WINDOW_SIZE]

        windows.append(window)

    print(f"Ventanas generadas: {len(windows)}")

    # =====================================================
    # GENERAR EPISODIOS CANDIDATOS
    # =====================================================

    candidate_episodes = set()

    for window in windows:

        # Para cada tamaño de episodio
        for size in range(2, min(MAX_EPISODE_SIZE + 1, len(window) + 1)):

            # Generar subsecuencias reales de la ventana
            for combo in combinations(range(len(window)), size):

                episode = tuple(window[i] for i in combo)

                candidate_episodes.add(episode)

    candidate_episodes = list(candidate_episodes)

    print(f"\nCandidatos generados: {len(candidate_episodes)}")

    print("\n========================================")
    print("TOTAL DE EPISODIOS CANDIDATOS")
    print("========================================")

    print(len(candidate_episodes))

    # =====================================================
    # TABLA DE VENTANAS
    # =====================================================

    window_rows = []

    for i, window in enumerate(windows):
        window_rows.append({
            "Window_ID": f"W{i+1}",
            "Events": ", ".join(window)
        })

    windows_df = pd.DataFrame(window_rows)

    # =====================================================
    # BUSCAR EPISODIOS FRECUENTES
    # =====================================================

    frequent_episodes = []

    for episode in candidate_episodes:

        count = 0

        presence_vector = []

        for window in windows:

            occurs = is_subsequence(episode, window)

            presence_vector.append(int(occurs))

            if occurs:
                count += 1

        support = count / len(windows)

        if support >= MIN_SUPPORT:

            frequent_episodes.append({
                "Episode": " -> ".join(episode),
                "Length": len(episode),
                "Occurrences": count,
                "Support": round(support, 4),
            })

    print(f"Episodios frecuentes encontrados: {len(frequent_episodes)}")

    # =====================================================
    # TABLA DE EPISODIOS
    # =====================================================

    episode_rows = []

    for ep in frequent_episodes:

        row = {
            "Episode": ep["Episode"],
            "Length": ep["Length"],
            "Occurrences": ep["Occurrences"],
            "Support": ep["Support"]
        }


        episode_rows.append(row)

    episodes_df = pd.DataFrame(episode_rows)

    # =====================================================
    # REGLAS
    # =====================================================

    rules = []

    for ep in frequent_episodes:

        items = ep["Episode"].split(" -> ")

        if len(items) < 2:
            continue

        antecedent = tuple(items[:-1])

        consequent = items[-1]

        antecedent_count = 0

        for window in windows:

            if is_subsequence(antecedent, window):
                antecedent_count += 1

        if antecedent_count > 0:

            confidence = ep["Occurrences"] / antecedent_count

            rules.append({
                "Rule": f'{" -> ".join(antecedent)} => {consequent}',
                "Support": ep["Support"],
                "Confidence": round(confidence, 4)
            })

    rules_df = pd.DataFrame(rules)

    # =====================================================
    # EXPORTAR HOJAS
    # =====================================================

    # Ventanas
    windows_df.to_excel(
        writer,
        sheet_name=f"W{WINDOW_SIZE}_Windows",
        index=False
    )

    # Episodios frecuentes
    episodes_df.to_excel(
        writer,
        sheet_name=f"W{WINDOW_SIZE}_Episodes",
        index=False
    )

    # Reglas
    rules_df.to_excel(
        writer,
        sheet_name=f"W{WINDOW_SIZE}_Rules",
        index=False
    )

    # =====================================================
    # RESUMEN
    # =====================================================

    summary_rows.append({
        "Window_Size": WINDOW_SIZE,
        "Total_Windows": len(windows),
        "Frequent_Episodes": len(frequent_episodes),
        "Rules_Generated": len(rules)
    })

# =========================================================
# EXPORTAR RESUMEN
# =========================================================

summary_df = pd.DataFrame(summary_rows)

summary_df.to_excel(
    writer,
    sheet_name="Summary",
    index=False
)

# =========================================================
# GUARDAR EXCEL
# =========================================================

writer.close()

# =========================================================
# FINAL
# =========================================================

print("\n========================================")
print("EPISODE MINING TERMINADO")
print("========================================")

print(f"\nArchivo generado: {OUTPUT}")