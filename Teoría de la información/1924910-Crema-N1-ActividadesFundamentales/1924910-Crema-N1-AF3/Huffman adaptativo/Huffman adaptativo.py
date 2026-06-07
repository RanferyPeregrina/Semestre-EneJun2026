import sys

# --- CLASE LOGGER: Para guardar consola en archivo de texto ---
class Logger(object):
    def __init__(self, filename="resultado_huffman_adaptativo.txt"):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        self.terminal.flush()
        self.log.flush()

sys.stdout = Logger()

# --- ESTRUCTURA DEL ÁRBOL HUFFMAN ADAPTATIVO ---

class Node:
    def __init__(self, symbol=None, weight=0, order=0, parent=None):
        self.symbol = symbol  # None para nodos internos, carácter para hojas
        self.weight = weight
        self.order = order    # Número de orden para mantener la propiedad de Huffman
        self.parent = parent
        self.left = None
        self.right = None
        self.is_nyt = False   # Flag para el nodo NYT (Not Yet Transmitted)

class AdaptiveHuffmanTree:
    def __init__(self):
        # Inicializamos con el nodo NYT (Not Yet Transmitted)
        self.nyt = Node(weight=0, order=512)
        self.nyt.is_nyt = True
        self.root = self.nyt
        self.nodes = [self.nyt]  # Lista de todos los nodos para búsquedas rápidas
        self.seen_symbols = {}   # Mapa de símbolo -> Nodo hoja

    def get_code(self, char):
        """Obtiene el camino binario actual para un carácter."""
        if char in self.seen_symbols:
            node = self.seen_symbols[char]
            return self._build_path(node)
        else:
            # Si es nuevo, retorna camino al NYT + código fijo (simulado)
            return self._build_path(self.nyt) + f" [ASC:{ord(char)}]"

    def _build_path(self, node):
        path = ""
        curr = node
        while curr.parent:
            if curr.parent.left == curr:
                path = "0" + path
            else:
                path = "1" + path
            curr = curr.parent
        return path

    def update(self, char):
        """
        Algoritmo de actualización del Huffman Adaptativo:
        1. Si es nuevo: divide NYT.
        2. Si existe: va al nodo correspondiente.
        3. Incrementa pesos y reordena (swaps) hasta la raíz.
        """
        if char not in self.seen_symbols:
            # === PASO 1: Procesar Símbolo Nuevo ===
            old_nyt = self.nyt
            
            # Crear nuevo nodo NYT y nuevo nodo Hoja
            new_nyt = Node(weight=0, parent=old_nyt)
            new_nyt.is_nyt = True
            
            new_symbol_node = Node(symbol=char, weight=1, parent=old_nyt)
            
            old_nyt.is_nyt = False
            old_nyt.left = new_nyt
            old_nyt.right = new_symbol_node
            
            # Actualizar referencias
            self.nyt = new_nyt
            self.seen_symbols[char] = new_symbol_node
            
            # Agregar a la lista de nodos
            self.nodes.append(new_nyt)
            self.nodes.append(new_symbol_node)
            
            # El nodo a incrementar es el padre (old_nyt) que ahora tiene peso 1
            curr = old_nyt
            curr.weight += 1
            curr = curr.parent
        else:
            # === PASO 1 Alternativo: Símbolo Existente ===
            curr = self.seen_symbols[char]

        # === PASO 2: Incrementar y Reordenar ===
        while curr:
            # Encontrar el nodo con el mayor 'order' en el bloque del mismo peso
            leader = self._find_block_leader(curr)
            
            if leader and leader != curr and leader != curr.parent:
                print(f"    [INTERCAMBIO] Intercambiando nodo '{self._n_str(curr)}' con '{self._n_str(leader)}' (Peso {curr.weight})")
                self._swap_nodes(curr, leader)
            
            # Incrementar peso
            curr.weight += 1
            curr = curr.parent
        
        # Recalcular órdenes
        self._assign_orders()

    def _find_block_leader(self, node):
        """Busca el nodo con mayor orden que tenga el mismo peso que 'node'."""
        best_node = None
        max_order = -1
        
        # Filtramos nodos con mismo peso
        candidates = [n for n in self.nodes if n.weight == node.weight and n != node]
        
        for cand in candidates:
            # No podemos intercambiar con un ancestro directo
            if cand == node.parent: 
                continue
            
            if cand.order > max_order:
                max_order = cand.order
                best_node = cand
        
        # Solo retornamos líder si su orden es mayor al del nodo actual
        if best_node and best_node.order > node.order:
            return best_node
        return None

    def _swap_nodes(self, node_a, node_b):
        """Intercambia la posición de dos nodos en el árbol (mantiene sus subárboles)."""
        # Intercambiar órdenes
        node_a.order, node_b.order = node_b.order, node_a.order
        
        pa, pb = node_a.parent, node_b.parent
        
        if pa == pb:  # Mismo padre
            pa.left, pa.right = pa.right, pa.left
        else:
            if pa.left == node_a:
                pa.left = node_b
            else:
                pa.right = node_b
            
            if pb.left == node_b:
                pb.left = node_a
            else:
                pb.right = node_a
            
            node_a.parent = pb
            node_b.parent = pa

    def _n_str(self, node):
        """String helper para debug."""
        if node.is_nyt:
            return "NYT"
        if node.symbol:
            return f"'{node.symbol}'"
        return f"Int(w={node.weight})"

    def _assign_orders(self):
        """Reasigna números de orden recorriendo el árbol de derecha a izquierda."""
        self.counter = len(self.nodes) + 500
        q = [self.root]
        ordered_list = []
        while q:
            n = q.pop(0)
            ordered_list.append(n)
            # Prioridad derecha luego izquierda
            if n.right:
                q.append(n.right)
            if n.left:
                q.append(n.left)
        
        for node in ordered_list:
            node.order = self.counter
            self.counter -= 1

