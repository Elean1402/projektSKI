import unittest
#import logging
from src.gui import*

class FenStringLib(unittest.TestCase):
    #@unittest.skip("hier gibts noch fehler")
    def test_fenToMatrix1(self):
        """Tests for FEN"""
        fen1 = "2rr3/5r02/1rr1rr2r0r0/2rb3b01/2r0b04/5b0bb1/2bb2b02/3b02"
        testMatrix =Gui.fenToMatrix(fen1)
        
        
        targetMatrix = np.flip(np.array(
            [[0,0,0,2,0,0,0,0],
             [0,0,0,0,0,1,0,0],
             [0,2,0,2,0,0,1,1],
             [0,0,5,0,0,0,4,0],
             [0,0,1,4,0,0,0,0],
             [0,0,0,0,0,4,8,0],
             [0,0,8,0,0,4,0,0],
             [0,0,0,0,4,0,0,0]]),0)
        print("testMatrix:\n",testMatrix,"\ntarget:\n", targetMatrix,self)
        self.assertEqual(np.array_equal(testMatrix, targetMatrix),True)
    
    def test_fenToMatrix2(self):
        """Tests for FEN"""
        fen1 = "2rr3/8/8/8/8/8/8/8"
        testMatrix =Gui.fenToMatrix(fen1)
        
        
        targetMatrix = np.flip(np.array(
            [[0,0,0,2,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0]]),0)
        print("testcase:\n",testMatrix,"\ntarget:\n", targetMatrix,self)
        self.assertEqual(np.array_equal(testMatrix, targetMatrix),True)

    def test_fenToMatrix3(self):
        """Tests for FEN"""
        fen1 = "8/8/1rr1rr2r0r0/8/8/8/8/8"
        testMatrix =Gui.fenToMatrix(fen1)
        
        
        targetMatrix = np.flip(np.array(
            [[0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,2,0,2,0,0,1,1],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0]]),0)
        print("testcase:\n",testMatrix,"\ntarget:\n", targetMatrix,self)
        self.assertEqual(np.array_equal(testMatrix, targetMatrix),True)

    
    def test_fenToMatrix4(self):
        """Tests for FEN"""
        fen1 = "8/8/8/2r05/8/8/8/8"
        testMatrix =Gui.fenToMatrix(fen1)
        
        
        targetMatrix = np.flip(np.array(
            [[0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,1,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0]]),0)
        print("testcase:\n",testMatrix,"\ntarget:\n", targetMatrix,self)
        self.assertEqual(np.array_equal(testMatrix, targetMatrix),True)
        
    
    
    def test_fenToMatrix5(self):
        """Tests for FEN"""
        fen1 = "8/8/8/2rb5/8/8/8/8"
        testMatrix =Gui.fenToMatrix(fen1)
        
        
        targetMatrix = np.flip(np.array(
            [[0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,5,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0]]),0)
        print("testcase:\n",testMatrix,"\ntarget:\n", targetMatrix,self)
        self.assertEqual(np.array_equal(testMatrix, targetMatrix),True)
        
    def test_fenToMatrix6(self):
        """Tests for FEN"""
        fen1 = "8/8/8/8/2r0b04/8/8/8"
        testMatrix =Gui.fenToMatrix(fen1)
        
        
        targetMatrix = np.flip(np.array(
            [[0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,1,4,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0]]),0)
        print("testcase:\n",testMatrix,"\ntarget:\n", targetMatrix,self)
        self.assertEqual(np.array_equal(testMatrix, targetMatrix),True)
        
    def test_fenToMatrix7(self):
        """Tests for FEN"""
        fen1 = "8/8/8/8/8/8/5b02/8"
        testMatrix =Gui.fenToMatrix(fen1)
        
        
        targetMatrix = np.flip(np.array(
            [[0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,4,0,0],
             [0,0,0,0,0,0,0,0]]),0)
        print("testcase:\n",testMatrix,"\ntarget:\n", targetMatrix,self)
        self.assertEqual(np.array_equal(testMatrix, targetMatrix),True)
    
    def test_fenToMatrix8(self):
        """Tests for FEN"""
        fen1 = "1b0b01rr1/8/8/8/8/8/5b02/8"
        testMatrix =Gui.fenToMatrix(fen1)
        
        
        targetMatrix = np.flip(np.array(
            [[0,0,4,4,0,2,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,4,0,0],
             [0,0,0,0,0,0,0,0]]),0)
        print("testcase:\n",testMatrix,"\ntarget:\n", targetMatrix,self)
        self.assertEqual(np.array_equal(testMatrix, targetMatrix),True)  
    
    def test_fenToMatrix9(self):
        """Tests for FEN"""
        fen1 = "1b0b01rr1/8/8/8/8/8/5b02/1b0b01rr1"
        testMatrix =Gui.fenToMatrix(fen1)
        
        
        targetMatrix = np.flip(np.array(
            [[0,0,4,4,0,2,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,4,0,0],
             [0,0,4,4,0,2,0,0]]),0)
        print("testcase:\n",testMatrix,"\ntarget:\n", targetMatrix,self)
        self.assertEqual(np.array_equal(testMatrix, targetMatrix),True)     
        
    def test_fenToMatrix10(self):
        """Tests for FEN"""
        fen1 = "1b0b01rr1/rrbbrbbr4/8/8/8/8/5b02/1b0b01rr1"
        testMatrix =Gui.fenToMatrix(fen1)
        
        
        targetMatrix = np.flip(np.array(
            [[0,0,4,4,0,2,0,0],
             [2,8,5,3,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,4,0,0],
             [0,0,4,4,0,2,0,0]]),0)
        print("testcase:\n",testMatrix,"\ntarget:\n", targetMatrix,self)
        self.assertEqual(np.array_equal(testMatrix, targetMatrix),True)     
        
    
    
    def test_fenToMatrix11(self):
        """Tests for FEN"""
        fen1 = "r0r0r0r0r0r0/1r0r0r0r0r0r01/8/8/8/8/1b0b0b0b0b0b01/b0b0b0b0b0b0"
        testMatrix =Gui.fenToMatrix(fen1)
        
        
        targetMatrix = np.flip(np.array(
            [[0,1,1,1,1,1,1,0],
             [0,1,1,1,1,1,1,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,4,4,4,4,4,4,0],
             [0,4,4,4,4,4,4,0]]),0)
        print("testcase:\n",testMatrix,"\ntarget:\n", targetMatrix,self)
        self.assertEqual(np.array_equal(testMatrix, targetMatrix),True)
    
    #@unittest.skip("Wo ist oben und unten, laut VL ist die erste Zeile im FEN oben")
    def test_fenToMatrix12(self):
        """Tests for FEN"""
        fen1 = "b5/8/8/8/8/8/8/r5"
        testMatrix =Gui.fenToMatrix(fen1)
        
        
        targetMatrix = np.array(
            [[0,1,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,4,0,0,0,0,0,0]])
        print("testcase:\n",testMatrix,"\ntarget:\n", targetMatrix,self)
        self.assertEqual(np.array_equal(testMatrix, targetMatrix),True)        
    
if __name__ == '__main__':
    
    unittest.main()
    