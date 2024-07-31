import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.evalFunction import *
from src.moveGenerator import MoveGenerator
from src.moveLib import *
from src.model import *


class AlphaBetaSearch:
    """
    This class implements the Alpha-Beta Search algorithm for a given game.
    """

    _gameover = [DictMoveEntry.CONTINUE_GAME]
    _totalGameOver = [DictMoveEntry.CONTINUE_GAME]
    _ALPHA_INIT = -float('inf')
    _BETA_INIT = float('inf')
    _board = [np.uint64(0), np.uint64(0), np.uint64(0), np.uint64(0)]
    _max_player = Player.NoOne
    _who_am_i: GameServerModel
    _my_color_is: Player.NoOne
    _start_time = 0
    _max_time = 0
    _end_time = 0

    _evalR = 0
    _evalB = 0
    _moveGen = 0
    _testmodus = False
    _depth_max = -1

    def __init__(self, gameDict: dict, iAm: GameServerModel, myColorIs: Player, depth_max: int, config1: Config,
                 config2: Config, testmodus=False, max_time: float = 0.5, ):
        """
        The constructor for AlphaBetaSearch class.
        """

        #############################################
        """Was soll das bedeuten????"""
        self.start_time = time.time()
        self.max_time = max_time
        self.end_time = time.time() + self.max_time
        ############################################

        self._max_player = Player.Red if self._convertPlayerString(
            gameDict[GameServerModel.CURRENT_PLAYER_STRING]) == Player.Red else Player.Blue
        ########################################################
        # WELCHER SPIELER BIN ICH ???????
        # self._who_am_i = ????
        ########################################################
        if (testmodus):
            self._who_am_i = GameServerModel.PLAYER1
            self._my_color_is = Player.Red
            self._testmodus = True
        else:
            self._who_am_i = iAm
            self._my_color_is = myColorIs
        # self._board_init = GameState.createBitBoardFromFEN(game[GameServerModel.FEN_BOARD])

        self._evalB = EvalFunction(config2)
        self._evalR = EvalFunction(config1)
        self._moveGen = MoveGenerator(GameState.createBitBoardFromFEN(gameDict[GameServerModel.FEN_BOARD]))
        self._board = GameState.createBitBoardFromFEN(gameDict[GameServerModel.FEN_BOARD])

    def startGame(self, gameDict: dict, depth: int):
        """
        The function to start the Alpha-Beta Search.
        """
        bestMove = []
        newboard = self._board.copy()
        # while(self._totalGameOver[0] == DictMoveEntry.CONTINUE_GAME):
        i = 0
        mycolor = self._my_color_is
        while (self._totalGameOver[0] == DictMoveEntry.CONTINUE_GAME):
            ###################
            # TODO Wait for legal user move
            # Server needs to wait until its our turn

            # waiting...

            # TODO CHECK if GAME OVER
            self._moveGen.checkBoardIfGameOver(self._totalGameOver, newboard)
            print("players turn=", mycolor, " totalgameOver=", self._totalGameOver[0])
            if (self._totalGameOver[0] != DictMoveEntry.CONTINUE_GAME):
                return self._totalGameOver[0]

            ## Measure Time
            alpha = self._ALPHA_INIT
            beta = self._BETA_INIT
            scoreWithMoveAlpha = (alpha, ())
            scoreWithMoveBeta = (beta, ())
            # print("testmodus=",self._testmodus)

            if (self._testmodus):

                moveList = self._moveGen.genMoves(mycolor, self._gameover, newboard)
                scoredMoveList = self._evalR.computeOverallScore(moveList, newboard,
                                                                 True) if mycolor == Player.Red else self._evalB.computeOverallScore(
                    moveList, newboard, True)
                if (len(scoredMoveList) == 0 or scoredMoveList[0][0] == 0):
                    self._totalGameOver[0] = DictMoveEntry.GAME_OVER_RED_WINS if mycolor == Player.Red else Player.Blue
                # print(scoredMoveList)
                for moveItem in scoredMoveList:

                    newBoard2 = self._moveGen.execSingleMove(moveItem, mycolor, self._gameover, newboard)
                    if (self._gameover[0] != DictMoveEntry.CONTINUE_GAME):
                        if (mycolor == self._max_player):
                            scoreWithMoveAlpha = (moveItem[3], moveItem)
                        else:
                            scoreWithMoveBeta = (moveItem[3], moveItem)
                        break
                    score = self._alpha_beta(self._ALPHA_INIT, self._BETA_INIT, depth - 1, self._max_player, newBoard2,
                                             self.change_player(mycolor))
                    # print("score ", score)
                    # print("a: ",scoreWithMoveAlpha)
                    if (self._max_player == mycolor):
                        print("typing=", type(scoreWithMoveAlpha[0]))
                        print("2nd, score", type(score), score)
                        temp = max(scoreWithMoveAlpha[0], score)
                        if (temp != scoreWithMoveAlpha[0]):
                            scoreWithMoveAlpha = (temp, moveItem)

                    else:
                        temp = min(scoreWithMoveBeta[0], score)
                        if (temp != scoreWithMoveBeta[0]):
                            scoreWithMoveBeta = (temp, moveItem)

            ## Measure Time ??

            ##TODO exec Best Move
            if (self._max_player == mycolor):
                if (scoreWithMoveAlpha[1] == ()):
                    self._totalGameOver[0] = DictMoveEntry.GAME_OVER_BLUE_WINS
                    print("totalgameover=", self._totalGameOver[0])
                else:
                    newboard = self._moveGen.execSingleMove(scoreWithMoveAlpha[1], mycolor, self._totalGameOver,
                                                            newboard, True)
                    print("totalgameover=", self._totalGameOver[0])
                    if (self._totalGameOver[0] != DictMoveEntry.CONTINUE_GAME):
                        return self._totalGameOver[0]
                    self._gameover[0] = DictMoveEntry.CONTINUE_GAME
                    # print("Alpha Zug ausgeführt!, newboard=\n", newboard)
            else:
                if (scoreWithMoveBeta[1] == ()):
                    self._totalGameOver[0] = DictMoveEntry.GAME_OVER_RED_WINS
                    print("totalgameover=", self._totalGameOver[0])
                else:
                    newboard = self._moveGen.execSingleMove(scoreWithMoveBeta[1], mycolor, self._totalGameOver,
                                                            newboard, True)
                    print("totalgameover=", self._totalGameOver[0])
                    if (self._totalGameOver[0] != DictMoveEntry.CONTINUE_GAME):
                        return self._totalGameOver[0]
                    self._gameover[0] = DictMoveEntry.CONTINUE_GAME
                    # print("Beta Zug ausgeführt!, newboard=\n", GameState.fromBitBoardToMatrix(newboard,True))

            # self._moveGen.checkBoardIfGameOver(self._totalGameOver,newboard)
            if (self._totalGameOver[0] != DictMoveEntry.CONTINUE_GAME):
                return self._totalGameOver[0]

            mycolor = self.change_player(mycolor)
            i += 1
            ## Send Info To Server

        return self._totalGameOver[0]

    def _alpha_beta(self, alpha: int, beta: int, depth: int | float, maxPlayer: Player, board: list[np.uint64],
                    myColor: Player) -> int:
        """Alpha Beta Search
            THE BASIS CODE OF THIS FUNCTION IS NOT FROM THE LECTURE,
            SOURCE: https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague
            AND HAS BEEN MODYFIED.
        Args:
            alpha (int): score
            beta (int): score
            depth (int | float): for Testing could be depth or time
            board (list[np.uint64]): bitboard array
            maxPlayer (Player): beginning Player
        """

        cboard = board.copy()
        changedColor = self.change_player(myColor)
        if (depth <= 0 or self._gameover[0] != DictMoveEntry.CONTINUE_GAME):
            # no time left or game_over
            # return score, move ?
            totalscore = self._evalR.computeOverallScore([],
                                                         board) if myColor == Player.Red else self._evalB.computeOverallScore(
                [], board)
            return totalscore[0][3]

        # print("changedColor=", changedColor)
        # print("mycolor=",myColor)
        if (self._max_player == myColor):
            maxScore = self._ALPHA_INIT

            # best move at the beginning at the list
            # moveList = self._moveGen.genMoves(self._my_color_is,self._gameover, cboard)

            # case: enemy moved with effect: game end
            self._moveGen.checkBoardIfGameOver(self._gameover, board, False)

            if (self._gameover != DictMoveEntry.CONTINUE_GAME):
                return maxScore
            moveList = self._moveGen.genMoves(myColor, self._gameover, cboard)
            if (len(moveList) == 0):
                return maxScore
            # print("testmodus",self._testmodus)
            if (self._testmodus):

                scoredMoveList = self._evalR.computeOverallScore(moveList, cboard,
                                                                 False) if myColor == Player.Red else self._evalB.computeOverallScore(
                    moveList, cboard, False)

                for moveItem in scoredMoveList:

                    newBoard = self._moveGen.execSingleMove(moveItem, myColor, self._gameover, cboard)

                    self._moveGen.checkBoardIfGameOver(self._gameover, newBoard, False)
                    if (self._gameover[0] != DictMoveEntry.CONTINUE_GAME):
                        return moveItem[3]

                    retVal = self._alpha_beta(alpha, beta, depth - 1, maxPlayer, newBoard, changedColor)

                    maxScore = max(maxScore, retVal)
                    alpha = max(alpha, retVal)

                    if (beta <= alpha):
                        break
                print("maxscore:", maxScore)
            return maxScore
        else:
            minScore = self._BETA_INIT

            # print("Beta my color=", myColor)
            # case: enemy moved with effect: game end
            self._moveGen.checkBoardIfGameOver(self._gameover, board, False)

            if (self._gameover != DictMoveEntry.CONTINUE_GAME):
                return minScore
            # best move at the beginning at the list
            moveList = self._moveGen.genMoves(myColor, self._gameover, cboard)
            if (len(moveList) == 0):
                return minScore

            if (self._testmodus):

                scoredMoveList = self._evalR.computeOverallScore(moveList,
                                                                 cboard) if myColor == Player.Red else self._evalB.computeOverallScore(
                    moveList, cboard)

                for moveItem in scoredMoveList:

                    newBoard = self._moveGen.execSingleMove(moveItem, myColor, self._gameover, cboard)

                    self._moveGen.checkBoardIfGameOver(self._gameover, newBoard, False)
                    if (self._gameover[0] != DictMoveEntry.CONTINUE_GAME):
                        return moveItem[3]

                    retVal = self._alpha_beta(alpha, beta, depth - 1, maxPlayer, newBoard, changedColor)

                    minScore = min(minScore, retVal)
                    alpha = min(beta, retVal)

                    if (beta <= alpha):
                        break

            return minScore

    def change_player(self, player):
        return Player.Blue if player == Player.Red else Player.Red

    def _convertPlayerString(self, pstr: str):
        return Player.Red if pstr == "r" else Player.Blue
