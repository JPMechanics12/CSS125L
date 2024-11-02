import operator

# Dictionary of allowed operations
operations = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '^': operator.pow
}

# Dictionary to store variables
variables = {}

def interpret_expression(expression):
    # Split the expression into components based on the operator
    for op in operations:
        if op in expression:
            left, right = expression.split(op)
            try:
                left = float(left.strip()) if left.strip() not in variables else variables[left.strip()]
                right = float(right.strip()) if right.strip() not in variables else variables[right.strip()]
                # Perform the corresponding operation
                result = operations[op](left, right)
                return result
            except ValueError:
                return "Error: Invalid number."
            except ZeroDivisionError:
                return "Error: Division by zero."
    return "Error: Unsupported operation."

def assign_variable(statement):
    # Split the assignment statement (e.g., x = 10 + 2)
    if '=' in statement:
        var_name, expression = statement.split('=')
        var_name = var_name.strip()
        expression = expression.strip()
        
        # Evaluate the expression and store the result in the variable
        result = interpret_expression(expression)
        if isinstance(result, (int, float)):
            variables[var_name] = result
            return None  # No output, just store the variable
        else:
            return result  # Return any error message
    else:
        return interpret_expression(statement)

def interpreter():
    print("Simple Arithmetic Interpreter with Variable Support. Type 'exit' to quit.")
    print("Supported operations: +, -, *, /, ^")
    
    while True:
        user_input = input(">>> ")

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Handle variable assignment or expression evaluation
        result = assign_variable(user_input)
        
        # Only print result if it's an error message
        if result is not None:
            print(result)

# Run the interpreter
interpreter()
