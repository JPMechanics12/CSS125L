import re
import sys
# Define token patterns
token_specification = [
    ('NUMBER',   r'\d+(\.\d*)?'),    # Integer or decimal number
    ('CIN',      r'cin'),            # 'cin' keyword
    ('COUT',     r'cout'),           # 'cout' keyword
    ('IDENT',    r'[A-Za-z_]\w*'),   # Identifiers (variable names, etc.)
    ('SHL',      r'>>'),             # Shift operator or input (cin >> x)
    ('SHR',      r'<<'),             # Shift operator or output (cout << x)
    ('OP',       r'[+\-*/=%]'),       # Arithmetic operators
    ('ASSIGN',   r'='),              # Assignment operator
    ('SEMI',     r';'),              # Semicolon
    ('NEWLINE',  r'\n'),             # Line endings
    ('SKIP',     r'[ \t]+'),         # Skip spaces and tabs
    ('STRING',   r'"[^"]*"'),        # String literals in quotes
    ('MISMATCH', r'.'),              # Any other character
]


# Compile regex
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)


def tokenize(code):
    tokens = []
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'SKIP' or kind == 'NEWLINE':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f"Unexpected character: {value}")
        tokens.append((kind, value))
    return tokens

# AST Node Class
class ASTNode:
    def __init__(self, node_type, children=None, value=None):
        self.node_type = node_type
        self.children = children if children else []
        self.value = value

