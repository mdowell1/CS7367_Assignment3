import tkinter
from tkinter import *
from tkinter.ttk import Combobox, Label
import Tool


class Window:
    deformations = {'Create Rectangle': Tool.Rectangle,
                    'Translate': Tool.Translate, 'Rigid': Tool.Rigid, 'Similarity': Tool.Similarity,
                    'Affine': Tool.Affine, 'Projective': Tool.Projective}
    selectedDeformation = deformations['Create Rectangle']

    def __init__(self):
        self.setup_canvas_window()
        self.create_bindings()
        self.root.mainloop()

    def donothing(self):
        x = 0

    def callback_cmb_deformation(self, eventObject):
        self.selectedDeformation = self.deformations[eventObject.widget.get()]
        print(eventObject.widget.get())

    # initialize tkinter root
    root = tkinter.Tk()
    window = Canvas(root, bg="white", height=500, width=500)  # canvas info
    cmb_deformation, cmb_outline, cmb_fill = None, None, None
    curTool = Tool.Rectangle

    def onClick(self):
        self.selectedDeformation.onClick()


    def setup_canvas_window(self):
        # create main menu bar for window
        menubar = Menu(self.root)

        # create menu for 'file' option - all of these currently do nothing
        fileMenu = Menu(menubar, tearoff=0)
        fileMenu.add_command(label="New", command=self.donothing)  # create 'new' option
        fileMenu.add_command(label="Open", command=self.donothing)  # create 'open' option
        fileMenu.add_command(label="Save", command=self.donothing)  # create 'save' option
        fileMenu.add_command(label="Save As", command=self.donothing)  # create 'save as' option
        fileMenu.add_command(label="Close", command=self.donothing)  # create 'close' option
        fileMenu.add_command(label="Quit", command=self.donothing)  # create 'quit' option
        menubar.add_cascade(label="File", menu=fileMenu)  # add the file menu to the menu bar
        self.root.config(menu=menubar)  # add menu bar to config

        toolBar = Frame(self.root)  # create toolbar for dropdown boxes

        # create deformation combobox and set up the options
        lbl_deformation = Label(toolBar, text="Mode: ")  # create label
        cmb_deformation = Combobox(toolBar, width=15, textvariable=StringVar(), state="readonly")
        cmb_deformation['values'] = list(self.deformations.keys())
        lbl_deformation.pack(side=LEFT, padx=2, pady=0)  # pack the label
        cmb_deformation.pack(side=LEFT, padx=2, pady=0)  # pack the combobox
        cmb_deformation.current(0)
        cmb_deformation.bind("<<ComboboxSelected>>", self.callback_cmb_deformation)

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
        self.window.pack()  # pack the window

    def create_bindings(self):
        # lambda needed or else we get a positional argument error
        self.window.bind("<Button-1>", lambda e: self.onClick())


w = Window()
windows = [w]
