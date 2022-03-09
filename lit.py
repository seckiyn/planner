"""
    This script will do the main work
    do -> do the given thing
    add !d to just add day
"""
import csv
import os
from PIL import Image
import chains
import inputs
from inputs import handle_input as hinp

# import datetime
# import sys
# import random
DEL = "," # CSV Delimiter
QCHR = "\"" # CSV QuoteChar
CCHR = "#" # CSV Comment Char
AEXT = ".md" # Advice Extention
BANG_CHR = "!" # Bang chr

def files(ext="csv"):
    """ Returns the file list consist of ext """
    file = [f for f in os.listdir(".") if os.path.isfile(f) and f.endswith("."+ext)]
    return file

def get_headers(file_name):
    """ Returns the headers as list of a file """
    with open(file_name+".csv", "r", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=DEL,\
                quotechar=QCHR, quoting=csv.QUOTE_MINIMAL)
        header = next(reader)
        return header

# print(*files(),sep="\n")
def setup(name="NewDoc", header_list=None, setup_chains=""):
    """ Set up a new document name: str, header_list: list"""
    if name+".csv" in files(): # Give a warning and return False if file already exists
        print("File already exists")
        return False
    if not header_list:
        header_list = ["NoHeader"]
    if setup_chains:
        header_list.append("#" + setup_chains)
        chains.setup(name, *setup_chains.split("x"))
    with open(name+".csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=DEL,\
                quotechar=QCHR, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header_list)

    return True # Return a true if everything is complete

def save(save_list, name=None):
    """ Save it to the document """
    tosave = None # Saving file name
    if name: # If there's a name saving gile name is name
        tosave = name
    if not name: # If there's not a name let user choose
        list_of_csv = files() # Get the list of .csv files
        for i, j in enumerate(list_of_csv): # Print files to user to pic
            print(i, j)
        answer = int(hinp("Which document")) # Take an answer
        tosave = list_of_csv[answer] # File name is choosen file name
    with open(tosave, "a", newline="") as csvfile: # Open file and write save_list using csv writer
        writer = csv.writer(csvfile, delimiter=DEL,\
                quotechar=QCHR, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(save_list)
    return True
#DEBUG
# setup("hello",["id","mid","burada"])
# save([1,2,"here"])

def add_advice(name):
    """ Adds advice to the name file """
    with open(name+AEXT, "a") as file:
        answer = hinp("What should I add")
        file.write(answer+"\n")
#DEBUG
# add_advice("hello")

def advice(name):
    """ Show one advice """
    list_of_advices = list()
    with open(name+AEXT, "r") as file:
        for line in file.readlines():
            list_of_advices.append(line[:-1]) # Remove line character
            print("list of advices: ", list_of_advices)

#DEBUG
# advice("hello")

def stats(name):
    """ Analyze the data """
    print(name)

# def add_chain(name, number, width, height):
#     """ Add one to the chain """
#     chains.add_chain(name, number, width, height)

def show_chain():
    """ Shows chain image """
    file_list = files(chains.EXT) # List of the files
    print(file_list)
    for index, file in enumerate(file_list): # Print files and indexes on screen
        print(str(index)+": "+str(file))
    index = int(hinp("Which one")) # Get the input
    file_name = file_list[index] # Filename
    img = Image.open(file_name)
    img.show()

def print_help():
    """ Prints a help text """
    help_text = """
Type:
    help --> Get this help text
    new or n --> Create a new task
    entry or e --> Enter a new task?
    help [function_name] --> Get help about specific function
    """
    print(help_text)
# show_chain()

def new():
    """ Create a new task """
    name = hinp("What is the name of the task")
    header_string = hinp("What are headers(comma(,) seperated)")
    headers = header_string.split(",")
    is_chains = hinp("Do you want to add a chain(y/n)")
    chainsize = None
    if is_chains:
        if is_chains[0].lower() == "y":
            is_chains = True
        elif is_chains[0].lower() == "n":
            is_chains = False
    if is_chains:
        running = True
        while running: # Try it till get a answer
            chainsize = hinp("What is the chain size(widthxheight)")
            try:
                chainsize = tuple(map(int, chainsize.split("x")))
                running = False
            except ValueError:
                print("Wrong!")
    # Setup everything
    setup_chains = "x".join(map(str, chainsize))
    setup_done = setup(name, headers, setup_chains)
    if chainsize and setup_done:
        chains.setup(name, *chainsize)

def handle_headers(string):
    """ Takes string of words seperated with commas and process it and returns a list """
    raw_list = string.split(",") # Seperate by commas
    header_list = list() # Header list
    for head in raw_list:
        s_head = head.strip() # Strip to get rid of spaces
        s_head = inputs.control_bangs(s_head) # Control if we should add something
        header_list.append(s_head)
    return header_list

def handle_chain(file, index=None, header=None): # file, index, sizex, sizey, ischain=True):
    """ Get's the file: str, index: int, header: str and process them """
    file = str(file)
    if not index or not header:
        with open(file+".csv", "r") as csvfile:
            my_header = csvfile.readline()
            i = 0
            for _ in csvfile.readlines():
                i += 1
            index = i
            header = my_header
    s_header = header.split(CCHR) # Take the header and split for any command
    ischain = None
    sizex = None
    sizey = None
    if len(s_header) == 2: # Is there any chain
        ischain = True
        sizex, sizey = s_header[-1].split("x") # Split it into sizex and sizey
    if not ischain: # If there's no chain just return False
        return False

    name = file.split(".")[0] # Name of the file
    sizex = int(sizex) # Turn str sizes to integer
    sizey = int(sizey)
    chains.add(name, index, sizex, sizey) # Save them using chains
    return True # Return true

def record():
    """ Record to a task """
    file_list = files() # Get the csv file list
    chain_index = 0
    for i, j in enumerate(file_list): # Print file list
        print(str(i)+": "+j)
    answer = int(hinp("Which one do you want to save")) # Ask for file
    name = file_list[answer]
    first_header = None # Header placeholder
    with open(name, "r") as file: # Check the file and get headers
        first_header = file.readline()
        i = 0
        for j in file.readlines():
            i += 1
        chain_index = i+1

    print(*(first_header.split(",")), sep="   |   ") # Print the headers

    save_string = hinp("What to save(comma(,) seperated)") # Ask for the list with commas
    save_list = handle_headers(save_string) # Handle the list with commas
    save(save_list, name) # Save it using save function
    handle_chain(name, chain_index, first_header) # Handle the chain if necessary

def test():
    """ Test function """
    while True:
        ans = hinp("Bang control")
        print(inputs.control_bangs(ans))

TO_DOS = {
        "save": save,
        "s": save,
        "addadvice": add_advice,
        "add_advice": add_advice,
        "add advice": add_advice,
        "+advice": add_advice,
        "+a": add_advice,
        "showchain": show_chain,
        "show_chain": show_chain,
        "sc": show_chain,
        "new": new,
        "setup":new,
        "record":record,
        "r":record,
        "entry":record,
        "e":record
        }

"""
        "addchain": add_chain,
        "add_chain": add_chain,
        "+chain": add_chain,
        "+c": add_chain,
"""
def run_function(todo, *args, **kwargs):
    """ Runs given function """
    if todo not in TO_DOS: # Check if todo in the list
        print("I can't do that")
        return False # If it's not return False
    function = TO_DOS[todo]
    function(*args, **kwargs)
    return True




if __name__ == "__main__":
    test()
