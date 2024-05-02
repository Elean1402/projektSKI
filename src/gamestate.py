import numpy as np
import itertools


class GameState:
    #Constants
    #TODO: Die Werte müssen noch geändert werden, bitte Arthur fragen
    VAL_R = 0
    VAL_B = 1
    VAL_RR = 2
    VAL_BB = 3
    VAL_RB = 4
    VAL_BR = 5
    BITBOARD = np.uint64(0)
    
    
    figureStack = {VAL_R:1, VAL_B:4, VAL_RR:2, VAL_RB:5, VAL_BB:8, VAL_BR:3}
    
    @classmethod
    def createBitBoardFrom(self,matrix:np.ndarray):
        """Creates Bitboard representation from given Matrix returned by function fenToMatrix 

        Args:
            matrix (np.array): holds the game state
        return:
            List[np.uint64]: game state transformed in Bitboard representation
        """
        revMat = np.fliplr(matrix)
        # Reihenfolge noch nicht klar..
        bitboardArray = [self.BITBOARD,self.BITBOARD,self.BITBOARD,self.BITBOARD,self.BITBOARD,self.BITBOARD]
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
        
        #figureState = {1: True, }
        for row in range(matrix.shape[0]):
            for col in range(matrix.shape[1]):
                match matrix[row][col]:
                    case 1: bitboardArray[self.VAL_R] = bitboardArray[self.VAL_R] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                    case 2: bitboardArray[self.VAL_RR] = bitboardArray[self.VAL_RR] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                    case 3: bitboardArray[self.VAL_BR] = bitboardArray[self.VAL_BR] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                    case 4: bitboardArray[self.VAL_B] = bitboardArray[self.VAL_B] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                    case 5: bitboardArray[self.VAL_RB] = bitboardArray[self.VAL_RB] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                    case 8: bitboardArray[self.VAL_BB] = bitboardArray[self.VAL_BB] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                    case _: continue

        return bitboardArray
    
    @classmethod
    def fromBitBoardToMatrix(self,BB:list):
        """Creates Matrix for Game state

        Args:
            BB (list[np.uint64]): Bitboards

        Returns:
            np.ndarray: Matrix as a game state
        """
        M = np.zeros((8,8))

        #TODO
        figures = [self.VAL_B,self.VAL_BR,self.VAL_BB,self.VAL_R,self.VAL_RB,self.VAL_RR]
        figures.sort()
        
        for figure in figures:
            binStringRepr = format(BB[figure],'064b')
            binMatrix = np.array(list(itertools.batched(binStringRepr,8)))
            tmp = np.zeros((8,8))
            for index,row in enumerate(binMatrix):
                tmp[index] = np.array(list(map(int,row)))
            M += tmp*self.figureStack[figure]
        return M