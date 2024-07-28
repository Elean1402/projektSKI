import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gamestate import *
from src.model import Player, BitMaskDict, DICT_MOVE, DictMoveEntry, BIT_MASK_ARRAY_KNIGHT_BLUE, \
    BIT_MASK_ARRAY_KNIGHT_RED, BIT_MASK_ARRAY_PAWN_BLUE, BIT_MASK_ARRAY_PAWN_RED, FilteredPositionsArray, \
    NotAccessiblePos, BoardCommand, BC_TO_BOARD_OPS_DICT, BITMASK_MIDGAME
from src.moveLib import MoveLib as mv
from collections import deque
from functools import lru_cache

class MoveGenerator:
    # _board = np.array([np.uint64(0),np.uint64(0),np.uint64(0),np.uint64(0)])
    # _boardIsInitialized = False
    _gameover = DictMoveEntry.CONTINUE_GAME
    # _WinnerIs = Player.NoOne
    _useTakeback = False
    _stack = []
    def __init__(self, board: list[np.uint64] = [np.uint64(0)], useTakeback: bool = False):
        """ Must use Gamestate._ZARR_... constants as indices
            for board.
            e.g. board[Gamestate._ZARR_INDEX_R_PAWNS] ...
        Args:
            board (list[np.uint64]): Bitboard Array of length 4
        """
        if(board[0] !=0):
            print("Board init:")
            self.prettyPrintBoard(board)
        if(useTakeback):
            self._useTakeback = useTakeback
            self._stack = deque([])

    def genMoves(self, player: Player, board: list[np.uint64],gameOver: list[DictMoveEntry]):
        """Generates all possible Moves
           ATTENTION IF LIST IS EMPTY GAME OVER: -> sets gameOver

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
        return self._genValidatedMoves(player, board, gameOver)

    def _startPosBelongsToPlayer(self,player: Player, pos: np.uint64, board: list[np.uint64]):
        """Double Check if startpos belongs to player

        Args:
            player (Player): use model.py
            pos (np.uint64): position of Figure

        Raises:
            TypeError: if player is not of Type Player

        Returns:
            boolean: true if correct otherwise false
        """
        posBelongsToPlayer = False
        if(player == Player.Blue):
            if(board[GameState._ZARR_INDEX_B_PAWNS] & pos & 
               ~(board[GameState._ZARR_INDEX_B_KNIGHTS] |
                 board[GameState._ZARR_INDEX_R_KNIGHTS]) 
               == pos 
               or
               board[GameState._ZARR_INDEX_B_KNIGHTS] & pos &
               ~(board[GameState._ZARR_INDEX_R_KNIGHTS])
               == pos):
                posBelongsToPlayer = True
        elif(player == Player.Red):
            if(board[GameState._ZARR_INDEX_R_PAWNS] & pos & 
               ~(board[GameState._ZARR_INDEX_B_KNIGHTS] |
                 board[GameState._ZARR_INDEX_R_KNIGHTS]) 
               == pos 
               or
               board[GameState._ZARR_INDEX_R_KNIGHTS] & pos &
               ~(board[GameState._ZARR_INDEX_B_KNIGHTS])
               == pos):
                posBelongsToPlayer = True
        else:
            raise TypeError("player is not from Type Player")
        return posBelongsToPlayer

    def _checkTargetPos(self, player:Player, move: tuple, board: list[np.uint64]):
        """Checks the move if possible and return a Command for the Bitboard operation
            Code needs to be restructured,
            too many if else statements and if possible shortened.
            
        Args:
            player (Player): use model.py - Class Player
            move (tuple): (uint64, uint64, uint64): (start, target, bitmask)

        Raises:
            TypeError: if type of move is wrong
            ValueError: if error in unvalidated movegeneration 

        Returns:
            list[Bordcommand]
        """
        
        if(len(move)!=3):
            print("len move", len(move))
            print("move",move)
            raise TypeError("move if from wrong Type. Should be (uint64,uint64,uint64): (start, target, bitmask)")
        
        start = move[0]
        target = move[1]
        bitmask = move[2]
        if(start == target):
            return [BoardCommand.Cannot_Move]
        if(target & NotAccessiblePos == target):
            raise ValueError("TargetPosition is on A1 or A8 or H1 or H8 (impossible), check how the moves are generated.")
        if(not self._startPosBelongsToPlayer(player, start,board)):
            raise ValueError("Startposition does not belong to player",player,", check also Bitboards")
        if(player == Player.Blue):
            # Figure on start is a Pawn
            if(start & board[GameState._ZARR_INDEX_B_PAWNS] & 
               ~(board[GameState._ZARR_INDEX_B_KNIGHTS] |
                 board[GameState._ZARR_INDEX_R_KNIGHTS]) 
               == start):
                #Case hit diagonal possible?
                if(bitmask == BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT] or
                   bitmask == BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT]):
                    #on target is an enemy knight
                    if(target & board[GameState._ZARR_INDEX_R_KNIGHTS] 
                       == target):
                        return [BoardCommand.Hit_Red_KnightOnTarget,BoardCommand.Delete_Blue_Pawn_from_StartPos]
                    #on target is only a enemy pawn        
                    elif(target & ( board[GameState._ZARR_INDEX_R_PAWNS] & 
                                    ~(board[GameState._ZARR_INDEX_R_KNIGHTS] |
                                    board[GameState._ZARR_INDEX_B_KNIGHTS]) )
                         == target):
                        return [BoardCommand.Hit_Red_PawnOnTarget,BoardCommand.Move_Blue_Pawn_no_Change,BoardCommand.Delete_Blue_Pawn_from_StartPos]
                    else:
                        return [BoardCommand.Cannot_Move]
                else:
                #standard move on free Target Position
                    if(target & ~(  board[GameState._ZARR_INDEX_B_PAWNS]   | 
                                    board[GameState._ZARR_INDEX_R_PAWNS]   | 
                                    board[GameState._ZARR_INDEX_B_KNIGHTS] |
                                    board[GameState._ZARR_INDEX_R_KNIGHTS]) 
                       == target):
                        return [BoardCommand.Move_Blue_Pawn_no_Change,BoardCommand.Delete_Blue_Pawn_from_StartPos]
                    #Target not free, only possible if our pawn is on target
                    elif(target & board[GameState._ZARR_INDEX_B_PAWNS] &
                                   ~(board[GameState._ZARR_INDEX_B_KNIGHTS] |
                                     board[GameState._ZARR_INDEX_R_KNIGHTS])
                        == target ):
                        return [BoardCommand.Upgrade_Blue_KnightOnTarget,BoardCommand.Delete_Blue_Pawn_from_StartPos]
                    #move on Target not possible
                    else:    
                        return [BoardCommand.Cannot_Move]
            #Figure is Knight
            elif(start &board[GameState._ZARR_INDEX_B_KNIGHTS] == start):
                #Case: target pos not occupied
                if(target & ~( board[GameState._ZARR_INDEX_B_PAWNS] |
                               board[GameState._ZARR_INDEX_R_PAWNS] |
                               board[GameState._ZARR_INDEX_B_KNIGHTS] |
                               board[GameState._ZARR_INDEX_R_KNIGHTS])
                   == target):
                    return [BoardCommand.Degrade_Blue_KnightOnTarget,BoardCommand.Delete_Blue_Knight_from_StartPos]
                #Case: only our pawn is on target
                elif(target & board[GameState._ZARR_INDEX_B_PAWNS] &
                     ~(board[GameState._ZARR_INDEX_B_KNIGHTS] |
                       board[GameState._ZARR_INDEX_R_KNIGHTS])
                     == target):
                    return [BoardCommand.Move_Blue_Knight_no_Change,BoardCommand.Delete_Blue_Knight_from_StartPos]
                #Case: only a enemy pawn is on target
                elif(target & board[GameState._ZARR_INDEX_R_PAWNS] &
                     ~(board[GameState._ZARR_INDEX_B_KNIGHTS] |
                       board[GameState._ZARR_INDEX_R_KNIGHTS])
                     == target):
                    return [BoardCommand.Hit_Red_PawnOnTarget,BoardCommand.Degrade_Blue_KnightOnTarget,BoardCommand.Delete_Blue_Knight_from_StartPos]
                    
                #Case: 2 figures are on target
                    #on target our knight
                elif(target & board[GameState._ZARR_INDEX_B_KNIGHTS]
                     == target):
                    return [BoardCommand.Cannot_Move]
                    #on target enemy knight
                elif(target & board[GameState._ZARR_INDEX_R_KNIGHTS] 
                     == target):
                    return [BoardCommand.Hit_Red_KnightOnTarget,BoardCommand.Move_Blue_Knight_no_Change,BoardCommand.Delete_Blue_Knight_from_StartPos]
        elif(player == Player.Red):
            # Figure on start is a Pawn
            if(start & board[GameState._ZARR_INDEX_R_PAWNS] & 
               ~(board[GameState._ZARR_INDEX_B_KNIGHTS] |
                 board[GameState._ZARR_INDEX_R_KNIGHTS]) 
               == start):
                #Case hit diagonal possible?
                if(bitmask == BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT] or
                   bitmask == BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT]):
                    #on target is an enemy knight
                    if(target & board[GameState._ZARR_INDEX_B_KNIGHTS] 
                       == target):
                        return [BoardCommand.Hit_Blue_KnightOnTarget, BoardCommand.Delete_Red_Pawn_from_StartPos]
                    #on target is only a enemy pawn        
                    elif(target & ( board[GameState._ZARR_INDEX_B_PAWNS] & 
                                    ~(board[GameState._ZARR_INDEX_R_KNIGHTS] |
                                    board[GameState._ZARR_INDEX_B_KNIGHTS]) )
                         == target):
                        return [BoardCommand.Hit_Blue_PawnOnTarget,BoardCommand.Move_Red_Pawn_no_Change,BoardCommand.Delete_Red_Pawn_from_StartPos]
                    else:
                        return [BoardCommand.Cannot_Move]
                else:
                #standard move on free Target Position
                    if(target & ~(  board[GameState._ZARR_INDEX_R_PAWNS]   | 
                                    board[GameState._ZARR_INDEX_B_PAWNS]   | 
                                    board[GameState._ZARR_INDEX_B_KNIGHTS] |
                                    board[GameState._ZARR_INDEX_R_KNIGHTS]) 
                       == target):
                        return [BoardCommand.Move_Red_Pawn_no_Change,BoardCommand.Delete_Red_Pawn_from_StartPos]
                    #Target not free, only possible if our pawn is on target
                    elif(target & board[GameState._ZARR_INDEX_R_PAWNS] &
                                   ~(board[GameState._ZARR_INDEX_B_KNIGHTS] |
                                     board[GameState._ZARR_INDEX_R_KNIGHTS])
                        == target ):
                        return [BoardCommand.Upgrade_Red_KnightOnTarget,BoardCommand.Delete_Red_Pawn_from_StartPos]
                    #move on Target not possible
                    else:    
                        return [BoardCommand.Cannot_Move]
            #Figure is Knight
            elif(start &board[GameState._ZARR_INDEX_R_KNIGHTS] == start):
                #Case: target pos not occupied
                if(target & ~( board[GameState._ZARR_INDEX_B_PAWNS] |
                               board[GameState._ZARR_INDEX_R_PAWNS] |
                               board[GameState._ZARR_INDEX_B_KNIGHTS] |
                               board[GameState._ZARR_INDEX_R_KNIGHTS])
                   == target):
                    return [BoardCommand.Degrade_Red_KnightOnTarget,BoardCommand.Delete_Red_Knight_from_StartPos]
                #Case: only our pawn is on target
                elif(target & board[GameState._ZARR_INDEX_R_PAWNS] &
                     ~(board[GameState._ZARR_INDEX_B_KNIGHTS] |
                       board[GameState._ZARR_INDEX_R_KNIGHTS])
                     == target):
                    return [BoardCommand.Move_Red_Knight_no_Change, BoardCommand.Delete_Red_Knight_from_StartPos]
                #Case: only a enemy pawn is on target
                elif(target & board[GameState._ZARR_INDEX_B_PAWNS] &
                     ~(board[GameState._ZARR_INDEX_B_KNIGHTS] |
                       board[GameState._ZARR_INDEX_R_KNIGHTS])
                     == target):
                    return [BoardCommand.Hit_Blue_PawnOnTarget,BoardCommand.Degrade_Red_KnightOnTarget,BoardCommand.Delete_Red_Knight_from_StartPos]
                    
                #Case: 2 figures are on target
                    #on target our knight
                elif(target & board[GameState._ZARR_INDEX_R_KNIGHTS]
                     == target):
                    return [BoardCommand.Cannot_Move]
                    #on target enemy knight
                elif(target & board[GameState._ZARR_INDEX_B_KNIGHTS] 
                     == target):
                    return [BoardCommand.Hit_Blue_KnightOnTarget,BoardCommand.Move_Red_Knight_no_Change,BoardCommand.Delete_Red_Knight_from_StartPos] 

    def _genValidatedMoves(self, player:Player,board: list[np.uint64],gameOver: list[DictMoveEntry])-> list[tuple[np.uint64,np.uint64,list[BoardCommand]]]: 
        """ Generates all unvalidated Moves of Player Blue or Red
            
        Args:
            player (Player): Please use model.py Player class

        Returns:
            List[Tuple[np.uint64, np.uint64, list]]: [(startpos,targetpos, boardcommands)]
        """
        pawnsPositions = self._getAllPawns(player,board)
        knightPositions = self._getAllKnights(player,board)
        filteredPositions = FilteredPositionsArray()
        validatedMoves = list()
        if(player == Player.Red):
            for bitmask in BIT_MASK_ARRAY_PAWN_RED:
                filteredPositions.append((bitmask,self._filterPositions(player,pawnsPositions, bitmask)))
            for bitmask in BIT_MASK_ARRAY_KNIGHT_RED:
                filteredPositions.append((bitmask, self._filterPositions(player, knightPositions, bitmask)))
            for (bm, filteredBits) in filteredPositions:
                for bit in self.getBitPositions(filteredBits):
                    boardCommands = self._checkTargetPos(player, (*self._getTarget(bit,bm),bm),board)
                    if(boardCommands != None):
                        if(BoardCommand.Cannot_Move in boardCommands):
                            continue
                    validatedMoves.append((*self._getTarget(bit,bm), boardCommands))
        elif(player == Player.Blue):
            for bitmask in BIT_MASK_ARRAY_PAWN_BLUE:
                filteredPositions.append((bitmask,self._filterPositions(player,pawnsPositions, bitmask)))
            for bitmask in BIT_MASK_ARRAY_KNIGHT_BLUE:
                filteredPositions.append((bitmask, self._filterPositions(player, knightPositions, bitmask)))
            for (bm, filteredBits) in filteredPositions:
                for bit in self.getBitPositions(filteredBits):
                    boardCommands = self._checkTargetPos(player, (*self._getTarget(bit,bm),bm),board)
                    if(boardCommands != None):
                        if(BoardCommand.Cannot_Move in boardCommands):
                            continue
                    validatedMoves.append((*self._getTarget(bit,bm), boardCommands))        
        else:
            raise TypeError("player is not from Type Player")
        
        if(len(validatedMoves) == 0):
            gameOver[0] = DictMoveEntry.GAME_OVER_BLUE_WINS if player == Player.Red else  DictMoveEntry.GAME_OVER_RED_WINS
            self._gameover = DictMoveEntry.GAME_OVER_BLUE_WINS if player == Player.Red else DictMoveEntry.GAME_OVER_RED_WINS
            #return validatedMoves
            
        
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

    def _getTarget(self, filteredPos: np.uint64, bitmask:np.uint64):
        """ Gets target field of concerned  bitmask
            ***Need to be optimized via dict which holds a function to make bit shifting***
        Arguments:
            filteredPos (np.uint64): SINGLE POSITION which can move onto direction described in Bitmask
            bitmask (Bitmask): The Bitmask in this function is used to determine the direction of the move
        Returns:
            (Tuple(np.uint64, np.uint64): (startPosition, targetposition)
            returns (0,0) if parameter filterPos= 0"""
        if(filteredPos == 0):
            return (np.uint64(0),np.uint64(0))
        
        targetPosition = np.uint64(0)
        if(bitmask == BitMaskDict[DictMoveEntry.PAWN_TO_LEFT]):
            targetPosition |= filteredPos << DICT_MOVE[DictMoveEntry.PAWN_TO_LEFT]
        elif(bitmask == BitMaskDict[DictMoveEntry.PAWN_TO_RIGHT]):
            targetPosition |= filteredPos >> DICT_MOVE[DictMoveEntry.PAWN_TO_RIGHT]
        
        elif(bitmask == BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM]):
            targetPosition |= filteredPos >> DICT_MOVE[DictMoveEntry.RED_PAWN_TO_BOTTOM]
        elif(bitmask == BitMaskDict[DictMoveEntry.RED_KNIGHT_LEFT]):
            targetPosition |= filteredPos >> DICT_MOVE[DictMoveEntry.RED_KNIGHT_LEFT]
        elif(bitmask == BitMaskDict[DictMoveEntry.RED_KNIGHT_RIGHT]):
            targetPosition |= filteredPos >> DICT_MOVE[DictMoveEntry.RED_KNIGHT_RIGHT]
        elif(bitmask == BitMaskDict[DictMoveEntry.RED_KNIGHT_TO_BOTLEFT]):
            targetPosition |= filteredPos >> DICT_MOVE[DictMoveEntry.RED_KNIGHT_TO_BOTLEFT]
        elif(bitmask == BitMaskDict[DictMoveEntry.RED_KNIGHT_TO_BOTRIGHT]):
            targetPosition |= filteredPos >> DICT_MOVE[DictMoveEntry.RED_KNIGHT_TO_BOTRIGHT]
        
        elif(bitmask == BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP]):
            targetPosition |= filteredPos << DICT_MOVE[DictMoveEntry.BLUE_PAWN_TO_TOP]
        elif(bitmask == BitMaskDict[DictMoveEntry.BLUE_KNIGHT_LEFT]):
            targetPosition |= filteredPos << DICT_MOVE[DictMoveEntry.BLUE_KNIGHT_LEFT]
        elif(bitmask == BitMaskDict[DictMoveEntry.BLUE_KNIGHT_RIGHT]):
            targetPosition |= filteredPos << DICT_MOVE[DictMoveEntry.BLUE_KNIGHT_RIGHT]
        elif(bitmask == BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT]):
            targetPosition |= filteredPos << DICT_MOVE[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT]
        elif(bitmask == BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT]):
            targetPosition |= filteredPos << DICT_MOVE[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT]
        
        elif(bitmask == BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT]):
            targetPosition |= filteredPos >> DICT_MOVE[DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT]
        elif(bitmask == BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT]):
            targetPosition |= filteredPos >> DICT_MOVE[DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT]
        
        elif(bitmask == BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT]):
            targetPosition |= filteredPos << DICT_MOVE[DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT]
        elif(bitmask == BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT]):
            targetPosition |= filteredPos << DICT_MOVE[DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT]
        else:
            raise ValueError("bitmask not recognized, please check Bitmask class or bitmask value")
        if(targetPosition == 0):
            raise ValueError("Something went wrong with bit shifting")
        return (filteredPos,targetPosition)

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

    def _filterPositions(self, player:Player, positions: np.uint64, bitmask: np.uint64):
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
        if(
            (player == Player.Red and (
            bitmask == BitMaskDict[DictMoveEntry.PAWN_TO_LEFT] or
            bitmask == BitMaskDict[DictMoveEntry.PAWN_TO_RIGHT] or
            bitmask == BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM] or
            bitmask == BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT] or
            bitmask == BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT] or
            bitmask == BitMaskDict[DictMoveEntry.RED_KNIGHT_LEFT] or
            bitmask == BitMaskDict[DictMoveEntry.RED_KNIGHT_RIGHT] or
            bitmask == BitMaskDict[DictMoveEntry.RED_KNIGHT_TO_BOTLEFT] or
            bitmask == BitMaskDict[DictMoveEntry.RED_KNIGHT_TO_BOTRIGHT]))
           or 
            (player == Player.Blue and (
            bitmask == BitMaskDict[DictMoveEntry.PAWN_TO_LEFT] or
            bitmask == BitMaskDict[DictMoveEntry.PAWN_TO_RIGHT] or
            bitmask == BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP] or
            bitmask == BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT] or
            bitmask == BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT] or
            bitmask == BitMaskDict[DictMoveEntry.BLUE_KNIGHT_LEFT] or
            bitmask == BitMaskDict[DictMoveEntry.BLUE_KNIGHT_RIGHT] or
            bitmask == BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT] or
            bitmask == BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT]))):
            #only positions which can move in direction of description of bitmask
            positions = positions & (bitmask)
        else:
            raise ValueError("Bitmask and choosed Player are wrong")
        return positions

    @classmethod
    def checkBoardIfGameOver(self, gameOver: list[DictMoveEntry], board: list[np.uint64], printBoard=False):
        """Game is over if last Row is reached or no possible Moves
        sets gameOver at given list and sets gameOver at class attribute"""
        if printBoard:
            self.prettyPrintBoard(self, board, gameOver)

        blue_pieces = board[GameState._ZARR_INDEX_B_KNIGHTS] | board[GameState._ZARR_INDEX_B_PAWNS]
        red_pieces = board[GameState._ZARR_INDEX_R_KNIGHTS] | board[GameState._ZARR_INDEX_R_PAWNS]

        if (blue_pieces & BitMaskDict[DictMoveEntry.GAME_OVER_BLUE_WINS]) != 0 or red_pieces == 0:
            gameOver[0] = DictMoveEntry.GAME_OVER_BLUE_WINS
            self._gameover = DictMoveEntry.GAME_OVER_BLUE_WINS
        elif (red_pieces & BitMaskDict[DictMoveEntry.GAME_OVER_RED_WINS]) != 0 or blue_pieces == 0:
            gameOver[0] = DictMoveEntry.GAME_OVER_RED_WINS
            self._gameover = DictMoveEntry.GAME_OVER_RED_WINS
                
        if gameOver[0] != DictMoveEntry.CONTINUE_GAME or self._gameover != DictMoveEntry.CONTINUE_GAME:
            if printBoard:
                print("Game Over")
                self.prettyPrintBoard(self, board, gameOver)

    def execSingleMove(self, move: tuple, player: Player, board: list[np.uint64],gameOver: list[DictMoveEntry],printB: bool = False):
        """Executes single Move and updates the Board and checks if Game Over

        Args:
            move (tuple): (startpos: uint64, targetpos: uint64, list[BoardCommands])
            player (Player): Red or Blue
            gameOver (list[DictMoveEntry]):
            board (list[np.uint64]): _description_
            printB (bool, optional): _description_. Defaults to False.
            usetakeback (bool): if true, no copy of board is made. 

        Returns:
             (Array[uint64]): Board
        """
        boardCopy = np.uint64(0)
        if(not self._useTakeback):
            boardCopy = board.copy()
        else:
            boardCopy = board
        # TODO check if Board is initialized
        # if(not boardIsInitialized):
        #     raise ValueError("Board is not initialized!")
        # Can this happen?
        if len(move) == 0:
            print("move is empty, Game Over")
            gameOver[0] = DictMoveEntry.GAME_OVER_BLUE_WINS if player == Player.Blue else DictMoveEntry.GAME_OVER_RED_WINS
            self._gameover = DictMoveEntry.GAME_OVER_BLUE_WINS if player == Player.Blue else DictMoveEntry.GAME_OVER_RED_WINS
            return boardCopy
        startpos = move[0]
        targetpos = move[1]
        boardCommands = move[2]
        [self._Board_Exec_Move(boardCopy,BC_TO_BOARD_OPS_DICT[bc],startpos,targetpos) for bc in boardCommands]
        # TODO exec Move
        # for bc in boardCommands:
        #     bc = BoardCommand(bc)
        #     if bc == BoardCommand.Hit_Red_PawnOnTarget:
        #         boardCopy[GameState._ZARR_INDEX_R_PAWNS] &= ~targetpos
        #     elif bc == BoardCommand.Hit_Blue_PawnOnTarget:
        #         boardCopy[GameState._ZARR_INDEX_B_PAWNS] &= ~targetpos
        #     elif bc == BoardCommand.Hit_Red_KnightOnTarget:
        #         boardCopy[GameState._ZARR_INDEX_R_KNIGHTS] &= ~targetpos
        #     elif bc == BoardCommand.Hit_Blue_KnightOnTarget:
        #         boardCopy[GameState._ZARR_INDEX_B_KNIGHTS] &= ~targetpos
           
        #     elif bc == BoardCommand.Upgrade_Blue_KnightOnTarget:
        #         boardCopy[GameState._ZARR_INDEX_B_KNIGHTS] |= targetpos
        #     elif bc == BoardCommand.Upgrade_Red_KnightOnTarget:
        #         boardCopy[GameState._ZARR_INDEX_R_KNIGHTS] |= targetpos
           
        #     elif bc == BoardCommand.Degrade_Blue_KnightOnTarget:
        #         boardCopy[GameState._ZARR_INDEX_B_PAWNS] |= targetpos
        #     elif bc == BoardCommand.Degrade_Red_KnightOnTarget:
        #         boardCopy[GameState._ZARR_INDEX_R_PAWNS] |= targetpos
            
        #     elif bc == BoardCommand.Move_Blue_Knight_no_Change:
        #         boardCopy[GameState._ZARR_INDEX_B_KNIGHTS] |= targetpos
        #     elif bc == BoardCommand.Move_Red_Knight_no_Change:
        #         boardCopy[GameState._ZARR_INDEX_R_KNIGHTS] |= targetpos
        #     elif bc == BoardCommand.Move_Blue_Pawn_no_Change:
        #         boardCopy[GameState._ZARR_INDEX_B_PAWNS] |= targetpos
        #     elif bc == BoardCommand.Move_Red_Pawn_no_Change:
        #         boardCopy[GameState._ZARR_INDEX_R_PAWNS] |= targetpos
           
        #     elif bc == BoardCommand.Delete_Red_Pawn_from_StartPos:
        #         boardCopy[GameState._ZARR_INDEX_R_PAWNS] &= ~startpos
        #     elif bc == BoardCommand.Delete_Blue_Pawn_from_StartPos:
        #         boardCopy[GameState._ZARR_INDEX_B_PAWNS] &= ~startpos
        #     elif bc == BoardCommand.Delete_Red_Knight_from_StartPos:
        #         boardCopy[GameState._ZARR_INDEX_R_KNIGHTS] &= ~startpos
        #     elif bc == BoardCommand.Delete_Blue_Knight_from_StartPos:
        #         boardCopy[GameState._ZARR_INDEX_B_KNIGHTS] &= ~startpos
            

        self.checkBoardIfGameOver(gameOver, boardCopy, printB)
        if(self._useTakeback):
            self._stack.append((move[0],move[1],move[2]))
        if printB == True:
            print("move executed, new Board ist:\n")
            self.prettyPrintBoard(boardCopy, gameOver) if not self._useTakeback else self.prettyPrintBoard(boardCopy, self._gameover)
        return boardCopy

    def takeback(self, board:list[np.uint64]):
        if(self._useTakeback and len(self._stack) > 0):
            self._gameover = DictMoveEntry.CONTINUE_GAME
            move = self._stack.pop()
            
            bcommands = move[2]
            
            [self._Board_Exec_Move(board, BC_TO_BOARD_OPS_DICT[command], move[0], move[1], True) for command in bcommands]
        else:
            raise Exception("useTakeback is False or stack is empty")
    
    def _Board_Exec_Move(self,bitboard: list[np.uint64], infoList:dict[BoardCommand,list], startPos: np.uint64, targetPos: np.uint64, unmake:bool = False)-> None:
        """Example:
            unmake = False: Delete = True -> use &= ~ operators, Delete = False -> use |= operators
            unmake = True: Delete = True -> use |= operators, Delete = False -> use &= ~ operators

        Args:
            bitboard (list[np.uint64]): _description_
            infoList (tuple[list,bool,bool]): (bitboard_indices, Delete, onTargetPosition), 
            startPos (np.uint64): Position
            targetPos (np.uint64): Position
            unmake (bool): If True, then unmake move otherwise exec move
        """
        #TODO
        boardIndices = infoList[0]
        delete = infoList[1]
        onTargetPosition = infoList[2]
        if(unmake):
            
            if(delete):
                #undo deleted Figure on targetPos 
                if(onTargetPosition):
                    bitboard[boardIndices[0]] |= targetPos
                #Firstpos = startpos: undo deleted Figure on startpos
                else:
                    bitboard[boardIndices[0]] |= startPos
            #delete = False
            else:
                if(onTargetPosition):
                    bitboard[boardIndices[0]] &= ~ targetPos
                else:
                    bitboard[boardIndices[0]] &= ~ startPos
                
        else:
            if(delete):
                #exec bc
                if(onTargetPosition):
                    bitboard[boardIndices[0]] &= ~ targetPos
                #Firstpos = startpos: delete Figure on startpos
                else:
                    bitboard[boardIndices[0]] &= ~ startPos
            #use first |= then &= ~: add Figure to targetPos and remove it from startPos
            else:
                if(onTargetPosition):
                    bitboard[boardIndices[0]] |=  targetPos
                else:
                    bitboard[boardIndices[1]] |=  startPos
    
    @staticmethod
    def isOpening(board:list[np.uint64]) -> bool:
        return ((board[0] & BITMASK_MIDGAME == 0) or 
                (board[1] & BITMASK_MIDGAME == 0) or
                (board[2] & BITMASK_MIDGAME == 0) or
                (board[3] & BITMASK_MIDGAME == 0))
            
    def prettyPrintBoard(self, board: list[np.uint64], *gameOver: list[DictMoveEntry]):
        # print("internal board", board)
        print("current Board\n", GameState.fromBitBoardToMatrix(board, True))
        if len(gameOver) != 0:
            print("Game status:", gameOver[0])  # raise ValueError("stop")
        print("1 = red, 4 = blue, 2 = rr, 3 = br, 5= rb, 8= bb")
    
    def prettyPrintBoard2(self, board: list[np.uint64], *gameOver: list[DictMoveEntry]):
        # print("internal board", board)
        return f"{GameState.fromBitBoardToMatrix(board, True)}\n" + f"{gameOver[0] if gameOver else []}\n" f"1 = red, 4 = blue, 2 = rr, 3 = br, 5= rb, 8= bb"

    def prettyPrintMoves(self, moves: list):
        print("\nMoves generated from MoveGenerator:")
        if len(moves) > 0:
            if(len(moves[0]) == 3):
                for start, target, bc in moves:
                    print((mv.move(start, target, 3), bc))
                print("")
            elif(len(moves[0]) == 2):
                for start, target in moves:
                    print((mv.move(start, target, 3)))
                print("")
        else:
            print([])
    
    def prettyPrintMove(self, move: tuple)-> str:
        return f"{mv.move(move[0],move[1],3)}"
