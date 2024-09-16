from Language.compiscriptVisitor import compiscriptVisitor
from Language.compiscriptParser import compiscriptParser
from Controller.semantic_utils import *
from Model.data_types import *
from Model.object_types import *
from Model.scope import ScopeManager
from Model.symbol_table import Symbol

class SemanticAnalyzer(compiscriptVisitor):
    """
    Class that implements the visitor pattern to perform semantic analysis on the parse
    tree generated by the ANTLR parser.

    The semantic analyzer is responsible for creating the symbol table and performing
    type checking on the program.
    """
    def __init__(self, logger=None):
        self.scope_manager = ScopeManager()         # Create a scope manager
        self.logger = logger                        # Get the logger for the class
        self.in_print_ctx = False                   # Flag to indicate if the visitor is in a print statement context
        self.in_return_ctx = False                  # Flag to indicate if the visitor is in a return statement context

    def visitProgram(self, ctx: compiscriptParser.ProgramContext):
        # Enter the global scope
        self.logger.debug("Entered global scope")
        return self.visitChildren(ctx)
    


    def visitDeclaration(self, ctx: compiscriptParser.DeclarationContext):
        self.logger.debug("Visiting declaration")
        # Check if the declaration is a variable declaration
        if ctx.funDecl() is not None:
            # Visit the function declaration
            self.logger.debug("Visiting function declaration in declaration")
            self.visitFunDecl(ctx.funDecl())
        
        elif ctx.varDecl() is not None:
            # Visit the variable declaration
            self.logger.debug("Visiting variable declaration in declaration")
            self.visitVarDecl(ctx.varDecl())

        # Check if the declaration is a statement
        elif ctx.statement() is not None:
            # Visit the statement
            self.logger.debug("Visiting statement in declaration")
            return self.visitStatement(ctx.statement())
        


    def visitStatement(self, ctx: compiscriptParser.StatementContext, scope_name=None):
        self.logger.debug("Visiting statement")
        # Check if the statement is a expression statement
        if ctx.exprStmt() is not None:
            # Visit the expression statement
            self.logger.debug("Visiting expression statement in statement")
            return self.visitExprStmt(ctx.exprStmt())

        # Check if the statement is a if statement
        elif ctx.ifStmt() is not None:
            # Visit the if statement
            self.logger.debug("Visiting if statement in statement")
            return self.visitIfStmt(ctx.ifStmt())
        
        # Check if the statement is a for statement
        elif ctx.forStmt() is not None:
            # Visit the for statement
            self.logger.debug("Visiting for statement in statement")
            return self.visitForStmt(ctx.forStmt())
        
        # Check if the statement is a while statement
        elif ctx.whileStmt() is not None:
            # Visit the while statement
            self.logger.debug("Visiting while statement in statement")
            return self.visitWhileStmt(ctx.whileStmt())
        
        # Check if the statement is a return statement
        elif ctx.returnStmt() is not None:
            # Visit the return statement
            self.logger.debug("Visiting return statement in statement")
            return self.visitReturnStmt(ctx.returnStmt())
        
        # Check if the statement is a print statement
        elif ctx.printStmt() is not None:
            # Visit the print statement
            self.logger.debug("Visiting print statement in statement")
            return self.visitPrintStmt(ctx.printStmt())
        
        # Check if the statement is a block statement
        elif ctx.block() is not None:
            # Visit the block statement
            self.logger.debug("Visiting block statement in statement")
            return self.visitBlockStmt(ctx.block(), scope_name)
        


    def visitForStmt(self, ctx: compiscriptParser.ForStmtContext):
        self.logger.debug("Visiting for statement")
        
        # Enter the scope of the for loop
        self.logger.debug("Entered for loop scope")
        self.scope_manager.enter_scope("For Loop")

        # Visit the initialization (variable declaration or expression statement)
        if ctx.varDecl() is not None:
            self.logger.debug("Visiting variable declaration in for loop")
            self.visitVarDecl(ctx.varDecl())
        elif ctx.exprStmt() is not None:
            self.logger.debug("Visiting expression statement in for loop initialization")
            self.visitExprStmt(ctx.exprStmt())
        else:
            self.logger.debug("No initialization in for loop")

        # Visit the condition (optional)
        if ctx.expression(0) is not None:
            self.logger.debug("Visiting condition expression in for loop")
            condition_type = self.visitExpression(ctx.expression(0))
            validate_boolean_expression_type(condition_type, " in for loop condition")
        else:
            self.logger.debug("No condition in for loop (infinite loop unless broken)")

        # Visit the update expression (optional)
        if ctx.expression(1) is not None:
            self.logger.debug("Visiting update expression in for loop")
            self.visitExpression(ctx.expression(1)) 
        else:
            self.logger.debug("No update expression in for loop")

        # Visit the body of the for loop
        if ctx.statement() is not None:
            self.logger.debug("Entering body scope of for loop")
            # Enter the scope of the body
            self.scope_manager.enter_scope("For Loop Body")  
            # Visit the body of the for loop
            self.visitStatement(ctx.statement())
            # Exit the scope of the body
            self.scope_manager.exit_scope()

        # Exit the scope of the for loop
        self.logger.debug("Exited for loop scope")
        self.scope_manager.exit_scope()



    def visitWhileStmt(self, ctx: compiscriptParser.WhileStmtContext):
        self.logger.debug("Visiting while statement")

        # Visit the condition expression
        if ctx.expression() is not None:
            self.logger.debug("Visiting condition expression in while loop")
            condition_type = self.visitExpression(ctx.expression())
            validate_boolean_expression_type(condition_type, " in while loop condition")
        else:
            raise Exception("While loop must have a condition expression.")

        # Visit the body of the while loop
        if ctx.statement() is not None:
            self.logger.debug("Visiting body of while loop")
            self.visitStatement(ctx.statement(), "While Loop")   



    def visitReturnStmt(self, ctx: compiscriptParser.ReturnStmtContext):
        self.logger.debug("Visiting return statement")
        # Visit the expression inside the return statement
        if ctx.expression() is not None:
            self.logger.debug("Visiting expression in return statement")
            return self.visitExpression(ctx.expression())

    def visitPrintStmt(self, ctx: compiscriptParser.PrintStmtContext):
        self.logger.debug("Visiting print statement")

        # Change print context flag to True 
        # to indicate that the visitor is in a print statement
        self.in_print_ctx = True

        # Visit the expression inside the print statement
        self.visit(ctx.expression())

        # Change print context flag to False 
        # to indicate that the visitor is no longer in a print statement
        self.in_print_ctx = False


    def visitBlockStmt(self, ctx: compiscriptParser.BlockContext, scope_name=None):
        self.logger.debug("Visiting block statement")
        # Enter a new scope for the block
        if scope_name is not None:
            self.logger.debug(f"Entered block scope '{scope_name}'")
            self.scope_manager.enter_scope(scope_name)
        else:
            self.logger.debug("Entered block scope")
            self.scope_manager.enter_scope("Block Scope")

        # Visit the block statements
        self.logger.debug("Visiting block statements")
        for i in range(len(ctx.declaration())):
            self.logger.debug(f"Visiting declaration {i} in block statement")
            self.visitDeclaration(ctx.declaration(i))

        # Exit the block scope
        self.logger.debug("Exited block scope")
        self.scope_manager.exit_scope()
        


    def visitFunDecl(self, ctx: compiscriptParser.FunDeclContext):
        self.logger.debug("Visiting function declaration")
        # Visit the function
        if ctx.function() is not None:
            self.logger.debug("Visiting function in function declaration")
            self.visitFunction(ctx.function())
        else:
            raise Exception("Function declaration must have a function definition.")


    def visitVarDecl(self, ctx: compiscriptParser.VarDeclContext):
        # Get the variable identifier
        self.logger.debug("Visiting variable declaration")
        identifier = ctx.IDENTIFIER().getText()
        self.logger.debug(f"Started variable declaration for var: {identifier}")

        # Check if the variable already exists in the current scope
        self.logger.debug(f"Checking if variable '{identifier}' already exists in the current scope")
        existing_var = self.scope_manager.get_symbol(identifier, Variable)
        if existing_var is not None:
            # Variable already exists in the current scope
            raise Exception(f"Variable '{identifier}' already exists in the current scope.")
        
        # Create a new variable symbol and add it to the current scope in the symbol table
        self.logger.debug(f"Creating new variable symbol for '{identifier}'")
        variable = Variable(data_type=None) # Initialize the variable without defining its data type
        new_var_symbol = Symbol(name=identifier, obj_type=variable)

        # Add the variable to the current scope
        self.logger.debug(f"Adding variable '{identifier}' to current scope {self.scope_manager.current_scope}")
        self.scope_manager.add_symbol(new_var_symbol)
        self.logger.debug(f"Added variable {identifier} to current scope {self.scope_manager.current_scope}")

        # Check if the variable has an initialization expression
        if ctx.expression() is not None:
            # Visit the expression to infer its type
            self.logger.debug(f"Visiting expression to infer type for variable '{identifier}'")
            expression_type = self.visit(ctx.expression())
            variable.data_type = expression_type
            self.logger.debug(f"Inferred type for variable {identifier}: {expression_type}")
        else:
            self.logger.debug(f"No initial value for '{identifier}', type is undefined.")

        # Log the variable declaration
        self.logger.debug(f"Variable '{identifier}' declared with type '{variable.data_type}' in scope {self.scope_manager.current_scope}")



    def visitExprStmt(self, ctx: compiscriptParser.ExprStmtContext):
        self.logger.debug("Visiting expression statement")
        if ctx.expression() is not None:
            self.logger.debug("Visiting expression in expression statement")
            return self.visitExpression(ctx.expression())
        


    def visitIfStmt(self, ctx: compiscriptParser.IfStmtContext):
        self.logger.debug("Visiting if statement")
        # Check if the if statement has an expression
        if ctx.expression() is not None:
            self.logger.debug("Visiting expression in if statement")
            # Visit the expression to infer its type
            condition_type = self.visitExpression(ctx.expression())
            # Validate that the condition type is BooleanType
            validate_boolean_expression_type(condition_type, " in if statement")
        else:
            raise Exception("If statement must have a condition expression.")
        
        if ctx.statement(0) is not None:
            self.logger.debug("Visiting statement in if statement")
            self.visitStatement(ctx.statement(0), "If Block")
        else:
            raise Exception("If statement must have a body.")

        if ctx.statement(1) is not None:
            self.logger.debug("Visiting statement in else statement")
            self.visitStatement(ctx.statement(1), "Else Block")
        else:
            self.logger.debug("No else statement in if statement")



    def visitFunction(self, ctx: compiscriptParser.FunctionContext):
        self.logger.debug("Visiting function")
        # Get the function identifier
        identifier = ctx.IDENTIFIER().getText()
        self.logger.debug(f"Started function declaration for function '{identifier}'")

        # Check if the function already exists in the current scope
        self.logger.debug(f"Checking if function '{identifier}' already exists in the current scope")
        existing_function = self.scope_manager.get_symbol(identifier, Function)
        if existing_function is not None:
            # Function already exists in the current scope
            raise Exception(f"Function '{identifier}' already exists in the current scope.")
        
        # Create a new function symbol and add it to the current scope in the symbol table
        self.logger.debug(f"Creating new function symbol for '{identifier}'")
        function = Function(return_type=None, parameters=[])
        new_function_symbol = Symbol(name=identifier, obj_type=function)
        self.logger.debug(f"Adding function '{identifier}' to current scope {self.scope_manager.current_scope}")
        self.scope_manager.add_symbol(new_function_symbol)

        # Enter the scope of the function
        self.logger.debug(f"Entered function scope '{identifier}'")
        scope_name = f"Function '{identifier}'"
        self.scope_manager.enter_scope(scope_name)
        # Handle function parameters (if any)
        if ctx.parameters() is not None:
            self.logger.debug("Visiting parameters in function")
            function.parameters = self.visitParameters(ctx.parameters())
            self.in_return_ctx = True
        else:
            self.logger.debug("No parameters in function")

        # Visit the function body
        if ctx.block() is not None:
            self.logger.debug("Visiting block in function")
            self.visitBlockStmt(ctx.block(), f"Function {identifier} Body")

        # Update the function symbol
        self.scope_manager.update_symbol(identifier, function)
        self.logger.debug(f"Updated function '{identifier}' with parameters '{function.parameters}'")
        self.logger.debug(f"Function '{identifier}' declared with return type '{function.return_type}' and parameters '{function.parameters}' in scope {self.scope_manager.current_scope}")
        
        # Exit the scope of the function
        self.logger.debug(f"Exited function scope '{identifier}'")
        self.scope_manager.exit_scope()
        self.in_return_ctx = False
        


    def visitParameters(self, ctx: compiscriptParser.ParametersContext):
        self.logger.debug("Visiting parameters")
        params = []
        # Visit the parameter list
        for param in ctx.IDENTIFIER():
            # Get the parameter identifier
            identifier = param.getText()
            self.logger.debug(f"Started parameter declaration for parameter '{identifier}'")

            # Check if the parameter already exists in the current scope
            self.logger.debug(f"Checking if parameter '{identifier}' already exists in the current scope")
            existing_param = self.scope_manager.get_symbol(identifier, Variable)
            if existing_param is not None:
                # Parameter already exists in the current scope
                raise Exception(f"Parameter '{identifier}' already exists in the current scope.")
            
            # Create a new parameter symbol and add it to the current scope in the symbol table
            self.logger.debug(f"Creating new parameter symbol for '{identifier}'")
            parameter = Variable(data_type=None)
            new_param_symbol = Symbol(name=identifier, obj_type=parameter)
            self.logger.debug(f"Adding parameter '{identifier}' to current scope {self.scope_manager.current_scope}")
            self.scope_manager.add_symbol(new_param_symbol)

            self.logger.debug(f"Added parameter {identifier} to current scope {self.scope_manager.current_scope}")
            # Add the parameter to the function's parameter list
            params.append(parameter)
        
        return params


    def visitExpression(self, ctx: compiscriptParser.ExpressionContext):
        self.logger.debug("Visiting expression")
        if ctx.assignment() is not None:
            self.logger.debug("Visiting assignment in expression")
            return self.visitAssignment(ctx.assignment())



    def visitAssignment(self, ctx: compiscriptParser.AssignmentContext):
        self.logger.debug("Visiting assignment")
        
        if ctx.IDENTIFIER() is not None:
            # Get the identifier of the variable being assigned
            identifier = ctx.IDENTIFIER().getText()
            self.logger.debug(f"Started assignment for variable '{identifier}'")

            # Check if the variable exists in the current scope
            variable_symbol = self.scope_manager.get_symbol(identifier, Variable)
            if variable_symbol is None:
                raise Exception(f"Variable '{identifier}' is not declared in the current scope - {self.scope_manager.current_scope}")
            
            # Get the variable symbol from the symbol table
            self.logger.debug(f"Found variable '{identifier}' in scope {self.scope_manager.current_scope}")
            # Visit the expression to infer its type
            expression_type = self.visit(ctx.assignment())

            # Check if the variable has a data type defined
            if variable_symbol.object_type.data_type is None:
                # Set the data type of the variable to the inferred type
                variable_symbol.object_type.data_type = expression_type
                self.logger.debug(f"Set type of variable '{identifier}' to '{expression_type}'")
            
            # Check if the variable's data type matches the inferred type
            elif str(variable_symbol.object_type.data_type) != str(expression_type):
                raise Exception(f"Type mismatch: Cannot assign '{expression_type}' to variable '{identifier}' of type '{variable_symbol.object_type.data_type}'")

            self.logger.debug(f"Assigned value to variable '{identifier}' of type '{variable_symbol.object_type.data_type}'")

        elif ctx.logic_or() is not None:
            self.logger.debug("Visiting logic_or in assignment")
            return self.visitLogic_or(ctx.logic_or())
        

        
    def visitLogic_or(self, ctx: compiscriptParser.Logic_orContext):
        self.logger.debug("Visiting logic_or")
        # Check if there is only one 'logic_and' element
        # meaning this step is a wrapper around 'logic_and' only
        if len(ctx.logic_and()) == 1:
            self.logger.debug("Single logic_and in logic_or")
            return self.visitLogic_and(ctx.logic_and(0))
        
        # Get the left term type
        left_term_type = self.visitLogic_and(ctx.logic_and(0))

        # Evaluate the rest of the 'logic_and' elements
        for i in range(1, len(ctx.logic_and())):
            self.logger.debug(f"Visiting logic_and {i} in logic_or")
            # Get the right term type
            right_term_type = self.visitLogic_and(ctx.logic_and(i))
            # Validate the types for the 'or' operator are BooleanType
            validate_logical_types(left_term_type, right_term_type, 'or')

        return BooleanType()


        
    def visitLogic_and(self, ctx: compiscriptParser.Logic_andContext):
        self.logger.debug("Visiting logic_and")
        # Check if there is only one 'equality' element
        # meaning this step is a wrapper around 'equality' only
        if len(ctx.equality()) == 1:
            self.logger.debug("Single equality in logic_and")
            return self.visitEquality(ctx.equality(0))
        
        # Get the type of the left term
        left_type = self.visitEquality(ctx.equality(0))

        # Evaluate the rest of the 'equality' elements
        for i in range(1, len(ctx.equality())):
            self.logger.debug(f"Visiting equality {i} in logic_and")
            # Get the type of the right term
            right_type = self.visitEquality(ctx.equality(i))
            # Validate the types for the 'and' operator are BooleanType
            validate_logical_types(left_type, right_type, 'and') 

        return BooleanType()



    def visitEquality(self, ctx: compiscriptParser.EqualityContext):
        self.logger.debug("Visiting equality")
        # Check if there is only one 'comparison' element
        # meaning this step is a wrapper around 'comparison' only
        if len(ctx.comparison()) == 1:
            self.logger.debug("Single comparison in equality")
            return self.visitComparison(ctx.comparison(0))
        
        # Get the type of the left term
        left_type = self.visitComparison(ctx.comparison(0))

        # Evaluate the rest of the 'comparison' elements
        for i in range(1, len(ctx.comparison())):
            self.logger.debug(f"Visiting comparison {i} in equality")
            # Get the type of the right term
            right_type = self.visitComparison(ctx.comparison(i))
            # Get the equality operator ('==', '!=')
            operator = ctx.getChild(2 * i - 1).getText()
            # Validate the types for the equality operator are the same
            # and are either NumType or StringType
            validate_equality_type(left_type, right_type, operator) 

        return BooleanType()


        
    def visitComparison(self, ctx: compiscriptParser.ComparisonContext):
        self.logger.debug("Visiting comparison")
        # Check if there is only one 'term' element
        # meaning this step is a wrapper around 'term' only
        if len(ctx.term()) == 1:
            self.logger.debug("Single term in comparison")
            return self.visitTerm(ctx.term(0))
        
        # Get the type of the left term
        left_type = self.visitTerm(ctx.term(0))
        self.logger.debug(f"Visited left term in comparison: {left_type}")

        # Evaluate the rest of the 'term' elements
        for i in range(1, len(ctx.term())):
            self.logger.debug(f"Visiting term {i} in comparison")
            # Get the type of the right term
            right_type = self.visitTerm(ctx.term(i))
            self.logger.debug(f"Visited right term in comparison: {right_type}")
            # Get the comparison operator ('<', '>', '<=', '>=')
            operator = ctx.getChild(2 * i - 1).getText()
            # Validate the types for the comparison operator are NumType
            validate_arithmetic_type(left_type, right_type, operator, 
                                     logger=self.logger, 
                                     print_context=self.in_print_ctx,
                                     return_context=self.in_return_ctx) 

        return BooleanType()
    
        

    def visitTerm(self, ctx: compiscriptParser.TermContext):
        self.logger.debug("Visiting term")
        # Check if there is only one 'factor' element
        # meaning this step is a wrapper around 'factor' only
        if len(ctx.factor()) == 1:
            self.logger.debug("Single factor in term")
            return self.visitFactor(ctx.factor(0))
        
        # Get the type of the left term
        left_type = self.visitFactor(ctx.factor(0))
        
        # Evaluate the rest of the 'factor' elements
        for i in range(1, len(ctx.factor())):
            self.logger.debug(f"Visiting factor {i} in term")
            # Get the type of the right term
            right_type = self.visitFactor(ctx.factor(i))
            # Get the operator between the factors ('+', '-')
            operator = ctx.getChild(2 * i - 1).getText()
            # Validate the types for the arithmetic operator are NumType
            validate_arithmetic_type(left_type, right_type, operator, 
                                     logger=self.logger, 
                                     print_context=self.in_print_ctx,
                                     return_context=self.in_return_ctx)

        return NumType()
    

        
    def visitFactor(self, ctx: compiscriptParser.FactorContext):
        self.logger.debug("Visiting factor")
        # Check if there is only one 'unary' element
        # meaning this step is a wrapper around 'unary' only
        if len(ctx.unary()) == 1:
            self.logger.debug("Single unary in factor")
            return self.visitUnary(ctx.unary(0))

        # Get the type of the left term
        left_type = self.visitUnary(ctx.unary(0))

        # Evaluate the rest of the 'unary' elements
        for i in range(1, len(ctx.unary())):
            self.logger.debug(f"Visiting unary {i} in factor")
            # Get the type of the right term
            right_type = self.visitUnary(ctx.unary(i))
            # Get the operator between the factors ('*', '/', '%')
            operator = ctx.getChild(2 * i - 1).getText()
            # Validate the types for the arithmetic operator are NumType
            validate_arithmetic_type(left_type, right_type, operator, 
                                     logger=self.logger, 
                                     print_context=self.in_print_ctx,
                                     return_context=self.in_return_ctx)

        return NumType()



    def visitUnary(self, ctx: compiscriptParser.UnaryContext):
        self.logger.debug("Visiting unary")
        if ctx.call() is not None:
            self.logger.debug("Visiting call in unary")
            return self.visitCall(ctx.call())
        


    def visitCall(self, ctx: compiscriptParser.CallContext):
        self.logger.debug("Visiting call")
        if ctx.primary() is not None:
            self.logger.debug("Visiting primary in call")
            return self.visitPrimary(ctx.primary())
        


    def visitPrimary(self, ctx: compiscriptParser.PrimaryContext):
        self.logger.debug("Visiting primary")
        
        if ctx.NUMBER() is not None:
            return NumType()
        elif ctx.STRING() is not None:
            return StringType()
        elif ctx.getText() == 'true' or ctx.getText() == 'false':
            return BooleanType()
        elif ctx.getText() == 'nil' or ctx.getText() == None:
            return NilType()
        elif ctx.IDENTIFIER() is not None:
            identifier = ctx.IDENTIFIER().getText()
            self.logger.debug(f"Getting type for identifier '{identifier}'")
            variable_symbol = self.scope_manager.get_symbol(identifier, Variable)
            if variable_symbol is None:
                raise Exception(f"Variable '{identifier}' is not declared in the current scope.")
            return variable_symbol.object_type.data_type