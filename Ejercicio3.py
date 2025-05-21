import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import random

# ---------------------- CLASE PARA UNA CANCIÓN ----------------------
class Cancion:
    def __init__(self, nombre):
        self.nombre = nombre         # Nombre de la canción
        self.siguiente = None        # Referencia a la siguiente canción (lista doblemente enlazada)
        self.anterior = None         # Referencia a la canción anterior

# ---------------------- CLASE PARA LA LISTA DE REPRODUCCIÓN ----------------------
class ListaReproduccion:
    def __init__(self):
        self.primera = None         # Primer nodo/canción de la lista
        self.actual = None          # Canción que está sonando actualmente
        self.modo_aleatorio = False # Indica si el modo aleatorio está activado

    def agregar_cancion(self, nombre):
        nueva = Cancion(nombre)     # Crea un nuevo nodo/canción
        if not self.primera:
            self.primera = self.actual = nueva  # Si la lista está vacía, es la primera y actual
        else:
            temp = self.primera
            while temp.siguiente:   # Busca el último nodo
                temp = temp.siguiente
            temp.siguiente = nueva  # Enlaza la nueva canción al final
            nueva.anterior = temp   # Enlaza hacia atrás

    def eliminar_cancion(self, nombre):
        temp = self.primera
        while temp:
            if temp.nombre == nombre:
                if temp.anterior:
                    temp.anterior.siguiente = temp.siguiente  # Salta el nodo a eliminar
                else:
                    self.primera = temp.siguiente             # Si es la primera, actualiza la cabeza
                if temp.siguiente:
                    temp.siguiente.anterior = temp.anterior   # Ajusta el enlace hacia atrás
                if self.actual == temp:
                    self.actual = temp.siguiente or temp.anterior  # Cambia la actual si se elimina
                return True
            temp = temp.siguiente
        return False

    def siguiente_cancion(self):
        if self.modo_aleatorio:
            canciones = self.obtener_lista()
            if canciones:
                # Elige una canción aleatoria distinta de la actual
                self.actual = random.choice([c for c in canciones if c != self.actual])
        elif self.actual and self.actual.siguiente:
            self.actual = self.actual.siguiente  # Avanza a la siguiente canción

    def anterior_cancion(self):
        if self.actual and self.actual.anterior:
            self.actual = self.actual.anterior   # Retrocede a la canción anterior

    def repetir(self):
        return self.actual.nombre if self.actual else "No hay canción."  # Devuelve el nombre de la actual

    def buscar(self, nombre):
        temp = self.primera
        while temp:
            if temp.nombre == nombre:
                return True
            temp = temp.siguiente
        return False

    def obtener_lista(self):
        lista = []
        temp = self.primera
        while temp:
            lista.append(temp)      # Agrega cada nodo/canción a la lista
            temp = temp.siguiente
        return lista

    def guardar_lista(self, archivo):
        with open(archivo, 'w') as f:
            for cancion in self.obtener_lista():
                f.write(cancion.nombre + '\n')  # Guarda cada canción en una línea

    def cargar_lista(self, archivo):
        with open(archivo, 'r') as f:
            for linea in f:
                self.agregar_cancion(linea.strip())  # Agrega cada línea como canción

