import tkinter as tk
from tkinter import messagebox
from TurnosMedicos import Cola, TIEMPOS_ESPECIALIDAD, LISTA_ESPECIALIDADES
from graficos import GraficoCola

cola = Cola()

# Ventana principal
root = tk.Tk()
root.title("Sistema de Gestión de Pacientes")
root.geometry("320x280")
root.configure(bg="#D8BFD8")  # Lila claro (Thistle)

ventana = tk.Toplevel(root)
ventana.configure(bg="#D8BFD8")

# ---- INICIAR INTERFAZ ---
def iniciar_interfaz():
    # ... todo tu código actual ...
    root = tk.Tk()
    root.title("Sistema de Gestión de Pacientes")
    # etc...
    root.mainloop()
# ---------------- Registro ----------------
def abrir_registro():
    registro = tk.Toplevel(root)
    registro.title("Registro de Pacientes")
    registro.configure(bg="#D8BFD8")
    registro.geometry("400x300")
    tk.Label(registro, text="Nombre del paciente:", bg="#D8BFD8").pack()
    nombre_entry = tk.Entry(registro)
    nombre_entry.pack()

    tk.Label(registro, text="Edad:", bg="#D8BFD8").pack()
    edad_entry = tk.Entry(registro)
    edad_entry.pack()

    tk.Label(registro, text="Especialidad requerida:", bg="#D8BFD8").pack()
    especialidad_var = tk.StringVar(registro)
    especialidad_var.set(LISTA_ESPECIALIDADES[0])
    especialidad_menu = tk.OptionMenu(registro, especialidad_var, *LISTA_ESPECIALIDADES)
    especialidad_menu.pack()

    def enviar():
        nombre = nombre_entry.get()
        edad = edad_entry.get()
        especialidad = especialidad_var.get()
        if nombre and edad and especialidad:
            minuto_actual = cola.tamano() + 1
            cola.registrar_paciente(nombre, int(edad), especialidad, minuto_actual)
            messagebox.showinfo("Registro exitoso", f"Paciente registrado:\n{nombre}, {edad}, {especialidad}")
            registro.destroy()
        else:
            messagebox.showwarning("Campos incompletos", "Por favor llena todos los campos.")

    tk.Button(registro, text="Registrar", command=enviar).pack(pady=10)

# ---------------- Visualización ----------------
def abrir_visualizacion():
    visual = tk.Toplevel(root)
    visual.configure(bg="#D8BFD8")
    visual.title("Pacientes Registrados")
    visual.geometry("400x300")

    estado = cola.obtener_estado_textual()
    if not estado:
        tk.Label(visual, text="No hay pacientes registrados.", bg="#D8BFD8").pack()
        return

    for i, texto in enumerate(estado, start=1):
        tk.Label(visual, text=f"{i}. {texto}", bg="#D8BFD8").pack(anchor='w')

# ---------------- Atención en bloque ----------------
def abrir_atencion():
    atencion = tk.Toplevel(root)
    atencion.configure(bg="#D8BFD8")
    atencion.title("Atención de Pacientes")
    atencion.geometry("500x400")

    if cola.estaVacia():
        tk.Label(atencion, text="No hay pacientes para atender.").pack()
        return

    historial = []
    acumulado = 0

    actual = cola.primero
    while actual is not None:
        paciente = actual.obtenerInfo()
        nombre = paciente.obtenerNombre()
        especialidad = paciente.obtenerEspecialidad()
        tiempo_atencion = TIEMPOS_ESPECIALIDAD[especialidad]
        minuto_entrada = paciente.obtenerMinutoEntradaACola()
        tiempo_espera = acumulado
        tiempo_total = tiempo_espera + tiempo_atencion

        historial.append((nombre, especialidad, minuto_entrada, tiempo_espera, tiempo_atencion, tiempo_total))
        acumulado += tiempo_atencion
        actual = actual.obtenerSiguiente()

    promedio_espera = sum([espera for _, _, _, espera, _, _ in historial]) / len(historial)

    tk.Label(atencion, text=f"Pacientes atendidos: {len(historial)}").pack()
    tk.Label(atencion, text=f"Promedio de espera en cola: {round(promedio_espera, 2)} minutos").pack(pady=5)

    for nombre, especialidad, entrada, espera, atencion_tiempo, total in historial:
        tk.Label(atencion, text=(
            f"{nombre} ({especialidad})\n"
            f"→ Ingresó a la cola en el minuto: {entrada}\n"
            f"→ Esperó en la cola: {espera} min\n"
            f"→ Tiempo de atención: {atencion_tiempo} min\n"
            f"→ Tiempo total estimado: {total} min"
        ), justify='left', anchor='w').pack(pady=3, anchor='w')
    
    graficador = GraficoCola(r'C:\Users\Mishel\OneDrive\Escritorio\Proyectos Uni\[IPC2]Practica2_202404409\grafo_demora')
    graficador.generar_grafo(historial)
    

def graficar_cola():
    if cola.estaVacia():
        messagebox.showinfo("Cola vacía", "No hay pacientes registrados.")
        return

    graficador = GraficoCola(r'C:\Users\Mishel\OneDrive\Escritorio\Proyectos Uni\[IPC2]Practica2_202404409\grafo_cola')
    graficador.generar_grafo_desde_cola(cola)
    messagebox.showinfo("Grafo generado", "Se ha generado el grafo de la cola correctamente.")

# ---------------- Botones ----------------
tk.Button(root, text="Registrar Paciente", command=abrir_registro).pack(pady=5)
tk.Button(root, text="Visualizar Pacientes", command=abrir_visualizacion).pack(pady=5)
tk.Button(root, text="Atender Pacientes", command=abrir_atencion).pack(pady=5)

root.mainloop()