# Parser Function
# Parser Function
def parse(tokens):
    index = 0
    variables = []  # Updated to store multiple string literals
    declaredvariables = []
    iterations = []
    operations = None
    counter = 0
    def parse_expression(index):
        nonlocal variables
        nonlocal iterations
        nonlocal declaredvariables
        nonlocal operations
        nonlocal counter
        # Parsing operators
        if (tokens[index][0] == 'COUT' and tokens[index + 1][0] == 'SHR' and
        tokens[index + 2][0] == 'IDENT' and tokens[index + 3][0] == 'OP' and
        tokens[index + 4][0] == 'IDENT' and tokens[index + 5][0] == 'SEMI'):
        
        # Check if we have enough values in 'iterations'
            if len(iterations) < 2:
                raise SyntaxError(f"Missing number of values at index {index}")

            # Handle addition operation
            if tokens[index + 3][1] == '+':
                value1 = tokens[index + 2][1]
                value2 = tokens[index + 4][1]

                
                
                # Ensure value1 and value2 are valid numbers (integers or stored identifiers)
                if value1 in declaredvariables and value2 in declaredvariables:
                    sum_value = iterations[declaredvariables.index(value1)] + iterations[declaredvariables.index(value2)]
                    if sum_value < 10:
                        operations = "+"
                else:
                    raise SyntaxError(f"Variables {value1} or {value2} not declared.")

                variables = sum_value
                concatenated_string = str(sum_value)  # Convert the sum to string for output
            elif tokens[index + 3][1] == '-':
                value1 = tokens[index + 2][1]
                value2 = tokens[index + 4][1]
                
                # Ensure value1 and value2 are valid numbers (integers or stored identifiers)
                if value1 in declaredvariables and value2 in declaredvariables:
                    sum_value = iterations[declaredvariables.index(value1)] - iterations[declaredvariables.index(value2)]
                    if sum_value < 10 and sum_value > 0:
                        operations = "-"
                else:
                    raise SyntaxError(f"Variables {value1} or {value2} not declared.")

                variables = sum_value
                concatenated_string = str(sum_value)  # Convert the sum to string for output
            elif tokens[index + 3][1] == '*':
                value1 = tokens[index + 2][1]
                value2 = tokens[index + 4][1]
                
                # Ensure value1 and value2 are valid numbers (integers or stored identifiers)
                if value1 in declaredvariables and value2 in declaredvariables:
                    sum_value = iterations[declaredvariables.index(value1)] * iterations[declaredvariables.index(value2)]
                else:
                    raise SyntaxError(f"Variables {value1} or {value2} not declared.")

                variables = sum_value
                concatenated_string = str(sum_value)  # Convert the sum to string for output
            elif tokens[index + 3][1] == '/':
                value1 = tokens[index + 2][1]
                value2 = tokens[index + 4][1]
                
                # Ensure value1 and value2 are valid numbers (integers or stored identifiers)
                if value1 in declaredvariables and value2 in declaredvariables:
                    sum_value = iterations[declaredvariables.index(value1)] / iterations[declaredvariables.index(value2)]
                else:
                    raise SyntaxError(f"Variables {value1} or {value2} not declared.")

                variables = sum_value
                concatenated_string = str(sum_value)  # Convert the sum to string for output
            elif tokens[index + 3][1] == '%':
                value1 = tokens[index + 2][1]
                value2 = tokens[index + 4][1]
                
                # Ensure value1 and value2 are valid numbers (integers or stored identifiers)
                if value1 in declaredvariables and value2 in declaredvariables:
                    sum_value = iterations[declaredvariables.index(value1)] % iterations[declaredvariables.index(value2)]
                else:
                    raise SyntaxError(f"Variables {value1} or {value2} not declared.")

                variables = sum_value
                concatenated_string = str(sum_value)  # Convert the sum to string for output


            counter += 1
            return ASTNode('OUTPUT', [("STRING", concatenated_string)]), index + 6
            

        
            
        if tokens[index][0] == 'IDENT' and tokens[index + 1][0] == 'ASSIGN' and tokens[index + 2][0] in ('NUMBER', 'IDENT') and tokens[index + 3][0] == 'SEMI':
            #print(f"Assignment detected: {tokens[index]} = {tokens[index + 2]}")
            counter += 1
            return ASTNode('ASSIGN', [tokens[index], tokens[index + 2]]), index + 4
        #print(f"This should be it: {tokens[index][0]} {tokens[index+1][0]} {tokens[index + 2][0]} {tokens[index + 3][0]}")
        if tokens[index][0] == 'IDENT' and tokens[index + 1][0] == 'OP' and tokens[index + 2][0] == 'NUMBER' and tokens[index + 3][0] == 'SEMI':
            testdeclaredvariables = tokens[index][1]
            testiterations = tokens[index + 2][1]
            
            if testdeclaredvariables in declaredvariables:
                index = declaredvariables.index(testdeclaredvariables)
                iterations[index] = testiterations
            else:
                declaredvariables.append(testdeclaredvariables)
                iterations.append(testiterations)


            counter += 1
            return ASTNode('ASSIGN', [tokens[index], tokens[index + 2]]), index + 4
        print(f"Declared Variables {declaredvariables}")
        print(f"Values : {iterations}")
            


        # Parsing arithmetic assignment: IDENT = IDENT OP IDENT; or IDENT = NUMBER OP NUMBER;
        if tokens[index][0] == 'IDENT' and tokens[index + 1][0] == 'ASSIGN' and tokens[index + 2][0] in ('NUMBER', 'IDENT'):
            if tokens[index + 3][0] == 'OP' and tokens[index + 4][0] in ('NUMBER', 'IDENT') and tokens[index + 5][0] == 'SEMI':
                counter += 1
                return ASTNode('ASSIGN_OP', [tokens[index], tokens[index + 2], tokens[index + 3], tokens[index + 4]]), index + 6

        # For printing expressions: cout << IDENT OP IDENT;
        if tokens[index][0] == 'COUT':
            concatenated_string = ""
            index += 1
            while index < len(tokens) and tokens[index][0] == 'SHR':
                if tokens[index + 1][0] == 'STRING':
                    string_literal = tokens[index + 1][1][1:-1]  # Remove quotes
                    concatenated_string += string_literal + " "  # Concatenate strings with a space
                    index += 2
                elif tokens[index + 1][0] == 'IDENT':
                    if tokens[index + 2][0] == 'OP' and tokens[index + 3][0] == 'IDENT':
                        # Expression like x + y
                        lhs = tokens[index + 1][1]
                        op = tokens[index + 2][1]
                        rhs = tokens[index + 3][1]
                        counter += 1
                        return ASTNode('EXPR_OUTPUT', [tokens[index + 1], tokens[index + 2], tokens[index + 3]]), index + 5
                    else:
                        variable = tokens[index + 1][1]
                        concatenated_string += variable + " "
                        index += 2
                else:
                    raise SyntaxError(f"Expected string literal or identifier after << at tokens: {tokens[index:index + 2]}")

            try:
                if tokens[index][0] == 'SEMI':
                    concatenated_string = concatenated_string.strip()  # Remove trailing space
                    variables.append(concatenated_string)  # Store the concatenated string
                    counter += 1
                    return ASTNode('OUTPUT', [("STRING", concatenated_string)]), index + 1
                else:
                    raise SyntaxError(f"Missing semicolon at the end of cout statement at tokens: {counter + 1}")
            except IndexError:
                print(f"Error! Perhaps Missing Semi-Colon at line {counter+1}")
                sys.exit(1) 



        
        # Parsing input: cin >> IDENT;
        if tokens[index][0] == 'CIN' and tokens[index + 1][0] == 'SHL' and tokens[index + 2][0] == 'IDENT' and tokens[index + 3][0] == 'SEMI':
        # Just add INPUT node with the IDENT, without prompting
            counter += 1
            return ASTNode('INPUT', [tokens[index + 2]]), index + 4

        # For printing expressions: cout << IDENT OP IDENT;
        if tokens[index][0] == 'COUT':
            concatenated_string = ""
            index += 1
            while index < len(tokens) and tokens[index][0] == 'SHR':
                if tokens[index + 1][0] == 'STRING':
                    string_literal = tokens[index + 1][1][1:-1]  # Remove quotes
                    concatenated_string += string_literal + " "  # Concatenate strings with a space
                    index += 2
                elif tokens[index + 1][0] == 'IDENT':
                    # Handle printing variables or expressions
                    if tokens[index + 2][0] == 'OP' and tokens[index + 3][0] == 'IDENT':
                        # Expression like x + y
                        lhs = tokens[index + 1][1]
                        op = tokens[index + 2][1]
                        rhs = tokens[index + 3][1]
                        counter += 1
                        return ASTNode('EXPR_OUTPUT', [tokens[index + 1], tokens[index + 2], tokens[index + 3]]), index + 5
                    else:
                        variable = tokens[index + 1][1]
                        concatenated_string += variable + " "
                        index += 2
                else:
                    raise SyntaxError(f"Expected string literal or identifier after << at tokens: {tokens[index:index + 2]}")

            # Ensure the statement ends with a semicolon
            if tokens[index][0] == 'SEMI':
                concatenated_string = concatenated_string.strip()  # Remove trailing space
                variables.append(concatenated_string)  # Store the concatenated string
                print("Gumagana ba toh")
                counter += 1
                return ASTNode('OUTPUT', [("STRING", concatenated_string)]), index + 1
            else:
                raise SyntaxError(f"Missing semicolon at the end of cout statement at tokens: {tokens[index:index + 2]}")

        # Parsing assignment: IDENT = NUMBER; or IDENT = IDENT;
        if tokens[index][0] == 'IDENT' and tokens[index + 1][0] == 'ASSIGN' and tokens[index + 2][0] in ('NUMBER', 'IDENT') and tokens[index + 3][0] == 'SEMI':
            counter += 1
            return ASTNode('ASSIGN', [tokens[index], tokens[index + 2]]), index + 4

        # Parsing arithmetic assignment: IDENT = IDENT OP IDENT; or IDENT = NUMBER OP NUMBER;
        if tokens[index][0] == 'IDENT' and tokens[index + 1][0] == 'ASSIGN' and tokens[index + 2][0] in ('NUMBER', 'IDENT'):
            if tokens[index + 3][0] == 'OP' and tokens[index + 4][0] in ('NUMBER', 'IDENT') and tokens[index + 5][0] == 'SEMI':
                counter += 1
                return ASTNode('ASSIGN_OP', [tokens[index], tokens[index + 2], tokens[index + 3], tokens[index + 4]]), index + 6
        
        raise SyntaxError(f"Invalid syntax at tokens: {tokens[index:index + 6]}")




    ast_nodes = []
    while index < len(tokens):
        try:
            ast_node, new_index = parse_expression(index)
            ast_nodes.append(ast_node)
            index = new_index
        except SyntaxError as e:
            print(f"Error while parsing: {e}")
            return None, None

    return ast_nodes, variables, iterations, declaredvariables , operations