# ---------------------- CLASE PARA LA INTERFAZ GRÁFICA ----------------------
class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Reproductor de Música Creativo 🎵")  # Título de la ventana
        self.root.geometry("600x500")                           # Tamaño de la ventana
        self.root.configure(bg='#d0e1f9')                       # Color de fondo

        self.lista = ListaReproduccion()                        # Instancia de la lista de reproducción

        # Etiqueta que muestra la canción actual
        self.etiqueta = tk.Label(root, text="🎶 Canción actual: Ninguna", font=("Helvetica", 14), bg='#d0e1f9', fg='#003366')
        self.etiqueta.pack(pady=15)

        # Lista de botones con su texto y función asociada
        botones = [
            ("➕ Agregar Canción", self.agregar),
            ("➖ Eliminar Canción", self.eliminar),
            ("⏭️ Siguiente", self.siguiente),
            ("⏮️ Anterior", self.anterior),
            ("🔁 Repetir", self.repetir),
            ("🔀 Modo Aleatorio", self.toggle_aleatorio),
            ("🔍 Buscar Canción", self.buscar),
            ("📜 Mostrar Lista", self.mostrar_lista),
            ("💾 Guardar Lista", self.guardar),
            ("📂 Cargar Lista", self.cargar),
        ]

        # Crea y muestra cada botón en la ventana
        for texto, comando in botones:
            b = tk.Button(root, text=texto, command=comando, width=30, bg='#88c9bf', fg='black', font=("Helvetica", 12, "bold"))
            b.pack(pady=3)

    def actualizar_etiqueta(self):
        # Actualiza la etiqueta con el nombre de la canción actual
        actual = self.lista.actual.nombre if self.lista.actual else "Ninguna"
        self.etiqueta.config(text=f"🎶 Canción actual: {actual}")

    def agregar(self):
        # Pide al usuario el nombre de la canción y la agrega a la lista
        nombre = simpledialog.askstring("Agregar", "Nombre de la canción:")
        if nombre:
            self.lista.agregar_cancion(nombre)
            self.actualizar_etiqueta()

    def eliminar(self):
        # Pide el nombre de la canción a eliminar y la elimina si existe
        nombre = simpledialog.askstring("Eliminar", "Nombre de la canción a eliminar:")
        if nombre:
            if self.lista.eliminar_cancion(nombre):
                messagebox.showinfo("Éxito", "Canción eliminada.")
            else:
                messagebox.showwarning("Error", "Canción no encontrada.")
            self.actualizar_etiqueta()

    def siguiente(self):
        # Pasa a la siguiente canción (o aleatoria si está activado)
        self.lista.siguiente_cancion()
        self.actualizar_etiqueta()

    def anterior(self):
        # Retrocede a la canción anterior
        self.lista.anterior_cancion()
        self.actualizar_etiqueta()

    def repetir(self):
        # Muestra el nombre de la canción actual (repetir)
        if self.lista.actual:
            messagebox.showinfo("Repetir", f"Reproduciendo de nuevo: {self.lista.repetir()}")
        self.actualizar_etiqueta()

    def toggle_aleatorio(self):
        # Activa o desactiva el modo aleatorio
        self.lista.modo_aleatorio = not self.lista.modo_aleatorio
        estado = "activado" if self.lista.modo_aleatorio else "desactivado"
        messagebox.showinfo("Modo Aleatorio", f"Modo aleatorio {estado}.")

    def buscar(self):
        # Busca una canción por nombre y muestra si está o no
        nombre = simpledialog.askstring("Buscar", "Nombre de la canción a buscar:")
        if nombre:
            encontrado = self.lista.buscar(nombre)
            msg = "encontrada ✅" if encontrado else "no está ❌"
            messagebox.showinfo("Buscar", f"La canción {msg}.")

    def mostrar_lista(self):
        # Muestra todas las canciones de la lista en un mensaje
        canciones = [c.nombre for c in self.lista.obtener_lista()]
        if canciones:
            messagebox.showinfo("Lista", "\n".join(canciones))
        else:
            messagebox.showinfo("Lista", "La lista está vacía.")

    def guardar(self):
        # Permite guardar la lista de canciones en un archivo de texto
        archivo = filedialog.asksaveasfilename(defaultextension=".txt")
        if archivo:
            self.lista.guardar_lista(archivo)
            messagebox.showinfo("Guardar", "Lista guardada exitosamente.")

    def cargar(self):
        # Permite cargar una lista de canciones desde un archivo de texto
        archivo = filedialog.askopenfilename()
        if archivo:
            self.lista = ListaReproduccion()  # Reinicia la lista
            self.lista.cargar_lista(archivo)
            self.actualizar_etiqueta()
            messagebox.showinfo("Cargar", "Lista cargada correctamente.")

# ---------------------- INICIO DE LA APLICACIÓN ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()