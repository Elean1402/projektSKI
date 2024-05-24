import unittest
from src.zuggenerator import*

class TestZuggenerator(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_General_Functions(self):
        """General Tests"""
        init_position(beta_p, beta_k, alpha_p, alpha_k)
        print_bitboards()
        moveList = alpha_generation()
        print(moveList)
        self.assertEqual(True,True)
        

if __name__ == '__main__':
    unittest.main()