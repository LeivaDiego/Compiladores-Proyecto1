from antlr4 import *
from lang.HelloLexer import HelloLexer
from lang.HelloParser import HelloParser


input_text = input("> ")
lexer = HelloLexer(InputStream(input_text))
stream = CommonTokenStream(lexer)
parser = HelloParser(stream)

tree = parser.r()

print(tree.toStringTree(recog=parser))