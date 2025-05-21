import tkinter as tk
from tkinter import messagebox

# ---------------------- NODO DE LA LISTA ENLAZADA ----------------------
class Node:
    def __init__(self, data):
        self.data = data      # Guarda el valor del nodo
        self.next = None      # Apunta al siguiente nodo (None si es el último)

# ---------------------- LISTA ENLAZADA SIMPLE ----------------------
class LinkedList:
    def __init__(self):
        self.head = None      # Referencia al primer nodo de la lista

    def append(self, data):
        # Agrega un nuevo nodo al final de la lista
        new_node = Node(data)
        if not self.head:
            self.head = new_node   # Si la lista está vacía, el nuevo nodo es la cabeza
        else:
            current = self.head
            while current.next:    # Recorre hasta el último nodo
                current = current.next
            current.next = new_node  # Enlaza el nuevo nodo al final

    def buscar(self, valor):
        # Busca todas las posiciones donde aparece el valor en la lista
        posiciones = []
        current = self.head
        index = 0
        while current:
            if current.data == valor:
                posiciones.append(index)
            current = current.next
            index += 1
        return posiciones

    def mostrar_lista(self):
        # Devuelve un string con todos los valores de la lista enlazada
        elementos = []
        actual = self.head
        while actual:
            elementos.append(str(actual.data))
            actual = actual.next
        return " → ".join(elementos) if elementos else "Vacía"

    def eliminar(self, valor):
        # Elimina el primer nodo que contenga el valor dado
        actual = self.head
        anterior = None
        while actual:
            if actual.data == valor:
                if anterior:
                    anterior.next = actual.next  # Elimina nodo intermedio o final
                else:
                    self.head = actual.next      # Elimina el primer nodo
                return True
            anterior = actual
            actual = actual.next
        return False

    def vaciar(self):
        # Elimina todos los nodos de la lista
        self.head = None

# ---------------------- FUNCIÓN AUXILIAR PARA VALIDAR ENTEROS ----------------------
def es_entero(valor):
    """Devuelve True si el valor es un número entero (positivo o negativo)."""
    try:
        int(valor)
        return True
    except ValueError:
        return False

# ---------------------- INTERFAZ GRÁFICA CON TKINTER ----------------------
class App:
    def __init__(self, root):
        self.lista = LinkedList()  # Instancia de la lista enlazada

        # Colores personalizados para la interfaz
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

        # Frame central para agrupar los widgets
        frame = tk.Frame(root, bg=color_frame, bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=480, height=290)

        # Etiqueta y entrada de texto para el valor a operar
        tk.Label(frame, text="Valor a operar:", font=("Segoe UI", 11), bg=color_frame).place(x=20, y=20)
        self.entry_valor = tk.Entry(frame, width=25, font=("Segoe UI", 11), bg=color_entrada)
        self.entry_valor.place(x=140, y=20)

        # Botón para agregar un valor a la lista
        self.btn_agregar = tk.Button(frame, text="Agregar", width=13, font=("Segoe UI", 10, "bold"),
                                     bg=color_boton, fg=color_texto_boton, activebackground=color_boton_hover,
                                     relief="ridge", bd=2, command=self.agregar, cursor="hand2")
        self.btn_agregar.place(x=20, y=60)

        # Botón para buscar un valor en la lista
        self.btn_buscar = tk.Button(frame, text="Buscar", width=13, font=("Segoe UI", 10, "bold"),
                                    bg=color_boton, fg=color_texto_boton, activebackground=color_boton_hover,
                                    relief="ridge", bd=2, command=self.buscar, cursor="hand2")
        self.btn_buscar.place(x=170, y=60)

        # Botón para eliminar un valor de la lista
        self.btn_eliminar = tk.Button(frame, text="Eliminar", width=13, font=("Segoe UI", 10, "bold"),
                                      bg=color_boton, fg=color_texto_boton, activebackground=color_boton_hover,
                                      relief="ridge", bd=2, command=self.eliminar, cursor="hand2")
        self.btn_eliminar.place(x=320, y=60)

        # Botón para vaciar toda la lista
        self.btn_limpiar = tk.Button(frame, text="Vaciar Lista", width=13, font=("Segoe UI", 10, "bold"),
                                     bg="#c62828", fg=color_texto_boton, activebackground="#b71c1c",
                                     relief="ridge", bd=2, command=self.vaciar, cursor="hand2")
        self.btn_limpiar.place(x=170, y=105)

        # Etiqueta para mostrar el contenido actual de la lista
        self.lbl_lista = tk.Label(frame, text="Lista actual: Vacía", fg=color_lista, bg=color_frame,
                                  font=("Consolas", 12, "bold"), wraplength=440, justify="left", anchor="w")
        self.lbl_lista.place(x=20, y=160, width=440, height=90)

        # Efecto hover para los botones (cambia color al pasar el mouse)
        for btn in [self.btn_agregar, self.btn_buscar, self.btn_eliminar, self.btn_limpiar]:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=color_boton_hover if b != self.btn_limpiar else "#b71c1c"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=color_boton if b != self.btn_limpiar else "#c62828"))

    # ---------------------- FUNCIONES DE LOS BOTONES ----------------------

    def agregar(self):
        # Agrega el valor ingresado a la lista si es un número entero (positivo o negativo)
        valor = self.entry_valor.get()
        if es_entero(valor.strip()):
            self.lista.append(int(valor.strip()))
            self.entry_valor.delete(0, tk.END)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Error", "Por favor, ingresa un número entero válido.")

    def buscar(self):
        # Busca el valor ingresado en la lista y muestra todas las posiciones si existe
        valor = self.entry_valor.get()
        if es_entero(valor.strip()):
            posiciones = self.lista.buscar(int(valor.strip()))
            if posiciones:
                if len(posiciones) == 1:
                    messagebox.showinfo("Encontrado", f"El valor {valor} se encuentra en la posición {posiciones[0]}.")
                else:
                    pos_str = ', '.join(str(p) for p in posiciones)
                    messagebox.showinfo("Repetido", f"El valor {valor} se repite en las posiciones: {pos_str}.")
            else:
                messagebox.showinfo("No encontrado", f"El valor {valor} no está en la lista.")
        else:
            messagebox.showwarning("Entrada inválida", "Por favor, ingresa un número entero.")

    def eliminar(self):
        # Elimina el valor ingresado de la lista si existe
        valor = self.entry_valor.get()
        if es_entero(valor.strip()):
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
        # Vacía toda la lista enlazada
        self.lista.vaciar()
        self.actualizar_lista()

    def actualizar_lista(self):
        # Actualiza el texto mostrado con el contenido actual de la lista enlazada
        texto = "Lista actual: " + self.lista.mostrar_lista()
        self.lbl_lista.config(text=texto)

# ---------------------- INICIO DE LA APLICACIÓN ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()