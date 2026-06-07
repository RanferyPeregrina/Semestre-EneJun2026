"""
═══════════════════════════════════════════════════════════════════
  CALCULADORA DE ENTROPÍA DE SHANNON
  Soporta: entrada manual  |  archivo de texto (.txt / .csv)
  Bases disponibles: log2 (bits)  |  log10 (hartleys)  |  ln (nats)
═══════════════════════════════════════════════════════════════════
  Autor: AF1 – Información Mutua y Entropía
  Uso:
      python entropia.py                  → modo interactivo (manual)
      python entropia.py datos.txt        → leer desde archivo
═══════════════════════════════════════════════════════════════════
  Formato del archivo de texto:
      # Las líneas que empiezan con # son comentarios y se ignoran
      # Una probabilidad por línea  → solo prob
      # O símbolo y probabilidad    → separados por espacio, coma o tabulador
      Ejemplo:
          s1  0.30
          s2  0.21
          s3  0.17
          ...
═══════════════════════════════════════════════════════════════════
"""

import math
import sys
import os


# ──────────────────────────────────────────────
#  CONSTANTES
# ──────────────────────────────────────────────
BASES = {
    "1": ("log2",  math.log2,  "bits"),
    "2": ("log10", math.log10, "hartleys (hart/sim)"),
    "3": ("ln",    math.log,   "nats"),
}

SEP = "═" * 60
sep = "─" * 60


# ──────────────────────────────────────────────
#  UTILIDADES
# ──────────────────────────────────────────────
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print(SEP)
    print("  CALCULADORA DE ENTROPÍA DE SHANNON")
    print(SEP)
    print()


def elegir_base():
    print("  Selecciona la base logarítmica:")
    for k, (nombre, _, unidad) in BASES.items():
        print(f"    [{k}]  {nombre:6s}  →  {unidad}")
    print()
    while True:
        opc = input("  Opción [1/2/3] (Enter = 1 bits): ").strip() or "1"
        if opc in BASES:
            nombre, fn_log, unidad = BASES[opc]
            print(f"\n  ✔  Usando {nombre} → unidades: {unidad}\n")
            return nombre, fn_log, unidad
        print("  ⚠  Opción inválida. Escribe 1, 2 o 3.")


# ──────────────────────────────────────────────
#  LECTURA DE DATOS
# ──────────────────────────────────────────────
def leer_manual():
    """Entrada interactiva: el usuario escribe símbolo y probabilidad."""
    print(sep)
    print("  ENTRADA MANUAL")
    print("  Escribe el símbolo (o solo Enter para auto-nombrar)")
    print("  y su probabilidad. Escribe 'fin' cuando termines.")
    print(sep)

    simbolos, probs = [], []
    idx = 1
    while True:
        sym_raw = input(f"\n  Símbolo {idx} (Enter = s{idx} | 'fin' para terminar): ").strip()
        if sym_raw.lower() == "fin":
            if len(probs) < 1:
                print("  ⚠  Ingresa al menos un símbolo.")
                continue
            break
        sym = sym_raw if sym_raw else f"s{idx}"

        while True:
            p_raw = input(f"  P({sym}) = ").strip().replace(",", ".")
            try:
                p = float(p_raw)
                if 0 < p <= 1:
                    break
                print("  ⚠  La probabilidad debe estar entre 0 (exclusivo) y 1.")
            except ValueError:
                print("  ⚠  Ingresa un número válido (ej: 0.30).")

        simbolos.append(sym)
        probs.append(p)
        idx += 1

    return simbolos, probs


def leer_archivo(ruta):
    """Lee símbolos y probabilidades desde un archivo .txt o .csv."""
    simbolos, probs = [], []
    idx = 1

    if not os.path.exists(ruta):
        print(f"\n  ✘  Archivo no encontrado: '{ruta}'")
        sys.exit(1)

    with open(ruta, "r", encoding="utf-8") as f:
        for num_linea, linea in enumerate(f, 1):
            linea = linea.strip()
            # Ignorar vacías y comentarios
            if not linea or linea.startswith("#"):
                continue

            # Separadores: espacio, tabulador, coma, punto y coma
            partes = linea.replace(",", " ").replace(";", " ").replace("\t", " ").split()

            if len(partes) == 1:
                # Solo probabilidad
                sym = f"s{idx}"
                p_str = partes[0]
            elif len(partes) >= 2:
                sym   = partes[0]
                p_str = partes[1]
            else:
                print(f"  ⚠  Línea {num_linea} ignorada (formato inválido): '{linea}'")
                continue

            try:
                p = float(p_str)
                if not (0 < p <= 1):
                    raise ValueError
            except ValueError:
                print(f"  ⚠  Línea {num_linea} ignorada (probabilidad inválida): '{p_str}'")
                continue

            simbolos.append(sym)
            probs.append(p)
            idx += 1

    if not simbolos:
        print("  ✘  No se encontraron datos válidos en el archivo.")
        sys.exit(1)

    print(f"  ✔  {len(simbolos)} símbolo(s) cargado(s) desde '{ruta}'\n")
    return simbolos, probs


# ──────────────────────────────────────────────
#  VALIDACIÓN DE PROBABILIDADES
# ──────────────────────────────────────────────
def validar_probs(simbolos, probs):
    total = sum(probs)
    print(sep)
    print(f"  Verificación: Σ P(sᵢ) = {total:.6f}")

    if abs(total - 1.0) > 0.01:
        print(f"  ⚠  La suma de probabilidades es {total:.4f}, no es exactamente 1.")
        while True:
            opc = input("  ¿Normalizar automáticamente? [s/n]: ").strip().lower()
            if opc == "s":
                probs = [p / total for p in probs]
                print(f"  ✔  Probabilidades normalizadas. Nueva suma = {sum(probs):.6f}")
                break
            elif opc == "n":
                print("  ⚠  Continuando con probabilidades sin normalizar.")
                break
    else:
        print(f"  ✔  Suma válida.\n")

    return simbolos, probs


