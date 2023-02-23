from abc import abstractmethod, ABC


class Tool(ABC):
    @staticmethod
    @abstractmethod
    def onClick(window, eventObject):
        print("default")

    @staticmethod
    @abstractmethod
    def onDrag(window, eventObject):
        print("default")

    @staticmethod
    @abstractmethod
    def onRelease(window, eventObject):
        print("default")


class Rectangle(Tool):
    color_outline = 'Black'
    color_fill = 'Black'

    @staticmethod
    def onClick(window, eventObject):

        rect = window.canvas.create_rectangle(eventObject.x, eventObject.y, eventObject.x,
                                              eventObject.y, fill=window.selectedFill, outline=window.selectedOutline)
        window.shapes[rect] = (eventObject.x, eventObject.y, 0, 0)
        window.numShapes += 1
        print("Rectangle onClick")

    @staticmethod
    def onDrag(window, eventObject):
        coords = window.shapes[window.numShapes]
        window.canvas.coords(window.numShapes, coords[0], coords[1], eventObject.x, eventObject.y)
        print("Rectangle onDrag")

    @staticmethod
    def onRelease(window, eventObject):
        coords = window.canvas.coords(window.numShapes)
        size = (coords[2] - coords[0], coords[3] - coords[1])
        window.shapes[window.numShapes] = (coords[0], coords[1], size[0], size[1])
        print("Rectangle onRelease")


# translate moves objects up, down, left, and right
class Translate(Tool):
    @staticmethod
    def onClick(window, eventObject):
        print("Translate onClick")

    @staticmethod
    def onDrag(window, eventObject):
        rect_id = window.canvas.find_closest(eventObject.x, eventObject.y)
        if len(rect_id) == 0:
            return
        rect_id = rect_id[0]
        coords = window.canvas.coords(rect_id)  # get recorded shape position

        # only continue if user clicked inside the object
        if coords[0] < eventObject.x < coords[2] and coords[1] < eventObject.y < coords[3]:
            dimensions = window.shapes[rect_id]  # has x0, y0, width, and height
            width = dimensions[2]
            height = dimensions[3]

            xPos = eventObject.x - width/2
            yPos = eventObject.y - height/3
            window.canvas.coords(rect_id, xPos, yPos, width + xPos, height + yPos)

    @staticmethod
    def onRelease(window, eventObject):
        print("Translate onRelease")


# rigid both translates and rotates objects
class Rigid(Tool):
    @staticmethod
    def onClick(canvas, eventObject):
        print("Rigid onClick")

    @staticmethod
    def onDrag(canvas, eventObject):
        print("Rigid onDrag")

    @staticmethod
    def onRelease(canvas, eventObject):
        print("Rigid onRelease")


class Similarity(Tool):
    @staticmethod
    def onClick(canvas):
        print("Similarity onClick")

    @staticmethod
    def onDrag(canvas):
        print("Similarity onDrag")

    @staticmethod
    def onRelease(canvas):
        print("Similarity onRelease")


class Affine(Tool):
    @staticmethod
    def onClick(canvas):
        print("Affine onClick")

    @staticmethod
    def onDrag(canvas):
        print("Affine onDrag")

    @staticmethod
    def onRelease(canvas):
        print("Affine onRelease")


class Projective(Tool):
    @staticmethod
    def onClick(canvas):
        print("Projective onClick")

    @staticmethod
    def onDrag(canvas):
        print("Projective onDrag")

    @staticmethod
    def onRelease(canvas):
        print("Projective onRelease")