# --- VISUALIZACIÓN ASCII ---

class AsciiTreePrinter:
    """Clase para dibujar árboles binarios en ASCII"""
    
    @staticmethod
    def print_tree(root, title="Árbol Huffman Adaptativo"):
        """Dibuja el árbol en formato ASCII"""
        print(f"\n{'='*60}")
        print(f"{title}")
        print(f"{'='*60}\n")
        
        if not root:
            print("Árbol vacío")
            return
        
        lines = AsciiTreePrinter._build_tree_string(root)
        for line in lines:
            print(line)
        print(f"\n{'='*60}\n")
    
    @staticmethod
    def _get_node_label(node):
        """Obtiene la etiqueta del nodo"""
        if node.is_nyt:
            return f"NYT({node.weight})"
        elif node.symbol:
            return f"'{node.symbol}'({node.weight})"
        else:
            return f"({node.weight})"
    
    @staticmethod
    def _build_tree_string(node, prefix="", is_left=True):
        """Construye las líneas del árbol ASCII"""
        if not node:
            return []
        
        label = AsciiTreePrinter._get_node_label(node)
        lines = []
        
        # Procesar hijo derecho
        if node.right:
            right_lines = AsciiTreePrinter._build_tree_string(
                node.right, prefix + ("│   " if is_left else "    "), False
            )
            lines.extend(right_lines)
        
        # Nodo actual
        current = prefix + ("└── " if is_left else "┌── ") + label
        lines.append(current)
        
        # Procesar hijo izquierdo
        if node.left:
            left_lines = AsciiTreePrinter._build_tree_string(
                node.left, prefix + ("    " if is_left else "│   "), True
            )
            lines.extend(left_lines)
        
        return lines

# --- EJECUCIÓN PRINCIPAL ---

def run_adaptive_huffman_simulation(sample):
    print("=== Simulación de Huffman Adaptativo ===")
    print(f"Muestra de entrada: \"{sample}\"\n")
    
    tree = AdaptiveHuffmanTree()
    
    encoded_stream = []
    
    # Mostrar árbol inicial
    print("--- Estado inicial del árbol ---")
    AsciiTreePrinter.print_tree(tree.root, "Árbol Inicial")
    
    for i, char in enumerate(sample):
        print(f"\n{'='*40}")
        print(f"--- Paso {i+1}: Procesando '{char}' ---")
        print(f"{'='*40}")
        
        # Obtener código antes de actualizar
        code = tree.get_code(char)
        encoded_stream.append(code)
        print(f"\n Transmite: {code}")
        
        # Actualizar árbol
        tree.update(char)
        
        # Mostrar árbol actualizado
        print(f"\n Árbol actualizado (Raíz peso: {tree.root.weight}):")
        AsciiTreePrinter.print_tree(tree.root)
    
    print("\n" + "="*60)
    print("=== Resultados Finales ===")
    print("="*60)
    print(f"Secuencia de códigos transmitidos:")
    print(" → ".join(encoded_stream))
    print(f"\nLongitud total de la muestra: {len(sample)} caracteres")
    print(f"Número de códigos generados: {len(encoded_stream)}")
    
    # Mostrar árbol final detallado
    print("\n--- Árbol Final ---")
    AsciiTreePrinter.print_tree(tree.root, "Árbol Huffman Adaptativo Final")
    
    # Mostrar tabla de símbolos
    print("\n--- Tabla de Símbolos ---")
    print(f"{'Símbolo':<10} {'Tipo':<10} {'Código Actual':<15} {'Peso':<5}")
    print("-" * 45)
    for symbol, node in sorted(tree.seen_symbols.items()):
        code = tree.get_code(symbol)
        print(f"{repr(symbol):<10} {'Hoja':<10} {code:<15} {node.weight:<5}")
    if tree.nyt:
        print(f"{'NYT':<10} {'Especial':<10} {'N/A':<15} {tree.nyt.weight:<5}")
    
    print("\n[INFO] Registro guardado en 'resultado_huffman_adaptativo.txt'")

if __name__ == "__main__":
    sample_text = "c8c426ed"
    run_adaptive_huffman_simulation(sample_text)