# Intermediate Representation Generation
"""def generate_ir(ast, variables,iterations,declaredvariables, operations):
    ir = []
    symbol_table = {}  # Stores variables and their values
"""
    # Modify generate_ir to prompt once for each INPUT node
def generate_ir(ast, variables, iterations, declaredvariables, operations):
    ir = []
    symbol_table = {}

    for node in ast:
        if node.node_type == 'ASSIGN':
            lhs = node.children[0][1]
            rhs = node.children[1][1]
            symbol_table[lhs] = rhs if isinstance(rhs, (int, float)) else symbol_table.get(rhs, 0)
            ir.append(f"{lhs} = {symbol_table[lhs]}")

        elif node.node_type == 'INPUT':
            variable = node.children[0][1]
            input_value = input(f"Enter value for {variable}: ")  # Prompt here
            symbol_table[variable] = int(input_value) if input_value.isdigit() else input_value
            ir.append(f"INPUT {variable} = {input_value}")

        elif node.node_type == 'OUTPUT':
            output_expr = ""
            for child in node.children:
                if isinstance(child, ASTNode) and child.node_type == 'EXPR':
                    lhs = child.children[0][1]
                    op = child.children[1][1]
                    rhs = child.children[2][1]
                    result = eval(f"{lhs} {op} {rhs}")
                    output_expr += str(result) + " "
                else:
                    value = symbol_table.get(child[1], child[1])
                    output_expr += str(value) + " "
            ir.append(f"OUTPUT {output_expr.strip()}")

    return ir, variables, iterations, declaredvariables, operations




