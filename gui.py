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
        self.pack()
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
        self.pack() # Pack self
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
        frm_main = MainFrame(self.master, name)
        self.grid_forget()
        print("Destroyed")
        self.destroy()

    def new(self):
        """ Summon the CreateFrame """
        frm_new = CreateFrame(self.master)
        self.grid_forget()
        print("Destroyed")
        self.destroy()




class MainFrame(ttk.Frame):
    def __init__(self, master, name):
        super().__init__(master)
        self.pack()

        self.name = name
        self.setup()

    def setup(self):
        btn_new = ttk.Button(self, text="DESTROY", command=lambda:print("BAAA!")).pack()


def main():
    """ Main function """
    root = tk.Tk()
    # frm_opening = OpeningFrame(root)
    frm = CreateFrame(root)
    root.mainloop()




if __name__ == "__main__":
    main()
