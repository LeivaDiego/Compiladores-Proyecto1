import os
import logging
import tkinter as tk
from antlr4 import FileStream, CommonTokenStream
from antlr4.error.Errors import ParseCancellationException
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from Model.parse_tree import TreeVisualizer
from Language.compiscriptLexer import compiscriptLexer
from Language.compiscriptParser import compiscriptParser
from Controller.driver import SemanticAnalyzer
from Controller.custom_exception import ThrowingErrorListener
from GUI.GUI import CompilerGUI  # Importamos la GUI desde el módulo GUI
import sys

# Define the custom logging level SUCCESS (between INFO and WARNING)
SUCCESS_LEVEL_NUM = 25
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")

# Define the method for logging success messages
def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kwargs)

# Add the 'success' method to the Logger class
logging.Logger.success = success

# Custom logger to redirect to the GUI terminal
def setup_logger(level, terminal_output):
    logger = logging.getLogger()  # Get the root logger
    logger.setLevel(level)  # Set the logging level

    # Create a console handler that outputs to the terminal in the GUI
    class TextRedirector(logging.Handler):
        def __init__(self, widget):
            super().__init__()
            self.widget = widget

        def emit(self, record):
            message = self.format(record)
            self.widget.config(state=tk.NORMAL)
            self.widget.insert(tk.END, message + '\n')
            self.widget.see(tk.END)
            self.widget.config(state=tk.DISABLED)

    # Remove existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Redirigir stdout y stderr a la terminal de la GUI mediante logging
    handler = TextRedirector(terminal_output)
    handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logger.addHandler(handler)

    # Redirigir también stdout y stderr para capturar todos los prints y errores.
    sys.stdout = StreamRedirector(terminal_output)
    sys.stderr = StreamRedirector(terminal_output)

    return logger

# Clase para redirigir stdout y stderr a la GUI
class StreamRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, message):
        if message.strip():  # Para evitar mensajes vacíos
            self.widget.config(state=tk.NORMAL)
            self.widget.insert(tk.END, message + '\n')
            self.widget.see(tk.END)
            self.widget.config(state=tk.DISABLED)

    def flush(self):
        pass  # Método requerido, pero no hace nada aquí


# Función que realiza el proceso de compilación
def run_compiler(file_path, is_debug=False, terminal_output=None):
    level = logging.DEBUG if is_debug else logging.INFO
    logger = setup_logger(level, terminal_output)

    try:
        logger.info(f"Starting {'debug' if is_debug else 'compilation'} for {file_path}...")
        input_stream = FileStream(file_path)
        lexer = compiscriptLexer(input_stream)
        lexer.removeErrorListeners()  # Remove the default error listener
        lexer.addErrorListener(ThrowingErrorListener.INSTANCE)  # Add custom error listener

        stream = CommonTokenStream(lexer)
        parser = compiscriptParser(stream)

        # Set BailErrorStrategy to stop parsing on first error
        parser._errHandler = DefaultErrorStrategy()
        parser.removeErrorListeners()
        parser.addErrorListener(ThrowingErrorListener.INSTANCE)

        # Try to parse the input file
        tree = parser.program()  # Start rule is 'program'
        logger.success("Parsing completed: No syntax errors found.")

        # Create a parse tree visualizer and visit the parse tree
        visualizer = TreeVisualizer(logger=logger)
        visualizer.visit(tree)

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file_name = f"parse_tree_{file_name}"

        visualizer.render(output_file=output_file_name, format='png', output_dir='src/Output')

        # Create a semantic analyzer and visit the parse tree
        analyzer = SemanticAnalyzer(logger=logger)
        analyzer.visit(tree)
        logger.success("Compilation completed: No errors found.")
        
        return "Compilation successful", None

    except ParseCancellationException as e:
        logger.error(f"Syntax error: {str(e)}")
        return None, f"Syntax error: {str(e)}"
    except Exception as e:
        logger.error(f"{str(e)}")
        return None, f"Error: {str(e)}"

# Función principal que inicializa la GUI y se encarga de la compilación
def main():
    # Crear la ventana principal de la GUI
    root = tk.Tk()

    # Inicializar la interfaz gráfica (pasamos la función `run_compiler` como callback)
    gui = CompilerGUI(root, run_compiler)

    # Iniciar el loop de la GUI
    root.mainloop()

if __name__ == '__main__':
    try:
        main()  # Levantamos la interfaz gráfica y esperamos la interacción del usuario
    except Exception as e:
        logging.error(f"{str(e)}")
