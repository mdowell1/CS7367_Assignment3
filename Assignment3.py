import json
import os.path
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox, Label
import Tool
import Transformations

# canvas info
canvas_size = (700, 700)
Transformations.xHalf = canvas_size[0] / 2
Transformations.yHalf = canvas_size[1] / 2


# create json file to save canvas
def create_json(window, filename):
    with open(filename, 'w') as f:  # create/open the file to write to
        for item in window.canvas.find_all():  # loop through all canvas objects
            print(json.dumps({  # create json of each item
                'coords': window.canvas.coords(item),  # include coordinates
                'fill': window.canvas.itemconfig(item)['fill'][-1],  # include fill color
                'outline': window.canvas.itemconfig(item)['outline'][-1]  # include outline color
            }), file=f)


# class for the main window
class Window:
    # region initialize variables
    deformations = {'Translate': Tool.Translate, 'Rigid': Tool.Rigid, 'Similarity': Tool.Similarity,
                    'Affine': Tool.Affine, 'Projective': Tool.Projective}
    global canvas_size
    root = tkinter.Tk()  # initialize tkinter root
    canvas = Canvas(root, bg="white", height=canvas_size[1], width=canvas_size[0])  # canvas info
    cmb_deformation, cmb_outline, cmb_fill = None, None, None  # start with no selected items in comboboxes
    selectedDeformation = deformations['Translate']  # start with translate tool selected
    selectedFill = 'Black'  # set default colors
    selectedOutline = 'Black'
    cornerClicked = False
    selectedCorner = None
    numShapes = 0  # record number of shapes (really records last used index)
    drawing = False  # not currently drawing
    selectedObj = None  # no object selected yet

    # endregion

    def __init__(self):  # initialize window
        self.setup_canvas_window()
        self.create_bindings()
        self.root.mainloop()

    # region save and load
    # saves the canvas to a default file - for 'save' option
    def save_canvas_default(self):
        i = 0  # starting with 0, find the next available file name to prevent overwriting
        while os.path.exists('newCanvas%s.json' % i):
            i += 1
        filename = 'newCanvas%s.json' % i  # get the file name + json extension
        create_json(self, filename)  # create the file

    # saves the canvas to a provided file - for 'save as' option
    def save_canvas_ask(self):
        # get the selected file name, make sure only .json is allowed
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("json files", "*.json")])
        create_json(self, filename)  # create the file

    # loads a canvas from a json file
    def load_canvas(self):
        filename = filedialog.askopenfilename()  # get the file
        if filename == '':  # in case user cancels
            return
        self.canvas.delete('all')  # delete everything on this canvas
        with open(filename) as f:  # open the file to read
            for line in f:  # read each line (json)
                item = json.loads(line)  # get the item recorded
                # create a new polygon with the recorded info
                self.canvas.create_polygon(*item["coords"], fill=item['fill'], outline=item['outline'])
                self.numShapes += 1  # increase number of shapes (really total count of all shapes - needed for indexing)

    # endregion

    # region combobox events
    # choosing the transformation
    def callback_cmb_deformation(self, eventObject):
        self.selectedDeformation = self.deformations[eventObject.widget.get()]

    # choosing the outline color
    def callback_cmb_outline(self, eventObject):
        self.selectedOutline = eventObject.widget.get()
        print(self.selectedOutline)

    # choosing the fill color
    def callback_cmb_fill(self, eventObject):
        self.selectedFill = eventObject.widget.get()
        print(self.selectedFill)

    # endregion

    # region mouse and key events
    def onClick(self, eventObject):  # when user clicks
        self.get_selected_object(eventObject)  # get clicked object
        self.check_if_corner(eventObject)  # check if a corner was clicked
        if self.cornerClicked:
            Tool.Translate.onClick(self, eventObject)
        else:
            self.selectedDeformation.onClick(self, eventObject)  # call onClick for the selected transformation

    def onDrag(self, eventObject):  # when user drags mouse
        if self.drawing:  # if currently drawing, call rectangle ondrag
            Tool.Rectangle.onDrag(self, eventObject)
        elif self.cornerClicked:
            Tool.Translate.onDrag(self, eventObject)
        else:  # if not currently drawing, call onDrag for the selected transformation
            self.selectedDeformation.onDrag(self, eventObject)

    def onRelease(self, eventObject):
        self.selectedObj = None  # reset selections
        self.selectedCorner = None
        self.drawing = False

        if self.cornerClicked:  # if we were moving a corner, call onRelease for the translate tool
            self.cornerClicked = False
            Tool.Translate.onRelease(self, eventObject)

        # if we were not drawing call onRelease for the selected transformation
        elif not self.drawing:
            self.selectedDeformation.onRelease(self, eventObject)

    def onShiftClick(self, eventObject):  # when user presses shift
        self.drawing = True  # allows them to draw rectangle
        Tool.Rectangle.onClick(self, eventObject)  # call rectangle onClick

    # endregion

    # method to get the object the user clicked
    def get_selected_object(self, eventObject):
        # find nearest items to click point
        nearest = self.canvas.find_closest(eventObject.x, eventObject.y)
        if len(nearest) == 0:  # if no item found, return
            return

        # get coordinates of first item in nearest list
        coords = self.canvas.coords(nearest[0])

        # get the min and max x and y values to check if user clicked inside the shape
        xMin = min(coords[0], coords[2], coords[4], coords[6])
        xMax = max(coords[0], coords[2], coords[4], coords[6])
        yMin = min(coords[1], coords[3], coords[5], coords[7])
        yMax = max(coords[1], coords[3], coords[5], coords[7])

        # if user clicked in the shape's range, set the selected object to this one
        if xMin < eventObject.x < xMax and yMin < eventObject.y < yMax:
            self.selectedObj = nearest

    def check_if_corner(self, eventObject):
        shape = self.canvas.find_closest(eventObject.x, eventObject.y)
        if len(shape) == 0:
            return

        coords = self.canvas.coords(shape[0])
        dist = 4

        # check if on top left corner
        if coords[1] - dist <= eventObject.y <= coords[1] + dist and coords[0] - dist <= eventObject.x <= coords[
            0] + dist:
            self.cornerClicked = True
            self.selectedCorner = 0
            print("Clicked top left corner")

        # check if bottom left corner
        if coords[7] - dist <= eventObject.y <= coords[7] + dist and coords[6] - dist <= eventObject.x <= coords[
            6] + dist:
            self.cornerClicked = True
            self.selectedCorner = 3
            print("Clicked bottom left corner")

        # check if on top right corner
        if coords[3] - dist <= eventObject.y <= coords[3] + dist and coords[2] - dist <= eventObject.x <= coords[
            2] + dist:
            self.cornerClicked = True
            self.selectedCorner = 1
            print("Clicked top right corner")

        # check if bottom right corner
        if coords[5] - dist <= eventObject.y <= coords[5] + dist and coords[4] - dist <= eventObject.x <= coords[
            4] + dist:
            self.cornerClicked = True
            self.selectedCorner = 2
            print("Clicked bottom right corner")

    # region setup
    def setup_canvas_window(self):
        # create main menu bar for window
        menubar = Menu(self.root)

        # create menu for 'file' option - all of these currently do nothing
        fileMenu = Menu(menubar, tearoff=0)
        fileMenu.add_command(label="New", command=lambda: self.canvas.delete('all'))  # create 'new' option
        fileMenu.add_command(label="Open", command=self.load_canvas)  # create 'open' option
        fileMenu.add_command(label="Save", command=self.save_canvas_default)  # create 'save' option
        fileMenu.add_command(label="Save As", command=self.save_canvas_ask)  # create 'save as' option
        fileMenu.add_command(label="Close", command=exit)  # create 'close' option
        fileMenu.add_command(label="Quit", command=exit)  # create 'quit' option
        menubar.add_cascade(label="File", menu=fileMenu)  # add the file menu to the menu bar
        self.root.config(menu=menubar)  # add menu bar to config

        toolBar = Frame(self.root)  # create toolbar for dropdown boxes

        # create deformation combobox and set up the options
        lbl_deformation = Label(toolBar, text="Mode: ")  # create label
        cmb_deformation = Combobox(toolBar, width=15, textvariable=StringVar(), state="readonly")
        cmb_deformation['values'] = list(self.deformations.keys())
        lbl_deformation.pack(side=LEFT, padx=2, pady=0)  # pack the label
        cmb_deformation.pack(side=LEFT, padx=2, pady=0)  # pack the combobox
        cmb_deformation.current(0)  # currently on first item
        cmb_deformation.bind("<<ComboboxSelected>>",
                             self.callback_cmb_deformation)  # set event for when item is changed

        # create outline combobox and set up the options
        lbl_outline = Label(toolBar, text="Outline: ")  # create label
        cmb_outline = Combobox(toolBar, width=10, textvariable=StringVar(), state="readonly")  # create combobox
        cmb_outline['values'] = ('Black', 'White', 'Red', 'Yellow', 'Green', 'Blue', 'Cyan', 'Magenta')
        lbl_outline.pack(side=LEFT, padx=2, pady=0)  # pack the label
        cmb_outline.pack(side=LEFT, padx=2, pady=0)  # pack the combobox
        cmb_outline.current(0)
        cmb_outline.bind("<<ComboboxSelected>>", self.callback_cmb_outline)

        # create fill combobox and set up the options
        lbl_fill = Label(toolBar, text="Fill: ")  # create label
        cmb_fill = Combobox(toolBar, width=10, textvariable=StringVar(), state="readonly")  # create combobox
        cmb_fill['values'] = ('Black', 'White', 'Red', 'Yellow', 'Green', 'Blue', 'Cyan', 'Magenta')
        lbl_fill.pack(side=LEFT, padx=2, pady=0)  # pack the label
        cmb_fill.pack(side=LEFT, padx=2, pady=0)  # pack the combobox
        cmb_fill.current(0)
        cmb_fill.bind("<<ComboboxSelected>>", self.callback_cmb_fill)

        toolBar.pack()  # pack the toolbox
        self.canvas.pack()  # pack the window

    # creates event bindings for each mouse event and shift click
    def create_bindings(self):
        self.canvas.bind("<Button-1>", self.onClick)
        self.canvas.bind("<ButtonRelease-1>", self.onRelease)
        self.canvas.bind("<B1-Motion>", self.onDrag)
        self.canvas.bind("<Shift-1>", self.onShiftClick)
        self.canvas.bind("<KeyRelease-Shift_L>", self.onShiftClick)
        self.canvas.bind("<KeyRelease-Shift_R>", self.onShiftClick)

    # endregion


# window that will run
w = Window()
