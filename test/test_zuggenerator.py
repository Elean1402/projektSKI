import unittest
from src.gamestate import *
from src.zuggenerator import *
from src.gui import *
from src.benchmark import *
class TestZuggenerator(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    ISIS_FEN = ["1b0b0b0b0b0/1b01bb2b01/8/3bb1b02/5rr2/2r01r03/2rr5/r0r0r0r0r0r0 b",
                "b0b0b01b01/2b03b01/8/3b01b02/1b01r01r02/2br1r03/b01r02r02/2r0r0r01 r",
                "b01b0b0b0b0/1b0b01b01b01/3b01b02/2b05/8/2r0r01rr2/1r04r01/r0r0r0r0r0r0 r",
                "b01b01b01/8/2b03b01/1b06/1r01b01b02/3r04/2r03r01/4r01 r",
                "b0b0b01bb1/2b0b0bbb02/5r02/3b04/4r0b02/8/2rrr01r02/r0r0r0r01r0 r",
                "3b02/5r02/3r04/8/8/2b02b02/2r05/6 b",
                "b02b01b0/2b0b04/3br1b02/2b03b01/2r03r01/4rr3/1rr1b0r03/3r01r0 r",
                "2b01b01/2bb5/3b02b01/3r0brb0r01/1b06/8/2r0rr4/2r01r0r0 r",
                "2b02bb/1bb2b03/5bb2/8/1r03r02/6r01/8/r01r01rrr0 b",
                "b01bbb01b0/1b02b03/3bbr01b01/8/3rr1b0b01/8/2r01r01rr1/r0r0r01r01 r",
                "b0b0b0b0b0b0/1bb3b0b01/3b04/4b03/5r02/1r02r03/2r0r02r01/r0r0r0r0r0r0 b",
                "1bbb01b0b0/4b03/4rr1b01/2b02b02/5r02/1r06/3r02r01/1rrr01r01 r",
                "b0b01b0b0b0/8/4b0b02/3br4/6b01/2rr3rb1/4rr3/r0r02r0r0 r",
                "b0b0b0b0b0b0/8/5b01b0/5r0b01/3b04/4r0rr1rb/3r04/r0r0r0r01r0 b",
                "6/1b06/2bb1b0b02/6bb1/1r0br5/3r0rr3/8/4r0r0 b", "6/8/6b01/4bb3/r0r0rr4b0/3b02r01/1rr3r2/6 r",
                "6/1b06/1r0b02bb2/2r02b02/8/5rr2/2r03r01/6 b",
                "b0b04/b02bb2b01/2b05/4rb3/6b01/2r04r0/1r01r0r01r01/r0r04 r",
                "b0b04/r0r0b02b0b0b0/2r02r0r0r0/8/8/b0b0b02b02/r0r0r02r0b0b0/4r0r0 b",
                "6/3bb4/1br6/r01b0b02bb1/1rr2r0r01b0/6rb1/4rr3/6 b",
                "1b0b01b0b0/3bb4/8/1r03b02/3b0rrr0b01/6r01/1r0r0r04/2r01r01 r", "6/7rr/4bb1r01/8/8/b02bb3b0/8/6 r",
                "b03b01/3bb2bb1/2bb1br3/1b06/5r02/2rr5/1r02rr3/r0r02rr1 b",
                "b03b01/4b02b01/r01b0578/8/3rbb3/1r06/r03r01 b",
                "b0b0b0b0b0b0/2bbb02bb1/4b03/8/3r04/8/1r0r01r0r0r01/r0r0r0r0r0r0 r",
                "2b03/1b0b05/6b01/3bb2r01/3r02r01/2b05/2r03r01/3r02 b", "1r0r0r0r1/8/1r1rb2rr1/5bb2/2b5/8/4bb3/1b2b1 b",
                "b0b0b01b0b0/4b01b01/2bb2b02/8/1r01br4/4r01r01/2r02rr2/r01r01r0r0 r",
                "6/8/4b03/1r01b0r03/2r02r0b01/1b02b01r01/1r06/6 b", "b0b0b0b0b0b0/8/8/4b03/1r01b01r02/8/3r02r01/6 r",
                "b0b0b0b01b0/2bb1b03/1b01b01bb2/3r04/2r05/2r01r0r0r01/3r04/r0r0r0r01r0 r",
                "2bb3/5b02/8/2bb5/5rr2/8/3b03r0/7 b", "6/1b06/1r03bb2/2r02b02/8/5r0r0/2r0r04/6 r",
                "6/1b0b0b0b0b0b01/1b0b0b0b0b0b01/8/8/1r0r0r0r0r0r01/1r0r0r0r0r0r01/6 b",
                "b0b02b0b0/1b01bb0b0b01/2b05/3b04/2r05/3r0r03/1r0r02r0r01/r0r01r0r0r0 r",
                "6/1bb1b02b01/8/2r05/3r01b02/5r0r02/2rr1r03/6 b",
                "b0b0b02bb/1b01b0bb1b01/2b05/5b02/1r06/8/2r0rrr0rr1r0/r0r01r01r0 r",
                "bb4bb/3b02b01/r07/2r02r02/4b03/2b02r02/2r01r01r0r0/1r01r02 r",
                "6/1bbbbbbbbbbbb1/8/8/8/1r0r0r0r0r0r01/8/r0r0r0r0r0r0 b ", "8/2b02b02/2r02r02/8/8/2b02b02/2r02r02/8 b",
                "1b03b0/3b01b02/8/4b0r02/4b03/4r0b02/3r01r02/1r01r01r0 r",
                "b0b0b0b0b0b0/2b01b0b02/1b01b04/4r03/2b01r03/6r01/1r0r0r01r02/r0r0r0r01r0 b",
                "b01b0b01b0/1b0bb1b0b0b01/3b04/2r05/4b0r02/8/1r0r0r0r0r0r01/1r0r0r0r01 r",
                "3b02/2b05/1b06/1r0rr2b01/8/5r02/1r0r03b01/3r02 b", "6/1b06/8/2b01bbb0rb1/1rbr0rr1r0r01/8/b07/6 b",
                "6/8/6rr1/8/8/8/b0b0b05/6 r", "3b02/2bb2b02/5b0bb1/2r0b04/2rb3b01/1rr1rr2r0r0/5r02/2rr3 b",
                "1b01b0b01/b01bb0b01bb0b01/1b06/8/7b0/1r02r01rr1/2rr2rr2/r0r01r0r01 b",
                "b02b01b0/3b01b02/b02b02b01/b01b05/5r02/1r02r02r0/2rrr02r01/r03r01 b",
                "6/1b03b02/3b01r0b01/bb2b04/1b01r02r0r0/1r0r02rbr01/1r06/6 r",
                "2b03/8/8/3b0b03/2b03b01/2r03r01/2r05/6 r",
                "2bbbb1b0/1b06/1b01b04/4b03/4r03/3r02b01/1r0r02rr2/2rr2r0 b",
                "b0b01b02/3bbb0bb2/2b03bb1/8/2b01r03/5r02/1rr1r0rr1rr1/1rr4 b",
                "6/1b02br3/6bb1/2b0b04/2r04r0/8/1rr1r0rr1r01/6 b",
                "1b04/2b03b01/b01rr5/r02b01b02/1b06/1r02b03/8/1r01r0r0r0 b",
                "bb1b0b0b0b0/b01b0b0b01b01/8/3b04/3r04/2r05/1rr2r0r01r0/1r0r0r0r0r0 r",
                "2bbb0b0b0/1bbb0b0b0b0b01/8/8/8/1r01r04/2r01r0r0r01/r0r0r0r0r0r0 b",
                "bb5/1bb6/bb6b/b6r/rb6/6rb1/4rr3/6 b"]
    ISIS_poss = [
        "C1-B1, C1-C2, C1-D1, D1-C1, D1-E1, E1-D1, E1-E2, E1-F1, F1-E1, F1-F2, F1-G1, G1-F1, G1-G2, B2-A2, B2-B3, B2-C2, D2-B3, D2-C4, D2-E4, D2-F3, G2-F2, G2-G3, G2-H2, D4-B5, D4-C6, D4-E6, D4-F5, F4-E4, F4-G4",
        "F8-G8, F8-F7, F8-E8, E8-F8, E8-E7, E8-D8, D8-E8, D8-D7, D8-C8, F7-G7, F7-F6, F7-E7, C7-D7, C7-B7, E6-F6, E6-E5, E6-D6, C6-E5, C6-D4, C6-B4, C6-A5, F5-G5, F5-E5, D5-E5, D5-C5",
        "B8-B7, B8-C8, C8-B8, C8-C7, C8-D8, D8-C8, D8-D7, D8-E8, E8-D8, E8-E7, E8-F8, F8-E8, F8-F7, F8-G8, G8-F8, G8-G7, B7-A7, B7-B6, B7-C7, C6-B6, C6-C5, C6-D6, D6-C6, D6-D5, D6-E6, G7-F7, G7-G6, G7-H7, F6-D5, F6-E4, F6-G4, F6-H5",
        "F8-E8, F8-F7, F8-G8, C7-B7, C7-C6, C7-D7, G7-F7, G7-G6, G7-H7, D6-C6, D6-E6, B5-A5, B5-C5",
        "B8-B7,B8-C8,C8-B8,C8-D8,D8-C8,D8-E8,D8-D7,E8-D8,E8-F8,E8-E7,G8-F8,G8-G7,C7-A6,C7-B5,C7D5,C7-E6,D7-D6,D7-E7,F7-E7,F7-G7,F7-F6,E5-D5,E5-D4,E5-E4,F3-E3,F3-E2,F3-G3",
        "C6-B6, C6-D6, F6-E6, F6-G6, F6-F7, E1-D1, E1-F1, E1-E2, E1-F2",
        "D6-B7, D6-C8, D6-E8, D6-F7, C4-B4, C4-D4, G4-F4, G4-H4, E3-C4, E3-D5, E3-F5, E3-G4, B2-A4, B2-C4, B2-D3, E2-F2, E1-D1, E1-D2, E1-E2, E1-F1, G1-F1, G1-G2",
        "D5-C5, E5-C6, E5-D7, E5-F7, E5-G6, G5-H5, C2-B2, C2-C3, D2-B3, D2-C4, D2-E4, D2-F3, D1-C1, D1-E1, F1-E1, F1-F2, F1-G1, G1-G2, G1-F1",
        "D1-C1, D1-D2, D1-E1, G1-E2, G1-H3, B2-A4, B2-C4, B2-D3, E2-D2, E2-E3, E2-F2, F3-D4, F3-E5, F3-G5, F3-H4",
        "B8-B7, B8-C8, C8-C7, C8-B8, C8-D8, D8-D7, D8-C8, D8-E8, F8-F7, F8-E8, F8-G8, C7-C6, C7-B7, C7-D7, E7-E6, E7-D7 ,E7-F7, G7-E6, G7-F5, G7-H5, D5-B4, D5-C3, D5-E3, D5-F4, E3-F3",
        "B1-C1, C1-B1, C1-C2, C1-D1, D1-C1, D1-D2, D1-E1, E1-D1, E1-E2, E1-F1, F1-E1, F1-F2, F1-G1, G1-F1, G1-G2, B2-A4, B2-C4, B2-D3, F2-E2, F2-F3, F2-G2, G2-F2, G2-G3, G2-H2, D3-C3, D3-D4, D3-E3, E4-D4, E4-E5, E4-F5, E4-F4",
        "C8-A7, C8-B6, C8-D6, C8-E7, D8-D7, D8-E8, F8-E8, F8-F7, F8-G8, D7-C7, D7-D6, D7-E7, G7-F7, G7-G6, G7-H7, B6-A6, B6-B5, B6-C6, F5-E5, F5-G5, E3-C2, E3-D1, E3-F1, E3-G2",
        "C6-E5, C8-B8, C6-B4, C8-C7, C8-D8, C6-A5, E7-D5, E7-G6, E7-F5, G8-F8, G8-G7, B8-B7, B8-C8, D4-B3, F8-F7, F8-G8, D4-C2, F8-E8, D4-F3, D4-E2",
        "H3-H4, C1-B1, C1-D1, E1-E2, G4-G5, G1-G2, B1-C1, D5-D6, D1-D2, F3-E3, F1-G1, F3-G3, F1-E1, H6-G8, H3-G3, C1-C2, G4-H4, E1-D1, E1-F1, G1-F1, B1-B2, D1-E1, D5-C5, D5-E6, D1-C1, D5-E5, F1-F2, H6-F7",
        "B2-A2, B2-C2, B2-B3, C3-A4, C3-E4, C3-B5, C3-D5, E3-D3, E3-F3, E3-E4, F3-E3, F3-G3, F3-F4, G4-E5, G4-F6, G4-H6",
        "A5-B5, A5-A4, B5-A5, B5-B4, C5-E4, C5-A4, C5-D3, C5-B3, G6-F6, G6-H6, G6-H5, G6-G5, B7-D6, B7-A5, F7-E7, F7-G7, F7-F6",
        "B2-A2, B2-C2, C3-D3, F4-E4, F4-G4, F4-F5, F3-D4, F3-E5, F3-G5, F3-H4",
        "B8-B7, B8-C8, C8-B8, C8-C7, C8-D8, B7-A7, B7-B6, B7-C7, D7-C7, D7-D6, D7-E7, E7-D7, E7-E6, E7-F7, G7-F7, G7-G6, G7-H7, C6-B6, C6-C5, C6-D6, H6-G6, H6-H5, H6-G5",
        "B1-A2, B1-C1, C1-B1, C1-B2, C1-D1, C1-C2, C2-D2, F2-E2, F2-G2, F2-G3, G2-F2, G2-F3, G2-H2, G2-H3, H2-G2, H2-G3, A6-B6, A6-B7, B6-A6, B6-A7, B6-C6, B6-C7, C6-B6, C6-B7, C6-D6, F6-E6, F6-G6, G7-F8, G7-H7, H7-G7, H7-G8",
        "D2-C4, D2-B3, D2-E4, D2-F3, C4-B4, C4-B5, C4-D4, C4-C5, D4-C4, D4-E4, D4-E5, D4-D5, G4-F6, G4-E5, G4-H6, H5-G5, H5-H6, G6-F8, G6-E7",
        "D8-C8, D8-E8, D8-D7, F8-E8, F8-G8, F8-F7, B7-A7, B7-C7, B7-B6, C7-B7, C7-D7, C7-C6, D7-C7, D7-E7, D7-D6, G6-F6, G6-H6, E5-C4, E5-G4, E5-D3, E5-F3, B4-A4, B4-C4, B4-B3",
        "G3-F3, G3-H3, G3-G2, H2-F1",
        "B1-C1, B1-B2, F1-E1, F1-G1, F1-F2, D2-B3, D2-F3, D2-C4, D2-E4, G2-E3, G2-F4, G2-H4, C3-A4, C3-E4, C3- B5, C3-D5, B4-A4, B4-C4, B4-B5",
        "B1-C1, B1-B2, F1-E1, F1-G1, F1-F2, D2-C2, D2-E2, D2-D3, G2-F2, G2-H2, G2-G3, C3-B3, C3-D3, C3-C4, E6-C7, E6-G7, E6-D8, E6-F8",
        "B8-C8, B8-B7, C8-B8, C8-C7, C8-D8, D8-C8, D8-D7, D8-E8, E8-D8, E8-E7, E8-F8, F8-E8,F8-F7, F8-G8, G8-F8, G8-G7, B7-A7, B7-B6, B7-C7, C7-B7, C7-C6, C7-D7, E7-D7, E7-E6, E7-F7,F7-E7, F7-F6, F7-G7, G7-F7, G7-G6, G7-H7, D5-C5, D5-D4, D5-E5",
        "D1-C1, D1-D2, D1-E1, B2-A2, B2-B3, B2-C2, C2-B2, C2-C3, C2-D2, G3-F3, G3-H3, D4-B5,D4-C6, D4-E6, D4-F5, C6-B6, C6-D6",
        "F5-G7, F5-E7, F5-H6, F5-H4, F5-D4, F5-E3, F5-G3, C4-C5, C4-C3, C4-B4, C4-D4, E2-F4, E2-D4,E2-C3,E2-C1,E2-G3,E2-G1, C1-C2, C1-B1, C1-D1, F1-F2, F1-G1, F1-E1",
        "B8-C8,B8-B7,D8-C8,D8-E8,D8-D7,F8-E8,F8-G8,G8-F8,G8-G7,C7-B7,C7-D7,C7-C6,F7-D6,F7-E5,F7-G5,F7-H6,E6-D6,E6-E5,E6-F6,G6-F6,G6-G5,G6-H6,B5-A5,B5-B4,B5-C5,D5-B4,D5-C3,D5-E3,D5-F4",
        "B6-A6,B6-C6,D4-D5,D4-C5,E3-D3,E3-F3,E6-D6,E6-F6,E6-E7,G5-H5",
        "B5-A5,B5-C5,B5-A4,D7-C7,D7-E7,D7-C6,F5-E4,F5-E5,F5-G5,F5-E4,G7-G6,G7-H7,G7-F7",
        "C8-B8, C8-C7, C8-D7, C8-D8, B7-A5, B7-C5, B7-D6, E4-E3, E4-F4, F7-H6, F7-G5, F7-E5, F7-D6, G7-H5, G7-F5, G7-E6, E2- G1, E2-C1",
        "B2-A4, B2-C4, B2-D3, C2-A3, C2-B4, C2-D4, C2-E3, D2- B3, D2-C4, D2-E4, D2-F3, E2-C3, E2-D4, E2-F4, E2-G3, F2-D3, F2-E4, F2-G4, F2-H3, G2-E3, G2-F4, G2-H4",
        "B1-B2,B1-C1,C1-B1,C1-C2,C1-D1,D1-C1,D1-D2,D1-E1,E1-D1,E1-E2,E1-F1,G1-F1,G1-G2,D2-C2,D2-D3,D2-E2,C3-B3,C3-C4,C3-D3,E3-D3,E3-E4,E3-F3,F3-E3,F3-F4,F3-G3,G3-F3,G3-G4,G3-H3,C4-B4,C4-C5,C4-D4,D5-C5,D5-E5",
        "F5-D4,F5-E3,F5-G3,F5-H4,H7-G7,H7-H6",
        "B3-A3, B3-C3, C4-B4, C4-D4, C4-C3, F6-E6, F6-G6, F6-F5, G6-F6, G6-H6, G6-G5, C7-B7, C7-D7, C7-C6, D7-C7, D7-E7, D7-D6",
        "B2-C2, B2-A2, B2-B3, C2-D2, C2-B2, C2-C3, D2-E2, D2-C2, D2-D3, E2-F2, E2-D2, E2-E3, F2-G2, F2-E2, F2-F3, G2-H2, G2-F2, G2-G3, B3-C3, B3-A3, B3-B4, C3-D3, C3-B3, C3-C4, D3-E3, D3-C3, D3-D4, E3-F3, E3-D3, E3-E4, F3-G3, F3-E3, F3-F4, G3-H3, G3-F3, G3-G4",
        "B1-B2, B1-C1, C1-B1, C1-C2, C1-D1, E1-D1, E1-E2, E1-F1, F1-E1, F1-F2, F1-G1, G1-F1, G1-G2, B2-A2, B2-B3, B2-C2, C2-B2, C2-C3, C2-D2, D3-C3, D3-D4, D3-E3, E3-D3, E3-E4, E3-F3, F2-E2, F2-F3, F2-G2, G2-F2, G2-G3, G2-H2, C4-B4, C4-C5, C4-D5, C4-D4",
        "B7-A5, B7-C5, B7-D6, D7-C7, D7-D6, D7-E7, G7-F7, G7-G6, G7-H7, F4-E4, F4-G4",
        "B1-B2, B1-C1, C1-B1, C1-C2, C1-D1, E1-D1, E1-E2 , E1-F1, G1-F1, G1-G2, C2-B2, C2-C3, D2-B3, D2-C4, D2-E4, D2-F3, E2-E3, F2-D3, F2-E4, F2-G4, F2-H3, H2-G2, H2-H3, B4-A4, B4-B5, B4-C4",
        "C1-B1, C1-C2, C1-D1, E1-D1, E1-E2, E1-F1, C2-B2, C2-D2, E2-D2, E2-E3, E2-F2, G2-F2, G2-G3, G2-H2, H2-G2, H2-H3, F3-E3, F3-E4, F3-F4, F3-G3, C5-B5, C5-C6, C5-D5, F5-E5, F5-F6, F5-G5, A6-A7, A6-B6",
        "B2->A4, B2->C4, B2->D3, C2->B4, C2->D4, C2->A3, C2->E3, D2->C4, D2->E4, D2->B3, D2->F3, E2->D4, E2->F4, E2->C3, E2->G3, F2->E4, F2->G4, F2->D3, F2->H3, G2->F4, G2->H4, G2->E3",
        "C6->B6, C6->D6, F6->E6, F6->G6, C2->B2, C2->D2, F2->E2, F2->G2",
        "C1-D1, E5-E4, D1-D2, E4-D2, E1-D2, F7-F6, D2-E4, F6-E6, F5-F6, D7-D6, E3-E4, D6-E6, E4-F6, E6-F4, F6-G8",
        "B6-B5, E5-D6, E7-D6, D2-D3, B8-C8, D3-C4, B5-C4, B2-B3, C8-D6, D1-C1, E8-D8, E4-E5, D6-E4, B3-C4, D6-E5, C4-C5, C7-B7, C1-D3, D8-B7, C5-C6, B7-C5, G3-G4, B7-C6, D3-E4, C6-C5, C1-C2, C5-E4, C2-E3, C5-D5, C2-D2, D5-E5, G4-F4, E5-F3, F4-E5, D8-D7, B1-C1, F8-F7, E5-F5, F7-E5",
        "C1-B1, C1-C2, C1-D1, D1-C1, D1-D2, D1-E1, E1-D1, E1-E2, E1-F1, F1-E1, F1-F2, F1-G1, B2-A2, B2-B3, B2-C2, C2-B2, C2-C3, C2-D2, D2-C2, D2-D3, D2-E2, E2-D2, E2-E3, E2-F2, F2-E2, F2-F3, F2-G2, G2-F2, G2-G3, G2-H2, F4-F5, F4-G4, C5--B5, C5-C6, C5-D6, C5-D5",
        "B6-A6, B6-C6, C7-B7, C7-C6, C7-D7, E8-D8, E8-E7, E8-F8, G2-F2, G2-G1, G2-H2, G5-F5, G5-G4, G5-H5",
        "B2-A2, B2-B3, B2-C2, C4-B4, C4-D4, C4-D5, E4-C5, E4-D6, E4-F6, E4-G5, F4-G5, G4-E5, G4-F6, G4-H6, B5-A7, B5-C7, B5-D6, A7-B7",
        "G3-F1, G3-E2",
        "C2-A3, C2-B4, C2-D4, C2-E3, C5-A6, C5-B7, C5-D7, C5-E6, D4-D5, D4-E4, E1-D1, E1-E2, E1-F1, F2-E2, F2-F3, F2-G2, F3-E3, F3-F4, G3-E4, G3-F5, G3-H5, G5-F5, G5-H5, G5-H6",
        "A2-A3, A2-B2, B3-A3, B3-B4, B3-C3, C1-B1, C1-D1, C2-A3, C2-B4, C2-D4, C2-E3, D2-D3, D2-E2, E1-D1, E1-E2, E1-F1, F1-E1, F1-G1, F2-D3, F2-E4, F2-G4, F2-H3, G2-G3, G2-H2, H5-G5, H5-G6, H5-H6",
        "B1-B2,B1-C1,E1-E2,E1-D1,E1-F1,G1-G2,G1-F1,D2-D3,D2-C2,D2-E2,F2-F3,F2-E2,F2-G2,A3-A4,A3-B3,D3-D4,D3-C3,D3-E3,G3-G4,G3-F3,G3-H3,A4-A5,A4-B4,C4-C5,C4-B4,C4-D4",
        "F3-E3,D5-C5,D5-E5,G5-G4,G5-F5,G5-H5,H5-H4,H5-G5,B6-A6,B6-C6,C6-C5,C6-B6,C6-B5,C6-D6,G6-G5,G6-H6,B7-B6,B7-A7,B7-C7",
        "C6-B6, C6-D6, C7-B7, C7-C6, C7-D7, G6-F6, G6-H6",
        "B2-A2, B2-B3, B2-C2, B3-A3, B3-B4, B3-C3, D1-B2, D1-C3, D1-E3, D1-F2, D3-C3, D3-D4, D3-E3, E1-C2, E1-D3, E1-F3, E1-G2, E4-D4, E4-F4, G1-F1, G1-G2, G6-F6, G6-F7, G6-G7, G6-H6",
        "B1-B2, B1-C1, C1-B1, C1-C2, C1-D1, E1-D1, E1-E2, E1-F1, D2-B3, D2-C4, D2-E4, D2-F3, E2-E3, F2-D3, F2-E4, F2-G4, F2-H3, C3-B3, C3-C4, C3-D3, G3-E4, G3-F5, G3-H5, C5-B5, C5-C6, C5-D5",
        "B2-A2, B2-B3, B2-C2, G3-E4, G3-F5, G3-H5, C4-B4, C4-D4, D4-C4, D4-C5, D4-D5, D4-E4",
        "C1-B1, C1-C2, C1-D1, E1-D1, E1-E2, E1-F1, F1-E1, F1-F2, F1-G1, G1-F1, G1-G2, B3-A3, B3-C3, A5-B5, C6-A7, C6-B8, C6-D8, C6-E7",
        "D5-C5, D5-E5, A7-A6, A7-B7, C7-B7, C7-C6, C7-D7, D7-C7, D7-D6, D7-E7, E7-D7, E7-E6, E7-F7, G7-F7, G7-G6, G7-H7, B8-A6, B8-C6, B8-D7, D8-C8, D8-D7, D8-E8, E8-D8, E8-E7, E8-F8, F8-E8, F8-F7, F8-G8, G8-F8, G8-G7",
        "C2-C3, D2-D3, E2-E3, F2-F3, G2-G3,G2-H2,F1-E1, G1-F1, D2-C2, E2-D2, F2-E2, G2-F2,E1-E2, F1-F2, G1-G2,E1-F1, F1-G1, C2-D2, D2-E2, E2-F2, F2-G2,D1-C3, B2-A4,D1-E3, B2-C4,B2-D3,D1-F2",
        "H3-G3,H3-H4, A4-A5,C4-A5,C4-B6, H5-G7,B1-C3, A3-B5, C4-D6,B1-D2, B2-D3, C4-E5,H5-F6,B2-A4"]
    ISIS_poss = [p.replace(">", "") for p in ISIS_poss]

    ###############
    # Blaue Steine
    ###############
    #Pawns Test
    # Check pawns hit for pawns and knights(+mix)
    FEN_b_pawns_hit = ["6/2r0b0r03/3r0r03/8/8/8/8/6 b", "6/2r0b0r03/2r0r04/8/8/8/8/6 b",
                       "6/2r0b0r03/3r0rr3/8/8/8/8/6 b", "6/2r0b0r03/2rrr04/8/8/8/8/6 b", "6/2r0b0r03/3r04/8/8/8/8/6 b",
                       "6/2r0b0r03/2brr04/8/8/8/8/6 b", "6/2r0b0r03/3r0br3/8/8/8/8/6 b"]
    poss_b_pawns_hit = ["D2-E3", "D2-C3", "D2-E3", "D2-C3", "", "D2-C3", "D2-E3"]

    # Check if pawns go on to other pawns
    FEN_b_pawns_build = ["6/2r0b0b0r02/3r04/8/8/8/8/6 b", "6/2r0b0r03/3b04/3r04/8/8/8/6 b",
                         "6/1r0b0b0r03/3r04/8/8/8/8/6 b"]
    poss_b_pawns_build = ["D2-E2, E2-E3, E2-D2, E2-E3", "D2-D3, D3-C3, D3-E3", "D2-C2, C2-C3, C2-D2, C2-D3"]

    # Check if pawns move and walls
    FEN_b_pawns_move = ["6/2r0b04/3r04/8/8/8/8/6 b", "6/2r0b0r03/8/8/8/8/8/6 b", "6/3b0r03/3r04/8/8/8/8/6 b",
                        "6/b0r06/8/8/8/8/8/6 b", "6/6r0b0/8/8/8/8/8/6 b", "6/6r0b0/7r0/8/8/8/8/6 b"]
    poss_b_pawns_move = ["D2-E2", "D2-D3", "D2-C2", "A2-A3", "H2-H3", ""]

    # Check pawns and corner and does not move on to knight
    FEN_b_pawns_wall = ["b05/1r06/8/8/8/8/8/6 b", "6/8/8/8/8/8/b0r06/6 b", "6/bbb0bb5/1bb6/8/8/8/8/6 b"]
    poss_b_pawns_wall = ["B1-C1", "", "A2-B4, A2-C3, B3-A5, B3-C5, B3-D4, C2-A3, C2-B4, C2-D4, C2-E3"]

    #Knights Test
    # Check knights hit for knights and pawns(+mix)
    FEN_b_knights_hit = ["6/3bb4/1r03r02/2r01r03/8/8/8/6 b", "6/3bb4/1rr3rr2/2rr1rr3/8/8/8/6 b",
                         "6/3bb4/1br3br2/2br1br3/8/8/8/6 b"]
    poss_b_knight_hit = ["D2-B3, D2-C4, D2-E4, D2-F3", "D2-B3, D2-C4, D2-E4, D2-F3", "D2-B3, D2-C4, D2-E4, D2-F3"]

    # Check if knights go on to other pawns
    FEN_b_knights_build = ["1bb4/b0r01r0b0r02/r0b0r0b0r03/1r01r04/8/8/8/6 b"]
    poss_b_knight_build = ["C1-A2, C1-B3, C1-D3, C1-E2"]

    # Check if knights move and walls
    FEN_b_knights_move = ["6/3bb4/8/8/8/8/8/6 b", "6/1bb6/8/8/8/8/8/6 b", "6/6bb1/8/8/8/8/8/6 b", "6/bb7/8/8/8/8/8/6 b",
                          "6/7bb/8/8/8/8/8/6 b"]
    poss_b_knight_move = ["D2-B3, D2-C4, D2-E4, D2-F3", "B2-A4, B2-C4, B2-D3", "G2-H4, G2-F4, G2-E3", "A2-B4, A2-C3",
                          "H2-G4, H2-F3"]

    # Check knights and corner and does not move on to knight
    FEN_b_knights_corner = ["1bb4/8/8/8/8/8/8/6 b", "4bb1/8/8/8/8/8/8/6 b", "6/8/8/8/8/1bb6/8/6 b",
                            "6/8/8/8/8/8/2bb5/6 b", "4bb1/3bb3bb/4bb1bb1/8/8/8/8/6 b"]
    poss_b_knights_corner = ["C1-A2, C1-B3, C1-D3, C1-E2", "F1-D2, F1-E3, F1-H2, F1-G3", "B6-C8, B6-D7", "C7-E8",
                             "H2-F3, H2-G4, E3-G4, E3-F5, E3-D5, E3-C4, D2-B3, D2-C4, D2-E4, D2-F3, G3-H5, G3-F5, G3-E4"]

    ###############
    # Rote Steine
    ###############
    #Pawns Test
    # Check pawns hit for pawns and knights(+mix)
    FEN_r_pawns_hit = ["6/8/8/8/8/3b0b03/3b0r0b02/6 r", "6/8/8/8/8/4b0b02/3b0r0b02/6 r",
                       "6/8/8/8/8/3bbb03/3b0r0b02/6 r", "6/8/8/8/8/4b0bb2/3b0r0b02/6 r", "6/8/8/8/8/4b03/3b0r0b02/6 r",
                       "6/8/8/8/8/3rbb03/3b0r0b02/6 r", "6/8/8/8/8/4b0rb2/3b0r0b02/6 r"]
    poss_r_pawns_hit = ["E7-D6", "E7-F6", "E7-D6", "E7-F6", "", "E7-D6", "E7-F6"]

    # Check if pawns go on to other pawns
    FEN_r_pawns_build = ["6/8/8/8/8/4b03/2b0r0r0b02/6 r", "6/8/8/8/8/4r03/3b0r0b02/6 r",
                         "6/8/8/8/8/4b03/3b0r0r0b01/6 r"]
    poss_r_pawns_build = ["D7-D6, D7-E6, D7-E7, E7-D7", "E6-D6, E6-F6, E6-E5, E7-E6", "E7-F7, F7-E7, F7-E6, F7-F6"]

    # Check if pawns move and walls
    FEN_r_pawns_move = ["6/8/8/8/8/4b03/4r0b02/6 r", "6/8/8/8/8/8/3b0r0b02/6 r", "6/8/8/8/8/4b03/3b0r03/6 r",
                        "6/8/8/8/8/8/6b0r0/6 r", "6/8/8/8/8/8/r0b06/6 r", "6/8/8/8/8/b07/r0b06/6 r"]
    poss_r_pawns_move = ["E7-D7", "E7-E6", "E7-F7", "H7-H6", "A7-A6", ""]

    # Check pawns and corner and does not move on to knight
    FEN_r_pawns_wall = ["6/8/8/8/8/8/1b06/r05 r", "6/r0b06/8/8/8/8/8/6 r", "6/8/8/8/8/6rr1/5rrr0rr/6 r"]
    poss_r_pawns_wall = ["B8-C8", "", "F7-D6, F7-E5, F7-G5, F7-H6, G6-E5, G6-F4, G6-H4, H7-F6, H7-G5"]

    #Knights Test
    # Check knights hit for knights and pawns(+mix)
    FEN_r_knights_hit = ["6/8/8/8/3b01b02/2b03b01/4rr3/6 r", "6/8/8/8/3bb1bb2/2bb3bb1/4rr3/6 r",
                         "6/8/8/8/3rb1rb2/2rb3rb1/4rr3/6 r"]
    poss_r_knight_hit = ["E7-C6, E7-D5, E7-F5, E7-G6", "E7-C6, E7-D5, E7-F5, E7-G6", "E7-C6, E7-D5, E7-F5, E7-G6"]

    # Check if knights go on to other pawns
    FEN_r_knights_build = ["6/8/8/8/4b01b01/3b0r0b0r0b0/2b0r0b01b0r0/4rr1 r"]
    poss_r_knight_build = ["F8-D7, F8-E6, F8-G6, F8-H7"]

    # Check if knights move and walls
    FEN_r_knights_move = ["6/8/8/8/8/8/4rr3/6 r", "6/8/8/8/8/8/6rr1/6 r", "6/1rr6/8/8/8/8/8/6 r", "6/8/8/8/8/8/7rr/6 r",
                          "6/rr7/8/8/8/8/8/6 r"]
    poss_r_knight_move = ["E7-C6, E7-D5, E7-F5, E7-G6", "G7-E6, G7-F5, G7-H5", "B7-A5, B7-C5, B7-D6", "H7-F6, H7-G5",
                          "A7-B5, A7-C6"]

    # Check knights and corner and does not move on to knight
    FEN_r_knights_corner = ["6/8/8/8/8/8/8/4rr1 r", "6/8/8/8/8/8/8/1rr4 r", "6/8/6rr1/8/8/8/8/6 r",
                            "6/5rr2/8/8/8/8/8/6 r", "6/8/8/8/8/1rr1rr4/rr3rr3/1rr4 r"]
    poss_r_knights_corner = ["F8-D7, F8-E6, F8-G6, F8-H7", "C8-A7, C8-B6, C8-D6, C8-E7", "G3-E2, G3-F1", "F2-D1",
                             "A7-C6, A7-B5, B6-A4, B6-C4, B6-D5, D6-B5, D6-C4, D6-E4, D6-F5, E7-C6, E7-D5, E7-F5, E7-G6"]

    def test_generate_zug(self):
        Player = ""
        M = Gui.fenToMatrix("br5/8/8/8/8/8/8/6")
        
        BB = GameState.createBitBoardFrom(M, True)
        #GUI = Gui("6/8/8/8/8/8/8/4rr1")

        FEN_b_pawns_hit = ["6/8/8/8/8/3b0b03/3b0r0b02/6 r", "6/8/8/8/8/4b0b02/3b0r0b02/6 r",
                       "6/8/8/8/8/3bbb03/3b0r0b02/6 r", "6/8/8/8/8/4b0bb2/3b0r0b02/6 r",
                       "6/8/8/8/8/3rbb03/3b0r0b02/6 r", "6/8/8/8/8/4b0rb2/3b0r0b02/6 r"]
        poss_b_pawns_hit = ["E7-D6", "E7-F6", "E7-D6", "E7-F6", "E7-D6", "E7-F6"]
        FEN = FEN_b_pawns_hit
        poss = poss_b_pawns_hit
        for i in range(len(FEN)):
            fen_string,Player = FEN[i].split(" ")
            moves = poss[i]

            print(fen_string)
            GUI = Gui(fen_string)
            GUI.start()
            print(Player)

            # Alpha
            if(Player == "b"):
                init_position(*GameState.createBitBoardFrom(Gui.fenToMatrix(fen_string), True))
                GameState.createBitBoardFrom(Gui.fenToMatrix(fen_string), True)
                #benchmark(fen_string, alpha_generation)
                a = alpha_generation()
                list_temp = moves_to_string(a)
                list_Alpha = []
                for element in list_temp:
                    if element not in list_Alpha:
                        list_Alpha.append(element)
                print(list_Alpha)
                move_list = []
                move_list.append(moves)
                print(move_list)
                assert list_Alpha == move_list

            # Beta
            elif(Player == "r"):
                init_position(*GameState.createBitBoardFrom(Gui.fenToMatrix(fen_string), True))
                #benchmark(fen_string, beta_generation)
                b = beta_generation()
                list_temp = moves_to_string(b)
                list_Beta = []
                for element in list_temp:
                    if element not in list_Beta:
                        list_Beta.append(element)
                print(list_Beta)
                print(moves)
                move_list = []
                move_list.append(moves)
                assert list_Beta == move_list
            else:
                raise ValueError("Player not found")


if __name__ == '__main__':
    benchmark("",unittest.main)
    unittest.main()