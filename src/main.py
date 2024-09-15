import os
from antlr4 import *
from Model.parse_tree import TreeVisualizer
from Language.compiscriptLexer import compiscriptLexer
from Language.compiscriptParser import compiscriptParser
from Controller.driver import SemanticAnalyzer

def main():
    # Path to the input file
    input_path = 'src/Input/var_decl.cspt' 

    # Create an input stream from the input file
    input_stream = FileStream(input_path)

    # Create a lexer and parser for the input stream
    lexer = compiscriptLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = compiscriptParser(stream)

    tree = parser.program() # Start rule is 'program'

    # Create a parse tree visualizer and visit the parse tree
    # to generate a PNG file of the parse tree
    visualizer = TreeVisualizer()
    visualizer.visit(tree)

    # Extract the file name without extension
    file_name = os.path.splitext(os.path.basename(input_path))[0]

    # Append the file name to the output file name
    output_file_name = f"parse_tree_{file_name}"

    visualizer.render(output_file=output_file_name, format='png', output_dir='src/Output')

    # Create a semantic analyzer and visit the parse tree
    analyzer = SemanticAnalyzer()
    # Visit the parse tree to perform semantic analysis
    analyzer.visit(tree)

if __name__ == '__main__':
    main()
