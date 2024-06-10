import os

def stattotex(variable_name, variable_value, filename, clear_file=False):
    '''
    Function that takes a variable name and value from Python and saves it to a file that allows for easy read-in and automatic updates in LaTeX.

    Parameters:
    - variable_name: The name of the variable for the output LaTeX file
    - variable_value: The value to be saved to the file. Can be a number, number formatted as a string, or a word (numeric or string input)
    - filename: The name of the file to be saved to
    - clear_file: Default is False. If True, the file will be deleted before writing to it. If false it will not be deleted, and the new variable definition will be appended to the end of the file - still superseding any previous definition for the same variable name.
    '''

    # Creating the LaTeX command

    # Cast variable_value as string
    variable_value = str(variable_value)
    # Replace % with \% for LaTeX
    variable_value = variable_value.replace("%", "\%")

    # Throw error if variable_name contains an underscore
    if "_" in variable_name:
        raise ValueError("variable_name cannot contain an underscore. LaTeX does not allow this.")

    # Delete the file if clear_file = True
    if clear_file:
        if os.path.exists(filename):
            os.remove(filename)

    # If prior file exists
    # Check for f"\\newcommand{{\\{variable_name}}}" in the file
    # If it exists, replace the entire line with the new command
    # If it does not exist, set command = f"\\newcommand{{\\{variable_name}}}{{{variable_value}}}"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            if f"\\newcommand{{\\{variable_name}}}" in file.read():
                command = f"\\renewcommand{{\\{variable_name}}}{{{variable_value}}}"
            else:
                command = f"\\newcommand{{\\{variable_name}}}{{{variable_value}}}"
    else:
        command = f"\\newcommand{{\\{variable_name}}}{{{variable_value}}}"

    # Writing the command to the file
    with open(filename, "a") as file:
        file.write(command + "\n")
