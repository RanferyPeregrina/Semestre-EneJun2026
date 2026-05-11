from tkinter import Tk, filedialog
from tkinter.filedialog import askopenfilename
import sys


class Tee:#Esto es para que las cosas se guarden en un TXT al final jeje.
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()  # Para que se guarde al momento
    def flush(self):
        for f in self.files:
            f.flush()
log_file = open("Salida.txt", "w", encoding="utf-8")
original_stdout = sys.stdout
sys.stdout = Tee(sys.stdout, log_file)

def LeerTexto():
    root = Tk()
    root.withdraw()
    Archivo = askopenfilename(title = "Elige el archivo de texto")
    if Archivo:
        with open(Archivo, "r", encoding="utf-8") as Archivo:
            Texto = Archivo.read()
    return Texto
# Esto lo voy a copiar y pegar en todos los programas. 🦀, hasta aquí -----------------------------


# ---------- Funciones de preprocesamiento de Boyer‑Moore ----------
def build_bad_char_table(pattern):
    """Tabla de último carácter (bad character rule)"""
    m = len(pattern)
    table = {}
    # Para cada carácter en el patrón, guardamos su índice más a la derecha
    for i, ch in enumerate(pattern):
        table[ch] = i
    return table

def build_good_suffix_table(pattern):
    """
    Construye la tabla de desplazamiento por buen sufijo (strong good suffix rule).
    Devuelve una lista `shift` de longitud m (número de desplazamiento para cada posición de fallo).
    """
    m = len(pattern)
    # 1. Calcular el array "suffix" : para cada i, la longitud del sufijo más largo de pattern[0..i]
    #    que también es sufijo de todo el patrón.
    suffix = [0] * m
    # 2. Calcular el array "border" para el buen sufijo.
    #    Usamos el algoritmo clásico de preprocesamiento de Boyer‑Moore.
    #    Primero, llenamos `suffix` usando el enfoque de "prefijo-sufijo"
    #    Implementación estándar:
    suffix[m-1] = m
    g = m-1
    f = m-1
    for i in range(m-2, -1, -1):
        if i > g and suffix[i + m - 1 - f] < i - g:
            suffix[i] = suffix[i + m - 1 - f]
        else:
            if i < g:
                g = i
            f = i
            while g >= 0 and pattern[g] == pattern[g + m - 1 - f]:
                g -= 1
            suffix[i] = f - g
    # 3. Construir la tabla `good_suffix_shift` inicializada con m
    good_suffix_shift = [m] * m
    # Caso 1: el sufijo ya ocurre en otra parte del patrón
    for i in range(m-1):
        good_suffix_shift[m - 1 - suffix[i]] = m - 1 - i
    # Caso 2: un prefijo del patrón es sufijo del texto coincidente
    for i in range(m-1):
        if suffix[i] == i+1:  # el sufijo que empieza en i cubre hasta el inicio
            for j in range(m-1 - i):
                if good_suffix_shift[j] == m:
                    good_suffix_shift[j] = m - 1 - i
    return good_suffix_shift

# ---------- Búsqueda Boyer‑Moore ----------
def boyer_moore_search(text, pattern, verbose=True):
    n = len(text)
    m = len(pattern)
    if m == 0 or n == 0 or m > n:
        return -1

    # Preprocesamiento
    bad_char = build_bad_char_table(pattern)
    good_suffix = build_good_suffix_table(pattern)

    if verbose:
        print("--- Tabla de mal carácter (última ocurrencia) ---")
        for ch, idx in bad_char.items():
            print(f"'{ch}' -> {idx}")
        print("\n--- Tabla de buen sufijo (desplazamiento por posición de fallo) ---")
        for i, sh in enumerate(good_suffix):
            print(f"Posición de fallo {i} (de izquierda): desplazar {sh}")
        print("\n--- Iniciando búsqueda ---\n")

    pos = 0
    comparisons = 0
    while pos <= n - m:
        # Comparar de derecha a izquierda
        j = m - 1
        while j >= 0 and pattern[j] == text[pos + j]:
            comparisons += 1
            j -= 1
        # Si se completó toda la comparación -> coincidencia
        if j < 0:
            if verbose:
                print(f"✓ Coincidencia encontrada en posición {pos}")
            return pos  # Devuelve la primera coincidencia (puedes modificarlo para todas)
        # Fallo en la posición j (desde la izquierda)
        comparisons += 1
        # Regla del mal carácter
        bad_char_shift = j - bad_char.get(text[pos + j], -1)
        if bad_char_shift < 1:
            bad_char_shift = 1
        # Regla del buen sufijo
        good_suffix_shift = good_suffix[j] if j < m else 1
        shift = max(bad_char_shift, good_suffix_shift)

        if verbose:
            print(f"Comparando T[{pos+j}]='{text[pos+j]}' con P[{j}]='{pattern[j]}'")
            print(f"  Desplazamiento por mal carácter: {bad_char_shift}")
            print(f"  Desplazamiento por buen sufijo : {good_suffix_shift}")
            print(f"  → Me muevo {shift} posiciones\n")

        pos += shift

    if verbose:
        print("No se encontró el patrón.")
    return -1

# ---------- Interfaz de usuario ----------
def leer_archivo():
    root = Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(title="Elige el archivo de texto")
    if archivo:
        with open(archivo, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def main():
    print("Algoritmo Boyer-Moore (búsqueda exacta)")
    print("Opciones:")
    print("1. Ingresar texto y patrón por consola")
    print("2. Seleccionar archivo de texto y luego escribir patrón")
    opcion = input("Elige opción (1/2): ").strip()
    if opcion == "2":
        texto = leer_archivo()
        if not texto:
            print("No se seleccionó ningún archivo.")
            return
        patron = input("Ingresa el patrón a buscar: ")
    else:
        texto = input("Texto completo: ")
        patron = input("Patrón a buscar: ")

    if not texto or not patron:
        print("Texto o patrón vacío.")
        return

    print("\n" + "="*60)
    print(f"Texto : {texto}")
    print(f"Patrón: {patron}")
    print("="*60 + "\n")

    pos = boyer_moore_search(texto, patron, verbose=True)
    if pos != -1:
        print(f"\n>>> PATRÓN ENCONTRADO en el índice {pos} <<<")
    else:
        print("\n>>> PATRÓN NO ENCONTRADO <<<")

if __name__ == "__main__":
    main()