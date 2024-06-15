import os
import sys
from collections import Counter
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gamestate import GameState
from src.model import *
from src.moveLib import MoveLib
from src.moveGenerator import MoveGenerator

class EvalFunction:
    _TURNOPTIONS = 0
    _player = 0
    _CONFIG_DICT = {
        Config.TURN_OPTIONS: -1,
        Config.MAT_PAWN: -1,
        Config.MAT_KNIGHT: -1,
        Config.TOTAL_SCORE_RATING_PAWN_BLUE: {},
        Config.TOTAL_SCORE_RATING_KNIGHT_BLUE: {},
        Config.TOTAL_SCORE_RATING_PAWN_RED: {},
        Config.TOTAL_SCORE_RATING_KNIGHT_RED: {},
        Config.MaxPlayer: Player.NoOne,
        Config.Player: Player.NoOne,
        Config.CONFIGVERSION: None
    }

    __RANGE = np.array([1, 6, 1, 1], dtype=np.uint64)
    __ZERO = np.uint64(0)

    def __init__(self, config: dict):
        if len(self._CONFIG_DICT) != len(config):
            raise ValueError("Configs do not have the same size")
        self._CONFIG_DICT.update(config)
        vals = self._CONFIG_DICT.values()
        if any(x == -1 for x in vals):
            raise ValueError("Config is not complete, missing key-value pair")
        if any(len(self._CONFIG_DICT[key]) == 0 for key in [
            Config.TOTAL_SCORE_RATING_PAWN_BLUE, Config.TOTAL_SCORE_RATING_KNIGHT_BLUE,
            Config.TOTAL_SCORE_RATING_PAWN_RED, Config.TOTAL_SCORE_RATING_KNIGHT_RED]):
            raise ValueError("Config: PIECESQUARE_TABLE_{Pawn,Knight} Dictionary not set")
        if self._CONFIG_DICT[Config.Player] == Player.NoOne:
            raise ValueError("Player not set")
        if self._CONFIG_DICT[Config.MaxPlayer] == Player.NoOne:
            raise ValueError("MaxPlayer not set")
        if self._CONFIG_DICT[Config.CONFIGVERSION] is None:
            raise ValueError("CONFIGVERSION NOT SET")

    def __mobility(self, board: list[np.uint64]):
        return 0

    def __turnOptions(self, size: int):
        self._TURNOPTIONS += size

    def _computeTurnOptions(self):
        val = self._TURNOPTIONS * self._CONFIG_DICT[Config.TURN_OPTIONS]
        self._TURNOPTIONS = 0
        return val

    def _moveIsNeighbourOfStartPos(self, startPos: np.uint64, targetPos: np.uint64):
        for shift in self.__RANGE:
            if (startPos << shift == targetPos) or (startPos >> shift == targetPos):
                return True
        return False

    def _scoreRating(self, startPos: np.uint64, targetmoves: list[np.uint64], board: list[np.uint64],
                     boardcommands: list[BoardCommand]):
        scoreList = ScoreListForMerging()
        targetScores = Counter()
        is_pawn = lambda pos: self._moveIsNeighbourOfStartPos(startPos, pos)

        pawn_mask = ~(board[GameState._ZARR_INDEX_B_KNIGHTS] | board[GameState._ZARR_INDEX_R_KNIGHTS])

        def update_scores(start_mask, score_dict, condition):
            targetScores.update(
                {key: score_dict[MoveLib.BitsToPosition(key)] for key in targetmoves if condition(startPos & start_mask, key)}
            )

        if startPos & board[GameState._ZARR_INDEX_R_PAWNS] & pawn_mask:
            update_scores(board[GameState._ZARR_INDEX_R_PAWNS], self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_PAWN_RED], is_pawn)
        elif startPos & board[GameState._ZARR_INDEX_R_KNIGHTS]:
            update_scores(board[GameState._ZARR_INDEX_R_KNIGHTS], self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_KNIGHT_RED], lambda s, k: not is_pawn(k))
        elif startPos & board[GameState._ZARR_INDEX_B_PAWNS] & pawn_mask:
            update_scores(board[GameState._ZARR_INDEX_B_PAWNS], self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_PAWN_BLUE], is_pawn)
        elif startPos & board[GameState._ZARR_INDEX_B_KNIGHTS]:
            update_scores(board[GameState._ZARR_INDEX_B_KNIGHTS], self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_KNIGHT_BLUE], lambda s, k: not is_pawn(k))

        if not targetScores:
            raise ValueError("Error in MoveList, please check Zuggenerator, move=", MoveLib.move(startPos, targetmoves[0], 3))

        scoreList.append((startPos, targetScores, boardcommands))
        self.__turnOptions(len(targetmoves))

        return scoreList

    def _updateConfig(self, player: Player, board: list[np.uint64]):
        updatedConf = self._CONFIG_DICT[Config.CONFIGVERSION](self._CONFIG_DICT[Config.MaxPlayer], player, board)
        self._CONFIG_DICT = updatedConf

    def __protectedFigures(self, board: list[np.uint64]):
        return 0

    def __unprotectedFigures(self, board: list[np.uint64]):
        return 0

    def __upgradeFigure(self, board: list[np.uint64]):
        return 0

    def __blockedFigures(self, board: list[np.uint64]):
        return 0

    def _materialPoints(self, board: list[np.uint64]):
        count_bits = lambda mask: bin(mask)[2:].count("1")
        bp = count_bits(board[GameState._ZARR_INDEX_B_PAWNS] & ~board[GameState._ZARR_INDEX_R_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_PAWN]
        bk = count_bits(board[GameState._ZARR_INDEX_B_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_KNIGHT]
        rp = count_bits(board[GameState._ZARR_INDEX_R_PAWNS] & ~board[GameState._ZARR_INDEX_B_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_PAWN]
        rk = count_bits(board[GameState._ZARR_INDEX_R_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_KNIGHT]
        return rp + rk - bp - bk if self._CONFIG_DICT[Config.MaxPlayer] == Player.Red else bp + bk - rp - rk

    def computeOverallScore(self, moveList: list, board: list[np.uint64], printList=False, returnSortedList=True) -> ScoredMoveList:
        scoredList = ScoredMoveList()
        totalScore = 0
        if not moveList:
            totalScore += self._materialPoints(board)
            totalScore += self._computeActualPositionalPoints(board)
            scoredList.append((np.uint64(0), np.uint64(0), int(0), int(totalScore), []))
            return scoredList

        tempScore = ScoreListForMerging()
        self._updateConfig(self._CONFIG_DICT[Config.Player], board)

        for index in moveList:
            tempScore.append(self._scoreRating(index[0], index[1], board, index[2]))

        totalScore += self._materialPoints(board)
        totalScore += self._computeActualPositionalPoints(board)

        scoredList = [
            (startpos, targetPos, adict[targetPos], totalScore + adict[targetPos], bc)
            for startpos, adict, bc in tempScore
            for targetPos in adict
        ]

        if returnSortedList:
            scoredList.sort()

        if printList:
            self.prettyPrintScorelist(scoredList)

        return scoredList

    def _computeActualPositionalPoints(self, board: list[np.uint64]):
        def compute_points(pawn_index, knight_index, pawn_score_dict, knight_score_dict):
            points = 0
            for piece_index, score_dict in [(pawn_index, pawn_score_dict), (knight_index, knight_score_dict)]:
                positions = MoveGenerator.getBitPositions(board[piece_index])
                points += sum(score_dict[MoveLib.BitsToPosition(bits)] for bits in positions)
            return points

        max_player = self._CONFIG_DICT[Config.MaxPlayer]
        if max_player == Player.Red:
            max_indices = (GameState._ZARR_INDEX_R_PAWNS, GameState._ZARR_INDEX_R_KNIGHTS)
            min_indices = (GameState._ZARR_INDEX_B_PAWNS, GameState._ZARR_INDEX_B_KNIGHTS)
            max_score_dicts = (self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_PAWN_RED], self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_KNIGHT_RED])
            min_score_dicts = (self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_PAWN_BLUE], self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_KNIGHT_BLUE])
        else:
            max_indices = (GameState._ZARR_INDEX_B_PAWNS, GameState._ZARR_INDEX_B_KNIGHTS)
            min_indices = (GameState._ZARR_INDEX_R_PAWNS, GameState._ZARR_INDEX_R_KNIGHTS)
            max_score_dicts = (self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_PAWN_BLUE], self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_KNIGHT_BLUE])
            min_score_dicts = (self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_PAWN_RED], self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_KNIGHT_RED])

        position_points_max = compute_points(*max_indices, *max_score_dicts)
        position_points_min = compute_points(*min_indices, *min_score_dicts)

        return position_points_max - position_points_min

    def prettyPrintScorelist(self, list: ScoredMoveList):
        if list:
            print("Scorelist:")
            for s, t, v, u, z in list:
                print((MoveLib.move(s, t, 3), "movescore=", v, "totalscore=", u, z))
