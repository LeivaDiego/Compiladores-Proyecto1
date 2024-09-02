# Generated from compiscript.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .compiscriptParser import compiscriptParser
else:
    from compiscriptParser import compiscriptParser

# This class defines a complete listener for a parse tree produced by compiscriptParser.
class compiscriptListener(ParseTreeListener):

    # Enter a parse tree produced by compiscriptParser#program.
    def enterProgram(self, ctx:compiscriptParser.ProgramContext):
        pass

    # Exit a parse tree produced by compiscriptParser#program.
    def exitProgram(self, ctx:compiscriptParser.ProgramContext):
        pass


    # Enter a parse tree produced by compiscriptParser#declaration.
    def enterDeclaration(self, ctx:compiscriptParser.DeclarationContext):
        pass

    # Exit a parse tree produced by compiscriptParser#declaration.
    def exitDeclaration(self, ctx:compiscriptParser.DeclarationContext):
        pass


    # Enter a parse tree produced by compiscriptParser#classDecl.
    def enterClassDecl(self, ctx:compiscriptParser.ClassDeclContext):
        pass

    # Exit a parse tree produced by compiscriptParser#classDecl.
    def exitClassDecl(self, ctx:compiscriptParser.ClassDeclContext):
        pass


    # Enter a parse tree produced by compiscriptParser#funDecl.
    def enterFunDecl(self, ctx:compiscriptParser.FunDeclContext):
        pass

    # Exit a parse tree produced by compiscriptParser#funDecl.
    def exitFunDecl(self, ctx:compiscriptParser.FunDeclContext):
        pass


    # Enter a parse tree produced by compiscriptParser#varDecl.
    def enterVarDecl(self, ctx:compiscriptParser.VarDeclContext):
        pass

    # Exit a parse tree produced by compiscriptParser#varDecl.
    def exitVarDecl(self, ctx:compiscriptParser.VarDeclContext):
        pass


    # Enter a parse tree produced by compiscriptParser#statement.
    def enterStatement(self, ctx:compiscriptParser.StatementContext):
        pass

    # Exit a parse tree produced by compiscriptParser#statement.
    def exitStatement(self, ctx:compiscriptParser.StatementContext):
        pass


    # Enter a parse tree produced by compiscriptParser#exprStmt.
    def enterExprStmt(self, ctx:compiscriptParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by compiscriptParser#exprStmt.
    def exitExprStmt(self, ctx:compiscriptParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by compiscriptParser#forStmt.
    def enterForStmt(self, ctx:compiscriptParser.ForStmtContext):
        pass

    # Exit a parse tree produced by compiscriptParser#forStmt.
    def exitForStmt(self, ctx:compiscriptParser.ForStmtContext):
        pass


    # Enter a parse tree produced by compiscriptParser#ifStmt.
    def enterIfStmt(self, ctx:compiscriptParser.IfStmtContext):
        pass

    # Exit a parse tree produced by compiscriptParser#ifStmt.
    def exitIfStmt(self, ctx:compiscriptParser.IfStmtContext):
        pass


    # Enter a parse tree produced by compiscriptParser#printStmt.
    def enterPrintStmt(self, ctx:compiscriptParser.PrintStmtContext):
        pass

    # Exit a parse tree produced by compiscriptParser#printStmt.
    def exitPrintStmt(self, ctx:compiscriptParser.PrintStmtContext):
        pass


    # Enter a parse tree produced by compiscriptParser#returnStmt.
    def enterReturnStmt(self, ctx:compiscriptParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by compiscriptParser#returnStmt.
    def exitReturnStmt(self, ctx:compiscriptParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by compiscriptParser#whileStmt.
    def enterWhileStmt(self, ctx:compiscriptParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by compiscriptParser#whileStmt.
    def exitWhileStmt(self, ctx:compiscriptParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by compiscriptParser#block.
    def enterBlock(self, ctx:compiscriptParser.BlockContext):
        pass

    # Exit a parse tree produced by compiscriptParser#block.
    def exitBlock(self, ctx:compiscriptParser.BlockContext):
        pass


    # Enter a parse tree produced by compiscriptParser#funAnon.
    def enterFunAnon(self, ctx:compiscriptParser.FunAnonContext):
        pass

    # Exit a parse tree produced by compiscriptParser#funAnon.
    def exitFunAnon(self, ctx:compiscriptParser.FunAnonContext):
        pass


    # Enter a parse tree produced by compiscriptParser#expression.
    def enterExpression(self, ctx:compiscriptParser.ExpressionContext):
        pass

    # Exit a parse tree produced by compiscriptParser#expression.
    def exitExpression(self, ctx:compiscriptParser.ExpressionContext):
        pass


    # Enter a parse tree produced by compiscriptParser#assignment.
    def enterAssignment(self, ctx:compiscriptParser.AssignmentContext):
        pass

    # Exit a parse tree produced by compiscriptParser#assignment.
    def exitAssignment(self, ctx:compiscriptParser.AssignmentContext):
        pass


    # Enter a parse tree produced by compiscriptParser#logic_or.
    def enterLogic_or(self, ctx:compiscriptParser.Logic_orContext):
        pass

    # Exit a parse tree produced by compiscriptParser#logic_or.
    def exitLogic_or(self, ctx:compiscriptParser.Logic_orContext):
        pass


    # Enter a parse tree produced by compiscriptParser#logic_and.
    def enterLogic_and(self, ctx:compiscriptParser.Logic_andContext):
        pass

    # Exit a parse tree produced by compiscriptParser#logic_and.
    def exitLogic_and(self, ctx:compiscriptParser.Logic_andContext):
        pass


    # Enter a parse tree produced by compiscriptParser#equality.
    def enterEquality(self, ctx:compiscriptParser.EqualityContext):
        pass

    # Exit a parse tree produced by compiscriptParser#equality.
    def exitEquality(self, ctx:compiscriptParser.EqualityContext):
        pass


    # Enter a parse tree produced by compiscriptParser#comparison.
    def enterComparison(self, ctx:compiscriptParser.ComparisonContext):
        pass

    # Exit a parse tree produced by compiscriptParser#comparison.
    def exitComparison(self, ctx:compiscriptParser.ComparisonContext):
        pass


    # Enter a parse tree produced by compiscriptParser#term.
    def enterTerm(self, ctx:compiscriptParser.TermContext):
        pass

    # Exit a parse tree produced by compiscriptParser#term.
    def exitTerm(self, ctx:compiscriptParser.TermContext):
        pass


    # Enter a parse tree produced by compiscriptParser#factor.
    def enterFactor(self, ctx:compiscriptParser.FactorContext):
        pass

    # Exit a parse tree produced by compiscriptParser#factor.
    def exitFactor(self, ctx:compiscriptParser.FactorContext):
        pass


    # Enter a parse tree produced by compiscriptParser#array.
    def enterArray(self, ctx:compiscriptParser.ArrayContext):
        pass

    # Exit a parse tree produced by compiscriptParser#array.
    def exitArray(self, ctx:compiscriptParser.ArrayContext):
        pass


    # Enter a parse tree produced by compiscriptParser#instantiation.
    def enterInstantiation(self, ctx:compiscriptParser.InstantiationContext):
        pass

    # Exit a parse tree produced by compiscriptParser#instantiation.
    def exitInstantiation(self, ctx:compiscriptParser.InstantiationContext):
        pass


    # Enter a parse tree produced by compiscriptParser#unary.
    def enterUnary(self, ctx:compiscriptParser.UnaryContext):
        pass

    # Exit a parse tree produced by compiscriptParser#unary.
    def exitUnary(self, ctx:compiscriptParser.UnaryContext):
        pass


    # Enter a parse tree produced by compiscriptParser#call.
    def enterCall(self, ctx:compiscriptParser.CallContext):
        pass

    # Exit a parse tree produced by compiscriptParser#call.
    def exitCall(self, ctx:compiscriptParser.CallContext):
        pass


    # Enter a parse tree produced by compiscriptParser#primary.
    def enterPrimary(self, ctx:compiscriptParser.PrimaryContext):
        pass

    # Exit a parse tree produced by compiscriptParser#primary.
    def exitPrimary(self, ctx:compiscriptParser.PrimaryContext):
        pass


    # Enter a parse tree produced by compiscriptParser#function.
    def enterFunction(self, ctx:compiscriptParser.FunctionContext):
        pass

    # Exit a parse tree produced by compiscriptParser#function.
    def exitFunction(self, ctx:compiscriptParser.FunctionContext):
        pass


    # Enter a parse tree produced by compiscriptParser#parameters.
    def enterParameters(self, ctx:compiscriptParser.ParametersContext):
        pass

    # Exit a parse tree produced by compiscriptParser#parameters.
    def exitParameters(self, ctx:compiscriptParser.ParametersContext):
        pass


    # Enter a parse tree produced by compiscriptParser#arguments.
    def enterArguments(self, ctx:compiscriptParser.ArgumentsContext):
        pass

    # Exit a parse tree produced by compiscriptParser#arguments.
    def exitArguments(self, ctx:compiscriptParser.ArgumentsContext):
        pass



del compiscriptParser