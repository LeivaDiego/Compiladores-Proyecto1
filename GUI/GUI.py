import tkinter as tk  
from tkinter import scrolledtext, Menu, PanedWindow, Frame, filedialog  
import subprocess  
from PIL import Image, ImageTk  

# Crear la ventana principal
root = tk.Tk()  
root.title("Compilador (Construcción de Compiladores CC3032) - Editor de Código")  
root.geometry("800x600") 

# Definir colores para los temas
dark_gray = "#2E2E2E"  # Color gris oscuro para el tema oscuro

# Función para cambiar el tema
def set_theme(theme):
    if theme == "claro":
        root.config(bg="white")
        code_editor.config(bg="white", fg="black", insertbackground="black")
        terminal_frame.config(bg="white")
        run_button.config(bg="lightgray", fg="black")
    elif theme == "oscuro":
        root.config(bg=dark_gray)
        code_editor.config(bg=dark_gray, fg="white", insertbackground="white")
        terminal_frame.config(bg=dark_gray)
        run_button.config(bg=dark_gray, fg="white")

# Función para ejecutar el código cuando se presiona el botón "Compilar"
def run_code():
    code = code_editor.get("1.0", tk.END)  # Obtenemos todo el contenido del editor de código.
    
    # Guardar el código en un archivo temporal
    with open("temp_code.py", "w") as f:
        f.write(code)  # Escribimos el código en un archivo temporal llamado 'temp_code.py'.
    
    # Ejecutar el archivo y capturar la salida
    process = subprocess.Popen(
        ["python", "temp_code.py"],  # Ejecutamos el archivo temporal usando Python.
        stdout=subprocess.PIPE,  
        stderr=subprocess.PIPE,  
        text=True  
    )
    output, error = process.communicate()  # Obtenemos la salida y el error de la ejecución.
    
    # Mostrar la salida en la "terminal" de la GUI
    terminal_output.config(state=tk.NORMAL)  
    terminal_output.delete("1.0", tk.END)  
    terminal_output.insert(tk.END, output + error)  
    terminal_output.config(state=tk.DISABLED)  

# Función para abrir un archivo y mostrar su contenido en el editor de código
def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Todos los archivos", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
                code_editor.delete("1.0", tk.END)  # Borra el contenido actual del editor
                code_editor.insert(tk.END, code)  # Inserta el contenido del archivo
        except Exception as e:
            terminal_output.config(state=tk.NORMAL)  
            terminal_output.insert(tk.END, f"Error al abrir el archivo: {e}\n")  
            terminal_output.config(state=tk.DISABLED)  

# Crear un PanedWindow para permitir el cambio de tamaño entre el editor de código y la consola
pane = PanedWindow(root, orient=tk.VERTICAL)
pane.pack(fill=tk.BOTH, expand=True)

# Crear el editor de código (área de texto con scroll)
code_editor = scrolledtext.ScrolledText(pane, undo=True, wrap=tk.WORD) 
pane.add(code_editor, stretch="always")  

# Crear un frame que contenga el botón y la terminal
terminal_frame = Frame(pane)
pane.add(terminal_frame, stretch="always")  

# Cargar la imagen de la flecha verde para el botón
image_path = "image.png"  
img = Image.open(image_path)
img = img.resize((20, 20), Image.LANCZOS)  
run_icon = ImageTk.PhotoImage(img)  

# Crear el botón para ejecutar el código con la imagen y el texto "Compilar"
run_button = tk.Button(terminal_frame, text="Compilar  ", image=run_icon, compound="right", command=run_code)  
run_button.pack(side=tk.TOP, anchor="w", padx=10, pady=5)  

# Crear la terminal (área de texto con scroll) para mostrar la salida del código dentro del frame de la terminal
terminal_output = scrolledtext.ScrolledText(terminal_frame, height=10, state=tk.DISABLED, wrap=tk.WORD, bg="black", fg="white")  
terminal_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)  

# Crear el menú en la barra de menú
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Crear el submenú de "Archivo"
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Archivo", menu=file_menu)

# Agregar la opción "Abrir Archivo" en el submenú "Archivo"
file_menu.add_command(label="Abrir Archivo", command=open_file)

# Crear el submenú de "Configuraciones"
config_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Configuraciones", menu=config_menu)

# Agregar el submenú de temas dentro de "Configuraciones"
theme_menu = Menu(config_menu, tearoff=0)
config_menu.add_cascade(label="Tema", menu=theme_menu)
theme_menu.add_command(label="Claro", command=lambda: set_theme("claro"))
theme_menu.add_command(label="Oscuro", command=lambda: set_theme("oscuro"))

root.mainloop()  # Inicia el loop principal de tkinter para que la ventana esté en funcionamiento.
