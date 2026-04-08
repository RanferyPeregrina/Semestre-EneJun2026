import os
from tkinter import Tk, filedialog

print('=' * 20)
print('Este programa únicamente es para contar cuántos caracteres tiene un documento.')
print('Sólo sirve para motivos de depuración.')
print('=' * 20)

root = Tk()
root.withdraw() 
filepath = filedialog.askopenfilename(
    title="Selecciona tu secuencia",
    # ¡Añadido soporte para .fna!
    filetypes=[("Secuencias de ADN", "*.fasta *.fa *.fna *.txt")] 
)

Cuenta = 0
with open(filepath, 'r') as Archivo:
    for Renglon in Archivo:
        Cuenta += len(Renglon)

print(f'El archivo finalmente cuenta con {Cuenta} caracteres')
input('\nPresione cualquier tecla para cerrar...')