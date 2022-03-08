""" This script handles any kind of input """
import sys
import datetime

# CONSTANTS
BANG_CHR="!" # Bang chr

insert_list = {
        "d": datetime.date.today,
        "k": lambda:"Now it's viable"
        }

def insert(count, string):
    """ Delete count and count+1'th characters from string """
    new_string = string
    bang = string[count+1:count+2]
    inserting = ""
    try:
        inserting = str(insert_list[bang]())
    except KeyError:
        print("Bang doesn't exists")
    new_string = new_string[:count] + inserting + new_string[count+2:]
    return new_string

def control_bangs(string):
    """ A function to control special characters in headers """
    new_string = string
    counts = list()
    while BANG_CHR in new_string:
        for i,j in enumerate(new_string):
            if j == BANG_CHR:
                new_string = insert(i, new_string)
                break
    return new_string

def process_input(answer):
    """ Process input and return processed input """
    answer = answer.strip() # Strip the unnecessary spaces
    answer = answer.lower() # Lower the answer so make it handle more easily?
    return_answer = control_bangs(answer)
    return return_answer
# TODO: Add bangs handle to here
def handle_input(text=None, end=":"):
    """
        Asks for input and returns the input text as wanted
        text: string ([text]: [userinput])
    """
    # Check if input pretext is viable
    if not text:
        text = "Your Input" + end # If there's no text
    else:
        text = text + str(end) + " " # If there's text adds end symbol and a space

    answer = input(text)
    answer = process_input(answer)
    if not answer or answer == "exit":
        sys.exit()
    return answer

def test():
    """ Testing """
    print(handle_input("Hello", end=" >>>"))

if __name__ == "__main__":
    while True:
        test()
