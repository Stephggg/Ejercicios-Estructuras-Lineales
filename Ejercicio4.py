# ===============================
# BIBLIOTECAS NECESARIAS
# ===============================

import tkinter as tk  # Biblioteca principal para crear interfaces gráficas en Python
from tkinter import ttk  # Widgets modernos (como botones estilizados)
from tkinter import messagebox  # Para mostrar mensajes emergentes al usuario
from tkinter import simpledialog  # Para solicitar entradas mediante cuadros emergentes
import heapq  # Proporciona una estructura de datos tipo heap para implementar la cola de prioridad

# ===============================
# LÓGICA DE LA COLA DE PRIORIDAD
# ===============================

class ColaPrioridad:
    def __init__(self):
        self.cola = []      # Lista principal que almacena tuplas (prioridad, nombre) como heap
        self.historial = [] # Lista para guardar los elementos que han sido desencolados

    def encolar(self, nombre, prioridad):
        heapq.heappush(self.cola, (prioridad, nombre))  # Inserta el elemento en el heap según prioridad

    def desencolar(self):
        if self.cola:
            elemento = heapq.heappop(self.cola)  # Extrae el elemento con mayor prioridad (menor número)
            self.historial.append(elemento)       # Lo agrega al historial de desencolados
            return elemento
        return None

    def buscar(self, nombre):
        # Busca un elemento por nombre (ignorando mayúsculas/minúsculas)
        for i, (p, n) in enumerate(self.cola):
            if n.lower() == nombre.lower():
                return (i + 1, p)  # Devuelve la posición (empezando en 1) y la prioridad
        return None

    def editar(self, nombre, nueva_prioridad):
        # Busca el elemento y cambia su prioridad
        for i, (p, n) in enumerate(self.cola):
            if n.lower() == nombre.lower():
                self.cola[i] = (nueva_prioridad, n)  # Cambia la prioridad
                heapq.heapify(self.cola)             # Reorganiza el heap para mantener la propiedad
                return True
        return False

    def vaciar(self):
        self.cola.clear()  # Elimina todos los elementos de la cola

    def obtener_estadisticas(self):
        # Calcula estadísticas: total de elementos, menor prioridad, promedio de prioridades
        if not self.cola:
            return (0, "N/A", "N/A")
        prioridades = [p for p, _ in self.cola]
        return (len(self.cola), min(prioridades), sum(prioridades) / len(prioridades))

# ===============================
# INTERFAZ GRÁFICA ESTÉTICA
# ===============================

