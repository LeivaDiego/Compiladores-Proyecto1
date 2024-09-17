import tkinter as tk  
from tkinter import scrolledtext, Menu, PanedWindow, Frame, filedialog, ttk, messagebox  
import os
from PIL import Image, ImageTk  

class CompilerGUI:
    def __init__(self, root, run_code_callback):
        self.root = root
        self.run_code_callback = run_code_callback
        self.current_file_path = None

        # Crear un PanedWindow para permitir el cambio de tamaño entre el explorador, el editor de código y la consola
        self.pane = PanedWindow(root, orient=tk.HORIZONTAL)
        self.pane.pack(fill=tk.BOTH, expand=True)

        # Crear el explorador de archivos
        self.explorer_frame = Frame(self.pane)
        self.pane.add(self.explorer_frame, width=200)

        # Añadir un Treeview (árbol) para mostrar archivos y carpetas
        self.file_tree = ttk.Treeview(self.explorer_frame)
        self.file_tree.pack(fill=tk.BOTH, expand=True)

        # Vincular la expansión del nodo con la función para cargar su contenido
        self.file_tree.bind("<<TreeviewOpen>>", self.on_tree_expand)

        # Vincular la selección del archivo en el explorador con la apertura del archivo
        self.file_tree.bind("<Double-1>", self.on_file_select)

        # Crear otro PanedWindow para el editor de código y la consola
        self.editor_console_pane = PanedWindow(self.pane, orient=tk.VERTICAL)
        self.pane.add(self.editor_console_pane)

        # Crear el editor de código (área de texto con scroll)
        self.code_editor = scrolledtext.ScrolledText(self.editor_console_pane, undo=True, wrap=tk.WORD) 
        self.editor_console_pane.add(self.code_editor, stretch="always")  

        # Crear un frame para los botones de acción
        self.button_frame = Frame(self.editor_console_pane)
        self.editor_console_pane.add(self.button_frame, stretch="never")

        # Crear un frame que contenga la terminal
        self.terminal_frame = Frame(self.editor_console_pane)
        self.editor_console_pane.add(self.terminal_frame, stretch="always")  

        # Crear la terminal (área de texto con scroll)
        self.terminal_output = scrolledtext.ScrolledText(self.terminal_frame, height=10, state=tk.DISABLED, wrap=tk.WORD, bg="black", fg="white")  
        self.terminal_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)  

        # Cargar la imagen de la flecha verde para el botón "Compilar"
        image_path = "src/GUI/play_icon.png"  # Coloca aquí tu imagen de "play"
        img = Image.open(image_path)
        img = img.resize((20, 20), Image.LANCZOS)  
        run_icon = ImageTk.PhotoImage(img)  

        # Crear el botón "Compilar"
        run_button = tk.Button(self.button_frame, text="Compilar", image=run_icon, compound="right", command=lambda: self.run_code(is_debug=False))  
        run_button.image = run_icon  # Para que la imagen no se recolecte como basura
        run_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Crear el botón "Debuguear"
        debug_button = tk.Button(self.button_frame, text="Debuguear", command=lambda: self.run_code(is_debug=True))
        debug_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Crear el botón "Guardar"
        save_button = tk.Button(self.button_frame, text="Guardar", command=self.save_file)  
        save_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Crear el menú en la barra de menú
        self.menu_bar = Menu(root)
        root.config(menu=self.menu_bar)

        # Crear el submenú de "Archivo"
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Abrir Archivo", command=self.open_file)
        self.file_menu.add_command(label="Abrir Carpeta", command=self.open_folder)


    # Función para ejecutar el código cuando se presiona el botón "Compilar" o "Debuguear"
    def run_code(self, is_debug=False):
        if self.current_file_path:
            # Antes de ejecutar, vacía la terminal de la GUI y la configura para recibir nueva salida
            self.terminal_output.config(state=tk.NORMAL)
            self.terminal_output.delete("1.0", tk.END)

            # Ejecuta el proceso de compilación o debugueo y captura el output y errores
            output, error = self.run_code_callback(self.current_file_path, is_debug, self.terminal_output)

            # Despliega el output (logs y mensajes de stdout/stderr) en la terminal de la GUI
            if error:
                self.terminal_output.insert(tk.END, error + "\n")  # Muestra el error
            if output:
                self.terminal_output.insert(tk.END, output + "\n")  # Muestra la salida exitosa

            # Asegura que el scroll siempre siga la última línea del output
            self.terminal_output.see(tk.END)
            self.terminal_output.config(state=tk.DISABLED)  # Evita que el usuario edite la terminal
        else:
            # Si no hay archivo seleccionado, muestra un mensaje de error
            messagebox.showerror("Error", "No hay ningún archivo abierto para compilar o debuguear.")


    # Función para guardar el contenido del editor de código en el archivo actual
    def save_file(self):
        if self.current_file_path:
            try:
                with open(self.current_file_path, 'w', encoding='utf-8') as file:
                    code = self.code_editor.get("1.0", tk.END)
                    file.write(code)
                    messagebox.showinfo("Guardar", f"Archivo guardado exitosamente: {os.path.basename(self.current_file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")
        else:
            messagebox.showerror("Error", "No hay ningún archivo abierto para guardar.")

    # Función para abrir un archivo y mostrar su contenido en el editor de código
    def open_file(self, file_path=None):
        if not file_path:
            file_path = filedialog.askopenfilename(filetypes=[("Todos los archivos", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    code = file.read()
                    self.code_editor.delete("1.0", tk.END)
                    self.code_editor.insert(tk.END, code)
                    self.current_file_path = file_path
                    self.root.title(f"Compilador - {os.path.basename(file_path)}")
            except Exception as e:
                self.terminal_output.config(state=tk.NORMAL)
                self.terminal_output.insert(tk.END, f"Error al abrir el archivo: {e}\n")
                self.terminal_output.config(state=tk.DISABLED)

    # Función para abrir una carpeta y poblar el explorador de archivos
    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.populate_file_explorer(folder_path)

    # Función para poblar el explorador con archivos y carpetas
    def populate_file_explorer(self, path):
        self.file_tree.delete(*self.file_tree.get_children())
        parent_node = self.file_tree.insert("", "end", text=path, open=True)
        self.load_tree_nodes(parent_node, path)

    # Función para cargar archivos y carpetas en un nodo
    def load_tree_nodes(self, parent_node, path):
        if self.file_tree.get_children(parent_node):
            self.file_tree.delete(*self.file_tree.get_children(parent_node))
        for item in os.listdir(path):
            abs_path = os.path.join(path, item)
            node = self.file_tree.insert(parent_node, "end", text=item, open=False)
            if os.path.isdir(abs_path):
                self.file_tree.insert(node, "end")

    # Función para manejar la expansión de un nodo (carpeta) y cargar su contenido
    def on_tree_expand(self, event):
        node = self.file_tree.focus()
        abs_path = self.get_node_path(node)
        self.load_tree_nodes(node, abs_path)

    # Función para obtener la ruta absoluta de un nodo en el Treeview
    def get_node_path(self, node):
        path = []
        while node:
            path.insert(0, self.file_tree.item(node, 'text'))
            node = self.file_tree.parent(node)
        return os.path.join(*path)

    # Función para manejar la selección de un archivo en el explorador
    def on_file_select(self, event):
        selected_item = self.file_tree.focus()
        file_path = self.get_node_path(selected_item)
        if os.path.isfile(file_path):
            self.open_file(file_path)
