""" GUI Mode for planner """
import tkinter as tk
from tkinter import ttk
import lit

class CreateFrame(ttk.Frame):
    """ Create a new task window """
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.setup()

    def setup():
        btn_submit = ttk.Button(self, text="SUBMIT", command=lambda:print("Not BAA!")).pack()

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
        self.tkvar = tk.StringVar(self.master) # Set the object you'll get the choice from
        self.tkvar.set(items[0]) # Set it's original text 
        self.drop_box = ttk.OptionMenu(self,self.tkvar, *items)
        btn_submit = ttk.Button(self, text="SUBMIT", command=self.summon)
        btn_new = ttk.Button(self, text="CREATE", command=self.new)

        self.drop_box.grid(column=0, row=0, padx=50, pady=50) # Pack the drop_box
        btn_submit.grid(column=0, row=1, padx=50, pady=(50,5)) # Pack the submit button
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
        btn_new = ttk.Button(self, text="CREATE", command=lambda:print("BAAA!")).pack()


def main():
    """ Main function """
    root = tk.Tk()
    frm_opening = OpeningFrame(root)
    root.mainloop()




if __name__ == "__main__":
    main()
