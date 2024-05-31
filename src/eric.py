import copy
import time

from evalFunction import *
from gamestate import *
from gui import *
from scoreConfig_evalFunc import *
from moveGenerator import MoveGenerator
from moveLib import *
class AlphaBetaSearch:
    """
    This class implements the Alpha-Beta Search algorithm for a given game.
    """
    alpha = 0
    beta = 0
    gameOver = [DictMoveEntry.CONTINUE_GAME]
    alpha = [-float('inf')]
    beta = [float('inf')]
    def __init__(self, game: list, max_time: float = 0.5):
        """
        The constructor for AlphaBetaSearch class.
        """
        self.game = game
        self.start_time = time.time()
        self.max_time = max_time
        self.end_time = time.time() + self.max_time
        #self.depth = 2
        self.player = self.game[GET_PLAYER_INDEX]
        self.bitboards = GameState.createBitBoardFromFEN(game[GET_BOARD_INDEX])
        #self.alpha = -float('inf')
        #self.beta = float('inf')
        self.move_lib = MoveLib()
        self.eval = EvalFunction(ScoreConfig.Version1(), self.player)
        self.moveGen = MoveGenerator(self.bitboards)
        self.gameOver = [DictMoveEntry.CONTINUE_GAME]
    def search(self, use_iterative_deepening: bool = False):
        """
        The function to start the Alpha-Beta Search.
        """

        if use_iterative_deepening:
            return self._iterative_deepening_search()
        else:
            _, best_move = self._alpha_beta_max(self.alpha, self.beta, self.depth, self.bitboards)
            print("Best move: ", self.move_lib.move(best_move[0], best_move[1],3))
            return best_move

    def _iterative_deepening_search(self):
        best_move = None
        depth = 2
        index = 0
        bool = True
        while bool:
            print("index", index)
            _, move = self._alpha_beta_max(self.alpha, self.beta, depth, self.bitboards)
            if move is not None:
                best_move = move

            if time.time() >= self.end_time or self.gameOver[0] != DictMoveEntry.CONTINUE_GAME:
                print("isOver",self.gameOver[0])
                #return best_move
                #break
                bool = False

            print("depth: {}, time: {}".format(depth, time.time() - self.start_time))
            #depth += 1

            index+=1
        print("best move",MoveLib.move(best_move[0], best_move[1],3), best_move[3])
        return best_move
    def _alpha_beta_max(self, alpha, beta, depth_left: int, bitboards, move=""):
        """
        The function to find the maximum score and the corresponding move.
        """

        print("depth_left",depth_left)
        if self.gameOver[0] != DictMoveEntry.CONTINUE_GAME:
            isOver = True
        if depth_left == 0 or self.gameOver[0] != DictMoveEntry.CONTINUE_GAME:
            best = self.eval.computeOverallScore(self.moveGen.genMoves(self.player, self.gameOver),
                                                 board=bitboards).pop()
            print("MOVE GEFUNDEN, totalscore=", best[3], move)
            return best[3], move

        scorelist = self.eval.computeOverallScore(self.moveGen.genMoves(self.player, self.gameOver), board=bitboards)
        best_move = None
        print("scoreList",scorelist)
        #for move in reversed(score_list):
        while(len(scorelist) > 0):
            move = scorelist.pop()
            print("Move:", move)
            if time.time() >= self.end_time:
                break
            old_boards = copy.deepcopy(bitboards)

            new_boards = self.moveGen.execSingleMove(move, self.player, self.gameOver)
            if(self.gameOver[0] != DictMoveEntry.CONTINUE_GAME):
                return move[3],move
            oldplayer = self.player
            self.change_player(self.player)

            score, _ = self._alpha_beta_min(alpha, beta, depth_left-1, new_boards)
            self.moveGen.updateBoard(old_boards, self.player, self.gameOver)


            print("score>=beta: ", score, ">=", beta)
            print("score>alpha: ", score, ">", alpha)
            if (score >= beta[0]):

                return beta, move  # fail hard beta-cutoff
            if score > alpha[0]:

                alpha[0] = score  # alpha acts like max in MiniMax
                best_move = move
        print("new Alpha =", alpha)
        return alpha[0], best_move

    def _alpha_beta_min(self, alpha: list, beta: list, depth_left: int, bitboards, move=""):
        """
        The function to find the minimum score and the corresponding move.
        """
        print("stop=depth_left", depth_left)

        if depth_left == 0 or self.gameOver[0] != DictMoveEntry.CONTINUE_GAME:
            scorelist = self.eval.computeOverallScore(self.moveGen.genMoves(self.player, self.gameOver), bitboards)
            best = self.eval.computeOverallScore(self.moveGen.genMoves(self.player, self.gameOver),
                                                 board=bitboards).pop()
            print("bet_min MOVE GEFUNDEN, totalscore=", best[3], move)

            return best[3], move
        scorelist = self.eval.computeOverallScore(self.moveGen.genMoves(self.player, self.gameOver), bitboards)
        best_move = None

        #´for move in reversed(scorelist):
        while (len(scorelist) > 0):
            move = scorelist.pop()
            print("Move:", move)
            if time.time() >= self.end_time:
                break
            old_boards = copy.deepcopy(bitboards)
            new_boards = self.moveGen.execSingleMove(move, self.player, self.gameOver)
            if (self.gameOver[0] != DictMoveEntry.CONTINUE_GAME):
                return move[3], move
            oldplayer = self.player
            self.change_player(self.player)

            score, _ = self._alpha_beta_max(alpha, beta, (depth_left - 1), new_boards)

            self.moveGen.updateBoard(old_boards, oldplayer, self.gameOver)

            if score <= alpha[0]:
                return alpha[0], move  # fail hard alpha-cutoff
            if score < beta[0]:
                beta[0] = score  # beta acts like min in MiniMax
                best_move = move
        print("new Beta =", beta)
        return beta[0], best_move

    def change_player(self, player):
        self.player = Player.Blue if player == Player.Red else Player.Red