import os

def stattotex(number, number_name, filename, clear_file=False):
    '''
    Function that takes number and associated name from Python and saves into a file that allows for easy read-in to LaTeX.

    Parameters:
    - number: The number to be saved to the file. Can be a number, number formatted as a string, or even a word
    - number_name: The name of the number in the LaTeX file
    - filename: The name of the file to be saved to
    - clear_file: Boolean that determines whether the file should be deleted before writing to it
    '''

    # Creating the LaTeX command

    # Cast number as string
    number = str(number)
    # Replace % with \% for LaTeX
    number = number.replace("%", "\%")

    # Throw error if number_name contains an underscore
    if "_" in number_name:
        raise ValueError("number_name cannot contain an underscore. LaTeX does not allow this.")

    # Delete the file if clear_file = True
    if clear_file:
        if os.path.exists(filename):
            os.remove(filename)

    # If prior file exists
    # Check for f"\\newcommand{{\\{number_name}}}" in the file
    # If it exists, replace the entire line with the new command
    # If it does not exist, set command = f"\\newcommand{{\\{number_name}}}{{{number}}}"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            if f"\\newcommand{{\\{number_name}}}" in file.read():
                command = f"\\renewcommand{{\\{number_name}}}{{{number}}}"
            else:
                command = f"\\newcommand{{\\{number_name}}}{{{number}}}"
    else:
        command = f"\\newcommand{{\\{number_name}}}{{{number}}}"

    # Writing the command to the file
    with open(filename, "a") as file:
        file.write(command + "\n")
