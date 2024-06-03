from src.AlphaBetaSearch import *

test = "6/8/8/8/8/4b03/4r0r02/6 b"
#beste moves= E6-F7 -> F7-F8 (gewonnen in 2 züge)
test2 = "6/8/8/8/3r0b03/8/8/6 b"
#beste moves= E5-E6 -> E6-E7 -> E7-E8 (gewonnen in 3 züge)
test3 = "6/8/8/8/8/8/8/b05 b"
test4 = "6/8/8/8/8/8/8/r05 b"
test5 = "6/8/8/8/1r01b04/8/8/6 b"
test6 = "6/8/8/8/2r0b04/8/8/6 b"
board, player = test6.split(" ")
game = {GameServerModel.FEN_BOARD: board,
		GameServerModel.CURRENT_PLAYER: player,
		GameServerModel.PLAYER1: True,
		GameServerModel.PLAYER2: False,
		}


def main() -> None:
	AlphaBetaSearch(game)


if __name__ == '__main__':
	main()