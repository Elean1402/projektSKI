import numpy as np
from src.fenStringLib import*
from src.moveLib import BITBOARD

#Constants
#TODO: Die Werte müssen noch geändert werden, bitte Arthur fragen
VAL_R = 0
VAL_B = 1
VAL_RR = 2
VAL_BB = 3
VAL_RB = 4
VAL_BR = 5

def createBitBoardFrom(matrix:np.ndarray):
    """Creates Bitboard representation from given Matrix return by function fenToMatrix 

    Args:
        matrix (np.array): holds the game state
    return:
        List[np.uint64]: game state transformed in Bitboard representation
    """
    revMat = np.fliplr(matrix)
    # Reihenfolge noch nicht klar..
    bitboardArray = [BITBOARD,BITBOARD,BITBOARD,BITBOARD,BITBOARD,BITBOARD]
    # the helperMatrix contains the exponents..
    helperMatrix = np.zeros((8,8))
    val = -1
    for x in range(helperMatrix.shape[0]):
        for y in range(helperMatrix.shape[1]):
           val +=1
           helperMatrix[x][y] = val 
    
    helperMatrix = np.fliplr(np.fliplr(helperMatrix.transpose()).transpose())
    print(helperMatrix)
    print("hmatrix val:",helperMatrix[0][1])
    if matrix.shape != helperMatrix.shape:
        raise Exception("shapes of Matrix and Helpermatrix incompatible")
    
    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            match matrix[row][col]:
                case 1: bitboardArray[VAL_R] = bitboardArray[VAL_R] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                case 2: bitboardArray[VAL_RR] = bitboardArray[VAL_RR] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                case 3: bitboardArray[VAL_BR] = bitboardArray[VAL_BR] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                case 4: bitboardArray[VAL_B] = bitboardArray[VAL_B] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                case 5: bitboardArray[VAL_RB] = bitboardArray[VAL_RB] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                case 8: bitboardArray[VAL_BB] = bitboardArray[VAL_BB] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                case _: continue

    return bitboardArray

