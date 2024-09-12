import subprocess
import os
import sys

def compile_qrc_to_py(qrc_file:str, output_file="resources_rc.py"):
    """
    Compiles the .qrc file to a Python file using pyside6-rcc.

    Args:
        qrc_file (str): The path to the .qrc file.
        output_file (str, optional): The output .py file name (default: resources_rc.py).
    """
    # Check if pyside6-rcc is available
    try:
        subprocess.run(['pyside6-rcc', '--version'], check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("Error: pyside6-rcc is not installed or not in PATH.")
        sys.exit(1)
    
    # Check if the .qrc file exists
    if not os.path.exists(qrc_file):
        print(f"Error: The qrc file '{qrc_file}' does not exist.")
        sys.exit(1)
    
    # Build the command to run
    command = ['pyside6-rcc', qrc_file, '-o', output_file]
    
    try:
        # Run the pyside6-rcc command
        subprocess.run(command, check=True)
        print(f"Successfully compiled '{qrc_file}' to '{output_file}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to compile the .qrc file. {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Default .qrc file name
    qrc_file = "resources.qrc"
    
    # Optionally take the .qrc file name as an argument
    if len(sys.argv) > 1:
        qrc_file = sys.argv[1]
    
    compile_qrc_to_py(qrc_file)
