from moveLib import *
from evalFunction import *
from scoreConfig_evalFunc import *
from gui import Gui
from gamestate import GameState
from benchmark import Benchmark
class AlphaBetaSearch:
    """
    This class implements the Alpha-Beta Search algorithm for a given game.

    Attributes:
        game (dict): The game state.
        depth (int): The maximum depth of the search tree.
        alpha (float): The best (highest) score that the maximizing player is assured of.
        beta (float): The best (lowest) score that the minimizing player is assured of.
    """

    def __init__(self, game: dict, depth = 5):
        """
        The constructor for AlphaBetaSearch class.

        Parameters:
            game (dict): The game state.
            depth (int): The maximum depth of the search tree. Default is 5.
        """
        self.game = game
        self.depth = depth
        self.game["bitboard"] = GameState.createBitBoardFrom(Gui.fenToMatrix(game["board"]), True)
        self.alpha = -float('inf')
        self.beta = float('inf')
        self.m = MoveLib()
        self.efblue = EvalFunction(ScoreConfig.Version1(), Player.Blue)
        self.efred = EvalFunction(ScoreConfig.Version1(), Player.Red)

    def search(self, use_iterative_deepening=False):
        """
        The function to start the Alpha-Beta Search.
    
        Parameters:
            use_iterative_deepening (bool): Whether to use Iterative Deepening Depth-First Search. Default is False.
    
        Returns:
            str: The best move.
        """
        if use_iterative_deepening:
            best_move = None
            for depth in range(1, self.depth + 1):
                _, move = self.alpha_beta_max(self.alpha, self.beta, depth, self.game, None)
                if move is not None:
                    best_move = move
            return best_move
        else:
            _, best_move = self.alpha_beta_max(self.alpha, self.beta, self.depth, self.game, None)
            return best_move

    def alpha_beta_max(self, alpha, beta, depth_left: int, game: dict, move: str):
        """
        The function to find the maximum score and the corresponding move.

        Parameters:
            alpha (float): The best (highest) score that the maximizing player is assured of.
            beta (float): The best (lowest) score that the minimizing player is assured of.
            depth_left (int): The remaining depth of the search tree.
            game (dict): The game state.
            move (str): The current move.

        Returns:
            tuple: The maximum score and the corresponding move.
        """
        if depth_left == 0:
            return 2, move

        scorelist = self.efblue.computeOverallScore(gen, board=game["bitboard"])
        best_score = alpha
        best_move = None

        for move in reversed(scorelist):
            score, _ = self.alpha_beta_min(alpha, beta, depth_left - 1, game, move)
            if score >= beta:
                return beta, move  # fail hard beta-cutoff
            if score > alpha:
                alpha = score  # alpha acts like max in MiniMax
                best_move = move

        return alpha, best_move

    def alpha_beta_min(self, alpha, beta, depth_left: int, game: dict, move: str):
        """
        The function to find the minimum score and the corresponding move.

        Parameters:
            alpha (float): The best (highest) score that the maximizing player is assured of.
            beta (float): The best (lowest) score that the minimizing player is assured of.
            depth_left (int): The remaining depth of the search tree.
            game (dict): The game state.
            move (str): The current move.

        Returns:
            tuple: The minimum score and the corresponding move.
        """
        if depth_left == 0:
            return 3, move

        scorelist = self.efred.computeOverallScore(gen, board=game["bitboard"])
        best_score = beta
        best_move = None

        for move in reversed(scorelist):
            score, _ = self.alpha_beta_max(alpha, beta, depth_left - 1, game, move)
            if score <= alpha:
                return alpha, move  # fail hard alpha-cutoff
            if score < beta:
                beta = score  # beta acts like min in MiniMax
                best_move = move

        return beta, best_move
    
    