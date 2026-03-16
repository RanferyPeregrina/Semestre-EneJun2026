import os
from graphviz import Digraph

ruta_binarios = r"C:\Program Files (x86)\Graphviz\bin"
os.environ["PATH"] += os.pathsep + ruta_binarios


class ArbolSufijosVisual:

    def __init__(self, texto):
        self.texto = texto + "$"
        self.raiz = {"hijos": {}, "id": 0}
        self.contador = 1
        self._construir()

    def _construir(self):
        for i in range(len(self.texto)):
            self._insertar(self.texto[i:], i)

    def _insertar(self, sufijo, indice_orig):
        actual = self.raiz

        while True:

            letra = sufijo[0]

            if letra not in actual["hijos"]:
                actual["hijos"][letra] = [
                    sufijo,
                    {"hijos": {}, "id": self.contador, "idx": indice_orig}
                ]
                self.contador += 1
                break

            etiqueta, hijo = actual["hijos"][letra]

            j = 0
            while j < len(etiqueta) and j < len(sufijo) and etiqueta[j] == sufijo[j]:
                j += 1

            if j == len(etiqueta):

                sufijo = sufijo[j:]
                actual = hijo

            else:

                intermedio = {"hijos": {}, "id": self.contador, "idx": -1}
                self.contador += 1

                resto_viejo = etiqueta[j:]
                intermedio["hijos"][resto_viejo[0]] = [resto_viejo, hijo]

                resto_nuevo = sufijo[j:]
                nueva_hoja = {"hijos": {}, "id": self.contador, "idx": indice_orig}
                self.contador += 1
                intermedio["hijos"][resto_nuevo[0]] = [resto_nuevo, nueva_hoja]

                actual["hijos"][letra] = [etiqueta[:j], intermedio]

                break

    def exportar_imagen(self, nombre_archivo):

        dot = Digraph(
            format='png',
            engine='dot'
        )

        # Configuración para grafos gigantes
        dot.attr(rankdir='LR')
        dot.attr(dpi='300')
        dot.attr(nodesep='0.5')
        dot.attr(ranksep='1')
        dot.attr(size="100,100!")
        dot.attr('node', shape='circle', fontsize='10')

        # Nodo raíz
        dot.node("0", "ROOT")

        stack = [(self.raiz, "0")]

        while stack:

            padre, id_p = stack.pop()

            for char, (etiqueta, hijo) in padre["hijos"].items():

                id_h = str(hijo["id"])

                if hijo["hijos"]:
                    lbl = ""
                else:
                    lbl = f"S{hijo['idx']}"

                dot.node(id_h, lbl)

                dot.edge(id_p, id_h, label=etiqueta)

                stack.append((hijo, id_h))

        ruta_final = dot.render(
            nombre_archivo,
            view=False,
            cleanup=True
        )

        print("Imagen creada en:", ruta_final)


# --- EJECUCIÓN ---

cadena = "RGFABASABPUEFABASABASABFWFDMOGFOASABASABABASABWM"

arbol = ArbolSufijosVisual(cadena)

arbol.exportar_imagen("mi_arbol_sufijos")