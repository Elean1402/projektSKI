from evalFunction import *
from gamestate import GameState
from gui import Gui
from scoreConfig_evalFunc import *
from moveGenerator import MoveGenerator


class AlphaBetaSearch:
    """
    This class implements the Alpha-Beta Search algorithm for a given game.

    Attributes:
        game (dict): The game state.
        depth (int): The maximum depth of the search tree.
        alpha (float): The best (highest) score that the maximizing player is assured of.
        beta (float): The best (lowest) score that the minimizing player is assured of.
    """

    def __init__(self, game: dict, depth=5):
        """
        The constructor for AlphaBetaSearch class.

        Parameters:
            game (dict): The game state.
            depth (int): The maximum depth of the search tree. Default is 5.
        """
        self.game = game
        self.depth = depth
        self.game["bitboards"] = GameState.createBitBoardFromFEN(game["board"])
        self.player = self.game["player"]
        self.alpha = -float('inf')
        self.beta = float('inf')
        self.m = MoveLib()
        self.eval = EvalFunction(ScoreConfig.Version1(), self.player)
        self.moveGen = MoveGenerator(self.game["bitboards"])
        self.gameOver = [DictMoveEntry.CONTINUE_GAME]

    def search(self):
        """
        The function to start the Alpha-Beta Search.

        Returns:
            str: The best move.
        """
        best_score, best_move = self.alpha_beta_max(self.alpha, self.beta, self.depth, self.game, "A3-A4")
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
        if self.gameOver != [DictMoveEntry.CONTINUE_GAME]:
            best = self.eval.computeOverallScore(self.moveGen.genMoves(self.player, self.gameOver),
                                                 board=game["bitboards"]).pop()
            return best[3], move

        scorelist = self.eval.computeOverallScore(self.moveGen.genMoves(self.player, self.gameOver), board=game["bitboards"])
        best_score = alpha
        best_move = None

        for move in reversed(scorelist):
            new_dict = game.copy()
            new_dict["bitboards"] = self.moveGen.execSingleMove(move, self.player, self.gameOver)
            oldplayer = self.player
            self.change_player(self.player)
            score, _ = self.alpha_beta_min(alpha, beta, depth_left - 1, new_dict, move)
            self.moveGen.updateBoard(game["bitboards"], oldplayer, self.gameOver)
            # retract move
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

        if self.gameOver != [DictMoveEntry.CONTINUE_GAME]:
            best = self.eval.computeOverallScore(self.moveGen.genMoves(self.player, self.gameOver), board=game["bitboards"]).pop()
            return best[3], move

        scorelist = self.eval.computeOverallScore(self.moveGen.genMoves(self.player, self.gameOver), board=game["bitboards"])
        best_score = beta
        best_move = None

        for move in reversed(scorelist):
            new_dict = game.copy()
            new_dict["bitboards"] = new_board = self.moveGen.execSingleMove(move, self.player, self.gameOver)
            oldplayer = self.player
            self.change_player(self.player)
            score, _ = self.alpha_beta_max(alpha, beta, depth_left - 1, new_dict, move)
            self.moveGen.updateBoard(game["bitboards"], oldplayer, self.gameOver)
            # retract move
            if score <= alpha:
                return alpha, move  # fail hard alpha-cutoff
            if score < beta:
                beta = score  # beta acts like min in MiniMax
                best_move = move

        return beta, best_move

    def change_player(self, player):
        self.player = Player.Blue if player == Player.Red else Player.Red