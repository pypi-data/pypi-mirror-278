import matrix
import formula
import math

def magnitude(a: list) -> float:
    return formula.pyth(formula.pyth(a[0][0], a[0][1]), a[0][2])
    
def dot(a: list, b: list) -> float:
    if(a == b):
        return magnitude(a) ** 2
    else:
        bCol = []
        for i in range(len(b[0])):
            bCol.append([b[0][i]])
        return matrix.multiplication(a, bCol)[0][0]

def angle(a: list, b: list) -> float:
    return math.acos(dot(a, b) / (magnitude(a) * magnitude(b))) / math.pi * 180

def cross(a: list, b: list) -> list:
    if(a == b):
        return [0, 0, 0]
    else:
        crossVector = []
        crossMatrix = [[1, 1, 1], a[0], b[0]]
        for i in range(3):
            crossVector.append(matrix.getCofactor(crossMatrix,0, i))
        return crossVector

def projection(a: list, b: list) -> list:
    scalar = dot(a, b) / (magnitude(b) ** 2)
    projectionVector = []
    for i in range(3):
        projectionVector.append(b[0][i] * scalar)
    return projectionVector

A = [[5, -2, 3]]
B = [[-4, 5, 7]]
print(matrix.add(A, B))