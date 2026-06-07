"""
═══════════════════════════════════════════════════════════════════
  CALCULADORA DE INFORMACIÓN MUTUA
  I(X;Y) = H(X) + H(Y) − H(X,Y)
  Soporta: entrada manual  |  archivo de texto (.txt / .csv)
  Bases disponibles: log2 (bits)  |  log10 (hartleys)  |  ln (nats)
═══════════════════════════════════════════════════════════════════
  Uso:
      python info_mutua.py                → modo interactivo (manual)
      python info_mutua.py conjunta.txt   → leer desde archivo

  Formato del archivo para distribución CONJUNTA p(x,y):
      # Comentarios con #
      # Primera fila: encabezados de Y  (y1 y2 y3 ...)
      # Filas siguientes: símbolo_X  p(x,y1)  p(x,y2) ...
      Ejemplo (2×2):
          #    y1    y2
          x1   0.30  0.10
          x2   0.20  0.40

  Formato del archivo para distribuciones MARGINALES separadas:
      # Escribe [X] y luego los símbolos de X, luego [Y] y los de Y
      [X]
      x1  0.40
      x2  0.60
      [Y]
      y1  0.50
      y2  0.50
      # Nota: si X e Y son independientes, I(X;Y) = 0
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

SEP = "═" * 62
sep = "─" * 62


# ──────────────────────────────────────────────
#  UTILIDADES
# ──────────────────────────────────────────────
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print(SEP)
    print("  CALCULADORA DE INFORMACIÓN MUTUA   I(X;Y)")
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
        print("  ⚠  Opción inválida.")


def safe_log(fn_log, p):
    """Retorna p·log(p); devuelve 0 si p=0 (límite correcto)."""
    return p * fn_log(p) if p > 0 else 0.0


# ──────────────────────────────────────────────
#  MODO: DISTRIBUCIÓN CONJUNTA MANUAL
# ──────────────────────────────────────────────
def manual_conjunta():
    """El usuario ingresa p(xᵢ, yⱼ) para cada par."""
    print(sep)
    print("  MODO: Distribución conjunta p(x, y)")
    print("  Ingresa la tabla de probabilidades conjuntas.")
    print(sep)

    while True:
        try:
            nx = int(input("\n  Número de valores de X (filas): "))
            ny = int(input("  Número de valores de Y (columnas): "))
            if nx > 0 and ny > 0:
                break
            print("  ⚠  Deben ser enteros positivos.")
        except ValueError:
            print("  ⚠  Ingresa un número entero.")

    # Nombres de los símbolos
    print()
    nombres_x, nombres_y = [], []
    for i in range(nx):
        s = input(f"  Nombre de X[{i+1}] (Enter = x{i+1}): ").strip() or f"x{i+1}"
        nombres_x.append(s)
    for j in range(ny):
        s = input(f"  Nombre de Y[{j+1}] (Enter = y{j+1}): ").strip() or f"y{j+1}"
        nombres_y.append(s)

    # Ingresar probabilidades
    print(f"\n  Ingresa p({nombres_x[i]}, {nombres_y[j]}) para cada combinación:\n")
    tabla = []
    for i in range(nx):
        fila = []
        for j in range(ny):
            while True:
                raw = input(f"    p({nombres_x[i]}, {nombres_y[j]}) = ").strip().replace(",", ".")
                try:
                    p = float(raw)
                    if 0 <= p <= 1:
                        fila.append(p)
                        break
                    print("    ⚠  Debe estar entre 0 y 1.")
                except ValueError:
                    print("    ⚠  Número inválido.")
        tabla.append(fila)

    return nombres_x, nombres_y, tabla


# ──────────────────────────────────────────────
#  MODO: DISTRIBUCIONES MARGINALES MANUALES
# ──────────────────────────────────────────────
def manual_marginales():
    """Ingresa P(X) y P(Y) por separado (asume independencia)."""
    print(sep)
    print("  MODO: Distribuciones marginales P(X) y P(Y) por separado")
    print("  (Usa este modo si solo conoces las distribuciones individuales)")
    print(sep)

    def pedir_dist(nombre_var):
        print(f"\n  → Distribución de {nombre_var}:")
        simbolos, probs = [], []
        idx = 1
        while True:
            sym_raw = input(f"    Símbolo {idx} ({nombre_var}) [Enter={nombre_var.lower()}{idx} | 'fin']: ").strip()
            if sym_raw.lower() == "fin":
                if not probs:
                    print("    ⚠  Ingresa al menos un símbolo.")
                    continue
                break
            sym = sym_raw or f"{nombre_var.lower()}{idx}"
            while True:
                raw = input(f"    P({sym}) = ").strip().replace(",", ".")
                try:
                    p = float(raw)
                    if 0 < p <= 1:
                        simbolos.append(sym)
                        probs.append(p)
                        idx += 1
                        break
                    print("    ⚠  Debe ser > 0 y ≤ 1.")
                except ValueError:
                    print("    ⚠  Número inválido.")
        return simbolos, probs

    sx, px = pedir_dist("X")
    sy, py = pedir_dist("Y")

    # Construir tabla conjunta asumiendo independencia
    tabla = [[px[i] * py[j] for j in range(len(sy))] for i in range(len(sx))]
    return sx, sy, tabla


# ──────────────────────────────────────────────
#  LECTURA DESDE ARCHIVO
# ──────────────────────────────────────────────
def leer_archivo(ruta):
    """
    Detecta automáticamente si el archivo tiene distribución conjunta o marginal.
    """
    if not os.path.exists(ruta):
        print(f"\n  ✘  Archivo no encontrado: '{ruta}'")
        sys.exit(1)

    with open(ruta, "r", encoding="utf-8") as f:
        lineas = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]

    # Detectar formato MARGINAL (con secciones [X] y [Y])
    if any(l.upper() in ("[X]", "[Y]") for l in lineas):
        return _leer_marginal(lineas, ruta)
    else:
        return _leer_conjunta(lineas, ruta)


def _leer_conjunta(lineas, ruta):
    """Formato: primera fila = nombres Y, resto = filaX prob1 prob2 ..."""
    nombres_y_raw = lineas[0].split()
    nombres_y = nombres_y_raw  # primer token puede ser encabezado vacío

    nombres_x, tabla = [], []
    for linea in lineas[1:]:
        partes = linea.replace(",", " ").replace(";", " ").split()
        if not partes:
            continue
        nombres_x.append(partes[0])
        try:
            fila = [float(p) for p in partes[1:]]
        except ValueError:
            print(f"  ⚠  Línea ignorada (valor inválido): '{linea}'")
            continue
        tabla.append(fila)

    print(f"  ✔  Distribución conjunta {len(nombres_x)}×{len(nombres_y)} cargada desde '{ruta}'\n")
    return nombres_x, nombres_y, tabla


def _leer_marginal(lineas, ruta):
    """Formato por secciones [X] y [Y]."""
    sx, px, sy, py = [], [], [], []
    modo = None
    for l in lineas:
        if l.upper() == "[X]":
            modo = "X"; continue
        if l.upper() == "[Y]":
            modo = "Y"; continue
        partes = l.replace(",", " ").replace(";", " ").split()
        if len(partes) < 2:
            continue
        try:
            p = float(partes[1])
        except ValueError:
            continue
        if modo == "X":
            sx.append(partes[0]); px.append(p)
        elif modo == "Y":
            sy.append(partes[0]); py.append(p)

    # Tabla conjunta bajo independencia
    tabla = [[px[i] * py[j] for j in range(len(sy))] for i in range(len(sx))]
    print(f"  ✔  Distribuciones marginales cargadas (X={len(sx)}, Y={len(sy)}) — asumiendo independencia\n")
    return sx, sy, tabla


# ──────────────────────────────────────────────
#  CÁLCULO DE INFORMACIÓN MUTUA
# ──────────────────────────────────────────────
def calcular_info_mutua(nx_names, ny_names, tabla, fn_log, nombre_log, unidad):
    nx = len(nx_names)
    ny = len(ny_names)

    # Marginales
    px = [sum(tabla[i][j] for j in range(ny)) for i in range(nx)]
    py = [sum(tabla[i][j] for i in range(nx)) for j in range(ny)]

    # Entropías
    Hx  = -sum(safe_log(fn_log, p) for p in px)
    Hy  = -sum(safe_log(fn_log, p) for p in py)
    Hxy = -sum(safe_log(fn_log, tabla[i][j])
               for i in range(nx) for j in range(ny))

    Ixy     = Hx + Hy - Hxy
    Hx_dado_y = Hxy - Hy   # H(X|Y)
    Hy_dado_x = Hxy - Hx   # H(Y|X)

    # ── Imprimir tabla conjunta ──
    print()
    print(SEP)
    print("  TABLA DE PROBABILIDADES CONJUNTAS  p(x, y)")
    print(SEP)

    col_w = 12
    header = f"  {'X \\ Y':<12}" + "".join(f"{y:>{col_w}}" for y in ny_names) + f"  {'P(X)':>{col_w}}"
    print(header)
    print("  " + "─" * (12 + col_w * (ny + 1) + 2))

    for i in range(nx):
        fila = f"  {nx_names[i]:<12}" + "".join(f"{tabla[i][j]:>{col_w}.6f}" for j in range(ny))
        fila += f"  {px[i]:>{col_w}.6f}"
        print(fila)

    print("  " + "─" * (12 + col_w * (ny + 1) + 2))
    py_row = f"  {'P(Y)':<12}" + "".join(f"{py[j]:>{col_w}.6f}" for j in range(ny))
    py_row += f"  {sum(px):>{col_w}.6f}"
    print(py_row)

    # ── Marginales ──
    print()
    print(sep)
    print("  DISTRIBUCIONES MARGINALES")
    print(sep)
    print(f"\n  P(X):  " + "  ".join(f"{nx_names[i]}={px[i]:.4f}" for i in range(nx)))
    print(f"  P(Y):  " + "  ".join(f"{ny_names[j]}={py[j]:.4f}" for j in range(ny)))

    # ── Resultados ──
    print()
    print(SEP)
    print("  RESULTADOS")
    print(SEP)
    print()
    print(f"  {'Entropía de X':<30}  H(X)   = {Hx:.6f}  {unidad}")
    print(f"  {'Entropía de Y':<30}  H(Y)   = {Hy:.6f}  {unidad}")
    print(f"  {'Entropía conjunta':<30}  H(X,Y) = {Hxy:.6f}  {unidad}")
    print()
    print(f"  {'H(X|Y) — Equivocación':<30}         = {Hx_dado_y:.6f}  {unidad}")
    print(f"  {'H(Y|X) — Ruido':<30}         = {Hy_dado_x:.6f}  {unidad}")
    print()
    print(f"  {'─'*58}")
    print(f"  INFORMACIÓN MUTUA  I(X;Y) = H(X) + H(Y) − H(X,Y)")
    print(f"  I(X;Y) = {Hx:.6f} + {Hy:.6f} − {Hxy:.6f}")
    print(f"  {'─'*58}")
    print(f"  ▶  I(X;Y) = {Ixy:.6f}  {unidad}")
    print(f"  {'─'*58}")
    print()

    # Diagnóstico
    if abs(Ixy) < 1e-9:
        print("  ℹ  I(X;Y) ≈ 0 → X e Y son estadísticamente INDEPENDIENTES.")
    elif abs(Ixy - Hx) < 1e-9:
        print("  ℹ  I(X;Y) = H(X) → Y determina X completamente (canal sin ruido).")
    else:
        red_x = (Ixy / Hx * 100) if Hx > 0 else 0
        red_y = (Ixy / Hy * 100) if Hy > 0 else 0
        print(f"  ℹ  Conocer Y reduce la incertidumbre de X en {red_x:.1f}%.")
        print(f"  ℹ  Conocer X reduce la incertidumbre de Y en {red_y:.1f}%.")

    print()
    return Hx, Hy, Hxy, Ixy, Hx_dado_y, Hy_dado_x, px, py


# ──────────────────────────────────────────────
#  GUARDAR RESULTADOS
# ──────────────────────────────────────────────
def guardar(nx_names, ny_names, tabla, px, py, Hx, Hy, Hxy, Ixy, Hx_dado_y, Hy_dado_x, nombre_log, unidad):
    nombre = input("  Nombre del archivo de salida (sin extensión, Enter para omitir): ").strip()
    if not nombre:
        print("  (No se guardó ningún archivo)\n")
        return

    ruta = nombre + "_infomutua.txt"
    nx = len(nx_names)
    ny = len(ny_names)

    with open(ruta, "w", encoding="utf-8") as f:
        f.write("RESULTADOS — INFORMACIÓN MUTUA I(X;Y)\n")
        f.write(f"Base logarítmica: {nombre_log} | Unidades: {unidad}\n")
        f.write("═" * 60 + "\n\n")
        f.write("Tabla conjunta p(x,y):\n")
        f.write(f"{'X/Y':<12}" + "".join(f"{y:>12}" for y in ny_names) + f"  {'P(X)':>12}\n")
        f.write("─" * 60 + "\n")
        for i in range(nx):
            f.write(f"{nx_names[i]:<12}" + "".join(f"{tabla[i][j]:>12.6f}" for j in range(ny)) + f"  {px[i]:>12.6f}\n")
        f.write("─" * 60 + "\n")
        f.write(f"{'P(Y)':<12}" + "".join(f"{py[j]:>12.6f}" for j in range(ny)) + "\n\n")
        f.write(f"H(X)         = {Hx:.6f}  {unidad}\n")
        f.write(f"H(Y)         = {Hy:.6f}  {unidad}\n")
        f.write(f"H(X,Y)       = {Hxy:.6f}  {unidad}\n")
        f.write(f"H(X|Y)       = {Hx_dado_y:.6f}  {unidad}\n")
        f.write(f"H(Y|X)       = {Hy_dado_x:.6f}  {unidad}\n")
        f.write(f"I(X;Y)       = {Ixy:.6f}  {unidad}\n")

    print(f"  ✔  Resultados guardados en '{ruta}'\n")


# ──────────────────────────────────────────────
#  PROGRAMA PRINCIPAL
# ──────────────────────────────────────────────
def main():
    limpiar()
    banner()

    if len(sys.argv) > 1:
        ruta = sys.argv[1]
        print(f"  Modo: archivo → '{ruta}'\n")
        nx_names, ny_names, tabla = leer_archivo(ruta)
    else:
        print("  Modo: entrada manual\n")
        print("  ¿Cómo deseas ingresar los datos?\n")
        print("    [1]  Distribución conjunta completa p(x,y)  ← recomendado")
        print("    [2]  Distribuciones marginales P(X) y P(Y) por separado")
        print()
        opc = input("  Opción [1/2] (Enter = 1): ").strip() or "1"
        if opc == "2":
            nx_names, ny_names, tabla = manual_marginales()
        else:
            nx_names, ny_names, tabla = manual_conjunta()

    # Validar suma total
    total = sum(tabla[i][j] for i in range(len(nx_names)) for j in range(len(ny_names)))
    print(f"\n  Verificación: Σ p(x,y) = {total:.6f}")
    if abs(total - 1.0) > 0.01:
        print(f"  ⚠  La suma es {total:.4f}. Normalizando automáticamente...")
        tabla = [[tabla[i][j] / total for j in range(len(ny_names))] for i in range(len(nx_names))]
    else:
        print("  ✔  Suma válida.\n")

    # Base
    nombre_log, fn_log, unidad = elegir_base()

    # Calcular
    Hx, Hy, Hxy, Ixy, Hx_dado_y, Hy_dado_x, px, py = calcular_info_mutua(
        nx_names, ny_names, tabla, fn_log, nombre_log, unidad
    )

    # Guardar
    print(sep)
    guardar(nx_names, ny_names, tabla, px, py, Hx, Hy, Hxy, Ixy,
            Hx_dado_y, Hy_dado_x, nombre_log, unidad)

    input("  Presiona Enter para salir...")


if __name__ == "__main__":
    main()
