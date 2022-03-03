""" This script handles any kind of input """
import sys

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
    answer = answer.strip() # Strip the unnecessary spaces
    answer = answer.lower() # Lower the answer so make it handle more easily?
    # Handle exits
    if not answer or answer == "exit":
        sys.exit()
    return answer

def test():
    """ Testing """
    text = handle_input("Text", end=">>")
    end = handle_input("End", end=">>")
    inputmebaby = handle_input(text=text, end=end)
    print(inputmebaby)

if __name__ == "__main__":
    while True:
        test()
