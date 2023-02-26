from abc import abstractmethod, ABC

import Transformations

lastPoint = None  # to help transformations be smooth


# abstract class - needed for easy calling of methods from Window class
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


# class for creating rectangles
class Rectangle(Tool):
    @staticmethod
    def onClick(window, eventObject):
        # create a new rectangle on the canvas at the clicked point using the selected colors
        window.canvas.create_polygon(eventObject.x, eventObject.y, eventObject.x,
                                     eventObject.y, fill=window.selectedFill, outline=window.selectedOutline)
        window.numShapes += 1  # increase number of shapes

    @staticmethod
    def onDrag(window, eventObject):
        # get the coordinates of the new shape
        coords = window.canvas.coords(window.numShapes)

        # update coordinates based on mouse location
        rightX = eventObject.x
        leftX = coords[0]
        topY = coords[1]
        bottomY = eventObject.y

        # combine the new coordinates for the rectangle
        newCoords = (leftX, topY, rightX, topY, rightX, bottomY, leftX, bottomY)
        window.canvas.coords(window.numShapes, *newCoords)  # set the new coordinates for this shape

    @staticmethod
    def onRelease(window, eventObject):
        pass


# translate moves objects up, down, left, and right - follows mouse
# 2 degrees of freedom - preserves orientation
class Translate(Tool):
    @staticmethod
    def onClick(window, eventObject):
        # when clicked, get the point and record it for later
        global lastPoint
        lastPoint = (eventObject.x, eventObject.y)

    @staticmethod
    def onDrag(window, eventObject):
        # if for some reason onClick didn't fire or no object is selected, return
        global lastPoint
        if lastPoint is None or window.selectedObj is None:
            return

        coords = window.canvas.coords(window.selectedObj)  # get recorded shape position

        # get new coordinates from the translate method, then update the shape with them
        newCoords = Transformations.translate(coords, lastPoint, (eventObject.x, eventObject.y))
        window.canvas.coords(window.selectedObj, *newCoords)
        lastPoint = (eventObject.x, eventObject.y)  # update last point to be the current point

    @staticmethod
    def onRelease(window, eventObject):
        # reset the last point
        global lastPoint
        lastPoint = None


# rigid both rotates and translates objects
# 3 degrees of freedom - preserves lengths
class Rigid(Tool):
    @staticmethod
    def onClick(window, eventObject):
        global lastPoint
        lastPoint = (eventObject.x, eventObject.y)

    @staticmethod
    def onDrag(window, eventObject):
        global lastPoint
        if lastPoint is None or window.selectedObj is None:
            return

        coords = window.canvas.coords(window.selectedObj)  # get recorded shape position

        # get new coordinates from the rigid method, then update the shape with them
        newCoords = Transformations.rigid(coords, lastPoint, (eventObject.x, eventObject.y))
        window.canvas.coords(window.selectedObj, *newCoords)
        lastPoint = (eventObject.x, eventObject.y)  # update last point to be the current point

    @staticmethod
    def onRelease(window, eventObject):
        global lastPoint
        lastPoint = None


# similarity scales, rotates, and translates objects
# 4 degrees of freedom - preserves angles
class Similarity(Tool):
    @staticmethod
    def onClick(window, eventObject):
        global lastPoint
        lastPoint = (eventObject.x, eventObject.y)

    @staticmethod
    def onDrag(window, eventObject):
        global lastPoint
        if lastPoint is None or window.selectedObj is None:
            return

        coords = window.canvas.coords(window.selectedObj)  # get recorded shape position

        # get new coordinates from the similarity method, then update the shape with them
        newCoords = Transformations.similarity(coords, lastPoint, (eventObject.x, eventObject.y))
        window.canvas.coords(window.selectedObj, *newCoords)
        lastPoint = (eventObject.x, eventObject.y)  # update last point to be the current point

    @staticmethod
    def onRelease(window, eventObject):
        global lastPoint
        lastPoint = None


# affine can scale, rotate, and translate freely as long as lines remain parallel
# 6 degrees of freedom - preserves parallelism
class Affine(Tool):
    @staticmethod
    def onClick(window, eventObject):
        global lastPoint
        lastPoint = (eventObject.x, eventObject.y)

    @staticmethod
    def onDrag(window, eventObject):
        global lastPoint
        if lastPoint is None or window.selectedObj is None:
            return

        coords = window.canvas.coords(window.selectedObj)  # get recorded shape position

        # get new coordinates from the affine method, then update the shape with them
        newCoords = Transformations.affine(coords)
        window.canvas.coords(window.selectedObj, *newCoords)
        lastPoint = (eventObject.x, eventObject.y)  # update last point to be the current point

    @staticmethod
    def onRelease(window, eventObject):
        global lastPoint
        lastPoint = None


# projective/perspective can do any operation as long as the lines remain straight
# 8 degrees of freedom - preserves straight lines
class Projective(Tool):
    @staticmethod
    def onClick(window, eventObject):
        global lastPoint
        lastPoint = (eventObject.x, eventObject.y)

    @staticmethod
    def onDrag(window, eventObject):
        global lastPoint
        if lastPoint is None or window.selectedObj is None:
            return

        coords = window.canvas.coords(window.selectedObj)  # get recorded shape position

        # get new coordinates from the projective method, then update the shape with them
        newCoords = Transformations.projective(coords)
        window.canvas.coords(window.selectedObj, *newCoords)
        lastPoint = (eventObject.x, eventObject.y)  # update last point to be the current point

    @staticmethod
    def onRelease(window, eventObject):
        global lastPoint
        lastPoint = None
