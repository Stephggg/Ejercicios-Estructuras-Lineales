import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------- FUNCIÓN PARA VERIFICAR PARÉNTESIS ----------------------

def verificar_balanceo_detallado(cadena):
    """
    Verifica si los paréntesis (), {}, [] están balanceados en la cadena.
    Si hay un error, indica el tipo de paréntesis y la posición exacta (empezando en 1).
    Devuelve: (balanceado: bool, mensaje: str, resumen: dict)
    """
    pila = []  # Lista que funcionará como pila para guardar los paréntesis de apertura y su posición
    pares = {')': '(', '}': '{', ']': '['}  # Diccionario que indica qué apertura corresponde a cada cierre
    resumen = {'(': 0, ')': 0, '{': 0, '}': 0, '[': 0, ']': 0}  # Diccionario para contar cada tipo de paréntesis

    # Recorre cada carácter de la cadena junto con su índice
    for i, char in enumerate(cadena):
        # Si el carácter es un paréntesis de apertura
        if char in '({[':
            pila.append((char, i))    # Guarda el tipo de paréntesis y su posición en la pila
            resumen[char] += 1        # Suma uno al contador de ese tipo de apertura
        # Si el carácter es un paréntesis de cierre
        elif char in ')}]':
            resumen[char] += 1        # Suma uno al contador de ese tipo de cierre
            if not pila:
                # Si la pila está vacía, significa que hay un cierre sin apertura previa
                return False, f"Error: paréntesis de cierre '{char}' sin apertura en posición {i+1}.", resumen
            ultimo, pos_ultimo = pila[-1]  # Obtiene el último paréntesis de apertura pendiente y su posición
            if ultimo != pares[char]:
                # Si el tipo de apertura no coincide con el cierre, hay un error de correspondencia
                return False, (
                    f"Error: paréntesis de cierre '{char}' en posición {i+1} no coincide con "
                    f"el de apertura '{ultimo}' en posición {pos_ultimo+1}."
                ), resumen
            pila.pop()  # Si coincide, elimina ese paréntesis de apertura de la pila

    # Si al final quedan aperturas sin cerrar en la pila
    if pila:
        char, pos = pila[-1]  # Toma el primer paréntesis de apertura sin cerrar y su posición
        return False, f"Error: paréntesis de apertura '{char}' sin cerrar en posición {pos+1}.", resumen

    # Si no hubo errores, retorna que está balanceado
    return True, "✅ Paréntesis balanceados correctamente.", resumen

# ---------------------- FUNCIÓN PARA CORREGIR PARÉNTESIS AUTOMÁTICAMENTE ----------------------

def corregir_parentesis(cadena):
    """
    Corrige la cadena agregando los paréntesis de cierre faltantes al final
    y eliminando los de cierre que no tienen apertura correspondiente.
    Devuelve la cadena corregida y balanceada.
    """
    pila = []       # Pila para guardar los paréntesis de apertura pendientes
    resultado = []  # Lista para construir la cadena corregida
    pares = {')': '(', '}': '{', ']': '['}      # Diccionario de cierre -> apertura
    apertura = {'(': ')', '{': '}', '[': ']'}   # Diccionario de apertura -> cierre

    # Recorre cada carácter de la cadena
    for char in cadena:
        if char in '({[':
            pila.append(char)        # Guarda la apertura en la pila
            resultado.append(char)   # Añade la apertura al resultado
        elif char in ')}]':
            # Si hay una apertura correspondiente en la pila y coincide con el cierre actual
            if pila and pila[-1] == pares[char]:
                pila.pop()           # Elimina la apertura de la pila
                resultado.append(char)  # Añade el cierre al resultado
            else:
                # Si hay un cierre sin apertura, lo ignora (no lo añade al resultado)
                continue
        else:
            resultado.append(char)   # Si no es paréntesis, lo añade al resultado

    # Al final, agrega los cierres faltantes para cada apertura que quedó pendiente
    while pila:
        resultado.append(apertura[pila.pop()])
    return ''.join(resultado)  # Devuelve la cadena corregida y balanceada

# ---------------------- INTERFAZ GRÁFICA ----------------------

ventana = tk.Tk()
ventana.title("🧠 Analizador de Paréntesis Balanceados")
ventana.geometry("650x450")
ventana.config(bg="#f5f8fc")
ventana.resizable(False, False)

# Título principal
ttk.Label(
    ventana,
    text="🔍 Verificador de Paréntesis ( ) [ ] { }",
    font=("Arial", 16, "bold"),
    background="#f5f8fc"
).pack(pady=10)

# Caja de entrada de texto
entrada = tk.Text(
    ventana,
    font=("Arial", 12),
    height=5,
    width=70
)
entrada.pack(pady=10)

# Botón para verificar
ttk.Button(
    ventana,
    text="Verificar",
    command=lambda: ejecutar_verificacion()
).pack(pady=5)

# Variables para mostrar resultados
resultado_var = tk.StringVar()
conteo_var = tk.StringVar()

# Etiqueta de resultado principal
resultado_label = ttk.Label(
    ventana,
    textvariable=resultado_var,
    font=("Arial", 13, "italic"),
    background="#f5f8fc"
)
resultado_label.pack(pady=10)

# Etiqueta de conteo de paréntesis
ttk.Label(
    ventana,
    text="📊 Conteo de Paréntesis:",
    background="#f5f8fc",
    font=("Arial", 12, "bold")
).pack()
conteo_label = ttk.Label(
    ventana,
    textvariable=conteo_var,
    font=("Consolas", 11),
    background="#f5f8fc"
)
conteo_label.pack(pady=5)

# Función para mostrar resultado
def ejecutar_verificacion():
    texto = entrada.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Entrada vacía", "Por favor ingrese una expresión.")
        return

    balanceado, mensaje, resumen = verificar_balanceo_detallado(texto)
    resultado_var.set(mensaje)
    resultado_label.config(foreground="green" if balanceado else "red")

    # Mostrar conteo de paréntesis
    resumen_text = (
        f"( : {resumen['(']}    ) : {resumen[')']}\n"
        f"{{ : {resumen['{']}}}    }} : {resumen['}']}\n"
        f"[ : {resumen['[']}    ] : {resumen[']']}"
    )
    conteo_var.set(resumen_text)

# Función para copiar resultado
def copiar_resultado():
    ventana.clipboard_clear()
    ventana.clipboard_append(resultado_var.get())
    ventana.update()
    messagebox.showinfo("Copiado", "Resultado copiado al portapapeles.")

# Función para mostrar la corrección
def mostrar_correccion():
    texto = entrada.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Entrada vacía", "Por favor ingrese una expresión.")
        return
    corregido = corregir_parentesis(texto)
    messagebox.showinfo("Cadena Corregida", f"Expresión balanceada:\n{corregido}")

# Botón copiar resultado
ttk.Button(ventana, text="Copiar resultado", command=copiar_resultado).pack(pady=10)

# Botón para corregir paréntesis
ttk.Button(ventana, text="Corregir paréntesis", command=mostrar_correccion).pack(pady=5)

ventana.mainloop()


'''
Ejemplo de uso
Mi amiga Laura (quien siempre ha sido muy puntual, aunque últimamente [especialmente desde que empezó su nuevo trabajo], ha estado llegando tarde a nuestras reuniones).
'''