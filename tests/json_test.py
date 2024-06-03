import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from jsonHandler import JSONHandler


###############
# Blaue Steine
###############
# Pawns Test
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

# Knights Test
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
# Pawns Test
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

# Knights Test
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

test_cases = [

]

def main():

	handler = JSONHandler("testcases/test.json")

	# Get the global variables from the current module
	global_vars = {var: globals()[var] for var in globals() if isinstance(globals()[var], list)}

	# Separate the FEN and poss lists
	fen_vars = [var for var in sorted(global_vars.keys()) if var.startswith("FEN")]
	poss_vars = [var for var in sorted(global_vars.keys()) if var.startswith("poss")]

	# Ensure there's an equal number of FEN and poss lists
	#assert len(fen_vars) == len(poss_vars), "Uneven number of FEN and poss lists"

	# Pair the FEN and poss lists
	for fen_var, moves_var in zip(fen_vars, poss_vars):
		fen_list = global_vars[fen_var]
		moves_list = global_vars[moves_var]
		handler.create_from_fen(fen_var, fen_list, moves_list)

if __name__ == "__main__":
	main()
