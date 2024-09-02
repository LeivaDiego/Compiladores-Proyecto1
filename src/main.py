import os
from antlr4 import *
from Model.parse_tree import TreeVisualizer
from Language.compiscriptLexer import compiscriptLexer
from Language.compiscriptParser import compiscriptParser

def main():
    input_path = 'src/Input/suma_simple.compiscript' 

    input_stream = FileStream(input_path)

    lexer = compiscriptLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = compiscriptParser(stream)

    tree = parser.program()
    visualizer = TreeVisualizer()
    visualizer.visit(tree)

    # Extract the file name without extension
    file_name = os.path.splitext(os.path.basename(input_path))[0]

    # Append the file name to the output file name
    output_file_name = f"parse_tree_{file_name}"

    visualizer.render(output_file=output_file_name, format='png', output_dir='src/Output')

if __name__ == '__main__':
    main()
