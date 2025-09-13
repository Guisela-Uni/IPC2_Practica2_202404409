# Diccionario de tiempos por especialidad
TIEMPOS_ESPECIALIDAD = {
    "Medicina General": 10,
    "Pediatria": 15,
    "Ginecologia": 20,
    "Detmatologia": 25
}

LISTA_ESPECIALIDADES = list(TIEMPOS_ESPECIALIDAD.keys())  # Para menú desplegable

# -------------------- Clases --------------------

class InfoNodo():
    def desplegar(self):
        pass
    def EsIgualALLave(self, llave):
        pass

class paciente(InfoNodo):
    def __init__(self, nombre, edad, especialidad, min_entrada):
        self.nombre = nombre
        self.edad = edad
        self.especialidad = especialidad
        self.min_entrada_cola = min_entrada

    def obtenerNombre(self):
        return self.nombre
    def obtenerEdad(self):
        return self.edad
    def obtenerEspecialidad(self):
        return self.especialidad
    def obtenerMinutoEntradaACola(self):
        return self.min_entrada_cola

    def asignarNombre(self, nombre):
        self.nombre = nombre
    def asignarEdad(self, edad):
        self.edad = edad
    def asignarEspecialidad(self, especialidad):
        self.especialidad = especialidad
    def asignarMinutoEntradaACola(self, min_entrada):
        self.min_entrada_cola = min_entrada

    def desplegar(self):
        print(self.nombre + " - " + str(self.especialidad) + " - " + str(self.min_entrada_cola))

    def EsIgualALLave(self, nombre):
        return self.nombre == nombre

class Nodo:
    def __init__(self, info):
        self.info = info
        self.siguiente = None

    def obtenerInfo(self):
        return self.info
    def obtenerSiguiente(self):
        return self.siguiente
    def asignarInfo(self, info):
        self.info = info
    def asignarSiguiente(self, nuevosiguiente):
        self.siguiente = nuevosiguiente

# -------------------- Cola personalizada --------------------

class Cola:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.historial_esperas = []

    def estaVacia(self):
        return self.primero is None

    def Push(self, item):
        nuevo = Nodo(item)
        if self.primero is not None:
            self.ultimo.asignarSiguiente(nuevo)
        else:
            self.primero = nuevo
        self.ultimo = nuevo

    def Pop(self, minuto_actual):
        if self.primero is None:
            return None

        nodo_atendido = self.primero
        self.primero = self.primero.obtenerSiguiente()
        if self.primero is None:
            self.ultimo = None

        paciente = nodo_atendido.obtenerInfo()
        espera = minuto_actual - paciente.obtenerMinutoEntradaACola()
        self.historial_esperas.append(espera)
        return paciente

    def tamano(self):
        actual = self.primero
        contador = 0
        while actual is not None:
            contador += 1
            actual = actual.obtenerSiguiente()
        return contador

    def registrar_paciente(self, nombre, edad, especialidad, minuto_actual):
        nuevo = paciente(nombre, edad, especialidad, minuto_actual)
        self.Push(nuevo)

    def obtener_estado_textual(self):
        estado = []
        actual = self.primero
        while actual is not None:
            paciente = actual.obtenerInfo()
            estado.append(f"{paciente.obtenerNombre()} ({paciente.obtenerEspecialidad()})")
            actual = actual.obtenerSiguiente()
        return estado

    def calcular_tiempos_estimados(self):
        tiempos = []
        actual = self.primero
        acumulado = 0

        while actual is not None:
            paciente = actual.obtenerInfo()
            atencion = TIEMPOS_ESPECIALIDAD[paciente.obtenerEspecialidad()]
            total = acumulado + atencion
            tiempos.append((paciente.obtenerNombre(), total))
            acumulado += atencion
            actual = actual.obtenerSiguiente()
        return tiempos

    def generar_dot(self):
        dot = "digraph ColaTurnos {\nrankdir=LR;\nnode [shape=box];\n"
        actual = self.primero
        while actual is not None:
            nombre = actual.obtenerInfo().obtenerNombre()
            dot += f'"{nombre}" -> '
            actual = actual.obtenerSiguiente()
        dot += "null;\n}"
        return dot

    def obtener_promedio_espera(self):
        if not self.historial_esperas:
            return 0
        return sum(self.historial_esperas) / len(self.historial_esperas)

