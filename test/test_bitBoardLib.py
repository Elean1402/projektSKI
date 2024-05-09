import unittest
from src.gamestate import*
from src.gui import*
import itertools

class BitBoardLib(unittest.TestCase):
    def test_createBitBoardFrom1(self):
        M = Gui.fenToMatrix("r05/8/8/8/8/8/8/8")
        BB = GameState.createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[GameState._ARR_INDEX_R], 2**62)
    
    def test_createBitBoardFrom2(self):
        M = Gui.fenToMatrix("5r0/8/8/8/8/8/8/8")
        BB = GameState.createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[GameState._ARR_INDEX_R], 2**57)
        
    def test_createBitBoardFrom3(self):
        M = Gui.fenToMatrix("6/8/8/8/8/8/8/5r0")
        BB = GameState.createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[GameState._ARR_INDEX_R], 2**1)
    
    def test_createBitBoardFrom3(self):
        M = Gui.fenToMatrix("6/8/8/8/8/8/8/r05")
        BB = GameState.createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[GameState._ARR_INDEX_R], 2**6)
        
    def test_createBitBoardFrom4(self):
        M = Gui.fenToMatrix("rr5/8/8/8/8/8/8/6")
        BB = GameState.createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[GameState._ARR_INDEX_RR], 2**62)
        
    def test_createBitBoardFrom4(self):
        M = Gui.fenToMatrix("6/6rr1/8/8/8/8/5rr2/6")
        BB = GameState.createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[GameState._ARR_INDEX_RR], 2**49+2**10)
    
    def test_createBitBoardFrom5(self):
        M = Gui.fenToMatrix("6/6rb1/8/8/8/8/5rb2/6")
        BB = GameState.createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[GameState._ARR_INDEX_RB], 2**49+2**10)
        
    def test_createBitBoardFrom6(self):
        M = Gui.fenToMatrix("6/6br1/8/8/8/8/5br2/6")
        BB = GameState.createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[GameState._ARR_INDEX_BR], 2**49+2**10)
        
    def test_createBitBoardFrom7(self):
        M = Gui.fenToMatrix("6/6bb1/8/8/8/8/5bb2/6")
        BB = GameState.createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[GameState._ARR_INDEX_BB], 2**49+2**10)


    
    def test_createBitBoardFrom6(self):
        M = Gui.fenToMatrix("1b0b01rr1/rrbbrbbr4/8/8/8/8/5b02/1b0b01rr1")
        BB = GameState.createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[GameState._ARR_INDEX_RR], 2**58+2**55+2**2)
        self.assertEqual(BB[GameState._ARR_INDEX_R], 0)
        self.assertEqual(BB[GameState._ARR_INDEX_B], 2**61+2**60+2**10+2**5+2**4)
        self.assertEqual(BB[GameState._ARR_INDEX_RB], 2**53)
        self.assertEqual(BB[GameState._ARR_INDEX_BR], 2**52)
        self.assertEqual(BB[GameState._ARR_INDEX_BB], 2**54)

    def test_fromBitBoardToMatrix1(self):
        BB = list([np.uint64(0),np.uint64(0),np.uint64(0),np.uint64(0),np.uint64(0),np.uint64(0)])
        BB[GameState._ARR_INDEX_R]= np.uint64(2)
        M=GameState.fromBitBoardToMatrix(BB)
        print("computed Matrix:\n",M)
        target= np.array([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0]])
        self.assertEqual(np.allclose(M,target),True)
        
    def test_fromBitBoardToMatrix2(self):
        targetMatrix= Gui.fenToMatrix("r05/8/8/8/8/8/8/6")
        BB= GameState.createBitBoardFrom(targetMatrix)
        M=GameState.fromBitBoardToMatrix(BB)
        print("computed Matrix:\n",M)
        self.assertEqual(np.allclose(M,targetMatrix),True)
    
    def test_fromBitBoardToMatrix3(self):
        targetMatrix= Gui.fenToMatrix("r05/2rrbbrbbr2/2r0r0rr1b0b0/bb7/1bb6/br7/8/6")
        BB= GameState.createBitBoardFrom(targetMatrix)
        M=GameState.fromBitBoardToMatrix(BB)
        print("computed Matrix:\n",M)
        self.assertEqual(np.allclose(M,targetMatrix),True)
    
    
    def test_createBitBoardFromMatrix_Zuggenerator1(self):
        """Pawn Test"""
        M = Gui.fenToMatrix("r5/8/8/8/8/8/8/8")
        BB = GameState.createBitBoardFrom(M,True)
        M2 = GameState.fromBitBoardToMatrix(BB,True)
        print("M:\n",M)
        print("M2:\n",M2)
        self.assertEqual(np.allclose(M,M2),True)
    
    def test_createBitBoardFromMatrix_Zuggenerator2(self):
        """Pawn Test"""
        M = Gui.fenToMatrix("5r/8/8/8/8/8/8/8")
        BB = GameState.createBitBoardFrom(M,True)
        M2 = GameState.fromBitBoardToMatrix(BB,True)
        print("M:\n",M)
        print("M2:\n",M2)
        self.assertEqual(np.allclose(M,M2),True)
    
    def test_createBitBoardFromMatrix_Zuggenerator3(self):
        """Pawn Test"""
        M = Gui.fenToMatrix("b5/8/8/8/8/8/8/5r")
        BB = GameState.createBitBoardFrom(M,True)
        M2 = GameState.fromBitBoardToMatrix(BB,True)
        print("M:\n",M)
        print("M2:\n",M2)
        self.assertEqual(np.allclose(M,M2),True)
        
    def test_createBitBoardFromMatrix_Zuggenerator4(self):
        """rr Test"""
        M = Gui.fenToMatrix("rr5/8/8/8/8/8/8/6")
        BB = GameState.createBitBoardFrom(M,True)
        M2 = GameState.fromBitBoardToMatrix(BB,True)
        print("M:\n",M)
        print("M2:\n",M2)
        self.assertEqual(np.allclose(M,M2),True)
    
    def test_createBitBoardFromMatrix_Zuggenerator5(self):
        """rr Test"""
        M = Gui.fenToMatrix("rr4rr/8/8/8/8/8/8/rr1rr3")
        BB = GameState.createBitBoardFrom(M,True)
        M2 = GameState.fromBitBoardToMatrix(BB,True)
        print("M:\n",M)
        print("M2:\n",M2)
        self.assertEqual(np.allclose(M,M2),True)
    
    def test_createBitBoardFromMatrix_Zuggenerator6(self):
        """bb Test"""
        M = Gui.fenToMatrix("rr4rr/8/8/bb3bb3/8/8/8/rr1rr3")
        BB = GameState.createBitBoardFrom(M,True)
        M2 = GameState.fromBitBoardToMatrix(BB,True)
        print("M:\n",M)
        print("M2:\n",M2)
        self.assertEqual(np.allclose(M,M2),True)
        
    def test_createBitBoardFromMatrix_Zuggenerator7(self):
        """rb Test"""
        M = Gui.fenToMatrix("rb5/8/8/8/8/8/8/6")
        BB = GameState.createBitBoardFrom(M,True)
        M2 = GameState.fromBitBoardToMatrix(BB,True)
        print("M:\n",M)
        print("M2:\n",M2)
        self.assertEqual(np.allclose(M,M2),True)
        
    def test_createBitBoardFromMatrix_Zuggenerator8(self):
        """rb Test"""
        M = Gui.fenToMatrix("rb1rb/1rbrb5/8/8/8/8/8/rbrbrb5")
        BB = GameState.createBitBoardFrom(M,True)
        M2 = GameState.fromBitBoardToMatrix(BB,True)
        print("M:\n",M)
        print("M2:\n",M2)
        self.assertEqual(np.allclose(M,M2),True)
        
    def test_createBitBoardFromMatrix_Zuggenerator9(self):
        """br Test"""
        M = Gui.fenToMatrix("br5/8/8/8/8/8/8/6")
        BB = GameState.createBitBoardFrom(M,True)
        M2 = GameState.fromBitBoardToMatrix(BB,True)
        print("M:\n",M)
        print("M2:\n",M2)
        self.assertEqual(np.allclose(M,M2),True)
        
    def test_createBitBoardFromMatrix_Zuggenerator10(self):
        """br Test"""
        M = Gui.fenToMatrix("5br/br5brbr/1br1brbr2br/8/8/8/8/6")
        BB = GameState.createBitBoardFrom(M,True)
        M2 = GameState.fromBitBoardToMatrix(BB,True)
        print("M:\n",M)
        print("M2:\n",M2)
        self.assertEqual(np.allclose(M,M2),True)
        



if __name__ == '__main__':
    
    unittest.main()