from evalFunction import *
from gamestate import *
from gui import *
from scoreConfig_evalFunc import *
from moveGenerator import MoveGenerator

GET_PLAYER_INDEX = 1  # Replace with the actual index
GET_BOARD_INDEX = 0 

class AlphaBetaSearch:
    def __init__(self, game):
        self.moveGen = MoveGenerator()
        self.game = game
        self.player = self.game[GET_PLAYER_INDEX]
        self.gameOver = False  # or some other initial state
        self.bitboards = self.game[GET_BOARD_INDEX]  # Set this to the initial bitboards
        self.eval = EvalFunction(ScoreConfig.Version1(), self.player)  # Set this to an instance of your evaluation function

    def alpha_beta(self, tiefe, alpha, beta, bitboards):
        if tiefe == 0:
            return self.eval.computeOverallScore(self.moveGen.genMoves(self.player, self.gameOver),
                                                 board=bitboards).pop()
        PVgefunden = False
        best = float('-inf')
        Zugliste = self.moveGen.genMoves(self.player, self.gameOver)
        for Zug in Zugliste:
            old_boards = self.bitboards.copy()  # Save the old bitboards
            oldplayer = self.player  # Save the old player
            self.moveGen.execSingleMove(Zug, self.player, self.gameOver)
            if PVgefunden:
                wert = -self.alpha_beta(tiefe-1, -alpha-1, -alpha)
                if wert > alpha and wert < beta:
                    wert = -self.alpha_beta(tiefe-1, -beta, -wert)
            else:
                wert = -self.alpha_beta(tiefe-1, -beta, -alpha)
            self.moveGen.updateBoard(old_boards, oldplayer, self.gameOver)
            if wert > best:
                if wert >= beta:
                    return wert
                best = wert
                if wert > alpha:
                    alpha = wert
                    PVgefunden = True
        return best

    def search(self):
        test7 = "6/r07/8/8/8/8/1b06/6 b"
        board, player = test7.split(" ")
        player = Player.Blue if player == "b" else Player.Red
        bitboard = GameState.createBitBoardFromFEN(board)
        gameArray = [board, player, True, False]
        search_instance = AlphaBetaSearch()
        result = search_instance.search(gameArray)
        print(result)
        return self.alpha_beta(5,-10000,10000, bitboard)

    if __name__ == '__main__':
        self.search()