from abc import abstractmethod, ABC
import numpy as np

lastPoint = None


def coordsToMatrix(coords) -> np.array:
    # convert coordinates to a numpy array and reshape them for matrix math
    coordArray = np.array(coords).reshape((2, 4), order='F')
    coordArray = np.vstack([coordArray, [1, 1, 1, 1]])  # adds row of 1s for math
    return coordArray


def matrixToCoords(matrix) -> list:
    # loop through the given matrix and get the new x, y coordinates as a list
    newPoints = []
    for i in range(4):
        newPoints.append(matrix[0][i])
        newPoints.append(matrix[1][i])
    return newPoints


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
        rect = window.canvas.create_polygon(eventObject.x, eventObject.y, eventObject.x,
                                            eventObject.y, fill=window.selectedFill, outline=window.selectedOutline)
        window.newShapes[rect] = (eventObject.x, eventObject.y, 0, 0)
        window.numShapes += 1

    @staticmethod
    def onDrag(window, eventObject):
        coords = window.newShapes[window.numShapes]
        x2 = eventObject.x
        y2 = coords[1]
        x3 = coords[0]
        y3 = eventObject.y

        newCoords = (coords[0], coords[1], x2, y2, eventObject.x, eventObject.y, x3, y3)
        print(newCoords)
        window.canvas.coords(window.numShapes, *newCoords)

    @staticmethod
    def onRelease(window, eventObject):
        coords = window.canvas.coords(window.numShapes)
        if coords[0] > coords[2]:  # if shape was drawn left to right, fix coordinates
            newRight = coords[0]
            newLeft = coords[2]
            coords[0] = newLeft
            coords[2] = newRight
            coords[4] = newRight
            coords[6] = newLeft

        if coords[1] > coords[5]:  # if shape was drawn down to up, fix coordinates
            newTop = coords[5]
            newBottom = coords[1]
            coords[1] = newTop
            coords[3] = newTop
            coords[5] = newBottom
            coords[7] = newBottom

        size = (coords[2] - coords[0], coords[5] - coords[1])
        window.newShapes[window.numShapes] = (coords[0], coords[1], size[0], size[1])
        window.canvas.coords(window.numShapes, *coords)
        print(window.canvas.type(1))


# translate moves objects up, down, left, and right
class Translate(Tool):
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

        # get new coordinates from the translate method, then update the shape with them
        newCoords = Transformations.translate(coords, (eventObject.x, eventObject.y))
        window.canvas.coords(window.selectedObj, *newCoords)
        lastPoint = (eventObject.x, eventObject.y)  # update last point to be the current point

    @staticmethod
    def onRelease(window, eventObject):
        global lastPoint
        lastPoint = None


# rigid both translates and rotates objects
class Rigid(Tool):
    @staticmethod
    def onClick(window, eventObject):
        global lastPoint
        lastPoint = (eventObject.x, eventObject.y)
        print("Rigid onClick")

    @staticmethod
    def onDrag(window, eventObject):
        global lastPoint
        if lastPoint is None or window.selectedObj is None:
            return

        coords = window.canvas.coords(window.selectedObj)  # get recorded shape position

        # get new coordinates from the rotate method
        rotateCoords = Transformations.rotate(coords, (eventObject.x, eventObject.y))

        # get new coordinates from the translate method, then update the shape with them
        newCoords = Transformations.translate(rotateCoords, (eventObject.x, eventObject.y))
        window.canvas.coords(window.selectedObj, *newCoords)
        lastPoint = (eventObject.x, eventObject.y)  # update last point to be the current point

        print("Rigid onDrag")

    @staticmethod
    def onRelease(window, eventObject):
        global lastPoint
        lastPoint = None
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


class Transformations:

    @staticmethod
    def translate(coords, newLoc) -> list:
        # get x and y change in location
        xDif = newLoc[0] - lastPoint[0]
        yDif = newLoc[1] - lastPoint[1]

        # convert coordinates to a numpy array and reshape them for matrix math
        coordArray = coordsToMatrix(coords)

        # Translation matrix
        M = np.array([[1, 0, xDif], [0, 1, yDif], [0, 0, 1]])
        translated = M @ coordArray  # @ does matrix multiplication

        # get the new x, y coordinates as a list
        return matrixToCoords(translated)

    @staticmethod
    def rotate(coords, newLoc):
        # get x and y change in location
        xDif = newLoc[0] - lastPoint[0]
        yDif = newLoc[1] - lastPoint[1]

        if xDif < 0 or yDif < 0:
            angle = -180
        elif xDif > 0 or yDif > 0:
            angle = 180
        else:
            return coords

        # convert coordinates to a numpy array and reshape them for matrix math
        coordArray = coordsToMatrix(coords)

        # Rotation matrix
        M = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
        translated = M @ coordArray  # @ does matrix multiplication
        # get the new x, y coordinates as a list
        return matrixToCoords(translated)


identityMatrix = [[1, 0], [0, 1]]
