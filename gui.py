#!/usr/bin/env python3
""" GUI Mode for planner """
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msgbox
from tkinter import simpledialog as dialog
from inputs import process_input as pinp
import lit

FRAMES = list()
# WINDOW_SIZE = "300x300"

def get(widget):
    """ Takes an Entry widget and returns its text processed """
    answer = pinp(widget.get())
    return answer

def grid_me(frame):
    """ Grid given frame """
    frame.grid(column=0, row=0, sticky="nsew")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

def return_frame(root):
    """ Return to the last frame """
    new = None # Placeholder for new
    is_slaves = False # Is there any frame on window right now
    slaves = root.grid_slaves() # Get the frame on the root
    if len(FRAMES) > 1: # If there's two or more frames in FRAME list
        old = FRAMES.pop() # Get rid of last frame
        new = FRAMES[-1] # Get the new frame
        slaves[0].grid_forget() # Forget the current frame
        # new.grid(column=0, row=0, sticky="nsew") # Grid the new frame
        grid_me(new)

def add_return_frame(frm):
    """ Adds frame to the FRAMES list """
    FRAMES.append(frm)

class CreateFrame(ttk.Frame):
    """ Create a new task window """
    def __init__(self, master):
        super().__init__(master)
        self.master = master # Add master to self to call later
        self.master.title("New Task") # Set title of the window
        # self.grid(row=0, column=0, sticky="nsew")
        grid_me(self)
        self.setup() # Do the setup
        self.isButton = True
        add_return_frame(self) # Add self to the return frame
    def setup(self):
        """ Will setup an Entry widget that get names, and various header size Entry
            widget and a Button widget that'll be submitting
        """
        self.entry_name = ttk.Entry(self) # Takes how many header
        self.btn_create = ttk.Button(self, text="CREATE", command=self.set_header) # A button to set headers entry boxes
        self.btn_submit = ttk.Button(self, text="SUBMIT", command=self.create) # A button to create file currently disabled

        self.btn_submit["state"] = "disabled" # Set the submit button disable until create button clicked

        self.entry_name.grid(column=0, row=0, padx=20, pady=20) # Grid was wrong choice?
        self.btn_create.grid(column=0, row=1, padx=20, pady=20)
        self.btn_submit.grid(column=0, row=3, padx=20, pady=20)
    def set_header(self):
        """ Will create header_number times Entry widget """
        self.entry_list = list() # Entry widgets' list
        header_number = None # Takes how many headers are there
        frm_entry = ttk.Frame(self) # New frame to put on entry boxes
        try: # Try if header number is a integer if it's not return False and end this function
            header_number = int(get(self.entry_name)) # Get the header number
        except ValueError:
            msgbox.showwarning(title="Not an integer", message="This is not a integer")
            return False

        for _ in range(header_number): # Create header_number times entry boxes
            self.entry_list.append(ttk.Entry(frm_entry, width=20))
        for index, widget in enumerate(self.entry_list): # Grid entry boxes to the frame
            widget.grid(column=0, row=index)
        self.btn_submit["state"] = "active" # Make submit button clickable
        self.btn_create["state"] = "disabled" # Make create button unclickable
        # Pack those things
        frm_entry.grid(column=0, row=2)
        return True # Return true if everything is okay
    def create(self):
        """ Create the csv file """
        name = dialog.askstring("File Name", "What is the file name") # Get the name of the file using dialog
        widget_list = self.entry_list # Get the widgets
        ischains = None # Place holder for ischains
        chainsize = "" # Place holder for chainsize
        ischains = msgbox.askquestion("Chains", "Do you want to add chains") # Get ischains using msgbox
        if ischains: # If user wants chains ask for size
            chainsize = dialog.askstring("Chains", "Size of chains(widthxheight)") # TODO: Change the input type
        header_list = list() # List of the headers
        for widget in widget_list: # Get the texts from widgets
            header_list.append(get(widget))

        isitdone = lit.setup(name, header_list, chainsize) # If this is false file name is already in use
        if not isitdone: # If file exists show error and create from beginning
            msgbox.showerror("File Error", "This file already exists")
            self.set_header() # TODO:Set header_number entry box to enable/disable
    def summon_self(self):
        """ This forgets instance of the class and creates from anew """
        self.pack_forget() # Unpack from master itself
        CreateFrame(self.master) # Create new instance
        # self.destroy() # Forget itself TODO: Do not destroy for back buttons?

