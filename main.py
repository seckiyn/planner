""" Main script """
import sys
import argparse
import lit
from inputs import handle_input as hinp


# TODO: Argument parser
def main():
    """ Main loop function """
    running = True
    while running: # Create the main loop
        answer = hinp("What should I do", end=">>") # Get the entry from user
        if answer in ("help", "h", "?"):
            lit.print_help()
        elif answer.split()[0] == "help": # Take help about functions
            func = None
            my_func = answer.split()[-1]
            try:
                func = lit.todos[my_func]
                print(func.__doc__)
            except KeyError:
                print("There's no function like that", my_func)
        else:
            lit.run_function(answer)
def args():
    """ Parse the arguments if there's any """
    # TODO: Add a way to record without entering program
    ap = argparse.ArgumentParser() # Argument parser
    ap.add_argument("-f", "--function", required=True,\
            help="Function to make") # Function argument
    args = vars(ap.parse_args()) # Parse the arguments
    function = args["function"]
    lit.run_function(function)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        args()
    else:
        main()
