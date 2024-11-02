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
