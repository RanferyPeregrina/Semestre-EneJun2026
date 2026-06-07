class SuffixTreeNode:
    def __init__(self, start, end):
        self.children = {}
        self.start = start
        self.end = end
        self.suffix_link = None
        self.leaf = False


class SuffixTree:
    def __init__(self, text, verbose=True):
        self.verbose = verbose
        self.text = self.preprocess_text(text) + "$"
        self.root = SuffixTreeNode(-1, -1)
        self.root.suffix_link = self.root
        self.all_trees = []
        self.build_ukkonen()
        
        if self.verbose:
            print("\n" + "="*70)
            print("RESUMEN: Se construyeron", len(self.all_trees), "arboles")
            print("="*70)

    def preprocess_text(self, text):
        """Convierte a mayusculas y elimina espacios"""
        processed = text.upper().replace(" ", "")
        return processed

    def get_edge_label(self, start, end):
        """Obtiene la etiqueta de una arista"""
        if end >= len(self.text):
            end = len(self.text) - 1
        if start > end:
            return ""
        return self.text[start:end + 1]

    def tree_to_string(self, node=None, prefix="", is_last=True):
        """Convierte el arbol a una representacion string"""
        if node is None:
            node = self.root
        
        result = []
        
        sorted_children = sorted(node.children.items())
        
        for i, (char, child) in enumerate(sorted_children):
            is_last_child = (i == len(sorted_children) - 1)
            
            label = self.get_edge_label(child.start, child.end)
            
            connector = "└── " if is_last_child else "├── "
            
            leaf_marker = " [LEAF]" if child.leaf else ""
            
            result.append(f"{prefix}{connector}'{char}' -> '{label}'{leaf_marker}")
            
            extension = "    " if is_last_child else "│   "
            result.extend(self.tree_to_string(child, prefix + extension, is_last_child))
        
        return result

    def print_tree(self, phase_num, stage_num, active_info=""):
        """Imprime el arbol en un formato bonito"""
        if not self.verbose:
            return
            
        print("\n" + "="*70)
        print(f"ARBOL EN FASE {phase_num}, STAGE {stage_num}")
        if active_info:
            print(f"({active_info})")
        print("-"*70)
        
        tree_str = self.tree_to_string(self.root)
        if not tree_str:
            print("[Arbol vacio]")
        else:
            print("\n".join(tree_str))
        print("="*70)

    def build_ukkonen(self):
        """Construye el arbol de sufijos usando Ukkonen"""
        n = len(self.text)
        self.root = SuffixTreeNode(-1, -1)
        self.root.suffix_link = self.root

        active_node = self.root
        active_edge = -1
        active_length = 0
        remainder = 0
        last_created_node = None
        
        print(f"\nTEXTO PROCESADO: '{self.text}' (sin espacios, mayusculas)")
        print(f"LONGITUD: {n} caracteres")
        print("\nINICIANDO CONSTRUCCION DEL ARBOL DE SUFIJOS...")

        for i in range(n):
            print(f"\n{'─'*70}")
            print(f"FASE {i}: Insertando caracter '{self.text[i]}' (posicion {i})")
            print(f"{'─'*70}")
            
            last_created_node = None
            remainder += 1
            
            print(f"  remainder = {remainder}")
            print(f"  active_node = {self._node_info(active_node)}")
            print(f"  active_length = {active_length}")
            print(f"  active_edge = {active_edge}")

            step = 1
            while remainder > 0:
                print(f"\n  PASO {step} (remainder={remainder})")
                
                if active_length == 0:
                    active_edge = i
                    print(f"    active_length=0 -> active_edge ahora es {active_edge} ('{self.text[active_edge]}')")

                current_char = self.text[active_edge]
                next_char = self.text[i]
                
                print(f"    current_char = '{current_char}'")
                print(f"    next_char = '{next_char}'")

                if current_char not in active_node.children:
                    print(f"    REGLA 2: '{current_char}' no existe, creando nueva hoja")
                    leaf = SuffixTreeNode(i, n - 1)
                    leaf.leaf = True
                    active_node.children[current_char] = leaf
                    print(f"    -> Nueva arista: '{current_char}' -> '{self.get_edge_label(i, n-1)}' [LEAF]")

                    if last_created_node is not None:
                        last_created_node.suffix_link = active_node
                        print(f"    -> Sufijo link: nodo anterior -> nodo actual")
                        last_created_node = None

                else:
                    next_node = active_node.children[current_char]
                    edge_length = next_node.end - next_node.start + 1
                    
                    print(f"    '{current_char}' ya existe, investigando...")
                    print(f"    nodo hijo: start={next_node.start}, end={next_node.end}, longitud_arista={edge_length}")

                    if active_length >= edge_length:
                        print(f"    active_length({active_length}) >= edge_length({edge_length}) -> saltando al hijo")
                        active_node = next_node
                        active_length -= edge_length
                        active_edge += edge_length
                        print(f"    active_node actualizado, active_length={active_length}, active_edge={active_edge}")
                        continue

                    check_pos = next_node.start + active_length
                    if check_pos < len(self.text):
                        char_at_check = self.text[check_pos]
                        print(f"    Comparando: self.text[{check_pos}] = '{char_at_check}' con next_char='{next_char}'")
                        
                        if char_at_check == next_char:
                            active_length += 1
                            print(f"    REGLA 3: Caracteres coinciden, active_length++ -> {active_length}")

                            if last_created_node is not None:
                                last_created_node.suffix_link = active_node
                                print(f"    -> Sufijo link actualizado")
                                last_created_node = None
                            break

                    print(f"    REGLA 2 (division): Creando nodo interno en posicion {active_length}")
                    split_node = SuffixTreeNode(next_node.start, next_node.start + active_length - 1)
                    active_node.children[current_char] = split_node
                    split_label = self.get_edge_label(split_node.start, split_node.end)
                    print(f"    -> Nueva arista dividida: '{current_char}' -> '{split_label}'")

                    leaf = SuffixTreeNode(i, n - 1)
                    leaf.leaf = True
                    split_node.children[next_char] = leaf
                    print(f"    -> Nueva hoja: '{next_char}' -> '{self.get_edge_label(i, n-1)}' [LEAF]")

                    next_node.start += active_length
                    split_node.children[self.text[next_node.start]] = next_node
                    print(f"    -> Resto de la arista original: '{self.text[next_node.start]}' -> '{self.get_edge_label(next_node.start, next_node.end)}'")

                    if last_created_node is not None:
                        last_created_node.suffix_link = split_node
                        print(f"    -> Sufijo link actualizado")

                    last_created_node = split_node

                remainder -= 1
                print(f"    remainder despues de procesar = {remainder}")

                if active_node == self.root and active_length > 0:
                    active_length -= 1
                    active_edge = i - remainder + 1
                    print(f"    Desde root: active_length-- -> {active_length}, active_edge={active_edge}")
                elif active_node != self.root:
                    if active_node.suffix_link is not None:
                        old_node = active_node
                        active_node = active_node.suffix_link
                        print(f"    Siguiendo suffix link: nodo {self._node_info(old_node)} -> {self._node_info(active_node)}")
                    else:
                        active_node = self.root
                        print(f"    Volviendo a la raiz (sin suffix link)")
                else:
                    active_node = self.root
                    print(f"    active_node es la raiz")
                
                step += 1
                
                if remainder == 0:
                    self.all_trees.append({
                        'phase': i,
                        'tree': self._copy_tree_state(),
                        'active_info': f"active_node={self._node_info(active_node)}, active_length={active_length}, active_edge={active_edge}"
                    })
                    self.print_tree(i, i, f"active_node={self._node_info(active_node)}, active_length={active_length}")
            
            print(f"\n  FASE {i} COMPLETADA")
        
        self.all_trees.append({
            'phase': n,
            'tree': self._copy_tree_state(),
            'active_info': "ARBOL FINAL"
        })
        self.print_tree(n, n, "ARBOL FINAL CON $")

    def _node_info(self, node):
        """Devuelve informacion legible del nodo"""
        if node == self.root:
            return "raiz"
        return f"nodo({hex(id(node))[-4:]})"
    
    def _copy_tree_state(self):
        """Copia el estado actual del arbol para visualizacion"""
        return self.tree_to_string(self.root)

    def show_all_trees(self):
        """Muestra todos los arboles intermedios construidos"""
        if not self.verbose:
            print("El modo verbose esta desactivado. No hay arboles guardados.")
            return
        
        print("\n" + "="*70)
        print("TODOS LOS ARBOLES CONSTRUIDOS DURANTE EL ALGORITMO")
        print("="*70)
        
        for i, tree_info in enumerate(self.all_trees):
            print(f"\n{'='*70}")
            print(f"ARBOL #{i+1} - FASE {tree_info['phase']}")
            print(f"{tree_info['active_info']}")
            print(f"{'-'*70}")
            if tree_info['tree']:
                print("\n".join(tree_info['tree']))
            else:
                print("[Arbol vacio]")
        
        print(f"\n{'='*70}")
        print(f"TOTAL: {len(self.all_trees)} arboles construidos")
        print(f"{'='*70}")

    def find_longest_common_substring(self, pattern):
        """Encuentra la subcadena comun mas larga entre el texto y el patron"""
        pattern = self.preprocess_text(pattern)
        longest = ""
        current = ""

        def dfs(node, depth):
            nonlocal longest, current
            for char, child in sorted(node.children.items()):
                edge_label = self.get_edge_label(child.start, child.end)
                temp_current = current + edge_label

                if temp_current in pattern:
                    if len(temp_current) > len(longest):
                        longest = temp_current
                    dfs(child, depth + 1)

        dfs(self.root, 0)
        return longest


if __name__ == "__main__":
    print("="*70)
    print("CONSTRUCTOR DE ARBOL DE SUFIJOS - ALGORITMO DE UKKONEN")
    print("="*70)
    
    texto = input("\nIngrese el texto: ")
    
    print("\n" + "-"*70)
    print("CONSTRUYENDO ARBOL...")
    print("-"*70)
    
    st = SuffixTree(texto, verbose=True)
    
    print("\n" + "="*70)
    print("MOSTRANDO TODOS LOS ARBOLES CONSTRUIDOS")
    print("="*70)
    st.show_all_trees()
    
    print("\n" + "="*70)
    print("BUSQUEDA DE SUBCADENA COMUN")
    print("="*70)
    
    patron = input("\nIngrese el patron para buscar subcadena comun: ")
    
    if patron.strip():
        resultado = st.find_longest_common_substring(patron)
        print(f"\nSubcadena comun mas larga: '{resultado}'")
        print(f"Longitud: {len(resultado)}")
    else:
        print("\nNo se ingreso ningun patron.")