from graphviz import Digraph

class GraficoCola:
    def __init__(self, ruta_base):
        self.ruta_base = ruta_base  # sin extensión

    def generar_grafo(self, historial):
        dot = Digraph(comment='Espera por paciente')
        dot.attr(rankdir='LR')  # Horizontal
        dot.attr('node', shape='box')  # Cuadros

        for i, (nombre, especialidad, entrada, espera, atencion, total) in enumerate(historial):
            etiqueta = f"{nombre}\n{especialidad}\nTiempo total: {total} min"
            dot.node(nombre, etiqueta)

            if i < len(historial) - 1:
                siguiente_nombre = historial[i + 1][0]
                dot.edge(nombre, siguiente_nombre)

        dot.save(self.ruta_base + '.dot')
        dot.render(self.ruta_base, format='png', view=True)