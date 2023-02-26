import numpy as np
import cv2

xHalf, yHalf = 0, 0


# region matrices
# returns the translation matrix
def translateMatrix(x, y):
    return np.array([[1, 0, x],
                     [0, 1, y],
                     [0, 0, 1]])


# returns the rotation matrix
def rotateMatrix(x, y):
    # rotates positive if mouse moving in positive direction on
    # x or y axis, negative otherwise
    if x < 0 or y < 0:
        angle = -0.1
    else:
        angle = 0.1

    return np.array([[np.cos(angle), -np.sin(angle), 0],
                     [np.sin(angle), np.cos(angle), 0],
                     [0, 0, 1]])


# returns the scale matrix
def scaleMatrix(x, y):
    # scales up if mouse moving in positive direction on x or y axis,
    # down otherwise
    if x < 0 or y < 0:
        scale = 0.9
    else:
        scale = 1.1

    return np.array([[scale, 0, 0],
                     [0, scale, 0],
                     [0, 0, 1]])


# returns the affine matrix
def affineMatrix(coords):
    newCoords = []
    original = []

    # affine only requires 3 points, so go to 6 instead of 8
    for i in range(1, 6, 2):
        # get a random x and y value to change by
        randChange = np.random.uniform(-5.0, 5.0, [1, 2])[0]
        # needed to get the original coordinates in correct format for cv2
        original.append([coords[i-1], coords[i]])
        # get new x and y coordinates and append to new coords list
        x = coords[i-1] + randChange[0]
        y = coords[i] + randChange[1]
        newCoords.append([x, y])

    # use cv2 to get the affine transformation matrix needed
    M = cv2.getAffineTransform(np.float32(original), np.float32(newCoords))
    return np.vstack([M, [1, 1, 1]])  # adds row of 1s for math and return


# returns the projective matrix
def projectiveMatrix(coords):
    newCoords = []
    original = []

    # projective needs all 4 points
    for i in range(1, 8, 2):
        # get a random x and y value to change by
        randChange = np.random.uniform(-5.0, 5.0, [1, 2])[0]
        original.append([coords[i - 1], coords[i]])

        x = coords[i - 1] + randChange[0]
        y = coords[i] + randChange[1]

        newCoords.append([x, y])

    # use cv2 to get the needed perspective transform matrix and return it
    return cv2.getPerspectiveTransform(np.float32(original), np.float32(newCoords))


# endregion

# region conversions
# change list of coords to matrix
def coordsToMatrix(coords) -> np.array:
    # convert coordinates to a numpy array and reshape them for matrix math
    coordArray = np.array(coords).reshape((2, 4), order='F')  # changes them to [x x x x], [y y y y] format
    coordArray = np.vstack([coordArray, [1, 1, 1, 1]])  # adds row of 1s for math
    return coordArray  # return new coordinates


# change coords matrix to list
def matrixToCoords(matrix) -> list:
    # loop through the given matrix and get the new x, y coordinates as a list
    newPoints = []
    for i in range(4):
        newPoints.append(matrix[0][i])  # add x value
        newPoints.append(matrix[1][i])  # add y value
    return newPoints  # return new coordinates


# endregion


# region transformations

# returns new coordinates after translation
def translate(coords, lastPoint, newLoc):
    # get x and y change in location
    xDif = newLoc[0] - lastPoint[0]
    yDif = newLoc[1] - lastPoint[1]

    # convert coordinates to a numpy array and reshape them for matrix math
    coordArray = coordsToMatrix(coords)

    # Translation matrix
    M = translateMatrix(xDif, yDif)
    translated = M @ coordArray  # @ does matrix multiplication

    # get the new x, y coordinates as a list and return
    return matrixToCoords(translated)


# returns new coordinates after rotation and translation
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

    # get the new x, y coordinates as a list and return
    return matrixToCoords(M)


# returns new coordinates after scaling, rotation, and translation
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

    # get the new x, y coordinates as a list and return
    return matrixToCoords(M)


# returns the new coordinates after semi-random affine transformation
def affine(coords):
    # convert coordinates to a numpy array and reshape them for matrix math
    coordArray = coordsToMatrix(coords)
    MA = affineMatrix(coords)  # get the affine matrix

    # multiply affine matrix by original coordinates
    M = MA @ coordArray
    return matrixToCoords(M)  # return new coords as a list


# returns the new coordinates after semi-random projective transformation
def projective(coords):
    # convert coordinates to a numpy array and reshape them for matrix math
    coordArray = coordsToMatrix(coords)
    MA = projectiveMatrix(coords)  # get the projective matrix

    # multiply projective matrix by original coordinates
    M = MA @ coordArray
    return matrixToCoords(M)  # return new coords as a list

# endregion
