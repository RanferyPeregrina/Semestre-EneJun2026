# -*- coding: utf-8 -*-
import random
import os

def generar_archivo_tarea():
    alfabeto = list("TosinhepärjälvuMyNk?JmPOdöSbLEV\n")
    # Definimos la ruta de destino
    ruta_destino = r"A:\Archivos\Respaldo"
    
    try:
        # Verificar si la carpeta existe, si no, intentar crearla
        if not os.path.exists(ruta_destino):
            os.makedirs(ruta_destino)

        entrada = input("Introduce tu matrícula (ej. 1234567): ")
        matricula = int(entrada)
        
        random.seed(matricula)
        longitud = matricula
        
        # Generar el contenido
        resultado = "".join(random.choice(alfabeto) for _ in range(longitud))
        
        # Construir la ruta completa del archivo
        nombre_archivo = f"resultado_{matricula}.txt"
        ruta_completa = os.path.join(ruta_destino, nombre_archivo)
        
        with open(ruta_completa, "w", encoding="utf-8") as archivo:
            archivo.write(resultado)
            
        print("-" * 50)
        print(f"¡Éxito! Se han generado {longitud} caracteres.")
        print(f"Archivo guardado en: {ruta_completa}")
        print("-" * 50)
        
    except ValueError:
        print("Error: La matrícula debe ser un número entero.")
    except PermissionError:
        print(f"Error de permisos: No se pudo escribir en {ruta_destino}. Verifica que la unidad A: esté conectada y no sea de solo lectura.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    generar_archivo_tarea()

input("\nPresiona Enter para salir...")