# Assembly Code Generation
def generate_assembly(ir, variables, iterations, declaredvariables, operations):
    assembly = [
        "section .text",
        "   org 0x100",
        "start:",
        "   mov ax,3",
        "   int 0x10",
        "main:",
        "mov ax,0000",
        "mov bx,0000",
        "mov cx,0000",
        "mov dx,0000",
    ]
    
    msg_counter = 1
    for line in ir:
        if line.startswith("INPUT"):
            continue

        elif line.startswith("OUTPUT"):
            if operations is None:
                output_value = line.split(' ', 1)[1]
                msg_label = f"msgn{msg_counter}"

                assembly.append(f"  LEA DX,[{msg_label}]")
                assembly.append(f"  mov ah,0x09")
                assembly.append(f"  int 0x21")
                
                
                

            elif operations == "+":
                assembly.append(f"  mov ax, [val1]")
                assembly.append(f"  mov bx, [val2]")
                assembly.append(f"  add ax,bx")
                assembly.append(f"  mov cx,10")
                assembly.append(f"  mov di,result_buffer")
                assembly.append(f"convert_to_ascii:")
                assembly.append(f"  XOR DX, DX")  
                assembly.append("  DIV CX")               
                assembly.append("  ADD DL, '0'")      
                assembly.append("  DEC DI")              
                assembly.append("  MOV [DI], DL")        
                assembly.append("  CMP AX, 0")            
                assembly.append("  JNE convert_to_ascii")
                assembly.append("  LEA DX, [DI]")
                assembly.append("  MOV AH, 0x09") 
                assembly.append("  INT 0x21") 
                
                # Only add newline after the result in this case
                assembly.append("  MOV AH, 0x02")
                assembly.append("  MOV DL, 0x0D") 
                assembly.append("  INT 0x21")
                assembly.append("  MOV DL, 0x0A") 
                assembly.append("  INT 0x21")
            elif operations == "-":
                assembly.append(f"  mov ax, [val1]")
                assembly.append(f"  mov bx, [val2]")
                assembly.append(f"  sub ax,bx")
                assembly.append(f"  mov cx,10")
                assembly.append(f"  mov di,result_buffer")
                assembly.append(f"convert_to_ascii:")
                assembly.append(f"  XOR DX, DX")  
                assembly.append("  DIV CX")               
                assembly.append("  ADD DL, '0'")      
                assembly.append("  DEC DI")              
                assembly.append("  MOV [DI], DL")        
                assembly.append("  CMP AX, 0")            
                assembly.append("  JNE convert_to_ascii")
                assembly.append("  LEA DX, [DI]")
                assembly.append("  MOV AH, 0x09") 
                assembly.append("  INT 0x21") 
                
                # Only add newline after the result in this case
                assembly.append("  MOV AH, 0x02")
                assembly.append("  MOV DL, 0x0D") 
                assembly.append("  INT 0x21")
                assembly.append("  MOV DL, 0x0A") 
                assembly.append("  INT 0x21")
        elif "=" in line:
            continue  # Skip assignments in assembly

    assembly.append("  int 0x20")
    assembly.append("section .data")

    if operations == "+" or operations == "-":
        assembly.append(f"val1 dw {iterations[0]}")
        assembly.append(f"val2 dw {iterations[1]}")
        assembly.append(f"result_buffer db 0, 0, 0, 0, 0, 0")

    for line in ir:
        if line.startswith("OUTPUT"):
            output_value = line.split(' ', 1)[1]
            msg_label = f"msgn{msg_counter}"

            if operations == None:
                assembly.append(f"{msg_label}: db 0x0A, 0x0D, \"{output_value} $\"")
            else:
                assembly.append(f"{msg_label}: db 0x0A, 0x0D, \" $\"")
            msg_counter += 1

    return assembly

