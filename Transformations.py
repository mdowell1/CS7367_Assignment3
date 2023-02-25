import numpy as np
import cv2

xHalf, yHalf = 0, 0


# region matrices
# get needed matrices
def translateMatrix(x, y):
    return np.array([[1, 0, x],
                     [0, 1, y],
                     [0, 0, 1]])


def rotateMatrix(x, y):
    if x < 0 or y < 0:
        angle = -0.1
    else:
        angle = 0.1

    return np.array([[np.cos(angle), -np.sin(angle), 0],
                     [np.sin(angle), np.cos(angle), 0],
                     [0, 0, 1]])


def scaleMatrix(x, y):
    if x < 0 or y < 0:
        scale = 0.9
    else:
        scale = 1.1

    return np.array([[scale, 0, 0],
                     [0, scale, 0],
                     [0, 0, 1]])


def affineMatrix(coords):
    newCoords = []
    original = []

    # affine only requires 3 points, so go to 6 instead of 8
    for i in range(1, 6, 2):
        pointRange = np.random.uniform(-5.0, 5.0, [1, 2])[0]
        original.append([coords[i-1], coords[i]])
        x = coords[i-1] + pointRange[0]
        y = coords[i] + pointRange[1]
        newCoords.append([x, y])

    M = cv2.getAffineTransform(np.float32(original), np.float32(newCoords))
    return np.vstack([M, [1, 1, 1]])  # adds row of 1s for math


def projectiveMatrix(coords):
    newCoords = []
    original = []

    # affine only requires 3 points, so go to 6 instead of 8
    for i in range(1, 8, 2):
        pointRange = np.random.uniform(-2.0, 2.0, [1, 2])[0]
        original.append([coords[i - 1], coords[i]])
        x = coords[i - 1] + pointRange[0]
        y = coords[i] + pointRange[1]

        newCoords.append([x, y])

    return cv2.getPerspectiveTransform(np.float32(original), np.float32(newCoords))


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


def rigid(coords, lastPoint, newLoc):
    # get x and y change in location
    xDif = newLoc[0] - lastPoint[0]
    yDif = newLoc[1] - lastPoint[1]

    # convert coordinates to a numpy array and reshape them for matrix math
    coordArray = coordsToMatrix(coords)
    originTranslation = translateMatrix(xHalf, yHalf)  # move translation origin to center of canvas
    returnTranslation = translateMatrix(-xHalf, -yHalf)  # move translation origin back to top left
    MT = translateMatrix(xDif, yDif)  # translation matrix
    MR = rotateMatrix(xDif, yDif)  # rotation matrix

    # first, move the coordinates to the new origin, then rotate and translate, then
    # return to the original origin, then apply changes to the original coordinates
    M = originTranslation @ MR @ MT @ returnTranslation @ coordArray

    # get the new x, y coordinates as a list
    return matrixToCoords(M)


def similarity(coords, lastPoint, newLoc):
    # get x and y change in location
    xDif = newLoc[0] - lastPoint[0]
    yDif = newLoc[1] - lastPoint[1]

    # convert coordinates to a numpy array and reshape them for matrix math
    coordArray = coordsToMatrix(coords)
    originTranslation = translateMatrix(xHalf, yHalf)  # to move translation origin to center of canvas
    returnTranslation = translateMatrix(-xHalf, -yHalf)  # to move translation origin back to top left
    MT = translateMatrix(xDif, yDif)  # translation matrix
    MR = rotateMatrix(xDif, yDif)  # rotation matrix
    MS = scaleMatrix(xDif, yDif)  # scale matrix

    # first, move the coordinates to the new origin, then scale, rotate, & translate, then
    # return to the original origin, then apply changes to the original coordinates
    M = originTranslation @ MS @ MR @ MT @ returnTranslation @ coordArray

    # get the new x, y coordinates as a list
    return matrixToCoords(M)


def affine(coords):
    # convert coordinates to a numpy array and reshape them for matrix math
    coordArray = coordsToMatrix(coords)
    MA = affineMatrix(coords)  # get the affine matrix

    # do affine transform
    M = MA @ coordArray
    return matrixToCoords(M)


def projective(coords):
    # convert coordinates to a numpy array and reshape them for matrix math
    coordArray = coordsToMatrix(coords)
    originTranslation = translateMatrix(xHalf, yHalf)  # to move translation origin to center of canvas
    returnTranslation = translateMatrix(-xHalf, -yHalf)  # to move translation origin back to top left

    MA = projectiveMatrix(coords)

    # first, move the coordinates to the new origin, then do affine transform, then
    # return to the original origin, then apply changes to the original coordinates
    M = originTranslation @ MA @ returnTranslation @ coordArray
    return matrixToCoords(M)

# endregion
