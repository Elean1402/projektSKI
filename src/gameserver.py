from src.eric import *

test = "6/8/8/8/8/4b03/4r0r02/6 b"
#beste moves= E6-F7 -> F7-F8 (gewonnen in 2 züge)
test2 = "6/8/8/8/3r0b03/8/8/6 b"
#beste moves= E5-E6 -> E6-E7 -> E7-E8 (gewonnen in 3 züge)
test3 = "6/8/8/8/8/8/8/b05 b"
test4 = "6/8/8/8/8/8/8/r05 b"
test5 = "6/8/8/8/1r01b04/8/8/6 b"
test6 = "6/8/8/8/2r0b04/8/8/6 b"
test7 = "6/r07/8/8/8/8/1b06/6 b"
board, player = test6.split(" ")
player = Player.Blue if player == "b" else Player.Red
game = {"board": board,
		"player": player,
		"player1": True,
		"player2": False,
		}

gameArray = [board, player, True, False]

def main() -> None:
	alpha_beta = AlphaBetaSearch(gameArray)
	alpha_beta.search(True)


if __name__ == '__main__':
	main()
