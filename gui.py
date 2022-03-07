""" GUI Mode for planner """
import tkinter as tk
import lit
from tkinter import ttk
from tkinter import messagebox as msgbox
from tkinter import simpledialog as dialog

# def setup(name="NewDoc",header_list=None,setup_chains=""):
# FRAMES TODO
# ADD BACK BUTTONS
# ADD CLEAR BUTTONS
class CreateFrame(ttk.Frame):
    """ Create a new task window """
    def __init__(self, master):
        super().__init__(master)
        self.master = master # Add master to self to call later
        self.master.title("New Task") # Set title of the window
        self.grid(row=0, column=0)
        self.setup() # Do the setup
        self.isButton = True

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
            header_number = int(self.entry_name.get()) # Get the header number
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
            header_list.append(widget.get())

        isitdone = lit.setup(name, header_list, chainsize) # If this is false file name is already in use
        if not isitdone: # If file exists show error and create from beginning
            msgbox.showerror("File Error", "This file already exists")
            self.set_header() # TODO:Set header_number entry box to enable/disable
    def summon_self(self):
        """ This forgets instance of the class and creates from anew """
        self.pack_forget() # Unpack from master itself
        CreateFrame(self.master) # Create new instance
        self.destroy() # Forget itself TODO: Do not destroy for back buttons?

class OpeningFrame(ttk.Frame):
    """ If there are tasks this will enable you to choose """
    def __init__(self, master):
        self.master = master # Set master to use later
        super().__init__(master) # Init the Frame object
        self.grid(column=0, row=0) # Grid self
        self.setup() # Setup the widgets

    def setup(self):
        """ Will setup a dropbox and a button to submit """
        # TODO:Add a way to remember last file choosen
        items = self.get_items()
        if not items: # If there's no item summon the CreateFrame
            self.new()
            # DEBUG
            print("There's no item here")

        # Tkinter widgets
        self.tkvar = tk.StringVar(self.master) # Set the object you'll get the choice from
        self.tkvar.set(items[0]) # Set it's original text 
        self.drop_box = ttk.OptionMenu(self,self.tkvar, *items)
        self.btn_submit = ttk.Button(self, text="SUBMIT", command=self.summon)
        btn_new = ttk.Button(self, text="CREATE", command=self.new)

        self.drop_box.grid(column=0, row=0, padx=50, pady=50) # Pack the drop_box
        self.btn_submit.grid(column=0, row=1, padx=50, pady=(50,5)) # Pack the submit button
        btn_new.grid(column=0, row=2, padx=50, pady=(5,50)) # Pack the create button

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
        self.destroy() # Destroy it # TODO: Use back button

    def new(self):
        """ Summon the CreateFrame """
        frm_new = CreateFrame(self.master)
        self.grid_forget()
        print("Destroyed")
        self.destroy()




class MainFrame(ttk.Frame):
    def __init__(self, master, name=None):
        super().__init__(master)
        self.grid(row=0, column=0)
        self.name = name
        """

        if self.name: # If name is given
            s_name = self.name.split(".") # If name is a file remove the extension
            if len(s_name) > 1:
                self.name = "".join(self.name.split[:-1])
            elif s_name == 1:
                self.name = s_name[0]
        """
        # DEBUG
        print(self.name)
        self.setup()

    def setup(self):
        """ If there's no name ask for name """
        # def save(save_list,name=None):
        if not self.name:
            # TODO: Add a way to get name
            name = None
            while not name: # In case of getting a empty string
                name = dialog.askstring("Name", "What is the name of the file you want to save?") # Ask for name
            self.name = name
        frm = ttk.Frame(self) # A frame for label : entry
        lbl_list = list() # List of labels widgets
        self.entry_list = list() # List of entry widgets
        header_names = lit.get_headers(self.name) # Get the headers

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


    def save(self):
        """ Gets entry list and saves it using lit module """
        e_list = self.entry_list
        name = self.name
        save_list = list()
        for entry in e_list:
            text = entry.get()
            if not text:
                msgbox.showwarning("No text", "You didn't fill all the file") #TODO: change text of msgbox
                return False
            save_list.append(text)
        completed = lit.save(save_list, name+".csv") # TODO: Add a constant for ".csv"
        if completed:
            msgbox.showinfo("SAVED", "You saved the file!")
    def clear(self):
        """ Clears the entris in entry list """
        e_list = self.entry_list
        for widget in e_list:
            widget.delete(0,"end")


def summon_main(root):
    """ Summons the main frame onto root """
    for widget in root.grid_slaves():
        widget.grid_forget()
    frm = MainFrame(root)

def summon_create(root):
    """ Summons the create frame onto root """
    for widget in root.grid_slaves():
        widget.grid_forget()
    frm = CreateFrame(root)

def summon_opening(root):
    """ Summons the opening frame onto root """
    for widget in root.grid_slaves():
        widget.grid_forget()
    frm = OpeningFrame(root)

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


import sys
def main():
    """ Main function """
    root = tk.Tk()
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

    # Add menus to the main menu
    menubar.add_cascade(label="New", menu=new_menu) # Add new menu to the main menu
    menubar.add_cascade(label="Help", menu=help_menu) # Add help menu to the main menu

    # Set the first frame
    # frm_opening = OpeningFrame(root)
    frm = MainFrame(root, "hello")
    root.config(menu=menubar)
    root.mainloop()




if __name__ == "__main__":
    main()
