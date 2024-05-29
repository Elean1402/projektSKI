import numpy as np
from src.gamestate import*
from src.model import Player,BitMaskDict, DICT_MOVE, DictMoveEntry,BIT_MASK_ARRAY_KNIGHT_BLUE,BIT_MASK_ARRAY_KNIGHT_RED,BIT_MASK_ARRAY_PAWN_BLUE,BIT_MASK_ARRAY_PAWN_RED,FilteredPositionsArray,NotAccessiblePos, UnvalidateMovesArray, BoardCommand
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
        """Generates all possible Moves
        

        Args:
            player (Player): use model.py
        Returns:
            list[Tuple[start,target,list[Boardcommands]]]
            if no possible Move empty list and this should lead into Gameover
        """
        #check if game is over
        #TODO
        return self._genValidatedMoves(player)
        
            
        
    
    def _startPosBelongsToPlayer(self,player: Player, pos: np.uint64):
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
            if(self._board[GameState._ZARR_INDEX_B_PAWNS] & pos & 
               ~(self._board[GameState._ZARR_INDEX_B_KNIGHTS] |
                 self._board[GameState._ZARR_INDEX_R_KNIGHTS]) 
               == pos 
               or
               self._board[GameState._ZARR_INDEX_B_KNIGHTS] & pos &
               ~(self._board[GameState._ZARR_INDEX_R_KNIGHTS])
               == pos):
                posBelongsToPlayer = True
        elif(player == Player.Red):
            if(self._board[GameState._ZARR_INDEX_R_PAWNS] & pos & 
               ~(self._board[GameState._ZARR_INDEX_B_KNIGHTS] |
                 self._board[GameState._ZARR_INDEX_R_KNIGHTS]) 
               == pos 
               or
               self._board[GameState._ZARR_INDEX_R_KNIGHTS] & pos &
               ~(self._board[GameState._ZARR_INDEX_B_KNIGHTS])
               == pos):
                posBelongsToPlayer = True
        else:
            raise TypeError("player is not from Type Player")
        return posBelongsToPlayer

    def _checkTargetPos(self, player:Player, move: tuple):
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
        if(not self._startPosBelongsToPlayer(player, start)):
            raise ValueError("Startposition does not belong to player",player,", check also Bitboards")
        if(player == Player.Blue):
            # Figure on start is a Pawn
            if(start & self._board[GameState._ZARR_INDEX_B_PAWNS] & 
               ~(self._board[GameState._ZARR_INDEX_B_KNIGHTS] |
                 self._board[GameState._ZARR_INDEX_R_KNIGHTS]) 
               == start):
                #Case hit diagonal possible?
                if(bitmask == BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT] or
                   bitmask == BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT]):
                    #on target is an enemy knight
                    if(target & self._board[GameState._ZARR_INDEX_R_KNIGHTS] 
                       == target):
                        return [BoardCommand.Hit_Red_KnightOnTarget,BoardCommand.Move_Blue_Knight_no_Change]
                    #on target is only a enemy pawn        
                    elif(target & ( self._board[GameState._ZARR_INDEX_R_PAWNS] & 
                                    ~(self._board[GameState._ZARR_INDEX_R_KNIGHTS] |
                                    self._board[GameState._ZARR_INDEX_B_KNIGHTS]) )
                         == target):
                        return [BoardCommand.Hit_Red_PawnOnTarget,BoardCommand.Move_Blue_Pawn_no_Change]
                    else:
                        return [BoardCommand.Cannot_Move]
                else:
                #standard move on free Target Position
                    if(target & ~(  self._board[GameState._ZARR_INDEX_B_PAWNS]   | 
                                    self._board[GameState._ZARR_INDEX_R_PAWNS]   | 
                                    self._board[GameState._ZARR_INDEX_B_KNIGHTS] |
                                    self._board[GameState._ZARR_INDEX_R_KNIGHTS]) 
                       == target):
                        return [BoardCommand.Move_Blue_Pawn_no_Change]
                    #Target not free, only possible if our pawn is on target
                    elif(target & self._board[GameState._ZARR_INDEX_B_PAWNS] &
                                   ~(self._board[GameState._ZARR_INDEX_B_KNIGHTS] |
                                     self._board[GameState._ZARR_INDEX_R_KNIGHTS])
                        == target ):
                        return [BoardCommand.Upgrade_Blue_KnightOnTarget]
                    #move on Target not possible
                    else:    
                        return [BoardCommand.Cannot_Move]
            #Figure is Knight
            elif(start &self._board[GameState._ZARR_INDEX_B_KNIGHTS] == start):
                #Case: target pos not occupied
                if(target & ~( self._board[GameState._ZARR_INDEX_B_PAWNS] |
                               self._board[GameState._ZARR_INDEX_R_PAWNS] |
                               self._board[GameState._ZARR_INDEX_B_KNIGHTS] |
                               self._board[GameState._ZARR_INDEX_R_KNIGHTS])
                   == target):
                    return [BoardCommand.Degrade_Blue_KnightOnTarget]
                #Case: only our pawn is on target
                elif(target & self._board[GameState._ZARR_INDEX_B_PAWNS] &
                     ~(self._board[GameState._ZARR_INDEX_B_KNIGHTS] |
                       self._board[GameState._ZARR_INDEX_R_KNIGHTS])
                     == target):
                    return [BoardCommand.Move_Blue_Knight_no_Change]
                #Case: only a enemy pawn is on target
                elif(target & self._board[GameState._ZARR_INDEX_R_PAWNS] &
                     ~(self._board[GameState._ZARR_INDEX_B_KNIGHTS] |
                       self._board[GameState._ZARR_INDEX_R_KNIGHTS])
                     == target):
                    return [BoardCommand.Hit_Red_PawnOnTarget,BoardCommand.Degrade_Blue_KnightOnTarget]
                    
                #Case: 2 figures are on target
                    #on target our knight
                elif(target & self._board[GameState._ZARR_INDEX_B_KNIGHTS]
                     == target):
                    return [BoardCommand.Cannot_Move]
                    #on target enemy knight
                elif(target & self._board[GameState._ZARR_INDEX_R_KNIGHTS] 
                     == target):
                    return [BoardCommand.Hit_Red_KnightOnTarget,BoardCommand.Move_Blue_Knight_no_Change]
        elif(player == Player.Red):
            # Figure on start is a Pawn
            if(start & self._board[GameState._ZARR_INDEX_R_PAWNS] & 
               ~(self._board[GameState._ZARR_INDEX_B_KNIGHTS] |
                 self._board[GameState._ZARR_INDEX_R_KNIGHTS]) 
               == start):
                #Case hit diagonal possible?
                if(bitmask == BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT] or
                   bitmask == BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT]):
                    #on target is an enemy knight
                    if(target & self._board[GameState._ZARR_INDEX_B_KNIGHTS] 
                       == target):
                        return [BoardCommand.Hit_Blue_KnightOnTarget,BoardCommand.Move_Red_Knight_no_Change]
                    #on target is only a enemy pawn        
                    elif(target & ( self._board[GameState._ZARR_INDEX_B_PAWNS] & 
                                    ~(self._board[GameState._ZARR_INDEX_R_KNIGHTS] |
                                    self._board[GameState._ZARR_INDEX_B_KNIGHTS]) )
                         == target):
                        return [BoardCommand.Hit_Blue_PawnOnTarget,BoardCommand.Move_Red_Pawn_no_Change]
                    else:
                        return [BoardCommand.Cannot_Move]
                else:
                #standard move on free Target Position
                    if(target & ~(  self._board[GameState._ZARR_INDEX_R_PAWNS]   | 
                                    self._board[GameState._ZARR_INDEX_B_PAWNS]   | 
                                    self._board[GameState._ZARR_INDEX_B_KNIGHTS] |
                                    self._board[GameState._ZARR_INDEX_R_KNIGHTS]) 
                       == target):
                        return [BoardCommand.Move_Red_Pawn_no_Change]
                    #Target not free, only possible if our pawn is on target
                    elif(target & self._board[GameState._ZARR_INDEX_R_PAWNS] &
                                   ~(self._board[GameState._ZARR_INDEX_B_KNIGHTS] |
                                     self._board[GameState._ZARR_INDEX_R_KNIGHTS])
                        == target ):
                        return [BoardCommand.Upgrade_Red_KnightOnTarget]
                    #move on Target not possible
                    else:    
                        return [BoardCommand.Cannot_Move]
            #Figure is Knight
            elif(start &self._board[GameState._ZARR_INDEX_R_KNIGHTS] == start):
                #Case: target pos not occupied
                if(target & ~( self._board[GameState._ZARR_INDEX_B_PAWNS] |
                               self._board[GameState._ZARR_INDEX_R_PAWNS] |
                               self._board[GameState._ZARR_INDEX_B_KNIGHTS] |
                               self._board[GameState._ZARR_INDEX_R_KNIGHTS])
                   == target):
                    return [BoardCommand.Degrade_Red_KnightOnTarget]
                #Case: only our pawn is on target
                elif(target & self._board[GameState._ZARR_INDEX_R_PAWNS] &
                     ~(self._board[GameState._ZARR_INDEX_B_KNIGHTS] |
                       self._board[GameState._ZARR_INDEX_R_KNIGHTS])
                     == target):
                    return [BoardCommand.Move_Red_Knight_no_Change]
                #Case: only a enemy pawn is on target
                elif(target & self._board[GameState._ZARR_INDEX_B_PAWNS] &
                     ~(self._board[GameState._ZARR_INDEX_B_KNIGHTS] |
                       self._board[GameState._ZARR_INDEX_R_KNIGHTS])
                     == target):
                    return [BoardCommand.Hit_Blue_PawnOnTarget,BoardCommand.Degrade_Red_KnightOnTarget]
                    
                #Case: 2 figures are on target
                    #on target our knight
                elif(target & self._board[GameState._ZARR_INDEX_R_KNIGHTS]
                     == target):
                    return [BoardCommand.Cannot_Move]
                    #on target enemy knight
                elif(target & self._board[GameState._ZARR_INDEX_B_KNIGHTS] 
                     == target):
                    return [BoardCommand.Hit_Blue_KnightOnTarget,BoardCommand.Move_Red_Knight_no_Change]                
    
    def _genValidatedMoves(self, player:Player): 
        """Generates all unvalidated Moves of Player Blue or Red

        Args:
            player (Player): Please use model.py Player class

        Returns:
            List[Tuple[np.uint64, np.uint64, list]]: [(startpos,targetpos, boardcommands)]
        """
        pawnsPositions = self._getAllPawns(player)
        knightPositions = self._getAllKnights(player)
        filteredPositions = FilteredPositionsArray()
        validatedMoves = list()
        if(player == Player.Red):
            for bitmask in BIT_MASK_ARRAY_PAWN_RED:
                filteredPositions.append((bitmask,self._filterPositions(player,pawnsPositions, bitmask)))
            for bitmask in BIT_MASK_ARRAY_KNIGHT_RED:
                filteredPositions.append((bitmask, self._filterPositions(player, knightPositions, bitmask)))
            for (bm, filteredBits) in filteredPositions:
                for bit in self._getBitPositions(filteredBits):
                    boardCommands = self._checkTargetPos(player, (*self._getTarget(bit,bm),bm))
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
                for bit in self._getBitPositions(filteredBits):
                    boardCommands = self._checkTargetPos(player, (*self._getTarget(bit,bm),bm))
                    if(boardCommands != None):
                        if(BoardCommand.Cannot_Move in boardCommands):
                            continue
                    validatedMoves.append((*self._getTarget(bit,bm), boardCommands))        
        else:
            raise TypeError("player is not from Type Player")
        return validatedMoves
    
    def _getBitPositions(self,n: np.uint64):
        """ Returns Generator over the Bits of n
        THIS FUNC IS FROM SOURCE:
        https://stackoverflow.com/questions/8898807/pythonic-way-to-iterate-over-bits-of-integer
        
        """
        while(n):
            b = n & (~n+np.uint64(1))
            yield b
            n^=b
    
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
    
    def prettyPrintMoves(self,moves: list):
        if(len(moves)>0):
            print([(mv.move(start,target,3),bc) for start,target,bc in moves])
            #print(moves)
        else:
            print([])