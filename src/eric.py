import time

from evalFunction import *
from gamestate import *
from gui import *
from scoreConfig_evalFunc import *


class AlphaBetaSearch:
    """
    This class implements the Alpha-Beta Search algorithm for a given game.
    """

    def __init__(self, game: dict, max_time: float = 5.0):
        """
        The constructor for AlphaBetaSearch class.
        """
        self.game = game
        self.start_time = time.time()
        self.max_time = max_time
        self.end_time = time.time() + self.max_time
        self.depth = 5
        self.bitboard = GameState.createBitBoardFrom(Gui.fenToMatrix(game["board"]), True)
        self.alpha = -float('inf')
        self.beta = float('inf')
        self.move_lib = MoveLib()
        self.eval_func_blue = EvalFunction(ScoreConfig.Version1(), Player.Blue)
        self.eval_func_red = EvalFunction(ScoreConfig.Version1(), Player.Red)

    def search(self, use_iterative_deepening: bool = False):
        """
        The function to start the Alpha-Beta Search.
        """

        if use_iterative_deepening:
            return self._iterative_deepening_search()
        else:
            _, best_move = self._alpha_beta_max(self.alpha, self.beta, self.depth, self.game)
            return best_move

    def _iterative_deepening_search(self):
        best_move = None
        depth = 1

        while True:
            _, move = self._alpha_beta_max(self.alpha, self.beta, depth, self.game)
            if move is not None:
                best_move = move

            if time.time() >= self.end_time:
                return best_move

            depth += 1

    def _alpha_beta_max(self, alpha: float, beta: float, depth_left: int, game: dict, move=""):
        """
        The function to find the maximum score and the corresponding move.
        """
        if depth_left == 0:  # or game_over(game):
            return self.eval_func_blue.computeOverallScore(gen, board=self.bitboard), move

        score_list = self.eval_func_blue.computeOverallScore(gen, board=self.bitboard)
        best_move = None

        for move in reversed(score_list):
            if time.time() >= self.end_time:
                break
            score, _ = self._alpha_beta_min(alpha, beta, depth_left - 1, game, move)
            if score >= beta:
                return beta, move  # fail hard beta-cutoff
            if score > alpha:
                alpha = score  # alpha acts like max in MiniMax
                best_move = move

        return alpha, best_move

    def _alpha_beta_min(self, alpha: float, beta: float, depth_left: int, game: dict, move=""):
        """
        The function to find the minimum score and the corresponding move.
        """
        if depth_left == 0:  # or game_over(game):
            return self.eval_func_blue.computeOverallScore(gen, board=game["bitboard"]), move

        score_list = self.eval_func_red.computeOverallScore(gen, board=game["bitboard"])
        best_move = None

        for move in reversed(score_list):
            if time.time() >= self.end_time:
                break
            score, _ = self._alpha_beta_max(alpha, beta, depth_left - 1, game, move)
            if score <= alpha:
                return alpha, move  # fail hard alpha-cutoff
            if score < beta:
                beta = score  # beta acts like min in MiniMax
                best_move = move

        return beta, best_move
