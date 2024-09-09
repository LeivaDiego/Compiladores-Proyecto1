from Language.compiscriptVisitor import compiscriptVisitor
from Language.compiscriptParser import compiscriptParser
from Model.data_types import NumType, BooleanType, StringType, NilType

# Semantic Analyzer
class SemanticAnalyzer(compiscriptVisitor):
    def __init__(self):
        # Symbol table to track variables and their types
        self.symbol_table = {}


    def visitVarDecl(self, ctx: compiscriptParser.VarDeclContext):
        # Get the variable name
        var_name = ctx.IDENTIFIER().getText()

        # Visit the expression on the right-hand side to infer the type
        var_type = self.visit(ctx.expression())

        # Add the variable and its type to the symbol table
        if var_name in self.symbol_table:
            raise Exception(f"Variable '{var_name}' is already declared.")
        else:
            self.symbol_table[var_name] = var_type
        
        print(f"Variable '{var_name}' declared with type '{var_type.data_type}'")
        return var_type


    def visitPrimary(self, ctx: compiscriptParser.PrimaryContext):
        # Infer the type of the primary expression
        if ctx.NUMBER():
            return NumType()  # Could also handle floating point numbers if necessary
        elif ctx.STRING():
            return StringType()
        elif ctx.IDENTIFIER():
            var_name = ctx.IDENTIFIER().getText()
            if var_name in self.symbol_table:
                return self.symbol_table[var_name]
            else:
                raise Exception(f"Undeclared variable '{var_name}'")
        elif ctx.getText() == "true" or ctx.getText() == "false":
            return BooleanType()
        elif ctx.getText() == "nil":
            return NilType()
        else:
            return self.visitChildren(ctx)


    def visitExpression(self, ctx: compiscriptParser.ExpressionContext):
        # Handle expressions leading to assignments or function calls
        return self.visit(ctx.assignment())


    def visitAssignment(self, ctx: compiscriptParser.AssignmentContext):
        # Visit the logic or (expression after the assignment)
        return self.visit(ctx.logic_or())


    def visitLogic_or(self, ctx: compiscriptParser.Logic_orContext):
        # Visit the logical and expression
        return self.visit(ctx.logic_and(0))

    def visitLogic_and(self, ctx: compiscriptParser.Logic_andContext):
        # Visit the equality expression
        return self.visit(ctx.equality(0))


    def visitEquality(self, ctx: compiscriptParser.EqualityContext):
        # Visit the comparison expression
        return self.visit(ctx.comparison(0))


    def visitComparison(self, ctx: compiscriptParser.ComparisonContext):
        # Visit the term expression
        return self.visit(ctx.term(0))


    def visitTerm(self, ctx: compiscriptParser.TermContext):
        # Visit the factor expression
        return self.visit(ctx.factor(0))


    def visitFactor(self, ctx: compiscriptParser.FactorContext):
        # Visit the unary expression
        return self.visit(ctx.unary(0))


    def visitUnary(self, ctx: compiscriptParser.UnaryContext):
        # Visit the primary expression
        return self.visit(ctx.call())

    
    def visitCall(self, ctx: compiscriptParser.CallContext):
        # Visit the primary expression
        return self.visit(ctx.primary())