class OpeningFrame(ttk.Frame):
    """ If there are tasks this will enable you to choose """
    def __init__(self, master):
        self.master = master # Set master to use later
        super().__init__(master) # Init the Frame object
        self.master.title("Choose a task") # Set title of the window
        # self.grid(column=0, row=0) # Grid self
        # self.grid(row=0, column=0, sticky="nsew")
        grid_me(self)
        self.setup() # Setup the widgets
        add_return_frame(self) # Add self to the return frame

    def setup(self):
        """ Will setup a dropbox and a button to submit """
        # TODO:Add a way to remember last file choosen
        items = self.get_items()
        if not items: # If there's no item summon the CreateFrame
            self.new()
            # DEBUG
            print("There's no item here")

        frm_btn = ttk.Frame(self)
        # Tkinter widgets
        self.tkvar = tk.StringVar(self.master) # Set the object you'll get the choice from
        self.tkvar.set(items[0]) # Set it's original text 
        self.drop_box = ttk.OptionMenu(self,self.tkvar, *items)
        # BUTTONS
        self.btn_submit = ttk.Button(frm_btn, text="SUBMIT", command=self.summon)
        btn_new = ttk.Button(frm_btn, text="CREATE", command=self.new)
        btn_back = ttk.Button(frm_btn, text="BACK", command=return_frame)
        btn_show = ttk.Button(frm_btn, text="SHOW", command=self.show)

        self.drop_box.grid(column=0, row=0, padx=50, pady=50) # Pack the drop_box
        frm_btn.grid(column=0, row=1)
        self.btn_submit.pack(padx=50, pady=(50,5)) # Pack the submit button
        btn_new.pack(padx=50, pady=(5,50)) # Pack the create button
        btn_back.pack(padx=50, pady=5)
        btn_show.pack(padx=50, pady=5)

    def get_items(self):
        """ Get the csv file list """
        return list(lit.files())

    def summon(self):
        """ Summon the MainFrame """
        # DEBUG
        print(self.tkvar.get())
        name = self.tkvar.get()
        name = name.split(".")[0] # Split the name to clear .csv part
        frm_main = MainFrame(self.master, name) # Create a MainFrame and pass root and name of the file
        self.grid_forget() # Forget itself
        print("Destroyed")
        # self.destroy() # Destroy it # TODO: Use back button

    def new(self):
        """ Summon the CreateFrame """
        frm_new = CreateFrame(self.master)
        self.grid_forget()
        print("Destroyed")

    def show(self):
        """ Show the chains """
        name = self.tkvar.get() # Name on the dropbox
        name, *_ = name.split(".") # Get the name of the file
        run = lit.show_chain(name) # Get if it did show
        if not run: # If it doesn't show, show an error
            msgbox.showwarning("File Error", "There's no chains file of that")




