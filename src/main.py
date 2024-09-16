import os
import logging
from antlr4 import FileStream, CommonTokenStream
from antlr4.error.Errors import ParseCancellationException
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from Model.parse_tree import TreeVisualizer
from Language.compiscriptLexer import compiscriptLexer
from Language.compiscriptParser import compiscriptParser
from Controller.driver import SemanticAnalyzer
from Controller.custom_exception import ThrowingErrorListener

# Define the custom logging level SUCCESS (between INFO and WARNING)
SUCCESS_LEVEL_NUM = 25
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")

# Define the method for logging success messages
def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kwargs)

# Add the 'success' method to the Logger class
logging.Logger.success = success

def setup_logger(level):
    logger = logging.getLogger()  # Get the root logger
    logger.setLevel(level)  # Set the logging level

    # Create a console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # Create a formatter
    formatter = logging.Formatter('%(levelname)s - %(message)s')

    # Add the formatter to the handler
    ch.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(ch)


def main():
    # Decide the mode (debug or production)
    is_debug = True # Set to True for debug mode, False for production mode
    if is_debug:
        setup_logger(logging.DEBUG)  # Verbose logging
    else:
        setup_logger(logging.INFO)  # Show info, warnings, errors, and critical

    # Get the logger
    logger = logging.getLogger(__name__)

    # Path to the input file
    input_path = 'src/Input/test.cspt' 

    # Create an input stream from the input file
    input_stream = FileStream(input_path)

    # Create a lexer and parser for the input stream
    lexer = compiscriptLexer(input_stream)
    lexer.removeErrorListeners()  # Remove the default error listener
    lexer.addErrorListener(ThrowingErrorListener.INSTANCE)  # Add custom error listener

    stream = CommonTokenStream(lexer)
    parser = compiscriptParser(stream)

    # Set BailErrorStrategy to stop parsing on first error
    parser._errHandler = DefaultErrorStrategy()
    # Remove default error listeners and add custom listener
    parser.removeErrorListeners()
    parser.addErrorListener(ThrowingErrorListener.INSTANCE)

    # Try to parse the input file
    try:
        tree = parser.program()  # Start rule is 'program'
        logger.success("Parsing completed: No syntax errors found.")
    except ParseCancellationException as e:
        logger.error(f"Syntax error: {str(e)}")
        return
    except Exception as e:
        logger.error(f"An error occurred during parsing: {str(e)}")
        return
    
    # Create a parse tree visualizer and visit the parse tree
    # to generate a PNG file of the parse tree
    visualizer = TreeVisualizer(logger=logger)
    visualizer.visit(tree)

    # Extract the file name without extension
    file_name = os.path.splitext(os.path.basename(input_path))[0]

    # Append the file name to the output file name
    output_file_name = f"parse_tree_{file_name}"

    visualizer.render(output_file=output_file_name, format='png', output_dir='src/Output')

    # Create a semantic analyzer and visit the parse tree
    analyzer = SemanticAnalyzer(logger=logger)
    
    # Visit the parse tree to perform semantic analysis
    analyzer.visit(tree)
    logger.success("Compilation completed: No errors found.")
    

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"{str(e)}")

