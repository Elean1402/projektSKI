import unittest
from src.bitBoardLib import*

class BitBoardLib(unittest.TestCase):
    def test_createBitBoardFrom1(self):
        M = fenToMatrix("r05/8/8/8/8/8/8/8")
        BB = createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[VAL_R], 2**62)
    
    def test_createBitBoardFrom2(self):
        M = fenToMatrix("5r0/8/8/8/8/8/8/8")
        BB = createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[VAL_R], 2**57)
        
    def test_createBitBoardFrom3(self):
        M = fenToMatrix("6/8/8/8/8/8/8/5r0")
        BB = createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[VAL_R], 2**1)
    
    def test_createBitBoardFrom3(self):
        M = fenToMatrix("6/8/8/8/8/8/8/r05")
        BB = createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[VAL_R], 2**6)
        
    def test_createBitBoardFrom4(self):
        M = fenToMatrix("rr5/8/8/8/8/8/8/6")
        BB = createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[VAL_RR], 2**62)
        
    def test_createBitBoardFrom4(self):
        M = fenToMatrix("6/6rr1/8/8/8/8/5rr2/6")
        BB = createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[VAL_RR], 2**49+2**10)
    
    def test_createBitBoardFrom5(self):
        M = fenToMatrix("6/6rb1/8/8/8/8/5rb2/6")
        BB = createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[VAL_RB], 2**49+2**10)
        
    def test_createBitBoardFrom6(self):
        M = fenToMatrix("6/6br1/8/8/8/8/5br2/6")
        BB = createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[VAL_BR], 2**49+2**10)
        
    def test_createBitBoardFrom7(self):
        M = fenToMatrix("6/6bb1/8/8/8/8/5bb2/6")
        BB = createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[VAL_BB], 2**49+2**10)


    
    def test_createBitBoardFrom6(self):
        M = fenToMatrix("1b0b01rr1/rrbbrbbr4/8/8/8/8/5b02/1b0b01rr1")
        BB = createBitBoardFrom(M)
        print("Matrix:\n", M)
        print(BB)
        self.assertEqual(BB[VAL_RR], 2**58+2**55+2**2)
        self.assertEqual(BB[VAL_R], 0)
        self.assertEqual(BB[VAL_B], 2**61+2**60+2**10+2**5+2**4)
        self.assertEqual(BB[VAL_RB], 2**53)
        self.assertEqual(BB[VAL_BR], 2**52)
        self.assertEqual(BB[VAL_BB], 2**54)
if __name__ == '__main__':
    
    unittest.main()