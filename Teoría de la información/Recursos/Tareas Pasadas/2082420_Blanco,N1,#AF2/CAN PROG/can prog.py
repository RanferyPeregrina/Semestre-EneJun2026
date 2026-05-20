import random

def text_to_bits(text, encoding='utf-8'):
    """Convierte un string de texto a una cadena de bits (0s y 1s)."""
    bits = bin(int.from_bytes(text.encode(encoding), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bits_to_text(bits, encoding='utf-8'):
    """Convierte una cadena de bits de vuelta a texto."""
    n = int(bits, 2)
    try:
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding) or '\0'
    except UnicodeDecodeError:
        # Si el ruido corrompió un byte de forma que no es válido en utf-8
        return "[Error de Decodificación]"

def binary_symmetric_channel(bits, p):
    """
    Simula un Canal Binario Simétrico (BSC).
    bits: cadena de entrada de 0s y 1s.
    p: probabilidad de error (probabilidad de que un bit se invierta).
    """
    output_bits = ""
    error_count = 0
    
    for bit in bits:
        if random.random() < p:
            # Ocurre un error: se invierte el bit
            output_bits += '1' if bit == '0' else '0'
            error_count += 1
        else:
            # El bit pasa sin cambios
            output_bits += bit
            
    return output_bits, error_count

def main():
    # --- PARÁMETROS DE LA SIMULACIÓN ---
    mensaje_original = "INFORMACION"
    probabilidad_error = 0.05  # 5% de probabilidad de que un bit falle
    
    print(f"--- SIMULACIÓN CAN PROG (Canal Binario Simétrico) ---")
    print(f"Mensaje original: {mensaje_original}")
    print(f"Probabilidad de error (p): {probabilidad_error}")
    
    # 1. Codificación de Fuente (Texto -> Bits)
    bits_entrada = text_to_bits(mensaje_original)
    print(f"\nBits enviados ({len(bits_entrada)} bits):")
    print(bits_entrada)
    
    # 2. Transmisión por el Canal Ruidoso
    bits_salida, errores = binary_symmetric_channel(bits_entrada, probabilidad_error)
    
    print(f"\nBits recibidos:")
    print(bits_salida)
    
    # 3. Decodificación de Destino (Bits -> Texto)
    mensaje_recibido = bits_to_text(bits_salida)
    
    # 4. Reporte de Resultados
    print(f"\n--- RESULTADOS ---")
    print(f"Mensaje reconstruido: {mensaje_recibido}")
    print(f"Bits erróneos totales: {errores}")
    print(f"Tasa de error real: {errores / len(bits_entrada):.4f}")

if __name__ == "__main__":
    main()