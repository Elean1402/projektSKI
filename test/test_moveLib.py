import numpy as np
import unittest
from src.moveLib import*
import time

class MoveLib(unittest.TestCase):
    
    def test_move(self):
        """Tests for movement representation"""
        self.assertEqual(move("A2", "A3"), ("A2","A3"))
        self.assertEqual(move("A2","A3", 1), (2**15,2**23))
        self.assertEqual(type(move("A2","A3", 1)[0]), type(np.uint64()))
        self.assertEqual(type(move("A2","A3", 1)[1]), type(np.uint64()))
    
    def test_extractValueFromString(self):
        """Tests for computing the integer value of a Position"""
        self.assertEqual(extractValueFromString('A1'), 0)
        self.assertEqual(extractValueFromString("A2"), 2**15)
        self.assertEqual(extractValueFromString('D1'),2**4)
        self.assertEqual(extractValueFromString('B1'),2**6)
        self.assertEqual(extractValueFromString('C8'),2**61)
        self.assertEqual(extractValueFromString('G1'),2**1)
        self.assertEqual(extractValueFromString('G8'),2**57)
        self.assertEqual(extractValueFromString("A8"),0)
        self.assertEqual(extractValueFromString('H8'),0)
        self.assertEqual(extractValueFromString('H1'),0)
        self.assertEqual(extractValueFromString('E5'),2**35)

    def test_mapRowToPowValue(self):
        """Test"""
        self.assertEqual(mapRowToPowValue('1'),0)
        self.assertEqual(mapRowToPowValue('2'),7)
        self.assertEqual(mapRowToPowValue('3'),15)
        self.assertEqual(mapRowToPowValue('8'),55)
        self.assertEqual(mapRowToPowValue('9'),None)
        self.assertEqual(mapRowToPowValue('A'),None)
        self.assertEqual(mapRowToPowValue('a'),None)

   
    
    def test_runtime_shift_vs_pow(self):
        it = 1000000
        self.assertLess(execShift(it)[1],execPow(it)[1])
        
        
    

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