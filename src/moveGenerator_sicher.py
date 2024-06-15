import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gamestate import *
from src.model import Player, BitMaskDict, DICT_MOVE, DictMoveEntry, BIT_MASK_ARRAY_KNIGHT_BLUE, \
    BIT_MASK_ARRAY_KNIGHT_RED, BIT_MASK_ARRAY_PAWN_BLUE, BIT_MASK_ARRAY_PAWN_RED, FilteredPositionsArray, \
    NotAccessiblePos, BoardCommand
from src.moveLib import MoveLib as mv


class MoveGenerator:
    # _board = np.array([np.uint64(0),np.uint64(0),np.uint64(0),np.uint64(0)])
    # _boardIsInitialized = False
    # _gameover = False
    # _WinnerIs = Player.NoOne

    def __init__(self, board: list[np.uint64]):
        """ Must use Gamestate._ZARR_... constants as indices
            for board.
            e.g. board[Gamestate._ZARR_INDEX_R_PAWNS] ...
        Args:
            board (list[np.uint64]): Bitboard Array of length 4
        """

        print("Board init:")
        self.prettyPrintBoard(board)

    def genMoves(self, player: Player, gameOver: list[DictMoveEntry], board: list[np.uint64]):
        """Generates all possible Moves
           ATTENTION IF LIST IS EMPTY GAME OVER

        Args:
            player (Player): use model.py
            gameOver (list[DictMoveEntry]): similiar to: OUT gameover. holds DictMoveEntry.CONTINUE | DictMoveEntry.GAME_OVER_BLUE_WINS | DictMoveEntry.GAME_OVER_RED_WINS
        Returns:
            list[Tuple[start,target,list[Boardcommands]]]
            if no possible Move empty list and this should lead into Gameover
        """
        if not isinstance(gameOver, list) or not isinstance(*gameOver, DictMoveEntry):
            raise TypeError("Please use for param. gameOver: e.g gameOver = [DictMoveEntry.CONTINUE]")
        # check if game is over
        # TODO
        return self._genValidatedMoves(player, gameOver, board)

    def _startPosBelongsToPlayer(self, player: Player, pos: np.uint64, board: list[np.uint64]):
        """Double Check if startpos belongs to player

        Args:
            player (Player): use model.py
            pos (np.uint64): position of Figure

        Raises:
            TypeError: if player is not of Type Player

        Returns:
            boolean: true if correct otherwise false
        """
        if player not in [Player.Blue, Player.Red]:
            raise TypeError("player is not from Type Player")

        player_pawns = board[GameState._ZARR_INDEX_B_PAWNS] if player == Player.Blue else board[
            GameState._ZARR_INDEX_R_PAWNS]
        player_knights = board[GameState._ZARR_INDEX_B_KNIGHTS] if player == Player.Blue else board[
            GameState._ZARR_INDEX_R_KNIGHTS]
        opponent_knights = board[GameState._ZARR_INDEX_R_KNIGHTS] if player == Player.Blue else board[
            GameState._ZARR_INDEX_B_KNIGHTS]

        posBelongsToPlayer = False
        if (player_pawns & pos & ~(
                player_knights | opponent_knights) == pos or player_knights & pos & ~opponent_knights == pos):
            posBelongsToPlayer = True

        return posBelongsToPlayer

    def _checkTargetPos(self, player: Player, move: tuple, board: list[np.uint64]):
        start, target, bitmask = move

        if start == target:
            return [BoardCommand.Cannot_Move]

        board_pawns = board[GameState._ZARR_INDEX_B_PAWNS]
        board_knights = board[GameState._ZARR_INDEX_B_KNIGHTS]
        board_r_knights = board[GameState._ZARR_INDEX_R_KNIGHTS]
        board_r_pawns = board[GameState._ZARR_INDEX_R_PAWNS]

        all_pawns = board_pawns | board_r_pawns
        all_knights = board_knights | board_r_knights

        is_clear_target = (target & ~(all_pawns | all_knights)) == target

        if player == Player.Blue:
            start_pawn = (start & board_pawns) and not (start & all_knights)
            start_knight = start & board_knights
            target_pawn = (target & board_pawns) and not (target & all_knights)
            target_knight = target & board_knights
            target_r_pawn = (target & board_r_pawns) and not (target & board_knights)
            target_r_knight = target & board_r_knights

            if start_pawn:
                if bitmask in {BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT],
                               BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT]}:
                    if target_r_knight:
                        return [BoardCommand.Hit_Red_KnightOnTarget, BoardCommand.Move_Blue_Knight_no_Change]
                    elif target_r_pawn:
                        return [BoardCommand.Hit_Red_PawnOnTarget, BoardCommand.Move_Blue_Pawn_no_Change]
                elif is_clear_target:
                    return [BoardCommand.Move_Blue_Pawn_no_Change]
                elif target_pawn:
                    return [BoardCommand.Upgrade_Blue_KnightOnTarget]
                # Handle other conditions here as needed

            elif start_knight:
                if is_clear_target:
                    return [BoardCommand.Degrade_Blue_KnightOnTarget]
                elif target_pawn:
                    return [BoardCommand.Move_Blue_Knight_no_Change]
                elif target_r_pawn:
                    return [BoardCommand.Hit_Red_PawnOnTarget, BoardCommand.Degrade_Blue_KnightOnTarget]
                elif target_knight:
                    return [BoardCommand.Cannot_Move]
                elif target_r_knight:
                    return [BoardCommand.Hit_Red_KnightOnTarget, BoardCommand.Move_Blue_Knight_no_Change]

        elif player == Player.Red:
            start_pawn = (start & board_r_pawns) and not (start & all_knights)
            start_knight = start & board_r_knights
            target_pawn = (target & board_pawns) and not (target & board_knights)
            target_knight = target & board_knights
            target_r_pawn = (target & board_r_pawns) and not (target & all_knights)
            target_r_knight = target & board_r_knights

            if start_pawn:
                if bitmask in {BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT],
                               BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT]}:
                    if target_knight:
                        return [BoardCommand.Hit_Blue_KnightOnTarget, BoardCommand.Move_Red_Knight_no_Change]
                    elif target_pawn:
                        return [BoardCommand.Hit_Blue_PawnOnTarget, BoardCommand.Move_Red_Pawn_no_Change]
                elif is_clear_target:
                    return [BoardCommand.Move_Red_Pawn_no_Change]
                elif target_r_pawn:
                    return [BoardCommand.Upgrade_Red_KnightOnTarget]
                # Handle other conditions here as needed

            elif start_knight:
                if is_clear_target:
                    return [BoardCommand.Degrade_Red_KnightOnTarget]
                elif target_r_pawn:
                    return [BoardCommand.Move_Red_Knight_no_Change]
                elif target_pawn:
                    return [BoardCommand.Hit_Blue_PawnOnTarget, BoardCommand.Degrade_Red_KnightOnTarget]
                elif target_r_knight:
                    return [BoardCommand.Cannot_Move]
                elif target_knight:
                    return [BoardCommand.Hit_Blue_KnightOnTarget, BoardCommand.Move_Red_Knight_no_Change]

        return [BoardCommand.Cannot_Move]

    def _genValidatedMoves(self, player: Player, gameOver: list[DictMoveEntry], board: list[np.uint64]) -> list[
        tuple[np.uint64, np.uint64, list[BoardCommand]]]:
        """Generates all unvalidated Moves of Player Blue or Red"""

        pawnsPositions = self._getAllPawns(player, board)
        knightPositions = self._getAllKnights(player, board)

        filteredPositions = FilteredPositionsArray()

        pawn_bitmasks, knight_bitmasks = {
            Player.Red: (BIT_MASK_ARRAY_PAWN_RED, BIT_MASK_ARRAY_KNIGHT_RED),
            Player.Blue: (BIT_MASK_ARRAY_PAWN_BLUE, BIT_MASK_ARRAY_KNIGHT_BLUE)
        }[player]

        for bitmask in pawn_bitmasks:
            filteredPositions.append((bitmask, self._filterPositions(player, pawnsPositions, bitmask)))
        for bitmask in knight_bitmasks:
            filteredPositions.append((bitmask, self._filterPositions(player, knightPositions, bitmask)))

        validatedMoves = [
            (*target, boardCommands)
            for (bm, filteredBits) in filteredPositions
            for bit in self.getBitPositions(filteredBits)
            if (target := self._getTarget(bit, bm)) and
               (boardCommands := self._checkTargetPos(player, (*target, bm), board)) is not None and
               BoardCommand.Cannot_Move not in boardCommands
        ]

        if not validatedMoves:
            gameOver[0] = (DictMoveEntry.GAME_OVER_BLUE_WINS if player == Player.Red else
                           DictMoveEntry.GAME_OVER_RED_WINS if player == Player.Blue else
                           DictMoveEntry.CONTINUE_GAME)

        return validatedMoves

    @classmethod
    def getBitPositions(self, n: np.uint64):
        """ Returns Generator over the Bits of n
        THIS FUNC IS FROM SOURCE:
        https://stackoverflow.com/questions/8898807/pythonic-way-to-iterate-over-bits-of-integer

        """
        one = np.uint64(1)
        while n:
            b = n & (~n + one)
            yield b
            n ^= b

    BITMASK_OPERATIONS = {BitMaskDict[DictMoveEntry.PAWN_TO_LEFT]: lambda x: x << DICT_MOVE[DictMoveEntry.PAWN_TO_LEFT],
                          BitMaskDict[DictMoveEntry.PAWN_TO_RIGHT]: lambda x: x >> DICT_MOVE[
                              DictMoveEntry.PAWN_TO_RIGHT],
                          BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM]: lambda x: x >> DICT_MOVE[
                              DictMoveEntry.RED_PAWN_TO_BOTTOM],
                          BitMaskDict[DictMoveEntry.RED_KNIGHT_LEFT]: lambda x: x >> DICT_MOVE[
                              DictMoveEntry.RED_KNIGHT_LEFT],
                          BitMaskDict[DictMoveEntry.RED_KNIGHT_RIGHT]: lambda x: x >> DICT_MOVE[
                              DictMoveEntry.RED_KNIGHT_RIGHT],
                          BitMaskDict[DictMoveEntry.RED_KNIGHT_TO_BOTLEFT]: lambda x: x >> DICT_MOVE[
                              DictMoveEntry.RED_KNIGHT_TO_BOTLEFT],
                          BitMaskDict[DictMoveEntry.RED_KNIGHT_TO_BOTRIGHT]: lambda x: x >> DICT_MOVE[
                              DictMoveEntry.RED_KNIGHT_TO_BOTRIGHT],
                          BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP]: lambda x: x << DICT_MOVE[
                              DictMoveEntry.BLUE_PAWN_TO_TOP],
                          BitMaskDict[DictMoveEntry.BLUE_KNIGHT_LEFT]: lambda x: x << DICT_MOVE[
                              DictMoveEntry.BLUE_KNIGHT_LEFT],
                          BitMaskDict[DictMoveEntry.BLUE_KNIGHT_RIGHT]: lambda x: x << DICT_MOVE[
                              DictMoveEntry.BLUE_KNIGHT_RIGHT],
                          BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT]: lambda x: x << DICT_MOVE[
                              DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT],
                          BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT]: lambda x: x << DICT_MOVE[
                              DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT],
                          BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT]: lambda x: x >> DICT_MOVE[
                              DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT],
                          BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT]: lambda x: x >> DICT_MOVE[
                              DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT],
                          BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT]: lambda x: x << DICT_MOVE[
                              DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT],
                          BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT]: lambda x: x << DICT_MOVE[
                              DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT], }

    def _getTarget(self, filteredPos: np.uint64, bitmask: np.uint64):
        if filteredPos == 0:
            return np.uint64(0), np.uint64(0)

        return filteredPos, self.BITMASK_OPERATIONS[bitmask](filteredPos)

    def _getAllPawns(self, player: Player, board: list[np.uint64]):
        """Gets all Pawns of player Blue or Red which can Move
        Arguments: player (Player): see model.py
        Returns: pos (np.uint64): All pawn positions of player"""
        pos = np.uint64(0)
        if player == Player.Red:
            pos |= (board[GameState._ZARR_INDEX_R_PAWNS] & (~board[GameState._ZARR_INDEX_R_KNIGHTS]) & (
                ~ board[GameState._ZARR_INDEX_B_KNIGHTS]))
        elif player == Player.Blue:
            pos |= (board[GameState._ZARR_INDEX_B_PAWNS] & (~board[GameState._ZARR_INDEX_R_KNIGHTS]) & (
                ~ board[GameState._ZARR_INDEX_B_KNIGHTS]))
        else:
            raise ValueError("Choosed Player invalid, please use Player Class from model.py")
        return pos

    def _getAllKnights(self, player: Player, board: list[np.uint64]):
        if player == Player.Red:
            return board[GameState._ZARR_INDEX_R_KNIGHTS]
        elif player == Player.Blue:
            return board[GameState._ZARR_INDEX_B_KNIGHTS]
        else:
            raise TypeError("parameter player is not from class Player, please use model.py: e.g. Player.Blue..")

    def _filterPositions(self, player: Player, positions: np.uint64, bitmask: np.uint64):
        """ Assuming Red starts at top
            ***optimize case pattern with Dict lookup later***
            Filters the positions of figures which can theoretically move in the direction described by Bitmask

        Args:
            player (Player): enum - see model.py
            positions (np.uint64): single Bitboard
            bitmask (BitMaskDict[DictMoveEntry): Filtermask for processing possible Moves

        Returns:
            positions (np.uint64): All possible Positions which can move in direction described by Bitmask
        """
        if ((player == Player.Red and (bitmask == BitMaskDict[DictMoveEntry.PAWN_TO_LEFT] or bitmask == BitMaskDict[
            DictMoveEntry.PAWN_TO_RIGHT] or bitmask == BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM] or bitmask ==
                                       BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT] or bitmask == BitMaskDict[
                                           DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT] or bitmask == BitMaskDict[
                                           DictMoveEntry.RED_KNIGHT_LEFT] or bitmask == BitMaskDict[
                                           DictMoveEntry.RED_KNIGHT_RIGHT] or bitmask == BitMaskDict[
                                           DictMoveEntry.RED_KNIGHT_TO_BOTLEFT] or bitmask == BitMaskDict[
                                           DictMoveEntry.RED_KNIGHT_TO_BOTRIGHT])) or (player == Player.Blue and (
                bitmask == BitMaskDict[DictMoveEntry.PAWN_TO_LEFT] or bitmask == BitMaskDict[
            DictMoveEntry.PAWN_TO_RIGHT] or bitmask == BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP] or bitmask ==
                BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT] or bitmask == BitMaskDict[
                    DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT] or bitmask == BitMaskDict[
                    DictMoveEntry.BLUE_KNIGHT_LEFT] or bitmask == BitMaskDict[
                    DictMoveEntry.BLUE_KNIGHT_RIGHT] or bitmask == BitMaskDict[
                    DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT] or bitmask == BitMaskDict[
                    DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT]))):
            # only positions which can move in direction of description of bitmask
            positions = positions & bitmask
        else:
            raise ValueError("Bitmask and choosed Player are wrong")
        return positions

    @classmethod
    def checkBoardIfGameOver(cls, gameOver: list[DictMoveEntry], board: list[np.uint64], printBoard=False):
        """Game is over if last Row is reached or no possible Moves
        Returns: Boolean: True for win else loose"""
        if printBoard:
            cls.prettyPrintBoard(cls, board, gameOver)

        blue_pieces = board[GameState._ZARR_INDEX_B_KNIGHTS] | board[GameState._ZARR_INDEX_B_PAWNS]
        red_pieces = board[GameState._ZARR_INDEX_R_KNIGHTS] | board[GameState._ZARR_INDEX_R_PAWNS]

        if (blue_pieces & BitMaskDict[DictMoveEntry.GAME_OVER_BLUE_WINS]) != 0 or red_pieces == 0:
            gameOver[0] = DictMoveEntry.GAME_OVER_BLUE_WINS
        elif (red_pieces & BitMaskDict[DictMoveEntry.GAME_OVER_RED_WINS]) != 0 or blue_pieces == 0:
            gameOver[0] = DictMoveEntry.GAME_OVER_RED_WINS

        if gameOver[0] != DictMoveEntry.CONTINUE_GAME:
            if printBoard:
                print("Game Over")
                cls.prettyPrintBoard(cls, board, gameOver)

    def execSingleMove(self, move: tuple, player: Player, gameOver: list[DictMoveEntry], board: list[np.uint64],
                       printB: bool = False):
        """Executes single Move and updates the Board and checks if Game Over

        Args:
            move (tuple): (startpos: uint64, targetpos: uint64, moveScore: int, totalscore: int,  list[BoardCommands])
            player (Player): Red or Blue
            gameOver (list[DictMoveEntry]):
            board (list[np.uint64]): _description_
            printB (bool, optional): _description_. Defaults to False.

        Returns:
             (Array[uint64]): Copy of Board
        """

        boardCopy = board.copy()
        # TODO check if Board is initialized
        # if(not boardIsInitialized):
        #     raise ValueError("Board is not initialized!")
        # Can this happen?
        if len(move) == 0:
            print("move is empty, Game Over")
            gameOver[
                0] = DictMoveEntry.GAME_OVER_BLUE_WINS if player == Player.Blue else DictMoveEntry.GAME_OVER_RED_WINS
            return boardCopy
        startpos = move[0]
        targetpos = move[1]
        boardCommands = move[2]
        # TODO exec Move
        for bc in boardCommands:
            bc = BoardCommand(bc)
            if bc == BoardCommand.Hit_Red_PawnOnTarget:
                boardCopy[GameState._ZARR_INDEX_R_PAWNS] &= ~targetpos
            elif bc == BoardCommand.Hit_Blue_PawnOnTarget:
                boardCopy[GameState._ZARR_INDEX_B_PAWNS] &= ~targetpos
            elif bc == BoardCommand.Hit_Red_KnightOnTarget:
                boardCopy[GameState._ZARR_INDEX_R_KNIGHTS] &= ~targetpos
            elif bc == BoardCommand.Hit_Blue_KnightOnTarget:
                boardCopy[GameState._ZARR_INDEX_B_KNIGHTS] &= ~targetpos
            elif bc == BoardCommand.Upgrade_Blue_KnightOnTarget:
                boardCopy[GameState._ZARR_INDEX_B_KNIGHTS] |= targetpos
                boardCopy[GameState._ZARR_INDEX_B_PAWNS] &= ~ startpos
            elif bc == BoardCommand.Upgrade_Red_KnightOnTarget:
                boardCopy[GameState._ZARR_INDEX_R_KNIGHTS] |= targetpos
                boardCopy[GameState._ZARR_INDEX_R_PAWNS] &= ~ startpos
            elif bc == BoardCommand.Degrade_Blue_KnightOnTarget:
                boardCopy[GameState._ZARR_INDEX_B_PAWNS] |= targetpos
                boardCopy[GameState._ZARR_INDEX_B_KNIGHTS] &= ~ startpos
            elif bc == BoardCommand.Degrade_Red_KnightOnTarget:
                boardCopy[GameState._ZARR_INDEX_R_PAWNS] |= targetpos
                boardCopy[GameState._ZARR_INDEX_R_KNIGHTS] &= ~ startpos
            elif bc == BoardCommand.Move_Blue_Knight_no_Change:
                boardCopy[GameState._ZARR_INDEX_B_KNIGHTS] |= targetpos
                boardCopy[GameState._ZARR_INDEX_B_KNIGHTS] &= ~startpos
            elif bc == BoardCommand.Move_Red_Knight_no_Change:
                boardCopy[GameState._ZARR_INDEX_R_KNIGHTS] |= targetpos
                boardCopy[GameState._ZARR_INDEX_R_KNIGHTS] &= ~startpos
            elif bc == BoardCommand.Move_Blue_Pawn_no_Change:
                boardCopy[GameState._ZARR_INDEX_B_PAWNS] |= targetpos
                boardCopy[GameState._ZARR_INDEX_B_PAWNS] &= ~startpos
            elif bc == BoardCommand.Move_Red_Pawn_no_Change:
                boardCopy[GameState._ZARR_INDEX_R_PAWNS] |= targetpos
                boardCopy[GameState._ZARR_INDEX_R_PAWNS] &= ~startpos

        self.checkBoardIfGameOver(gameOver, boardCopy, printB)
        if printB == True:
            print("move executed, new Board ist:\n")
            self.prettyPrintBoard(boardCopy, gameOver)
        return boardCopy

    def prettyPrintBoard(self, board: list[np.uint64], *gameOver: list[DictMoveEntry]):
        # print("internal board", board)
        print("current Board\n", GameState.fromBitBoardToMatrix(board, True))
        if len(gameOver) != 0:
            print("Game status:", gameOver[0])  # raise ValueError("stop")
        print("1 = red, 4 = blue, 2 = rr, 3 = br, 5= rb, 8= bb")

    def prettyPrintMoves(self, moves: list):
        print("\nMoves generated from MoveGenerator:")
        if len(moves) > 0:
            for start, target, bc in moves:
                print((mv.move(start, target, 3), bc))
            # print([(mv.move(start,target,3),bc) for start,target,bc in moves])
            print("")
        else:
            print([])
