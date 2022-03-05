""" This script will create a image of chain image and will control addition to them"""

from PIL import Image, ImageDraw

# Constants
EXT = "png"
WIDTH = 100 # 100
HEIGHT = 100
COLORS = {
    "gray":(206, 206, 206), # X color
    "green":(173, 208, 172),
    "darkgreen":(102, 140, 125),
    "purple":(99, 7, 100), # Lines Color
    "dark":(53, 53, 70) # Background Color
    }

LWIDTH = 3 # Line width


def setup(name, setup_width, setup_height):
    """ Will create WxH checkerboard like image and saves it"""
    name += "."+EXT # Name and the extention
    setup_width = int(setup_width) # Make it integer
    setup_height = int(setup_height)
    width = setup_width * WIDTH # Width of the png
    height = setup_height * HEIGHT # Height of the png
    img = Image.new(mode="RGB", size=(width, height), color=COLORS["dark"]) # Make the background
    draw = ImageDraw.Draw(img) # Image draw instance
    to_draw = list() # Line draw list
    for till_width in range(1, setup_width):
        start_point = till_width * WIDTH
        to_draw.append((start_point, 0, start_point, height))
    for till_height in range(1, setup_height):
        start_point = till_height * HEIGHT
        to_draw.append((0, start_point, width, start_point))

    for draw_tuple in to_draw:
        draw.line(draw_tuple, fill=COLORS["purple"], width=1)
    img.save(name)

def add_x(name, x_pos, y_pos):
    """ Add x to the image """
    name += "."+EXT # Image to open
    img = Image.open(name) # Open the file
    draw = ImageDraw.Draw(img) # Draw object
    first = (
        x_pos * WIDTH,
        y_pos * HEIGHT,
        x_pos * WIDTH+WIDTH,
        y_pos * HEIGHT+HEIGHT
        )
    second = (
        first[0] + WIDTH,
        first[1],
        first[2] - WIDTH,
        first[3]
        )
    draw.line(first, COLORS["gray"], width=LWIDTH)
    draw.line(second, COLORS["gray"], width=LWIDTH)
    img.save(name)

def add(name, number, add_width, add_height):
    """ Find the numberth cell and add an x
        name: str name of the file
        number: int number of cell
    """
    overflow = add_width * add_height
    if number > overflow:
        print("The chains is over")
        return False
    number -= 1 # Make it usable
    y_pos = (number // add_width)
    x_pos = (number % add_width)
    # print("Number: ",number+1,x,y)
    add_x(name, x_pos, y_pos)
    return True

def test():
    setup("newdeneme",4,4)
    """ Test function """
    add("newdeneme", 5, 4, 4)
    Image.open("newdeneme"+"."+EXT).show()


if __name__ == "__main__":
    test()
