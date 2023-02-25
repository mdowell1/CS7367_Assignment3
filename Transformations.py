import numpy as np


# region matrices
# get needed matrices
def translateMatrix(x, y):
    return np.array([[1, 0, x], [0, 1, y], [0, 0, 1]])


def rotateMatrix(x, y):
    if x < 0 or y < 0:
        angle = -60
    else:
        angle = 60
    return np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])


# endregion

# region conversions
# change list of coords to matrix
def coordsToMatrix(coords) -> np.array:
    # convert coordinates to a numpy array and reshape them for matrix math
    coordArray = np.array(coords).reshape((2, 4), order='F')
    coordArray = np.vstack([coordArray, [1, 1, 1, 1]])  # adds row of 1s for math
    return coordArray


# change coords matrix to list
def matrixToCoords(matrix) -> list:
    # loop through the given matrix and get the new x, y coordinates as a list
    newPoints = []
    for i in range(4):
        newPoints.append(matrix[0][i])
        newPoints.append(matrix[1][i])
    return newPoints


# endregion


# region transformations

def translate(coords, lastPoint, newLoc) -> list:
    # get x and y change in location
    xDif = newLoc[0] - lastPoint[0]
    yDif = newLoc[1] - lastPoint[1]

    # convert coordinates to a numpy array and reshape them for matrix math
    coordArray = coordsToMatrix(coords)

    # Translation matrix
    M = translateMatrix(xDif, yDif)
    translated = M @ coordArray  # @ does matrix multiplication

    # get the new x, y coordinates as a list
    return matrixToCoords(translated)


def rotate(coords, lastPoint, newLoc):
    # get x and y change in location
    xDif = newLoc[0] - lastPoint[0]
    yDif = newLoc[1] - lastPoint[1]

    # convert coordinates to a numpy array and reshape them for matrix math
    coordArray = coordsToMatrix(coords)
    MT = translateMatrix(xDif, yDif)  # translation matrix
    MR = rotateMatrix(xDif, yDif)  # rotation matrix
    M = MR @ MT
    rigid = M @ coordArray

    # get the new x, y coordinates as a list
    return matrixToCoords(rigid)

# endregion