class InterfazColaPrioridad:
    def __init__(self, root):
        self.root = root
        self.root.title("🧺 Cola de Prioridad - Interfaz Estética")
        self.root.configure(bg="#fff5e6")  # Fondo cálido

        self.cola = ColaPrioridad()        # Instancia de la lógica de la cola

        fuente = ("Segoe UI", 10)          # Fuente base para los widgets

        # Título principal
        titulo = tk.Label(root, text="Cola de Prioridad", font=("Segoe UI", 18, "bold"), fg="#cc6600", bg="#fff5e6")
        titulo.pack(pady=(10, 5))

        # Frame para agrupar los widgets
        frame = tk.Frame(root, bg="#fff5e6")
        frame.pack(padx=20, pady=10)

        # Entradas para nombre y prioridad
        tk.Label(frame, text="Nombre:", font=fuente, bg="#fff5e6").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.nombre_entry = tk.Entry(frame, width=30, font=fuente, bg="#fffaf0")
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Prioridad (número):", font=fuente, bg="#fff5e6").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.prioridad_entry = tk.Entry(frame, width=30, font=fuente, bg="#fffaf0")
        self.prioridad_entry.grid(row=1, column=1, padx=5, pady=5)

        # Botones de acción con sus funciones
        botones = [
            ("➕ Encolar", self.encolar),
            ("➖ Desencolar", self.desencolar),
            ("🔍 Buscar", self.buscar),
            ("✏️ Editar Prioridad", self.editar),
            ("🗑 Vaciar Cola", self.vaciar_cola),
        ]
        for i, (texto, comando) in enumerate(botones):
            boton = tk.Button(frame, text=texto, command=comando,
                              font=fuente, width=25, bg="#ffd9b3", fg="#663300",
                              activebackground="#ffcc99", relief="raised", bd=2)
            boton.grid(row=2+i, column=0, columnspan=2, pady=4)

        # Lista visual de elementos en la cola
        tk.Label(frame, text="📋 Elementos en la cola:", font=fuente, bg="#fff5e6").grid(row=7, column=0, columnspan=2, pady=(10, 2))
        self.lista = tk.Listbox(frame, width=45, height=6, font=("Consolas", 10), bg="#fffaf0")
        self.lista.grid(row=8, column=0, columnspan=2, pady=4)

        # Estadísticas de la cola
        self.stats_label = tk.Label(frame, text="Estadísticas: Total=0, Mayor=N/A, Promedio=N/A", font=fuente, bg="#fff5e6")
        self.stats_label.grid(row=9, column=0, columnspan=2, pady=(10, 5))

        # Historial de desencolados
        tk.Label(frame, text="🕘 Historial:", font=fuente, bg="#fff5e6").grid(row=10, column=0, columnspan=2, pady=(5, 2))
        self.historial = tk.Text(frame, height=5, width=45, state="disabled", font=("Consolas", 10), bg="#fffaf0")
        self.historial.grid(row=11, column=0, columnspan=2, pady=(0, 10))

    # ===============================
    # FUNCIONES DE LA INTERFAZ
    # ===============================

    def actualizar_lista(self):
        """Actualiza visualmente la lista de elementos actuales en la cola"""
        self.lista.delete(0, tk.END)
        for prioridad, nombre in sorted(self.cola.cola):
            self.lista.insert(tk.END, f"{nombre} (Prioridad: {prioridad})")

        total, min_p, prom = self.cola.obtener_estadisticas()
        if total:
            self.stats_label.config(text=f"Estadísticas: Total={total}, Mayor={min_p}, Promedio={prom:.2f}")
        else:
            self.stats_label.config(text="Estadísticas: Total=0, Mayor=N/A, Promedio=N/A")

    def actualizar_historial(self):
        """Muestra el historial de elementos desencolados"""
        self.historial.config(state="normal")
        self.historial.delete("1.0", tk.END)
        for prioridad, nombre in self.cola.historial:
            self.historial.insert(tk.END, f"{nombre} (Prioridad: {prioridad})\n")
        self.historial.config(state="disabled")

    def encolar(self):
        """Agrega un nuevo elemento a la cola"""
        nombre = self.nombre_entry.get().strip()
        prioridad = self.prioridad_entry.get().strip()

        if not nombre or not prioridad.isdigit():
            messagebox.showwarning("Datos inválidos", "Por favor, completa correctamente los campos.")
            return

        self.cola.encolar(nombre, int(prioridad))
        self.actualizar_lista()

    def desencolar(self):
        """Elimina el elemento con mayor prioridad"""
        elemento = self.cola.desencolar()
        if elemento:
            messagebox.showinfo("Elemento desencolado", f"{elemento[1]} fue eliminado.")
            self.actualizar_lista()
            self.actualizar_historial()
        else:
            messagebox.showinfo("Cola vacía", "No hay elementos para desencolar.")

    def buscar(self):
        """Busca un elemento por nombre"""
        nombre = self.nombre_entry.get().strip()
        resultado = self.cola.buscar(nombre)
        if resultado:
            pos, prioridad = resultado
            messagebox.showinfo("Encontrado", f"{nombre} está en la posición {pos} con prioridad {prioridad}.")
        else:
            messagebox.showinfo("No encontrado", f"No se encontró a {nombre} en la cola.")

    def vaciar_cola(self):
        """Elimina todos los elementos de la cola"""
        self.cola.vaciar()
        self.actualizar_lista()

    def editar(self):
        """Permite cambiar la prioridad de un elemento existente"""
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showwarning("Dato requerido", "Primero ingresa un nombre.")
            return

        nueva = simpledialog.askinteger("Editar Prioridad", f"Nueva prioridad para {nombre}:")
        if nueva is not None:
            if self.cola.editar(nombre, nueva):
                messagebox.showinfo("Actualizado", f"Prioridad de {nombre} modificada.")
                self.actualizar_lista()
            else:
                messagebox.showerror("No encontrado", f"{nombre} no está en la cola.")

# ===============================
# EJECUCIÓN PRINCIPAL DEL PROGRAMA
# ===============================

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazColaPrioridad(root)
    root.mainloop()