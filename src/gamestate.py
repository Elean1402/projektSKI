import numpy as np
import itertools


class GameState:
    #Constants
    #TODO: Die Werte müssen noch geändert werden, bitte Arthur fragen
    _ARR_INDEX_R = 0
    _ARR_INDEX_B = 1
    _ARR_INDEX_RR = 2
    _ARR_INDEX_BB = 3
    _ARR_INDEX_RB = 4
    _ARR_INDEX_BR = 5
    BITBOARD = np.uint64(0)
    
    
    figureStack = {_ARR_INDEX_R:1, _ARR_INDEX_B:4, _ARR_INDEX_RR:2, _ARR_INDEX_RB:5, _ARR_INDEX_BB:8, _ARR_INDEX_BR:3}
    
    @classmethod
    def createBitBoardFrom(self,matrix:np.ndarray):
        """Creates Bitboard representation from given Matrix returned by function fenToMatrix 

        Args:
            matrix (np.array): holds the game state
        return:
            List[np.uint64]: game state transformed in Bitboard representation
        """
        #revMat = np.fliplr(matrix)
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
                    case 1: bitboardArray[self._ARR_INDEX_R] = bitboardArray[self._ARR_INDEX_R] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                    case 2: bitboardArray[self._ARR_INDEX_RR] = bitboardArray[self._ARR_INDEX_RR] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                    case 3: bitboardArray[self._ARR_INDEX_BR] = bitboardArray[self._ARR_INDEX_BR] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                    case 4: bitboardArray[self._ARR_INDEX_B] = bitboardArray[self._ARR_INDEX_B] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                    case 5: bitboardArray[self._ARR_INDEX_RB] = bitboardArray[self._ARR_INDEX_RB] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
                    case 8: bitboardArray[self._ARR_INDEX_BB] = bitboardArray[self._ARR_INDEX_BB] | (np.uint64(1) << np.uint64(helperMatrix[row][col]))
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
        figures = [self._ARR_INDEX_B,self._ARR_INDEX_BR,self._ARR_INDEX_BB,self._ARR_INDEX_R,self._ARR_INDEX_RB,self._ARR_INDEX_RR]
        figures.sort()
        
        for figure in figures:
            binStringRepr = format(BB[figure],'064b')
            binMatrix = np.array(list(itertools.batched(binStringRepr,8)))
            tmp = np.zeros((8,8))
            for index,row in enumerate(binMatrix):
                tmp[index] = np.array(list(map(int,row)))
            M += tmp*self.figureStack[figure]
        return M