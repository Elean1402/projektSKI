import numpy as np
from src.gamestate import*
from src.model import Player,BitMask, DICT_MOVE, DictMoveEntry,BIT_MASK_ARRAY_KNIGHT_BLUE,BIT_MASK_ARRAY_KNIGHT_RED,BIT_MASK_ARRAY_PAWN_BLUE,BIT_MASK_ARRAY_PAWN_RED,FilteredPositionsArray
from src.moveLib import MoveLib as mv

class MoveGenerator:
    _board = np.array([np.uint64(0),np.uint64(0),np.uint64(0),np.uint64(0)])
    
    
    
    def __init__(self, board: list[np.uint64]):
        """ Must use Gamestate._ZARR_... constants as indices
            for board.
            e.g. board[Gamestate._ZARR_INDEX_R_PAWNS] ...
        Args:
            board (list[np.uint64]): Bitboard Array of length 4
        """
        #print("initialized board", board)
        self._board = board
        
    
    def updateBoard(self,board:list[np.uint64]):
        self._board = board
        
    
    def genMoves(self,player:Player):
        
        #check if game is over
        #TODO
        unvalidatedMoves = self._genUnvalidatedMoves(player)
        #TODO: Validate moves and filter them
        
            
    def _genUnvalidatedMoves(self, player:Player): 
        pawnsPositions = self._getAllPawns(player)
        knightPositions = self._getAllKnights(player)
        filteredPositions = FilteredPositionsArray()
        unvalidatedMoves = list()
        if(player == Player.Red):
            for bitmask in BIT_MASK_ARRAY_PAWN_RED:
                filteredPositions.append((bitmask,self._filterPositions(player,pawnsPositions, bitmask)))
            for bitmask in BIT_MASK_ARRAY_KNIGHT_RED:
                filteredPositions.append((bitmask, self._filterPositions(player, knightPositions, bitmask)))
            for (bm, filteredBits) in filteredPositions:
                for bit in self._getBitPositions(filteredBits):
                    unvalidatedMoves.append(self._getTarget(bit,bm))
                
        return unvalidatedMoves
    
    def _getBitPositions(n: np.uint64):
        """ Returns Generator over the Bits of n
        THIS FUNC IS FROM SOURCE:
        https://stackoverflow.com/questions/8898807/pythonic-way-to-iterate-over-bits-of-integer
        
        """
        while(n):
            b = n & (~n+np.uint64(1))
            yield b
            n^=b
    
    def _getTarget(self, filteredPos: np.uint64, bitmask:BitMask):
        """ Gets target field of concerned  bitmask
            ***Need to be optimized via dict which holds a function to make bit shifting***
        Arguments:
            filteredPos (np.uint64): SINGLE POSITION which can move onto direction described in Bitmask
            bitmask (Bitmask): The Bitmask in this function is used to determine the direction of the move
        Returns:
            (Tuple(np.uint64, np.uint64): (startPosition, targetposition)"""

        targetPosition = np.uint64(0)
        if(bitmask == BitMask.PAWN_TO_LEFT):
            targetPosition |= filteredPos << DICT_MOVE[DictMoveEntry.PAWN_TO_LEFT]
        elif(bitmask == BitMask.PAWN_TO_RIGHT):
            targetPosition |= filteredPos >> DICT_MOVE[DictMoveEntry.PAWN_TO_RIGHT]
        
        elif(bitmask == BitMask.RED_PAWN_TO_BOTTOM):
            targetPosition |= filteredPos >> DICT_MOVE[DictMoveEntry.RED_PAWN_TO_BOTTOM]
        elif(bitmask == BitMask.RED_KNIGHT_LEFT):
            targetPosition |= filteredPos >> DICT_MOVE[DictMoveEntry.RED_KNIGHT_LEFT]
        elif(bitmask == BitMask.RED_KNIGHT_RIGHT):
            targetPosition |= filteredPos >> DICT_MOVE[DictMoveEntry.RED_KNIGHT_RIGHT]
        elif(bitmask == BitMask.RED_KNIGHT_TO_BOTLEFT):
            targetPosition |= filteredPos >> DICT_MOVE[DictMoveEntry.RED_KNIGHT_TO_BOTLEFT]
        elif(bitmask == BitMask.RED_KNIGHT_TO_BOTRIGHT):
            targetPosition |= filteredPos >> DICT_MOVE[DictMoveEntry.RED_KNIGHT_TO_BOTRIGHT]
        
        elif(bitmask == BitMask.BLUE_PAWN_TO_TOP):
            targetPosition |= filteredPos << DICT_MOVE[DictMoveEntry.BLUE_PAWN_TO_TOP]
        elif(bitmask == BitMask.BLUE_KNIGHT_LEFT):
            targetPosition |= filteredPos << DICT_MOVE[DictMoveEntry.BLUE_KNIGHT_LEFT]
        elif(bitmask == BitMask.BLUE_KNIGHT_RIGHT):
            targetPosition |= filteredPos << DICT_MOVE[DictMoveEntry.BLUE_KNIGHT_RIGHT]
        elif(bitmask == BitMask.BLUE_KNIGHT_TO_TOPLEFT):
            targetPosition |= filteredPos << DICT_MOVE[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT]
        elif(bitmask == BitMask.BLUE_KNIGHT_TO_TOPRIGHT):
            targetPosition |= filteredPos << DICT_MOVE[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT]
        
        elif(bitmask == BitMask.RED_PAWN_TO_BOTTOM_LEFT):
            targetPosition |= filteredPos >> DICT_MOVE[DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT]
        elif(bitmask == BitMask.RED_PAWN_TO_BOTTOM_RIGHT):
            targetPosition |= filteredPos >> DICT_MOVE[DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT]
        
        elif(bitmask == BitMask.BLUE_PAWN_TO_TOP_LEFT):
            targetPosition |= filteredPos << DICT_MOVE[DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT]
        elif(bitmask == BitMask.BLUE_PAWN_TO_TOP_RIGHT):
            targetPosition |= filteredPos << DICT_MOVE[DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT]
        else:
            raise ValueError("bitmask not recognized, please check Bitmask class or bitmask value")
        if(targetPosition == 0):
            raise ValueError("Something went wrong with bit shifting")
        return (filteredPos,targetPosition)
    
    
    def _getAllPawns(self, player:Player):
        """Gets all Pawns of player Blue or Red which can Move
        Arguments: player (Player): see model.py
        Returns: pos (np.uint64): All pawn positions of player"""
        pos = np.uint64(0)
        if(player == Player.Red):
            pos |= (self._board[GameState._ZARR_INDEX_R_PAWNS] & (~self._board[GameState._ZARR_INDEX_R_KNIGHTS]) & (~ self._board[GameState._ZARR_INDEX_B_KNIGHTS]))
        elif(player == Player.Blue):
            pos |= (self._board[GameState._ZARR_INDEX_B_PAWNS] & (~self._board[GameState._ZARR_INDEX_R_KNIGHTS]) & (~ self._board[GameState._ZARR_INDEX_B_KNIGHTS]))
        else:
            raise ValueError("Choosed Player invalid, please use Player Class from model.py")
        return pos
    
    def _getAllKnights(self, player:Player):
        if(player == Player.Red):
            return self._board[GameState._ZARR_INDEX_R_KNIGHTS]
        elif(player == Player.Blue):
            return self._board[GameState._ZARR_INDEX_B_KNIGHTS]
        else:
            raise TypeError("parameter player is not from class Player, please use model.py: e.g. Player.Blue..")
        
    def _filterPositions(self, player:Player, positions: np.uint64, bitmask: BitMask):
        """ Assuming Red starts at top
            ***optimize case pattern with Dict lookup later***
            Filters the positions of figures in the direction of description of Bitmask

        Args:
            player (Player): enum - see model.py
            positions (np.uint64): single Bitboard
            bitmask (BitMask): Filtermask for processing possible Moves

        Returns:
            positions (np.uint64): All possible Positions which can move in direction descriped in Bitmask 
        """
        if(
            (player == Player.Red and (
            bitmask == BitMask.PAWN_TO_LEFT or
            bitmask == BitMask.PAWN_TO_RIGHT or
            bitmask == BitMask.RED_PAWN_TO_BOTTOM or
            bitmask == BitMask.RED_KNIGHT_LEFT or
            bitmask == BitMask.RED_KNIGHT_RIGHT or
            bitmask == BitMask.RED_KNIGHT_TO_BOTLEFT or
            bitmask == BitMask.RED_KNIGHT_TO_BOTRIGHT))
           or 
            (player == Player.Blue and (
            bitmask == BitMask.PAWN_TO_LEFT or
            bitmask == BitMask.PAWN_TO_RIGHT or
            bitmask == BitMask.BLUE_PAWN_TO_TOP or
            bitmask == BitMask.BLUE_KNIGHT_LEFT or
            bitmask == BitMask.BLUE_KNIGHT_RIGHT or
            bitmask == BitMask.BLUE_KNIGHT_TO_TOPLEFT or
            bitmask == BitMask.BLUE_KNIGHT_TO_TOPRIGHT))):
            #only positions which can move in direction of description of bitmask
            positions = positions & (~ bitmask)
        else:
            raise ValueError("Bitmask and choosed Player are wrong")
        return positions
        
    def _validateMoves(list):
        """ Filter the List
            Only possible Moves should be in the list """
            #TODO
        return list
    
    def _gameover(self):
        """Game is over if last Row is reached or
           no possible Moves
        Returns: Boolean: True for win else loose"""
        #todo
        
        return False
    
    
    def execSingleMove(self,move):
        #TODO check if Board is initialized
        #TODO exec Move
        #TODO update Board
        
        return self._board.copy()
    
    
    def prettyPrintBoard(self):
        #print("internal board", self._board)
        print("current Board\n",GameState.fromBitBoardToMatrix(self._board,True))
        print("1 = red, 4 = blue, 2 = rr, 3 = br, 5= rb, 8= bb")
    
    def prettyPrintMoves(self, moves: list[tuple[np.uint64,np.uint64]]):
        if(len(moves)>0):
            print( mv.move(start,target) for (start,target) in moves )
        else:
            raise ValueError("Something went wrong with parameter moves")