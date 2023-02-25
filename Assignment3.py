import os.path
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox, Label
import Tool
import json

canvas_size = (700, 700)


def create_json(window, filename):
    with open(filename, 'w') as f:
        for item in window.canvas.find_all():
            print(json.dumps({
                'coords': window.canvas.coords(item),
                'fill': window.canvas.itemconfig(item)['fill'][-1],
                'outline': window.canvas.itemconfig(item)['outline'][-1]
            }), file=f)


class Window:
    deformations = {'Translate': Tool.Translate, 'Rigid': Tool.Rigid, 'Similarity': Tool.Similarity,
                    'Affine': Tool.Affine, 'Projective': Tool.Projective}

    global canvas_size

    # initialize tkinter root
    root = tkinter.Tk()
    canvas = Canvas(root, bg="white", height=canvas_size[1], width=canvas_size[0])  # canvas info
    cmb_deformation, cmb_outline, cmb_fill = None, None, None
    curTool = Tool.Rectangle
    selectedDeformation = deformations['Translate']  # deformations['Create Rectangle']
    selectedFill = 'Black'
    selectedOutline = 'Black'
    newShapes = {}
    numShapes = 0
    drawing = False
    cornerClicked = False
    selectedObj = None

    def __init__(self):
        self.setup_canvas_window()
        self.create_bindings()
        self.clear_canvas()

    def clear_canvas(self):
        self.canvas.delete('all')
        self.root.mainloop()

    def save_canvas_default(self):
        i = 0
        while os.path.exists('newCanvas%s.json' % i):
            i += 1
        filename = 'newCanvas%s.json' % i
        create_json(self, filename)
        print("save to {0}".format(filename))

    def save_canvas_ask(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("json files", "*.json")])
        print("save to {0}".format(filename))

    def load_canvas(self):
        filename = filedialog.askopenfilename()
        self.canvas.delete('all')
        with open(filename) as f:
            for line in f:
                item = json.loads(line)
                self.canvas.create_polygon(*item["coords"], fill=item['fill'], outline=item['outline'])
                self.numShapes += 1
        print("save")

    def get_selected_object(self, eventObject):
        nearest = self.canvas.find_closest(eventObject.x, eventObject.y)
        if len(nearest) == 0:
            return
        coords = self.canvas.coords(nearest[0])
        if coords[0] < eventObject.x < coords[2] and coords[1] < eventObject.y < coords[5]:
            self.selectedObj = nearest

    def callback_cmb_deformation(self, eventObject):
        self.selectedDeformation = self.deformations[eventObject.widget.get()]

    def callback_cmb_outline(self, eventObject):
        self.selectedOutline = eventObject.widget.get()
        print(self.selectedOutline)

    def callback_cmb_fill(self, eventObject):
        self.selectedFill = eventObject.widget.get()
        print(self.selectedFill)

    def onClick(self, eventObject):
        self.get_selected_object(eventObject)
        self.check_if_corner(eventObject)
        self.selectedDeformation.onClick(self, eventObject)

    def onDrag(self, eventObject):
        if self.drawing:
            Tool.Rectangle.onDrag(self, eventObject)
        elif not self.cornerClicked:
            self.selectedDeformation.onDrag(self, eventObject)

    def onRelease(self, eventObject):
        self.selectedObj = None
        if self.drawing:
            self.drawing = False
            Tool.Rectangle.onRelease(self, eventObject)
        else:
            self.cornerClicked = False
            self.selectedDeformation.onRelease(self, eventObject)

    def onShiftClick(self, eventObject):
        self.drawing = True
        Tool.Rectangle.onClick(self, eventObject)
        print("shift click")

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
            print("Clicked top left corner")

        # check if bottom left corner
        if coords[7] - dist <= eventObject.y <= coords[7] + dist and coords[6] - dist <= eventObject.x <= coords[
            6] + dist:
            self.cornerClicked = True
            print("Clicked bottom left corner")

        # check if on top right corner
        if coords[3] - dist <= eventObject.y <= coords[3] + dist and coords[2] - dist <= eventObject.x <= coords[
            2] + dist:
            self.cornerClicked = True
            print("Clicked top right corner")

        # check if bottom right corner
        if coords[5] - dist <= eventObject.y <= coords[5] + dist and coords[4] - dist <= eventObject.x <= coords[
            4] + dist:
            self.cornerClicked = True
            print("Clicked bottom right corner")

    def setup_canvas_window(self):
        # create main menu bar for window
        menubar = Menu(self.root)

        # create menu for 'file' option - all of these currently do nothing
        fileMenu = Menu(menubar, tearoff=0)
        fileMenu.add_command(label="New", command=self.clear_canvas)  # create 'new' option
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
        cmb_deformation.current(0)
        cmb_deformation.bind("<<ComboboxSelected>>", self.callback_cmb_deformation)

        # create outline combobox and set up the options
        lbl_outline = Label(toolBar, text="Outline: ")  # create label
        cmb_outline = Combobox(toolBar, width=10, textvariable=StringVar(), state="readonly")
        cmb_outline['values'] = ('Black', 'White', 'Red', 'Yellow', 'Green', 'Blue', 'Cyan', 'Magenta')
        lbl_outline.pack(side=LEFT, padx=2, pady=0)  # pack the label
        cmb_outline.pack(side=LEFT, padx=2, pady=0)  # pack the combobox
        cmb_outline.current(0)
        cmb_outline.bind("<<ComboboxSelected>>", self.callback_cmb_outline)

        # create fill combobox and set up the options
        lbl_fill = Label(toolBar, text="Fill: ")  # create label
        cmb_fill = Combobox(toolBar, width=10, textvariable=StringVar(), state="readonly")
        cmb_fill['values'] = ('Black', 'White', 'Red', 'Yellow', 'Green', 'Blue', 'Cyan', 'Magenta')
        lbl_fill.pack(side=LEFT, padx=2, pady=0)  # pack the label
        cmb_fill.pack(side=LEFT, padx=2, pady=0)  # pack the combobox
        cmb_fill.current(0)
        cmb_fill.bind("<<ComboboxSelected>>", self.callback_cmb_fill)

        toolBar.pack()  # pack the toolbox
        self.canvas.pack()  # pack the window

    def create_bindings(self):
        # lambda needed or else we get a positional argument error
        self.canvas.bind("<Button-1>", self.onClick)
        self.canvas.bind("<ButtonRelease-1>", self.onRelease)
        self.canvas.bind("<B1-Motion>", self.onDrag)
        self.canvas.bind("<Shift-1>", self.onShiftClick)
        self.canvas.bind("<KeyRelease-Shift_L>", self.onShiftClick)
        self.canvas.bind("<KeyRelease-Shift_R>", self.onShiftClick)


w = Window()
windows = [w]
