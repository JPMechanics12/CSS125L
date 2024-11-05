import os

def run_ms_dos_file(file_path):
    try:
        # Open the file using the default associated application
        os.startfile(file_path)
    except OSError as e:
        print(f"Error running file: {e}")

# Specify the path to the MS-DOS file you want to run
ms_dos_file_path = r'output.com'

run_ms_dos_file(ms_dos_file_path)