from collections import defaultdict
import pandas as pd

# LISTA DE SECUENCIAS (TRANSACCIONES) - HUAZONTLES
sequences = [
    ['limpiar huazontles', 'huazontles', 'lavar'],                         # T1
    ['cocer huazontles', 'huazontles', 'olla', 'agua', 'sal'],            # T2
    ['escurrir huazontles', 'huazontles', 'colador'],                     # T3
    ['desmenuzar huazontles', 'huazontles', 'mezclar huevo', 'sal'],      # T4
    ['batir claras', 'mezclar huevo', 'huazontles'],                      # T5
    ['formar tortitas', 'huazontles', 'harina', 'huevo batido'],          # T6
    ['freir tortitas', 'tortitas', 'aceite', 'sarten'],                   # T7
    ['preparar caldillo', 'jitomate', 'cebolla', 'ajo'],                  # T8
    ['hervir caldillo', 'caldillo', 'olla', 'sal'],                       # T9
    ['servir tortitas', 'tortitas', 'caldillo']                           # T10
]

# Soporte mínimo requerido para que un patrón sea considerado frecuente
min_support = 2

# FUNCION PARA CONTAR CUANTAS VECES APARECE UN PATRON
def count_patterns(sequences, patterns):
    counts = defaultdict(int)
    for seq in sequences:
        for pat in patterns:
            idx = 0
            for item in seq:
                if item == pat[idx]:
                    idx += 1
                    if idx == len(pat):
                        break
            if idx == len(pat):
                counts[tuple(pat)] += 1
    return counts

# CREAR PATRONES INICIALES DE UN SOLO ITEM
unique_items = set(item for seq in sequences for item in seq)
patterns = [[item] for item in unique_items]

# APLICAR APRIORI PARA SECUENCIAS
frequent_patterns = []
support_data = []
k = 1

while patterns:
    counts = count_patterns(sequences, patterns)

    # Filtrar solo los patrones que cumplen con el soporte minimo
    patterns = [pat for pat, count in counts.items() if count >= min_support]
    frequent_patterns.extend(patterns)

    # Guardar datos de soporte de los patrones frecuentes actuales
    for pat in patterns:
        support = count_patterns(sequences, [pat])[tuple(pat)]
        support_data.append({
            "Longitud_del_patron": len(pat),
            "Patron": " -> ".join(pat),
            "Soporte": support
        })

    # Generar nuevos patrones combinando los actuales
    new_patterns = []
    for i in range(len(patterns)):
        for j in range(len(patterns)):
            if patterns[i][1:] == patterns[j][:-1]:
                combined = list(patterns[i]) + [patterns[j][-1]]
                new_patterns.append(combined)
    patterns = new_patterns
    k += 1

# MOSTRAR RESULTADOS POR CONSOLA
print("Patrones frecuentes en la preparacion de huazontles:\n")
for entry in support_data:
    print(f"{entry['Patron']} (Soporte: {entry['Soporte']})")

print("\nTotal de patrones frecuentes encontrados:", len(support_data))

# EXPORTAR A EXCEL
df = pd.DataFrame(support_data)
if not df.empty:
    df.sort_values(by=['Longitud_del_patron', 'Soporte'],
                   ascending=[True, False], inplace=True)
    df.to_excel("patrones_secuenciales_huazontles.xlsx", index=False)
    print("\nResultados exportados a 'patrones_secuenciales_huazontles.xlsx'")
else:
    print("\nNo se encontraron patrones con el soporte minimo indicado.")
