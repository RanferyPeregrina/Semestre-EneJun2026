import pandas as pd
from itertools import combinations
from collections import defaultdict

# ============================================
# 1. Leer datos desde Excel (sin filtrar por nombre)
# ============================================
archivo_excel = "Secuencias.xlsx"
nombre_hoja = "Datos"

# Leer todas las columnas
df_raw = pd.read_excel(archivo_excel, sheet_name=nombre_hoja)

# Mostrar los nombres de las columnas para depuración
print("Nombres de columnas encontrados:")
for i, col in enumerate(df_raw.columns):
    print(f"   {i}: '{col}'")

# Suponemos que la primera columna es "Que ocurre" y la segunda "Código"
# Si no es así, ajusta los índices (0 y 1)
col_descripcion = df_raw.columns[0]   # primera columna
col_codigo = df_raw.columns[1]        # segunda columna

print(f"\nColumna de descripción: '{col_descripcion}'")
print(f"Columna de código: '{col_codigo}'")

# Extraer las listas
descripciones = df_raw[col_descripcion].tolist()
eventos = df_raw[col_codigo].tolist()

# Eliminar filas con valores nulos en código
datos_validos = [(desc, cod) for desc, cod in zip(descripciones, eventos) if pd.notna(cod)]
descripciones = [d for d, c in datos_validos]
eventos = [c for d, c in datos_validos]

print(f"\nArchivo: {archivo_excel}")
print(f"Hoja: {nombre_hoja}")
print(f"Total de eventos cargados: {len(eventos)}")
print(f"Primeros 10 eventos: {eventos[:10]}")
print(f"Eventos únicos: {len(set(eventos))}\n")

# ============================================
# 2. Función para contar co-ocurrencias con ventana deslizante
# ============================================
def contar_coocurrencias(eventos, tamanio_ventana):
    conteo = defaultdict(int)
    n = len(eventos)
    for i in range(n - tamanio_ventana + 1):
        ventana = eventos[i:i + tamanio_ventana]
        unicos = list(set(ventana))
        for a, b in combinations(unicos, 2):
            par = tuple(sorted([a, b]))
            conteo[par] += 1
    return conteo

# ============================================
# 3. Probar ventanas (tamaño 3 hasta 10, por rendimiento)
# ============================================
n = len(eventos)
resultados_por_tamanio = {}

print("🔄 Procesando ventanas...")
print(f"📐 Ventanas desde tamaño 3 hasta {min(10, n-1)}\n")

for w in range(3, min(11, n)):
    print(f"  Procesando ventana de tamaño {w}...")
    conteo = contar_coocurrencias(eventos, w)
    resultados_por_tamanio[w] = conteo
    print(f"    -> {len(conteo)} pares diferentes encontrados")

print("\n✅ Procesamiento completado\n")

# ============================================
# 4. Mostrar resultados en consola
# ============================================
for w, conteo in resultados_por_tamanio.items():
    print(f"\n{'='*60}")
    print(f"VENTANA DE TAMAÑO {w}")
    print(f"{'='*60}")
    pares_ordenados = sorted(conteo.items(), key=lambda x: x[1], reverse=True)
    print("Top 15 pares más frecuentes:")
    for i, (par, freq) in enumerate(pares_ordenados[:15], 1):
        print(f"  {i:2d}. {par[0]} <-> {par[1]} : {freq} veces")
    total_ventanas = n - w + 1
    print(f"\n📊 Total de ventanas evaluadas: {total_ventanas}")

# ============================================
# 5. Exportar a Excel con resultados
# ============================================
archivo_salida = "resultados_coocurrencias.xlsx"
with pd.ExcelWriter(archivo_salida, engine='openpyxl') as writer:
    # Resumen
    resumen = []
    for w, conteo in resultados_por_tamanio.items():
        resumen.append({
            "Tamaño_ventana": w,
            "Total_pares_encontrados": len(conteo),
            "Total_ventanas_evaluadas": n - w + 1
        })
    pd.DataFrame(resumen).to_excel(writer, sheet_name="Resumen", index=False)
    
    # Hoja por cada ventana
    for w, conteo in resultados_por_tamanio.items():
        df = pd.DataFrame([
            {"Evento_A": par[0], "Evento_B": par[1], "Frecuencia": freq}
            for par, freq in conteo.items()
        ]).sort_values("Frecuencia", ascending=False)
        df.to_excel(writer, sheet_name=f"Ventana_{w}", index=False)
    
    # Hoja con la lista original (usando las descripciones reales)
    df_original = pd.DataFrame({
        "Indice": range(1, n+1),
        col_descripcion: descripciones,  # <- usa el nombre real de la columna
        "Codigo": eventos
    })
    df_original.to_excel(writer, sheet_name="Lista_original", index=False)

print(f"\n✅ Resultados guardados en '{archivo_salida}'")
print("\n💡 Nota: Se usaron las columnas por posición (primera y segunda) para evitar problemas de nombres.")