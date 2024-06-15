class TimeExceeded(Exception):
    pass


class MinimaxSearch:
    def __init__(self, game):
        self.move_count2 = 0
        self.move_count = 0
        self.game = game
        self.player = game["player"]
        self.opponent = Player.Red if self.player == Player.Blue else Player.Blue
        self.eval = EvalFunction(ScoreConfig.Version2(self.player, self.player))
        self.evalo = EvalFunction(ScoreConfig.Version2(self.player, self.opponent))
        self.gameover = [DictMoveEntry.CONTINUE_GAME]
        self.total_gameover = False
        self.bitboards = game["bitboards"]
        self.moveGen = MoveGenerator(self.bitboards)
        self.best_move = None
        self.time_limit = 100000
        self.start_time = time.time()

    def search(self, time_limit=100, depth=2):
        self.start_time = time.time()
        self.time_limit = time_limit
        try:
            result, temp_move = self.minimaxMax(depth, self.bitboards)
            if temp_move is not None:
                self.best_move = temp_move
        except TimeExceeded:
            pass
        print(f"Total scoresmoves looked at: {self.move_count}")
        print(f"Total moves looked at: {self.move_count2}")
        return self.best_move

    def minimaxMax(self, depthleft, bitboards):
        bitboard = bitboards.copy()
        moves = self.moveGen.genMoves(self.player, self.gameover, bitboard)
        self.moveGen.checkBoardIfGameOver(self.gameover, bitboard)
        if self.gameover[0] != DictMoveEntry.CONTINUE_GAME or depthleft == 0 or not moves:
            if self.gameover[0] != DictMoveEntry.CONTINUE_GAME:
                self.total_gameover = True
            points = self.eval.computeOverallScore(moves, bitboard)[0][3]
            return points, None
        scorelist = self.evalo.computeOverallScore(moves, bitboard, False)
        best_score = -float('inf')
        best_move = None
        for move in scorelist:
            self.move_count += 1
            if time.time() - self.start_time > self.time_limit:
                raise TimeExceeded()
            new_board = self.moveGen.execSingleMove(move, self.player, self.gameover, bitboard, False)
            score, _ = self.minimaxMin(depthleft - 1, new_board)
            if score > best_score:
                best_move = scorelist[0]
                best_score = score
        return best_score, best_move

    def minimaxMin(self, depthleft, bitboards):
        bitboard = bitboards.copy()
        moves = self.moveGen.genMoves(self.opponent, self.gameover, bitboard)
        self.moveGen.checkBoardIfGameOver(self.gameover, bitboard)
        if self.gameover[0] != DictMoveEntry.CONTINUE_GAME or depthleft == 0 or not moves:
            if self.gameover[0] != DictMoveEntry.CONTINUE_GAME:
                self.total_gameover = True
            points = self.evalo.computeOverallScore(moves, bitboard)[0][3]
            return points, None
        scorelist = self.evalo.computeOverallScore(moves, bitboard, False)
        best_score = float('inf')
        best_move = None
        for move in scorelist:
            self.move_count += 1
            if time.time() - self.start_time > self.time_limit:
                raise TimeExceeded()
            new_board = self.moveGen.execSingleMove(move, self.opponent, self.gameover, bitboard, False)
            score, _ = self.minimaxMax(depthleft - 1, new_board)
            if score < best_score:
                best_move = scorelist[0]
                best_score = score
        return best_score, best_move