import os
import subprocess

def asm_to_com(asm_file, com_file):
    # Check if the asm file exists
    if not os.path.exists(asm_file):
        print(f"Error: {asm_file} not found.")
        return

    # Assemble the .asm file to a .com file using NASM
    try:
        # Use NASM to create the .com file
        result = subprocess.run(['.\\nasm', '-f', 'bin', '-o', com_file, asm_file],
                                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # If NASM executed successfully, output success message
        print(f"Successfully created {com_file} from {asm_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error during assembly: {e.stderr.decode()}")

# Example usage:
asm_file = 'output.asm'
com_file = 'output.com'
asm_to_com(asm_file, com_file)







# Utility to write ASM file
def write_asm_file(filename, assembly_code):
    with open(filename, 'w') as f:
        f.write('\n'.join(assembly_code))

# Utility to read C++ file
def read_cpp_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Main Compiler Flow
if __name__ == "__main__":
    # Step 1: Read C++ code from file
    cpp_filename = "temp_code.cpp" # Change this to your C++ file name
    cpp_code = read_cpp_file(cpp_filename)
    print(f"Read C++ code from {cpp_filename}:\n{cpp_code}")

    # Step 2: Tokenize
    tokens = tokenize(cpp_code)
    print(f"Tokens: {tokens}")

    # Step 3: Parse to AST

    ast,variable1,iterations,declaredvariables, operations  = parse(tokens)
    print(f"Latest Variable1 {variable1}")
    print(f"AST: {[node.node_type for node in ast]}")

    # Step 4: Generate Intermediate Representation (IR)
    ir_code,variable1,iterations,declaredvariables, operations  = generate_ir(ast,variable1,iterations,declaredvariables, operations )
    print(f"IR: {ir_code}")
    print(f"Latest Variable1 {variable1}")
    # Step 5: Generate Assembly Code
    assembly_code = generate_assembly(ir_code,variable1,iterations,declaredvariables, operations)
    print("Assembly Code:")
    for line in assembly_code:
        print(line)

    # Step 6: Write assembly code to .asm file
    output_asm_filename = "output.asm"
    write_asm_file(output_asm_filename, assembly_code)
    print(f"Assembly code written to '{output_asm_filename}'.")     
import os
import subprocess

import os
import subprocess

def asm_to_com(asm_file, com_file):
    # Check if the asm file exists
    if not os.path.exists(asm_file):
        print(f"Error: {asm_file} not found.")
        return

    # Assemble the .asm file to a .com file using NASM
    try:
        # Use NASM to create the .com file
        result = subprocess.run(
            ['.\\nasm', '-f', 'bin', '-o', com_file, asm_file],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Print NASM output
        print(result.stdout.decode())
        print(f"Successfully created {com_file} from {asm_file}")

    except subprocess.CalledProcessError as e:
        # Print both standard output and error for troubleshooting
        print(f"NASM Output:\n{e.stdout.decode()}")
        print(f"NASM Error:\n{e.stderr.decode()}")

# Example usage
asm_file = 'output.asm'
com_file = 'output.com'
asm_to_com(asm_file, com_file)

def asm_to_com(asm_file_path):
    # Ensure NASM is installed
    if subprocess.run(["nasm", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
        print("NASM is not installed. Please install NASM and try again.")
        return

    # Define output .com file path
    com_file_path = os.path.splitext(asm_file_path)[0] + ".com"
    
    # Assemble the .asm file into a .com file
    result = subprocess.run(
        ["nasm", "-f", "bin", asm_file_path, "-o", com_file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Check result and save the .com file if successful
    if result.returncode == 0:
        if os.path.exists(com_file_path):
            print(f"Successfully saved the .com file: {com_file_path}")
        else:
            print("Failed to save the .com file.")
    else:
        print(f"Error assembling file: {result.stderr}")

# Example usage:
asm_to_com("output.asm")

