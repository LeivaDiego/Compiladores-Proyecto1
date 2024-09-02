from Language.compiscriptVisitor import compiscriptVisitor
from Language.compiscriptParser import compiscriptParser
from Model.data_types import NumType, BooleanType, StringType, NilType

class SemanticAnalyzer(compiscriptVisitor):
    def __init__(self):
        self.symbol_table = {}

    def visitPrimary(self, ctx: compiscriptParser.PrimaryContext):
        if ctx.NUMBER():
            return NumType()
        
        elif ctx.STRING():
            return StringType()

        elif ctx.getText() == 'true' or ctx.getText() == 'false':
            return BooleanType()
        
        elif ctx.getText() == 'nil':
            return NilType()
        
        else:
            return self.visit(ctx.expression())