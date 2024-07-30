import subprocess
#import time
import os

"""

About

This program executes a given .ipynb file a certain number of times. Inputs for both programs are given before the first execution.
The .ipynb file is converted into a .py file and then executed.

execution_in_loop.py is specialized to execute quantum_key_distribution.ipynb, so it asks to the user some inputs related to quantum_key_distribution.ipynb.

You can execute quantum_key_distribution.ipynb using always the same initial key length or by using an interval: for example, analyzing key lengths from 197 to 500, executing a certain number of times per key length value (ex. 10 executions with keylength = 197, other 10 with keylength=198 and so on until 500 is executed the 10th time).

The file quantum_key_distribution.ipynb can also be executed alone, only once, without using execution_in_loop.py

Examples of inputs (in order) that can be given to execution_in_loop.py when executed:

    the .ipynb file to execute: C:\\...(insert path)...\\quantum_esame\\execution_in_loop.py

    how many times it has to be executed (per every key value): 10

    simualtor (insert 0, default value) or real quantum computer(insert 1): 0
        (if 1 is chosen instead of 0, there will be more inputs at this point, needed for the configuration)

    initial key length: e
        (it can be chosen either a number, e for the example or i for a range)
        (if i is chosen, the start and the end of the range will be required)

    Where to store the results (a .csv file is needed): C:\\...(insert path)...\\quantum_esame\\csv files\\results_of_executions.csv

"""

def executionLoop(script_name, loop_count, execute_on_which_device, token=None, key_length=None, filename = os.getcwd() + "\\results_of_executions.csv"):
    # Execution in a loop
        for i in range(loop_count):
            print("------ EXECUTION NUMBER " + str(i+1) + " ------")
            try:
                # Pass inputs to the script via stdin
                if execute_on_which_device == 1:
                    if token is not None:
                        inputs = f"{execute_on_which_device}\n{token}\n{key_length if key_length else 'e'}\n{filename}\n"
                    else:
                        inputs = f"{execute_on_which_device}\n{key_length if key_length else 'e'}\n{filename}\n"
                else:
                    inputs = f"{execute_on_which_device}\n{key_length if key_length else 'e'}\n{filename}\n"
                result = subprocess.run(["python", script_name], input=inputs, text=True)
                #time.sleep(1)  # 1 second of pause between every execution

                # Check if the subprocess exited with an error
                if result.returncode != 0:
                    print(f"Execution number {i+1} exited with an error (return code: {result.returncode}).")
                    print("Next executions won't be executed.")
                    exit()

            except Exception as e:
                print(e)
                exit()

def run_notebook_in_loop(notebook_name, loop_count, execute_on_which_device, token=None, key_length=None, filename = os.getcwd() + "\\results_of_executions.csv", given_range_begin=0,given_range_end=1):
    # Convert notebook into Python script
    if not os.path.exists(notebook_name):
        print(f"The file {notebook_name} does not exist.")
    else:
        # Convert the notebook and run it in a loop
        subprocess.run(["jupyter", "nbconvert", "--to", "script", notebook_name])

        # Obtain the name of the python script
        script_name = notebook_name.replace(".ipynb", ".py")

        if key_length == 'i':
            #all values from given_range_begin to given_range_end. For each key, there will be loop_count executions
            print("Range: " + str(given_range_begin) + " - " + str(given_range_end))
            for currentKey in range(given_range_begin,given_range_end+1):
                print("Current Key Length to test: " + str(currentKey))
                executionLoop(script_name, loop_count, execute_on_which_device, token, currentKey, filename)
        else:
            executionLoop(script_name, loop_count, execute_on_which_device, token, key_length, filename)

# Ask the user for the parameters
notebook_name = input("Insert the name (including the path) of your file, adding the extension .ipynb: ")
loop_count = int(input("Enter the number of times to run the notebook: ") or 1)
execute_on_which_device = int(input("Enter 0 to use the simulator (default). Enter 1 to use the first available real quantum computer: ") or 0)

# Ask the user if they want to insert the token
if execute_on_which_device == 1:
    use_token = input("Do you want to insert the token? Enter 'y' for yes and 'n' for no: ") or 'n'
    if use_token.lower() == 'y':
        token = input("Enter your token: ")
    else:
        print("Credentials saved on the device will be used.")
        token = None
else:
    token = None

key_length_input = input("Enter the initial key length, 'e' for default example or 'i' to select a range: ")

#default values
key_length = None
given_range_begin=None
given_range_end=None

#Managing key related inputs
if key_length_input != 'e' and key_length_input != 'i':
    key_length = int(key_length_input)

elif key_length_input == 'i':
    key_length = 'i'

    try:
        given_range_begin = int(input("Enter the first value of the range: "))
    except:
        given_range_begin = 0
        print("Error. Default value: " + str(given_range_begin))

    try:
        given_range_end = int(input("Enter the last value of the range: "))
    except:
        given_range_end = given_range_begin + 1 #executing one time by default
        print("Error. Default value: " + str(given_range_end))

else:
    key_length = 'e'

#Managing file name input
filename = str(input("Insert the name of the file (including the path) where to save your results (pressing enter will lead to use the default location, the current folder, and a default name for your file: results_of_executions.csv):"))
if not filename:
    filename = os.getcwd() + "\\results_of_executions.csv"

# Execution in a loop
try:
    run_notebook_in_loop(notebook_name, loop_count, execute_on_which_device, token, key_length, filename,given_range_begin,given_range_end)
except Exception as e:
    print(e)
