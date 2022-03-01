# Create a image of chain image

from PIL import Image, ImageDraw

# Constants
EXT="png"
WIDTH=100 # 100
HEIGHT= 100
COLORS={
    "gray":(206,206,206), # X color
    "green":(173,208,172),
    "darkgreen":(102,140,125),
    "purple":(99,7,100), # Lines Color
    "dark":(53,53,70) # Background Color
}

LWIDTH=3 # Line width


def setup(name,w, h):
    """ Will create WxH checkerboard like image and saves it"""
    name += "."+EXT # Name and the extention
    width = w * WIDTH # Width of the png
    height = h * HEIGHT # Height of the png
    img = Image.new(mode="RGB", size=(width,height),color=COLORS["dark"]) # Make the background
    draw = ImageDraw.Draw(img) # Image draw instance
    toDraw = list() # Line draw list
    for i in range(1,w):
        start_point = i*WIDTH
        toDraw.append((start_point, 0, start_point, height))
    for j in range(1,h):
        start_point = j*HEIGHT
        toDraw.append((0, start_point, width, start_point))

    for d in toDraw:
        draw.line(d, fill=COLORS["purple"], width=1)
    img.save(name)

def add_x(name, x, y):
    """ Add x to the image """
    name += "."+EXT # Image to open
    img = Image.open(name) # Open the file
    draw = ImageDraw.Draw(img) # Draw object
    first = (
            x*WIDTH,
            y*HEIGHT,
            x*WIDTH+WIDTH,
            y*HEIGHT+HEIGHT
            )
    second = (
            first[0]+WIDTH,
            first[1],
            first[2]-WIDTH,
            first[3]
            )
    draw.line(first,COLORS["gray"],width=LWIDTH)
    draw.line(second,COLORS["gray"],width=LWIDTH)
    img.save(name)

def add(name, number,w,h):
    """ Find the numberth cell and add an x
        name: str name of the file
        number: int number of cell
    """
    # TODO:Add overflow warning
    number -= 1 # Make it usable
    y = (number // w)
    x = (number % w)
    print("Number: ",number+1,x,y)
    add_x(name, x, y)

def test():
    add("planner",1,4,4)
    Image.open("planner"+"."+EXT).show()




if __name__=="__main__":
    test()









