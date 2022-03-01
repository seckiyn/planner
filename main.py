import save
import lit
from inputs import handle_input as hinp


def main():
    running = True
    while running: # Create the main loop
        answer = hinp("What should I do", end=">>") # Get the entry from user
        if answer in ("help","h","?"): # 
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
            lit.do(answer)

if __name__=="__main__":
    main()