class MainFrame(ttk.Frame):
    """ Record a task """
    def __init__(self, master, name=None):
        super().__init__(master)
        self.name = name # What is name
        is_everything_okay = self.setup()
        if not is_everything_okay:
            return None
        self.master.title("Record Task")
        add_return_frame(self) # Add self to the return frame
        # self.grid(row=0, column=0) # Grid self into root
        # self.grid(row=0, column=0, sticky="nsew")
        grid_me(self)


    def setup(self):
        """ If there's no name ask for name """
        # def save(save_list,name=None):
        if not self.name:
            # TODO: Add a way to get name
            name = None
            in_files = None
            while not name or not in_files: # In case of getting a empty string
                name = dialog.askstring("Name", "What is the name of the file you want to save?") # Ask for name
                in_files = name+".csv" in lit.files()
            self.name = name
        frm = ttk.Frame(self) # A frame for label : entry
        lbl_list = list() # List of labels widgets
        self.entry_list = list() # List of entry widgets
        header_names = lit.get_headers(self.name) # Get the headers
        if not header_names:
            msgbox.showwarning("Empty", "File is empty!")
            return False

        # Create labels entries
        for name in header_names:
            if "#" in name: # If header is a comment header do not include
                pass
            else:
                lbl = ttk.Label(frm, text=str(name)) # Label with header name on it
                lbl_list.append(lbl) # Add it to the label list
                entry = ttk.Entry(frm) # Entry
                entry.bind("<Return>", lambda event: self.save()) # Bind key Enter to save when pressed enter
                self.entry_list.append(entry) # Add it to the entry list

        self.entry_list[0].focus_set() # Set focus to the first entry

        # Pack those headers
        for index, label in enumerate(lbl_list):
            label.grid(column=0, row=index, padx=5, pady=5)
        for index, entry in enumerate(self.entry_list):
            entry.grid(column=1, row=index, padx=5, pady=5)


        # Button to submit and clear and back #TODO:Add back button functionality
        frm_button = ttk.Frame(self)

        btn_submit = ttk.Button(frm_button, text="SUBMIT", command=self.save)
        btn_clear = ttk.Button(frm_button, text="CLEAR", command=self.clear)
        btn_back = ttk.Button(frm_button, text="BACK", command=lambda:print("BAAA!"))

        btn_submit.grid(column=0, row=0, padx=5, pady=3)
        btn_clear.grid(column=0, row=1, padx=5, pady=3)
        btn_back.grid(column=0, row=2, padx=5, pady=3)

        # Pack frames
        frm.grid(column=0, row=0)
        frm_button.grid(column=0, row=1)
        return True


    def save(self):
        """ Gets entry list and saves it using lit module """
        e_list = self.entry_list
        name = self.name
        save_list = list()
        for entry in e_list:
            text = get(entry)
            if not text:
                msgbox.showwarning("No text", "You didn't fill all the file") #TODO: change text of msgbox
                return False
            save_list.append(text)
        completed = lit.save(save_list, name+".csv") # TODO: Add a constant for ".csv"
        if completed:
            msgbox.showinfo("SAVED", "You saved the file!")
        lit.handle_chain(name)
        return True
    def clear(self):
        """ Clears the entris in entry list """
        e_list = self.entry_list
        for widget in e_list:
            widget.delete(0,"end")
# def handle_chain(file, index, header): # file, index, sizex, sizey, ischain=True):

def summon_main(root):
    """ Summons the main frame onto root """
    for widget in root.grid_slaves():
        widget.grid_forget()
    MainFrame(root) # Show mainframe

def summon_create(root):
    """ Summons the create frame onto root """
    for widget in root.grid_slaves():
        widget.grid_forget()
    CreateFrame(root) # Show createframe

def summon_opening(root):
    """ Summons the opening frame onto root """
    for widget in root.grid_slaves():
        widget.grid_forget()
    OpeningFrame(root) # Show opening frame

def show_about():
    """ Show about window """
    about_text = """
Made by Mustafa Akkaya
 github.com/seckiyn/
"""
    title = "About"
    msgbox.showinfo(title, about_text)

def show_help():
    """ Show help window """
    help_text = """
This is a help text """
    title = "Help"
    msgbox.showinfo(title, help_text)



def main():
    """ Main function """
    root = tk.Tk()
    # root.geometry(WINDOW_SIZE)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    # Menu starts
    menubar = tk.Menu(root) # Main menu object
    # New Menu Dropdowns
    new_menu = tk.Menu(menubar, tearoff=0)
    new_menu.add_command(label="Main", command=lambda: summon_main(root))
    new_menu.add_command(label="Create", command=lambda: summon_create(root))
    new_menu.add_command(label="Opening", command=lambda: summon_opening(root))
    new_menu.add_separator()
    new_menu.add_command(label="Exit", command=sys.exit)

    # About menu dropdowns
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="About", command=show_about)
    help_menu.add_command(label="Help", command=show_help)

    # Back menu
    back_menu = tk.Menu(menubar, tearoff=0)
    back_menu.add_command(label="Back", command=lambda: return_frame(root))

    # Add menus to the main menu
    menubar.add_cascade(label="New", menu=new_menu) # Add new menu to the main menu
    menubar.add_cascade(label="Help", menu=help_menu) # Add help menu to the main menu
    menubar.add_cascade(label="Navigate", menu=back_menu)

    # Set the first frame
    OpeningFrame(root) # This will create a frame and show itself
    # frm = MainFrame(root, "hello")
    root.config(menu=menubar)
    root.mainloop()




if __name__ == "__main__":
    main()
