import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.model import*
from src.scoreConfig_evalFunc import ScoreConfig

from src.abs_for_internal_usage import AlphaBetaSearch
test = "6/8/8/8/8/4b03/4r0r02/6 b"
#beste moves= E6-F7 -> F7-F8 (gewonnen in 2 züge)
test2 = "6/8/8/8/3r0b03/8/8/6 b"
#beste moves= E5-E6 -> E6-E7 -> E7-E8 (gewonnen in 3 züge)
test3 = "6/8/8/8/8/8/8/b05 b"
test4 = "6/8/8/8/8/8/8/r05 b"
test5 = "6/8/8/8/1r01b04/8/8/6 b"
test6 = "6/8/8/8/2r0b04/8/8/6 b"
test7 = "6/8/8/8/1r0b0r04/2r05/8/6 b"
board, player = test7.split(" ")
gameDict = {GameServerModel.FEN_BOARD: board,
		GameServerModel.CURRENT_PLAYER_STRING : player,
		GameServerModel.PLAYER1: True,
		GameServerModel.PLAYER2: False,
		}


def main() -> None:
	ab = AlphaBetaSearch(gameDict,GameServerModel.PLAYER1, Player.Red,8,ScoreConfig.Version2(Player.Red,Player.Red), ScoreConfig.Version1(Player.Red,Player.Blue),True)
	ab.startGame(gameDict,6)

if __name__ == '__main__':
	main()