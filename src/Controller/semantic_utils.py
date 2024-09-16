from Model.data_types import BooleanType, NumType, StringType

def validate_logical_types(left_type, right_type, operator):
    """
    Validate that both types are BooleanType for logical operators ('and', 'or').
    """
    if not isinstance(left_type, BooleanType) or not isinstance(right_type, BooleanType):
        raise Exception(f"Type mismatch: Operator '{operator}' requires boolean operands, found '{left_type}' and '{right_type}'")


def validate_arithmetic_type(left_type, right_type, operator, logger, print_context):
    """
    Validate that both types are NumType for arithmetic operators ('+', '-', '*', '/', '%') 
    or comparison operators ('<', '>', '<=', '>=').
    """
    # Check if the + operator is being used and print the context 
    if operator == '+' and print_context:
        logger.debug("Operator '+' is being used as a concatenation operator.")
        return
    
    if not isinstance(left_type, NumType) or not isinstance(right_type, NumType):
        raise Exception(f"Type mismatch: Operator '{operator}' requires numeric operands, found '{left_type}' and '{right_type}'")


def validate_equality_type(left_type, right_type, operator):
    """
    Validate that both types are the same for equality operators ('==', '!=').
    Only NumType or StringType can be compared.
    """
    if not isinstance(left_type, type(right_type)):
        raise Exception(f"Type mismatch: Cannot compare '{left_type}' with '{right_type}' using '{operator}'")

    if not isinstance(left_type, (NumType, StringType)):
        raise Exception(f"Type mismatch: Operator '{operator}' requires operands to be either both numbers or both strings, found '{left_type}' and '{right_type}'")


def validate_boolean_expression_type(expression_type, extra_message=""):
    """
    Validate that the expression type is BooleanType.
    """
    if not isinstance(expression_type, BooleanType):
        raise Exception(f"Type mismatch: Expected boolean expression{extra_message}")
    

def validate_num_expression_type(expression_type, extra_message=""):
    """
    Validate that the expression type is NumType.
    """
    if not isinstance(expression_type, NumType):
        raise Exception(f"Type mismatch: Expected numeric expression{extra_message}")