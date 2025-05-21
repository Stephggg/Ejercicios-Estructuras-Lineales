import tkinter as tk
from tkinter import messagebox

# Clase que representa un nodo de la lista enlazada
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Clase que representa la lista enlazada
class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def buscar(self, valor):
        current = self.head
        index = 0
        while current:
            if current.data == valor:
                return index
            current = current.next
            index += 1
        return -1

    def mostrar_lista(self):
        elementos = []
        actual = self.head
        while actual:
            elementos.append(str(actual.data))
            actual = actual.next
        return " → ".join(elementos) if elementos else "Vacía"

    def eliminar(self, valor):
        actual = self.head
        anterior = None
        while actual:
            if actual.data == valor:
                if anterior:
                    anterior.next = actual.next
                else:
                    self.head = actual.next
                return True
            anterior = actual
            actual = actual.next
        return False

    def vaciar(self):
        self.head = None

# Clase que gestiona la interfaz gráfica usando tkinter
class App:
    def __init__(self, root):
        self.lista = LinkedList()

        # Colores personalizados
        fondo = "#e3f2fd"
        color_frame = "#ffffff"
        color_boton = "#1976d2"
        color_boton_hover = "#1565c0"
        color_texto_boton = "#ffffff"
        color_entrada = "#e1f5fe"
        color_lista = "#0d47a1"

        root.title("Lista Enlazada - Interfaz Gráfica")
        root.geometry("520x350")
        root.config(bg=fondo)
        root.resizable(False, False)

        # Frame central para mejor presentación
        frame = tk.Frame(root, bg=color_frame, bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=480, height=290)

        # Etiqueta y entrada de texto para el valor
        tk.Label(frame, text="Valor a operar:", font=("Segoe UI", 11), bg=color_frame).place(x=20, y=20)
        self.entry_valor = tk.Entry(frame, width=25, font=("Segoe UI", 11), bg=color_entrada)
        self.entry_valor.place(x=140, y=20)

        # Botones con color y efecto hover
        self.btn_agregar = tk.Button(frame, text="Agregar", width=13, font=("Segoe UI", 10, "bold"),
                                     bg=color_boton, fg=color_texto_boton, activebackground=color_boton_hover,
                                     relief="ridge", bd=2, command=self.agregar, cursor="hand2")
        self.btn_agregar.place(x=20, y=60)

        self.btn_buscar = tk.Button(frame, text="Buscar", width=13, font=("Segoe UI", 10, "bold"),
                                    bg=color_boton, fg=color_texto_boton, activebackground=color_boton_hover,
                                    relief="ridge", bd=2, command=self.buscar, cursor="hand2")
        self.btn_buscar.place(x=170, y=60)

        self.btn_eliminar = tk.Button(frame, text="Eliminar", width=13, font=("Segoe UI", 10, "bold"),
                                      bg=color_boton, fg=color_texto_boton, activebackground=color_boton_hover,
                                      relief="ridge", bd=2, command=self.eliminar, cursor="hand2")
        self.btn_eliminar.place(x=320, y=60)

        self.btn_limpiar = tk.Button(frame, text="Vaciar Lista", width=13, font=("Segoe UI", 10, "bold"),
                                     bg="#c62828", fg=color_texto_boton, activebackground="#b71c1c",
                                     relief="ridge", bd=2, command=self.vaciar, cursor="hand2")
        self.btn_limpiar.place(x=170, y=105)

        # Etiqueta para mostrar el contenido actual de la lista
        self.lbl_lista = tk.Label(frame, text="Lista actual: Vacía", fg=color_lista, bg=color_frame,
                                  font=("Consolas", 12, "bold"), wraplength=440, justify="left", anchor="w")
        self.lbl_lista.place(x=20, y=160, width=440, height=90)

        # Efecto hover para los botones
        for btn in [self.btn_agregar, self.btn_buscar, self.btn_eliminar, self.btn_limpiar]:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=color_boton_hover if b != self.btn_limpiar else "#b71c1c"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=color_boton if b != self.btn_limpiar else "#c62828"))

    def agregar(self):
        valor = self.entry_valor.get()
        if valor.strip().isdigit():
            self.lista.append(int(valor.strip()))
            self.entry_valor.delete(0, tk.END)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Error", "Por favor, ingresa un número entero válido.")

    def buscar(self):
        valor = self.entry_valor.get()
        if valor.strip().isdigit():
            posicion = self.lista.buscar(int(valor.strip()))
            if posicion != -1:
                messagebox.showinfo("Encontrado", f"El valor {valor} se encuentra en la posición {posicion}.")
            else:
                messagebox.showinfo("No encontrado", f"El valor {valor} no está en la lista.")
        else:
            messagebox.showwarning("Entrada inválida", "Por favor, ingresa un número entero.")

    def eliminar(self):
        valor = self.entry_valor.get()
        if valor.strip().isdigit():
            eliminado = self.lista.eliminar(int(valor.strip()))
            if eliminado:
                messagebox.showinfo("Éxito", f"Se eliminó el valor {valor}.")
            else:
                messagebox.showinfo("No encontrado", f"No se encontró el valor {valor} en la lista.")
            self.entry_valor.delete(0, tk.END)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Entrada inválida", "Por favor, ingresa un número entero.")

    def vaciar(self):
        self.lista.vaciar()
        self.actualizar_lista()

    def actualizar_lista(self):
        texto = "Lista actual: " + self.lista.mostrar_lista()
        self.lbl_lista.config(text=texto)

# Código para ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()