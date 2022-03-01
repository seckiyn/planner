"""
    This script will do the main work
    do -> do the given thing


"""
import csv
from inputs import handle_input as hinp
import sys
import os
import random
import chains
from PIL import Image
DEL="," # CSV Delimiter
QCHR="\"" # CSV QuoteChar
CCHR="#" # CSV Comment Char
AEXT=".md" # Advice Extention

def files(ext="csv"):
    """ Returns the file list consist of ext """
    """
    # TODO: Add a more stable way to find files
    path = sys.argv[0]
    path = os.getcwd()
    # print(path)
    file, *other= os.walk(path)
    *_, file_list = file
    csvfiles = list()
    for i in file_list: # Find csv files
        extention = str(i).split(".")[-1]
        if extention.lower() == ext.lower():
            csvfiles.append(i)
    return csvfiles
    """
    files = [f for f in os.listdir(".") if os.path.isfile(f) and f.endswith("."+ext)]
    return files


# print(*files(),sep="\n")
def setup(name="NewDoc",header_list=None,setup_chains=""):
    """ Set up a new document name: str, header_list: list"""
    # TODO: Add a warning if file is exists
    if name+".csv" in files():
        print("File already exists")
        return False
    if not header_list:
        header_list=["NoHeader"]
    if setup_chains:
        header_list.append("#"+setup_chains)
    with open(name+".csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=DEL,
                quotechar=QCHR, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header_list)

def save(save_list,name=None):
    """ Save it to the document """
    tosave = None
    if name:
        tosave = name
    if not name:
        list_of_csv = files()
        for i, j in enumerate(list_of_csv):
            print(i, j)
        answer = int(hinp("Which document"))
        tosave = list_of_csv[answer]
    with open(tosave, "a", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=DEL,
                quotechar=QCHR, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(save_list)
#DEBUG
# setup("hello",["id","mid","burada"])
# save([1,2,"here"])

def add_advice(name):
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

def stats():
    """ Analyze the data """
    pass

def add_chain(name, number,w,h):
    """ Add one to the chain """
    chains.add_chain(name, number,w,h)

def show_chain():
    file_list = files(chains.EXT) # List of the files
    print(file_list)
    for i,j in enumerate(file_list): # Print files and indexes on screen
        print(str(i)+": "+str(j))
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
    isChains = hinp("Do you want to add a chain(y/n)")
    chainsize = None
    if isChains:
        if isChains[0].lower() == "y":
            isChains = True
        elif isChains[0].lower() == "n":
            isChains = False
    if isChains:
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
    setup(name, headers,setup_chains)
    if chainsize:
        chains.setup(name, *chainsize)

def record():
    """ Record to a task """
    file_list = files() # Get the csv file list
    chain_save = 0
    for i, j in enumerate(file_list): # Print file list
        print(str(i)+": "+j)
    answer = int(hinp("Which one do you want to save")) # Ask for file
    name = file_list[answer]
    toprint = None # Header placeholder
    with open(name,"r") as file: # Check the file and get headers
        toprint = file.readline()
        i = 0
        for j in file.readlines():
            i += 1
        chain_save = i+1
        #DEBUG
        print(f"there is {i} lines here")

    print(toprint) # Print the headers 
    ###CHAINS###
    ischain = None
    chainsize = None
    my_chain = toprint.split(CCHR)
    if len(my_chain) == 2:
        chainsize = map(int, my_chain[-1].split("x"))
        ischain = True
    # TODO:Add a script that handles chain adding
    save_string = hinp("What to save(comma(,) seperated)")
    save_list = save_string.split(",")
    save(save_list,name)
    #DEBUG
    # print(f"Chain_save: {chain_save}, chainsize: {chainsize}")
    if ischain:
        chains.add(name.split(".")[0], chain_save,*chainsize)

def test():
    while True:
        record()

todos = {
        "save": save,
        "s": save,
        "addadvice": add_advice,
        "add_advice": add_advice,
        "add advice": add_advice,
        "+advice": add_advice,
        "+a": add_advice,
        "addchain": add_chain,
        "add_chain": add_chain,
        "+chain": add_chain,
        "+c": add_chain,
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

def do(todo,*args,**kwargs):
    if todo not in todos: # Check if todo in the list
        print("I can't do that")
        return False # If it's not return False
    function = todos[todo]
    function(*args,**kwargs)




if __name__=="__main__":
    test()
