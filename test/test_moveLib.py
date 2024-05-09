import numpy as np
import unittest
from src.moveLib import*
import time

class TestMoveLib(unittest.TestCase):
    
    def test_move(self):
        """Tests for movement representation"""
        self.assertEqual(MoveLib.move("A2", "A3",0), ("A2","A3"))
        self.assertEqual(MoveLib.move("A2","A3", 1), (2**15,2**23))
        self.assertEqual(type(MoveLib.move("A2","A3", 1)[0]), type(np.uint64()))
        self.assertEqual(type(MoveLib.move("A2","A3", 1)[1]), type(np.uint64()))
    
    def test_extractValueFromString(self):
        """Tests for computing the integer value of a Position"""
        self.assertEqual(MoveLib.extractValueFromString('A1'), 0)
        self.assertEqual(MoveLib.extractValueFromString("A2"), 2**15)
        self.assertEqual(MoveLib.extractValueFromString('D1'),2**4)
        self.assertEqual(MoveLib.extractValueFromString('B1'),2**6)
        self.assertEqual(MoveLib.extractValueFromString('C8'),2**61)
        self.assertEqual(MoveLib.extractValueFromString('G1'),2**1)
        self.assertEqual(MoveLib.extractValueFromString('G8'),2**57)
        self.assertEqual(MoveLib.extractValueFromString("A8"),0)
        self.assertEqual(MoveLib.extractValueFromString('H8'),0)
        self.assertEqual(MoveLib.extractValueFromString('H1'),0)
        self.assertEqual(MoveLib.extractValueFromString('E5'),2**35)

    def test_mapRowToPowValue(self):
        """Test"""
        self.assertEqual(MoveLib.mapRowToPowValue('1'),0)
        self.assertEqual(MoveLib.mapRowToPowValue('2'),7)
        self.assertEqual(MoveLib.mapRowToPowValue('3'),15)
        self.assertEqual(MoveLib.mapRowToPowValue('8'),55)
        self.assertEqual(MoveLib.mapRowToPowValue('9'),None)
        self.assertEqual(MoveLib.mapRowToPowValue('A'),None)
        self.assertEqual(MoveLib.mapRowToPowValue('a'),None)

   
    
    def test_runtime_shift_vs_pow(self):
        it = 1000000
        self.assertLess(execShift(it)[1],execPow(it)[1])
        
    def test_BitsToPosition(self):
        val = MoveLib.BitsToPosition(np.uint64(2**7))
        self.assertEqual(val, "A1")
    
    def test_BitsToPosition2(self):
        val = MoveLib.BitsToPosition(np.uint64(2**11))
        self.assertEqual(val, "E2")    
    
    def test_BitsToPosition3(self):
        val = MoveLib.BitsToPosition(np.uint64(2**19))
        self.assertEqual(val, "E3")
        
    def test_BitsToPosition4(self):
        val = MoveLib.BitsToPosition(np.uint64(2**20))
        self.assertEqual(val, "D3")  
    
    def test_BitsToPosition5(self):
        val = MoveLib.BitsToPosition(np.uint64(2**12))
        self.assertEqual(val, "D2") 

def execPow(it:int):
    val = 0
    start = time.time()
    
    for i in range(it):
        val = pow(2, 63)
    
    end = time.time()
    delta = (end - start) * 1000
    return val,delta

def execShift(it:int):
    val = 0
    start = time.time()
    
    for i in range(it):
        val = 2 << 63
    
    end = time.time()
    delta = (end - start) * 1000
    return val, delta
    
if __name__ == '__main__':
    unittest.main()