# ──────────────────────────────────────────────
#  CÁLCULO DE ENTROPÍA
# ──────────────────────────────────────────────
def calcular_entropia(simbolos, probs, fn_log, nombre_log, unidad):
    """Calcula y muestra la entropía símbolo por símbolo."""

    print()
    print(SEP)
    print("  RESULTADOS — ENTROPÍA DE SHANNON")
    print(SEP)
    print()

    # Encabezado de tabla
    col1, col2, col3, col4 = 10, 12, 20, 22
    h3 = f"I(si) = -{nombre_log}(P)"
    h4 = f"-P*{nombre_log}(P)"
    print(f"  {'Simbolo':<{col1}} {'P(si)':>{col2}} {h3:>{col3}} {h4:>{col4}}")
    print(f"  {'':─<{col1}} {'':─>{col2}} {'':─>{col3}} {'':─>{col4}}")

    contribuciones = []
    info_propias   = []

    for sym, p in zip(simbolos, probs):
        I    = -fn_log(p)          # autoinformación
        cont =  p * I              # contribución a H
        info_propias.append(I)
        contribuciones.append(cont)
        print(f"  {sym:<{col1}} {p:>{col2}.6f} {I:>{col3}.6f} {cont:>{col4}.6f}")

    H = sum(contribuciones)
    H_max = fn_log(len(simbolos))
    eficiencia = (H / H_max * 100) if H_max > 0 else 0

    print(f"  {'':─<{col1}} {'':─>{col2}} {'':─>{col3}} {'':─>{col4}}")
    print(f"  {'TOTAL':<{col1}} {sum(probs):>{col2}.6f} {'':>{col3}} {H:>{col4}.6f}")
    print()
    print(f"  {'─'*56}")
    print(f"  H(X)      = {H:.6f}  {unidad}")
    print(f"  H_max     = {H_max:.6f}  {unidad}  [= {nombre_log}({len(simbolos)} símbolos)]")
    print(f"  Eficiencia= {eficiencia:.2f}%")
    print(f"  {'─'*56}")
    print()

    # Símbolo más y menos informativo
    i_max = info_propias.index(max(info_propias))
    i_min = info_propias.index(min(info_propias))
    print(f"  Símbolo más  informativo: {simbolos[i_max]} → I = {info_propias[i_max]:.6f} {unidad}  (P = {probs[i_max]:.4f})")
    print(f"  Símbolo menos informativo: {simbolos[i_min]} → I = {info_propias[i_min]:.6f} {unidad}  (P = {probs[i_min]:.4f})")
    print()

    return H, H_max, eficiencia


# ──────────────────────────────────────────────
#  GUARDAR RESULTADOS
# ──────────────────────────────────────────────
def guardar_resultados(simbolos, probs, info_propias, contribuciones, H, H_max, eficiencia, nombre_log, unidad):
    nombre_archivo = input("  Nombre del archivo de salida (sin extensión, Enter para omitir): ").strip()
    if not nombre_archivo:
        print("  (No se guardó ningún archivo)\n")
        return

    ruta = nombre_archivo + "_entropia.txt"
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("RESULTADOS — ENTROPÍA DE SHANNON\n")
        f.write(f"Base logarítmica: {nombre_log} | Unidades: {unidad}\n")
        f.write("─" * 60 + "\n")
        f.write(f"{'Símbolo':<12} {'P(sᵢ)':>12} {'I(sᵢ)':>16} {'-P·log(P)':>16}\n")
        f.write("─" * 60 + "\n")
        for sym, p, I, c in zip(simbolos, probs, info_propias, contribuciones):
            f.write(f"{sym:<12} {p:>12.6f} {I:>16.6f} {c:>16.6f}\n")
        f.write("─" * 60 + "\n")
        f.write(f"{'H(X)':<20} {H:.6f} {unidad}\n")
        f.write(f"{'H_max':<20} {H_max:.6f} {unidad}\n")
        f.write(f"{'Eficiencia':<20} {eficiencia:.2f}%\n")
    print(f"  ✔  Resultados guardados en '{ruta}'\n")


# ──────────────────────────────────────────────
#  PROGRAMA PRINCIPAL
# ──────────────────────────────────────────────
def main():
    limpiar()
    banner()

    # Determinar fuente de datos
    if len(sys.argv) > 1:
        ruta = sys.argv[1]
        print(f"  Modo: archivo → '{ruta}'\n")
        simbolos, probs = leer_archivo(ruta)
    else:
        print("  Modo: entrada manual\n")
        simbolos, probs = leer_manual()

    # Elegir base
    print()
    nombre_log, fn_log, unidad = elegir_base()

    # Validar
    simbolos, probs = validar_probs(simbolos, probs)

    # Calcular
    info_propias   = [-fn_log(p) for p in probs]
    contribuciones = [p * I for p, I in zip(probs, info_propias)]
    H, H_max, eficiencia = calcular_entropia(simbolos, probs, fn_log, nombre_log, unidad)

    # Guardar
    print(sep)
    guardar_resultados(simbolos, probs, info_propias, contribuciones, H, H_max, eficiencia, nombre_log, unidad)

    input("  Presiona Enter para salir...")


if __name__ == "__main__":
    main()
