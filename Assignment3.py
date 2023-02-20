import tkinter
from tkinter import *
from tkinter.ttk import Combobox, Label


def donothing():
    x = 0


# initialize tkinter root
root = tkinter.Tk()
window = Canvas(root, bg="white", height=500, width=500)  # canvas info
cmb_deformation, cmb_outline, cmb_fill = None, None, None

def setup_canvas_window():
    # create main menu bar for window
    menubar = Menu(root)

    # create menu for 'file' option - all of these currently do nothing
    fileMenu = Menu(menubar, tearoff=0)
    fileMenu.add_command(label="New", command=donothing)  # create 'new' option
    fileMenu.add_command(label="Open", command=donothing)  # create 'open' option
    fileMenu.add_command(label="Save", command=donothing)  # create 'save' option
    fileMenu.add_command(label="Save As", command=donothing)  # create 'save as' option
    fileMenu.add_command(label="Close", command=donothing)  # create 'close' option
    fileMenu.add_command(label="Quit", command=donothing)  # create 'quit' option
    menubar.add_cascade(label="File", menu=fileMenu)  # add the file menu to the menu bar
    root.config(menu=menubar)  # add menu bar to config

    toolBar = Frame(root)  # create toolbar for dropdown boxes

    # create deformation combobox and set up the options
    lbl_deformation = Label(toolBar, text="Mode: ")  # create label
    cmb_deformation = Combobox(toolBar, width=15, textvariable=StringVar(), state="readonly")
    cmb_deformation['values'] = ('Create Rectangle', 'Translate', 'Rigid', 'Similarity', 'Affine', 'Projective')
    lbl_deformation.pack(side=LEFT, padx=2, pady=0)  # pack the label
    cmb_deformation.pack(side=LEFT, padx=2, pady=0)  # pack the combobox
    cmb_deformation.current(0)

    # create outline combobox and set up the options
    lbl_outline = Label(toolBar, text="Outline: ")  # create label
    cmb_outline = Combobox(toolBar, width=10, textvariable=StringVar(), state="readonly")
    cmb_outline['values'] = ('Black', 'White', 'Red', 'Yellow', 'Green', 'Blue', 'Cyan', 'Magenta')
    lbl_outline.pack(side=LEFT, padx=2, pady=0)  # pack the label
    cmb_outline.pack(side=LEFT, padx=2, pady=0)  # pack the combobox
    cmb_outline.current(0)

    # create fill combobox and set up the options
    lbl_fill = Label(toolBar, text="Fill: ")  # create label
    cmb_fill = Combobox(toolBar, width=10, textvariable=StringVar(), state="readonly")
    cmb_fill['values'] = ('Black', 'White', 'Red', 'Yellow', 'Green', 'Blue', 'Cyan', 'Magenta')
    lbl_fill.pack(side=LEFT, padx=2, pady=0)  # pack the label
    cmb_fill.pack(side=LEFT, padx=2, pady=0)  # pack the combobox
    cmb_fill.current(0)

    toolBar.pack()  # pack the toolbox
    window.pack()  # pack the window


if __name__ == '__main__':
    print("Hi")
    setup_canvas_window()
    root.mainloop()
