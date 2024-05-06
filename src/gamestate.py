import numpy as np
import itertools
import sys


minimum_version = (3,12)
if sys.version_info < minimum_version:
    sys.exit("You need Python 3.12")

class GameState:
    #Constants
    #TODO: Die Werte müssen noch geändert werden, bitte Arthur fragen
    #wenn die Werte geändert werden, muss die fromBitBoardToMatrix() angepasst werden
    _ARR_INDEX_R = 0
    _ARR_INDEX_RR = 1
    _ARR_INDEX_BR = 2
    _ARR_INDEX_B = 3
    _ARR_INDEX_BB = 4
    _ARR_INDEX_RB = 5
    
    # for Zuggenerator, these indices will be used in an Array. Attention the indices must be consecutively e.g. 0,1,2,3,4 and starting from 0
    _ZARR_INDEX_R_PAWNS = 0
    _ZARR_INDEX_R_KNIGHTS = 1
    _ZARR_INDEX_B_PAWNS = 2
    _ZARR_INDEX_B_KNIGHTS = 3
    
    BITBOARD = np.uint64(0)
    
    
    figureStack = {_ARR_INDEX_R:1, _ARR_INDEX_B:4, _ARR_INDEX_RR:2, _ARR_INDEX_RB:5, _ARR_INDEX_BB:8, _ARR_INDEX_BR:3}
    
    @classmethod
    def createBitBoardFrom(self,matrix:np.ndarray,mode=False):
        """Creates Bitboard representation from given Matrix returned by function fenToMatrix 

        Args:
            matrix (np.array): holds the game state
            mode: boolean: False for constructing GUI
                           True for Zuggenerator
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
        
        if( mode == True):
            #Bitboard adjustments for Zuggenerator
            # rr : set at pos x pawn and knight
            bitboardArray[self._ARR_INDEX_R] = bitboardArray[self._ARR_INDEX_RR] | bitboardArray[self._ARR_INDEX_R]
            # bb : analogous to rr 
            bitboardArray[self._ARR_INDEX_B] = bitboardArray[self._ARR_INDEX_BB] | bitboardArray[self._ARR_INDEX_B]
            # rb : set at pos x pawn (red) and knight (top, blue)
            bitboardArray[self._ARR_INDEX_R] = bitboardArray[self._ARR_INDEX_RB] | bitboardArray[self._ARR_INDEX_R]
            # br : set at pos x pawn (blue) and knight (top,red)
            bitboardArray[self._ARR_INDEX_B] = bitboardArray[self._ARR_INDEX_BR] | bitboardArray[self._ARR_INDEX_B]
            
            bBoardZuggen = np.array([self.BITBOARD,self.BITBOARD,self.BITBOARD,self.BITBOARD])
            bBoardZuggen[self._ZARR_INDEX_R_PAWNS] = bitboardArray[self._ARR_INDEX_R]
            bBoardZuggen[self._ZARR_INDEX_R_KNIGHTS] = bitboardArray[self._ARR_INDEX_RR] | bitboardArray[self._ARR_INDEX_BR]
            bBoardZuggen[self._ZARR_INDEX_B_PAWNS] = bitboardArray[self._ARR_INDEX_B]
            bBoardZuggen[self._ZARR_INDEX_B_KNIGHTS] = bitboardArray[self._ARR_INDEX_BB] | bitboardArray[self._ARR_INDEX_RB]
            return bBoardZuggen
            
        return bitboardArray
    
    @classmethod
    def fromBitBoardToMatrix(self,BB:list, mode=False):
        """Creates Matrix for Game state

        Args:
            BB (list[np.uint64]): Bitboards
            mode : False: for GUI usage
                   True: BB is output from Zuggenerator

        Returns:
            np.ndarray: Matrix as a game state
        """
        M = np.zeros((8,8))

        #TODO
        if(mode == False):
            figures = [self._ARR_INDEX_B,self._ARR_INDEX_BR,self._ARR_INDEX_BB,self._ARR_INDEX_R,self._ARR_INDEX_RB,self._ARR_INDEX_RR]
            figures.sort()
        
            for figure in figures:
                binStringRepr = format(BB[figure],'064b')
                binMatrix = np.array(list(itertools.batched(binStringRepr,8)))
                tmp = np.zeros((8,8))
                for index,row in enumerate(binMatrix):
                    tmp[index] = np.array(list(map(int,row)))
                M += tmp*self.figureStack[figure]
        
        else:
            if(BB.shape[0] != 4):
                raise ValueError(self, "Bitboardarray lengths not equal 4, check output of Zuggenerator")
            
            r = BB[self._ZARR_INDEX_R_PAWNS] & ~BB[self._ZARR_INDEX_R_KNIGHTS] & ~BB[self._ZARR_INDEX_B_KNIGHTS]
            rr =  BB[self._ZARR_INDEX_R_PAWNS] & BB[self._ZARR_INDEX_R_KNIGHTS]
            br = BB[self._ZARR_INDEX_B_PAWNS] & BB[self._ZARR_INDEX_R_KNIGHTS]
            
            b = BB[self._ZARR_INDEX_B_PAWNS] & ~ BB[self._ZARR_INDEX_B_KNIGHTS] & ~BB[self._ZARR_INDEX_R_KNIGHTS]
            bb =BB[self._ZARR_INDEX_B_PAWNS] & BB[self._ZARR_INDEX_B_KNIGHTS]
            rb = BB[self._ZARR_INDEX_R_PAWNS] & BB[self._ZARR_INDEX_B_KNIGHTS]
            
            figures = [r,rr,br,b,bb,rb]
            
            for index,figure in enumerate(figures):
                binStringRepr = format(figure, '064b')
                binMatrix = np.array(list(itertools.batched(binStringRepr,8)))
                tmp = np.zeros((8,8))
                for i,row in enumerate(binMatrix):
                    tmp[i] = np.array(list(map(int,row)))
                print("Mtemp:\n",M)    
                print(figure,"tmp\n",tmp,"\nfigVal\n",self.figureStack[index])
                M += tmp*self.figureStack[index]
        
        return M
                