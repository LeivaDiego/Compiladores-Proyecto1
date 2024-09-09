from Language.compiscriptVisitor import compiscriptVisitor
from Language.compiscriptParser import compiscriptParser
from Model.data_types import NumType, BooleanType, StringType, NilType
from Model.scope import ScopeManager

# Semantic Analyzer
class SemanticAnalyzer(compiscriptVisitor):
    def __init__(self):
        self.scope_manager = ScopeManager()  # Create a scope manager

    def visitProgram(self, ctx: compiscriptParser.ProgramContext):
        # Enter the global scope
        return self.visitChildren(ctx)
    
    def visitBlock(self, ctx: compiscriptParser.BlockContext):
        # Visit the block and create a new scope
        self.scope_manager.enter_scope()
        print("Entered new scope")

        # Visit the statements in the block
        self.visitChildren(ctx)

        # Exit the scope
        self.scope_manager.exit_scope()

    def visitVarDecl(self, ctx: compiscriptParser.VarDeclContext):
        # Get the variable name
        var_name = ctx.IDENTIFIER().getText()

        # Visit the expression on the right-hand side to infer the type
        var_type = self.visit(ctx.expression())

        self.scope_manager.add_symbol(var_name, var_type)
        print(f"Declared variable '{var_name}' of type '{var_type}'")

    def visitPrintStmt(self, ctx: compiscriptParser.PrintStmtContext):
        var_name = ctx.expression().getText()
        symbol = self.scope_manager.lookup(var_name)

        if symbol is None:
            raise Exception(f"ERROR: Variable '{var_name}' not defined")
        
        print(f"Printing variable '{var_name}' of type '{symbol.symbol_type}'")

    def visitPrimary(self, ctx: compiscriptParser.PrimaryContext):
        # Infer the type of the primary expression
        if ctx.NUMBER():
            return NumType()
        
        elif ctx.STRING():
            return StringType()
        
        elif ctx.IDENTIFIER():
            var_name = ctx.IDENTIFIER().getText()
            symbol = self.scope_manager.lookup(var_name)
            if symbol is None:
                raise Exception(f"Undeclared variable '{var_name}'")
            return symbol.symbol_type  # Return the type of the found symbol
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
