import os
from tkinter import Tk, filedialog

# =========================
# LECTOR DE FASTA / FNA
# =========================
def read_fasta(filepath):
    """
    Lee archivos .fasta, .fa, .fna o .txt.
    Ignora la primera línea (>) y concatena el ADN.
    """
    sequence = []
    with open(filepath, 'r') as file:
        for line in file:
            if not line.startswith(">"):
                # Limpiamos saltos de línea y pasamos a mayúsculas
                sequence.append(line.strip().upper())
    
    # Unimos todo y agregamos el símbolo centinela '$' al final del texto
    return "".join(sequence) + "$" 


# =========================
# EL CORAZÓN DE CAPS-SA (Merge informado por LCP)
# =========================
# Aquí es donde realmente debes aplicar la lógica del artículo.
# Esta función debe reemplazar al "sorted()" nativo de Python.
def merge_con_lcp(text, izq, der):
    """
    FUSIONA dos listas de sufijos ya ordenadas (izq y der).
    Aquí es donde debes programar los Casos 1, 2 y 3 del artículo 
    (comparando l_x y m) para evitar comparar letras repetidas.
    """
    resultado = []
    i, j = 0, 0
    
    # Lógica base de un Merge tradicional (Falta inyectar la optimización LCP aquí)
    while i < len(izq) and j < len(der):
        # NOTA: text[izq[i]:] hace copias de strings, lo cual es lento. 
        # En la versión final, deberás comparar índices letra por letra usando la optimización LCP.
        if text[izq[i]:] < text[der[j]:]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
            
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    
    return resultado

def merge_sort_sufijos(text, indices):
    """
    Divide recursivamente el arreglo de sufijos (Paso 1 del artículo).
    """
    if len(indices) <= 1:
        return indices
    
    medio = len(indices) // 2
    izq = merge_sort_sufijos(text, indices[:medio])
    der = merge_sort_sufijos(text, indices[medio:])
    
    return merge_con_lcp(text, izq, der)


# =========================
# EXPORTACIÓN DE DATOS
# =========================
def guardar_resultados(text, sa, lcp_arr):
    """Guarda los resultados en disco en lugar de saturar la consola."""
    output_dir = r"A:\Archivos\Respaldo"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "salmonella_output.txt")
    
    print(f"\nGuardando resultados en: {output_path}...")
    with open(output_path, 'w') as f:
        f.write("SA_Index\tLCP\tSufijo_Parcial\n")
        # Guardamos solo una muestra para no crear un archivo de 50GB
        for i in range(min(1000, len(sa))):
            sufijo = text[sa[i]:sa[i]+30]
            lcp_val = lcp_arr[i] if i < len(lcp_arr) else 0
            f.write(f"{sa[i]}\t{lcp_val}\t{sufijo}...\n")
            
    print("¡Archivo guardado con éxito!")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    root = Tk()
    root.withdraw() 
    filepath = filedialog.askopenfilename(
        title="Selecciona tu secuencia",
        # ¡Añadido soporte para .fna!
        filetypes=[("Secuencias de ADN", "*.fasta *.fa *.fna *.txt")] 
    )

    if not filepath:
        print("Operación cancelada.")
        exit()

    print(f"\nProcesando: {filepath}")
    text = read_fasta(filepath)
    print(f"Longitud total (con centinela): {len(text)} bases")

    print("\nIniciando ordenamiento por mezcla (Merge-Sort base)...")
    indices_iniciales = list(range(len(text)))
    
    # Llamamos a nuestro algoritmo en lugar del de Python
    sa = merge_sort_sufijos(text, indices_iniciales)

    # Nota: Por ahora mantenemos tu función LCP original para que corra, 
    # pero el objetivo final es que esta info salga directamente de merge_con_lcp().
    # lcp_arr = build_lcp_array(text, sa) 
    lcp_arr = [0] * len(sa) # Placeholder rápido

    guardar_resultados(text, sa, lcp_arr)