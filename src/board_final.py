import numpy as np
from gamestate import GameState
from gui import Gui
import random

"""
Notes:
    Only static methods -> don't create instances e.g. just call Board.func()
    To use:
        initBoard(*Bitboards, blue_turn) -> None   # new game
        generate_moves() -> [(source1, [dest1, dest2, ...]), ...] # generates all possible moves of the current player
        exec_move(source, dest) -> (blue_pawns, blue_knights, red_pawns, red_knights) # executes move of the current player
        takeback -> takeback last move
        isOver  -> checks if the game is over
        --> check isOver after initBoard and after exec_move

        isOpening() -> bool # true if the current game is in the opening phase

    In process (don't use yet):
        eval() -> int # evaluation of the current board
        
    """



class Board():
    @staticmethod
    def initBoard(red_pawns, red_knights,blue_pawns, blue_knights, blue_turn=True) -> None:
        """
        Sets up new game:
        Call like this: 
            Board.initBoard(*GameState.createBitBoardFrom(Gui.fenToMatrix(FEN_board),True),blue_turn:bool)

        Imports needed for that:
            from src.gamestate import GameState
            from src.gui import Gui
        """
        Board.blue_turn = blue_turn
        Board.blue_p = blue_pawns
        Board.blue_k = blue_knights
        Board.blue = blue_pawns | blue_knights
        Board.red_p = red_pawns
        Board.red_k = red_knights
        Board.red = red_pawns | red_knights
        Board.l_blue_p=[]
        Board.l_blue_k=[]
        Board.l_red_p=[]
        Board.l_red_k=[]
        for bit_board, figure_list in zip((Board.blue_p, Board.blue_k, Board.red_p, Board.red_k),(Board.l_blue_p,Board.l_blue_k,Board.l_red_p,Board.l_red_k)):
            for bit in range(64):
                if bit_board & (np.uint64(1 << bit)):
                    figure_list.append(np.uint64(1 << bit))

    @staticmethod
    def generate_moves() -> list:
        """
        Format of the returned list:
        [(source1, [dest1, dest2, ...]), (source2, [dest1, dest2, ...]), ...]
        """
        if Board.blue_turn:
            return Board.blue_generation()
        else:
            return Board.red_generation()
    
    @staticmethod
    def exec_move(source:np.uint64, dest:np.uint64) -> tuple:
        """
        switches player automatically after execution
        Args: source, dest
        Returns: (blue_p, blue_k, red_p, red_k) # all bitboards for transition table
        """
        if Board.blue_turn:
            if source & Board.blue_k:
                Board.blue_k_move_execution(source, dest)
            else:
                Board.blue_p_move_execution(source, dest)
        else:
            if source & Board.red_k:
                Board.red_k_move_execution(source, dest)
            else:
                Board.red_p_move_execution(source, dest)
        Board.blue_turn = not Board.blue_turn
        return Board.blue_p, Board.blue_k, Board.red_p, Board.red_k
         
    @staticmethod
    def takeback() -> None:
        """
        switches player automatically after execution
        
        """
        if Board.blue_turn:
            s,d = Board.red_takeback(*Board.stack.pop())
        else:
            s,d = Board.blue_takeback(*Board.stack.pop())
        Board.blue_turn = not Board.blue_turn
        return s,d
    @staticmethod
    def isOver() -> str:
        """
        Returns: "blue" or "red" if the appropriate player has won, "" if not
        Call like: 
        if Board.isOver():
            print(f"{Board.isOver() Won}")
            -> exit
        """
        if Board.blue & Board.blue_on_ground_row:
            return "Blue"
        elif Board.red & Board.red_on_ground_row:
            return "Red"
        else:
            return ""   

    @staticmethod
    def isOpening() -> bool:
        return (Board.blue | Board.red) & Board.r45 == 0
        
    
    ################### Class Variables #####################
    
        
    blue_on_ground_row = np.uint64(0b0111111000000000000000000000000000000000000000000000000000000000)
    red_on_ground_row = np.uint64(0b0000000000000000000000000000000000000000000000000000000001111110)

    # Turn
    blue_turn = True

    # Game Repr
    stack = []

    # Blue
    blue_p, blue_k = np.uint64(0b0111111001111110), np.uint64(0) 
    blue = blue_p | blue_k
    l_blue_k, l_blue_p = [],[]

    # Red pawns
    red_p, red_k = np.uint64(0b0111111001111110000000000000000000000000000000000000000000000000), np.uint64(0) 
    red = red_p | red_k
    l_red_k, l_red_p = [],[]

    # BLUE
    # blue pawn move bitboards
    blue_p_forward = np.uint64(0b0000000001111110111111111111111111111111111111111111111111111111)
    blue_p_right = np.uint64(0b0000000011111110111111101111111011111110111111101111111011111100)
    blue_p_left = np.uint64(0b0000000001111111011111110111111101111111011111110111111100111111)

    # blue pawn hit bitboards
    blue_p_hit_right = np.uint64(0b0000000011111100111111101111111011111110111111101111111011111110)
    blue_p_hit_left = np.uint64(0b0000000000111111011111110111111101111111011111110111111101111111)

    # blue knights move/hit bitboards
    blue_k_forward_right = np.uint64(0b0000000000000000111111001111111011111110111111101111111011111110)
    blue_k_right = np.uint64(0b0000000011111000111111001111110011111100111111001111110011111100)
    blue_k_forward_left = np.uint64(0b0000000000000000001111110111111101111111011111110111111101111111)
    blue_k_left = np.uint64(0b0000000000011111001111110011111100111111001111110011111100111111)

    # Shifts for moves
    # Pawns
    # Forward, left, right, hit left, hit right
    bpf, bpl, bpr, bphl, bphr = np.uint8(8), np.uint8(1), np.uint8(1), np.uint8(9), np.uint8(7)

    #Knights
    # left, forward left, right, forward right
    bkl, bkfl, bkr, bkfr = np.uint8(10), np.uint8(17), np.uint8(6), np.uint8(15)

    # RED
    # red pawn move bitboards
    red_p_forward = np.uint64(0b1111111111111111111111111111111111111111111111110111111000000000)
    red_p_left = np.uint64(0b0011111101111111011111110111111101111111011111110111111100000000)
    red_p_right = np.uint64(0b1111110011111110111111101111111011111110111111101111111000000000)

    # red pawn hit bitboards
    red_p_hit_right = np.uint64(0b1111111111111110111111101111111011111110111111101111110000000000)
    red_p_hit_left = np.uint64(0b1111111101111111011111110111111101111111011111110011111100000000)

    # red knights move/hit bitboards
    red_k_forward_right = np.uint64(0b1111111011111110111111101111111011111110111111000000000000000000)
    red_k_right = np.uint64(0b1111110011111100111111001111110011111100111111001111100000000000)
    red_k_forward_left = np.uint64(0b0111111101111111011111110111111101111111001111110000000000000000)
    red_k_left = np.uint64(0b0011111100111111001111110011111100111111001111110001111100000000)

    # Shifts for moves
    # Pawns
    # Forward, left, right, hit left, hit right
    rpf, rpl, rpr, rphl, rphr = np.uint8(8), np.uint8(1), np.uint8(1), np.uint8(7), np.uint8(9)

    #Knights
    # left, forward left, right, forward right
    rkl, rkfl, rkr, rkfr = np.uint8(6), np.uint8(15), np.uint8(10), np.uint8(17)

    @staticmethod
    def blue_p_move_generation(source:np.uint64) -> list:  
        dests = []
        blocked_squares = ~(Board.red | Board.blue_k) # Pawns unmovable squares
        # forward
        if (source & Board.blue_p_forward) << Board.bpf & blocked_squares: dests.append(source << Board.bpf) 
        # left
        if (source & Board.blue_p_left) << Board.bpl & blocked_squares: dests.append(source << Board.bpl) 
        # hit left
        if (source & Board.blue_p_hit_left) << Board.bphl & Board.red: dests.append(source << Board.bphl) 
        # hit right
        if (source & Board.blue_p_hit_right) << Board.bphr & Board.red: dests.append(source << Board.bphr) 
        # right
        if (source & Board.blue_p_right) >> Board.bpr & blocked_squares: dests.append(source >> Board.bpr) 
        return dests

    @staticmethod
    def blue_k_move_generation(source:np.uint64) -> list: 
        dests = []
        # left
        if (source & Board.blue_k_left) << Board.bkl & ~Board.blue_k: dests.append(source << Board.bkl) 
        # forward_left
        if (source & Board.blue_k_forward_left) << Board.bkfl & ~Board.blue_k: dests.append(source << Board.bkfl) 
        # right
        if (source & Board.blue_k_right) << Board.bkr & ~Board.blue_k: dests.append(source << Board.bkr) 
        # forward_right
        if (source & Board.blue_k_forward_right) << Board.bkfr & ~Board.blue_k: dests.append(source << Board.bkfr) 
        return dests

    @staticmethod
    def blue_p_move_execution(source:np.uint64, dest:np.uint64) -> None:
        # delete source Position 
        Board.l_blue_p.remove(source)
        Board.blue_p = Board.blue_p ^ source

        # on red_k -> hit & knight
        if dest & Board.red_k:
            # remove red knight
            
            Board.red_k = Board.red_k ^ dest
            Board.l_red_k.remove(dest)

            # add blue knigth
            Board.blue_k = Board.blue_k | dest
            Board.l_blue_k.append(dest)

            # new red
            Board.red = Board.red_p | Board.red_k
            Board.stack.append((source, dest, True))

        # on blue_p -> knight
        elif dest & Board.blue_p:
            # add blue knight
            Board.blue_k = Board.blue_k | dest
            Board.l_blue_k.append(dest)
            Board.stack.append((source, dest))


        # on red_p -> hit
        elif dest & Board.red_p:
            # remove red pawn
            Board.red_p = Board.red_p ^ dest
            Board.l_red_p.remove(dest)

            # move blue pawn
            Board.blue_p = Board.blue_p | dest
            Board.l_blue_p.append(dest)
            
            # new red
            Board.red = Board.red_p | Board.red_k
            Board.stack.append((source, dest, True))

        # simple move
        else: 
            # move blue pawn
            Board.blue_p = Board.blue_p | dest
            Board.l_blue_p.append(dest)
            Board.stack.append((source, dest))
        
        # new blue
        Board.blue = Board.blue_p | Board.blue_k
    
    @staticmethod
    def blue_k_move_execution(source:np.uint64, dest:np.uint64) -> None:
        # delete source Position 
        Board.blue_k = Board.blue_k ^ source
        Board.l_blue_k.remove(source)

        
        # on red_k -> hit & knight
        if dest & Board.red_k:
            # remove red knight
            Board.red_k = Board.red_k ^ dest
            Board.l_red_k.remove(dest)

            # add blue knight
            Board.blue_k = Board.blue_k | dest
            Board.l_blue_k.append(dest)

            # new red
            Board.red = Board.red_p | Board.red_k
            Board.stack.append((source, dest, True))

        # on blue_p -> knight
        elif dest & Board.blue_p:
            # add blue knight
            Board.blue_k = Board.blue_k ^ dest
            Board.l_blue_k.append(dest)
            Board.stack.append((source, dest))

        # on red_p -> hit & pawn
        elif dest & Board.red_p:
            # remove red pawn
            Board.red_p = Board.red_p ^ dest
            Board.l_red_p.remove(dest)
            
            # add blue pawn
            Board.blue_p = Board.blue_p | dest
            Board.l_blue_p.append(dest)
            
            # new red
            Board.red = Board.red_p | Board.red_k
            Board.stack.append((source, dest, True))


        # simple move -> pawn
        else: 
            # add blue pawn
            Board.blue_p = Board.blue_p | dest
            Board.l_blue_p.append(dest)
            Board.stack.append((source, dest))
        
        # new blue
        Board.blue = Board.blue_p | Board.blue_k
    
    @staticmethod
    def blue_generation():
        moves = []
        precon = ~(Board.blue_k | Board.red_k)
        for source in Board.l_blue_p:	
            if source & precon:   #pre-validation (pawn under knight)
                fig_moves = Board.blue_p_move_generation(source)
                if len(fig_moves):
                    moves.append((source, fig_moves))
        for source in Board.l_blue_k:
            fig_moves = Board.blue_k_move_generation(source)
            if len(fig_moves):
                moves.append((source, fig_moves))
        return moves

    @staticmethod
    def blue_takeback(source, dest, hit=False):
        # hit (add red)
        if hit:
            if Board.blue_k & dest:
                Board.l_red_k.append(dest)
                Board.red_k = Board.red_k | dest
            else:
                Board.l_red_p.append(dest)
                Board.red_p = Board.red_p | dest
            Board.red = Board.red_p | Board.red_k

        # delete dest
        if Board.blue_k & dest:
            # del Board.l_blue_k[-1]
            Board.l_blue_k.remove(dest)
            Board.blue_k = Board.blue_k ^ dest
        else:
            # del Board.l_blue_p[-1]
            Board.l_blue_p.remove(dest)  
            Board.blue_p = Board.blue_p ^ dest

        # add source
        if (Board.blue_p | Board.red_p) & source:
            Board.l_blue_k.append(source)
            Board.blue_k = Board.blue_k | source
        else:
            Board.l_blue_p.append(source)
            Board.blue_p = Board.blue_p | source
        
        Board.blue = Board.blue_p | Board.blue_k

        return source, dest
    ############ Red ##################

    @staticmethod
    def red_p_move_generation(source:np.uint64) -> list:	# after pre-validation wheather source can move (being below knight
        dests = []
        # Pawns unmovable squares
        blocked_squares = ~(Board.blue | Board.red_k)

        # forward
        if (source & Board.red_p_forward) >> Board.rpf & blocked_squares:
            dests.append(source >> Board.rpf) 

        # left
        if (source & Board.red_p_left) << Board.rpl & blocked_squares:
            dests.append(source << Board.rpl) 

        # right
        if (source & Board.red_p_right) >> Board.rpr & blocked_squares:
            dests.append(source >> Board.rpr) 

        # hit left
        if (source & Board.red_p_hit_left) >> Board.rphl & Board.blue:
            dests.append(source >> Board.rphl) 

        # hit right
        if (source & Board.blue_p_hit_right) >> Board.rphr & Board.blue:
            dests.append(source >> Board.rphr) 
        
        return dests

    @staticmethod
    def red_k_move_generation(source:np.uint64) -> list: # no pre-validation needed
        dests = []
        # left
        if (source & Board.red_k_left) >> Board.rkl & ~Board.red_k:
            dests.append(source >> Board.rkl) 

        # forward_left
        if (source & Board.red_k_forward_left) >> Board.rkfl & ~Board.red_k:
            dests.append(source >> Board.rkfl) 

        # right
        if (source & Board.red_k_right) >> Board.rkr & ~Board.red_k:
            dests.append(source >> Board.rkr) 

        # forward_left
        if (source & Board.red_k_forward_right) >> Board.rkfr & ~Board.red_k:
            dests.append(source >> Board.rkfr) 

        return dests

    @staticmethod
    def red_p_move_execution(source:np.uint64, dest:np.uint64) -> None:
        # delete source Position 
        Board.l_red_p.remove(source)
        Board.red_p = Board.red_p ^ source

        # on blue_k -> hit & knight
        if dest & Board.blue_k:
            # remove blue knight
            Board.blue_k = Board.blue_k ^ dest
            Board.l_blue_k.remove(dest)

            # add red knight
            Board.red_k = Board.red_k | dest
            Board.l_red_k.append(dest)
            
            # new blue
            Board.blue = Board.blue_p | Board.blue_k
            Board.stack.append((source, dest, True))
            
        # on red_p -> knight
        elif dest & Board.red_p:
            # add blue knight
            Board.red_k = Board.red_k | dest
            Board.l_red_k.append(dest)
            Board.stack.append((source, dest))

        # on blue_p -> hit
        elif dest & Board.blue_p:
            # remove blue pawn
            Board.blue_p = Board.blue_p ^ dest
            Board.l_blue_p.remove(dest)

            # move red pawn 
            Board.red_p = Board.red_p | dest
            Board.l_red_p.append(dest)

            # new blue
            Board.blue = Board.blue_p | Board.blue_k
            Board.stack.append((source, dest, True))

        # simple move
        else: 
            Board.red_p = Board.red_p | dest
            Board.l_red_p.append(dest)
            Board.stack.append((source, dest))
        
        # new red
        Board.red = Board.red_p | Board.red_k

    @staticmethod
    def red_k_move_execution(source:np.uint64, dest:np.uint64) -> None:
        # delete source Position 
        Board.red_k = Board.red_k ^ source
        Board.l_red_k.remove(source)
        
        # on blue_k -> hit & knight
        if dest & Board.blue_k:
            # remove blue knight
            Board.blue_k = Board.blue_k ^ dest
            Board.l_blue_k.remove(dest)

            # add red knight
            Board.red_k = Board.red_k | dest
            Board.l_red_k.append(dest)

            # new blue
            Board.blue = Board.blue_p | Board.blue_k
            Board.stack.append((source, dest, True))

        # on red_p -> knight
        elif dest & Board.red_p:
            # add red knight
            Board.red_k = Board.red_k ^ dest
            Board.l_red_k.append(dest)
            Board.stack.append((source, dest))

        # on blue_p -> hit & pawn
        elif dest & Board.blue_p:
            # remove blue pawn
            Board.blue_p = Board.blue_p ^ dest
            Board.l_blue_p.remove(dest)
            
            # add red pawn
            Board.red_p = Board.red_p | dest
            Board.l_red_p.append(dest)
            
            # new blue
            Board.blue = Board.blue_p | Board.blue_k
            Board.stack.append((source, dest, True))

        # simple move -> pawn
        else: 
            # add red pawn
            Board.red_p = Board.red_p | dest
            Board.l_red_p.append(dest)
            Board.stack.append((source, dest))

        # new red
        Board.red = Board.red_p | Board.red_k

    @staticmethod
    def red_generation() -> list:
        moves = []
        precon = ~(Board.blue_k | Board.red_k)
        for source in Board.l_red_p:	
            if source & precon:   #pre-validation (pawn under knight)
                fig_moves = Board.red_p_move_generation(source)
                if len(fig_moves):
                    moves.append((source, fig_moves))
        
        for source in Board.l_red_k:
            fig_moves = Board.red_k_move_generation(source)
            if len(fig_moves):
                moves.append((source, fig_moves))
        return moves

    @staticmethod        
    def red_takeback(source, dest, hit=False) -> None:
        # hit (add blue)
        if hit:
            if Board.red_k & dest:
                Board.l_blue_k.append(dest)
                Board.blue_k = Board.blue_k | dest
            else:
                Board.l_blue_p.append(dest)
                Board.blue_p = Board.blue_p | dest
            Board.blue = Board.blue_p | Board.blue_k

        # delete dest
        if Board.red_k & dest:
            # del Board.l_red_k[-1]
            Board.l_red_k.remove(dest)
            Board.red_k = Board.red_k ^ dest
        else:
            # del Board.l_red_p[-1]
            Board.l_red_p.remove(dest)
            Board.red_p = Board.red_p ^ dest

        # add source
        if (Board.blue_p | Board.red_p) & source:
            Board.l_red_k.append(source)
            Board.red_k = Board.red_k | source
        else:
            Board.l_red_p.append(source)
            Board.red_p = Board.red_p | source

        Board.red = Board.red_p | Board.red_k

        return source, dest

    r1 = np.uint64(0b0000000000000000000000000000000000000000000000000000000001111110)
    C1 = np.uint64(0b0000000000000000000000000000000000000000000000000000000000100000)
    F1 = np.uint64(0b0000000000000000000000000000000000000000000000000000000000000100)

    r2 = np.uint64(0b0000000000000000000000000000000000000000000000001111111100000000)
    r2r = np.uint64(0b0000000000000000000000000000000000000000000000000111111100000000)
    r2l = np.uint64(0b0000000000000000000000000000000000000000000000001111111000000000)
    r2mid = np.uint64(0b0000000000000000000000000000000000000000000000000111111000000000)
    A2 = np.uint64(0b0000000000000000000000000000000000000000000000001000000000000000)
    H2 = np.uint64(0b0000000000000000000000000000000000000000000000000000000100000000)


    r3 = np.uint64(0b0000000000000000000000000000000000000000111111110000000000000000)
    r4 = np.uint64(0b0000000000000000000000000000000011111111000000000000000000000000)
    r5 = np.uint64(0b0000000000000000000000001111111100000000000000000000000000000000)
    r6 = np.uint64(0b0000000000000000111111110000000000000000000000000000000000000000)
    r7 = np.uint64(0b0000000011111111000000000000000000000000000000000000000000000000)
    r7r = np.uint64(0b0000000001111111000000000000000000000000000000000000000000000000)
    r7l = np.uint64(0b0000000011111110000000000000000000000000000000000000000000000000)
    r7mid = np.uint64(0b0000000001111110000000000000000000000000000000000000000000000000)
    A7 = np.uint64(0b0000000010000000000000000000000000000000000000000000000000000000)
    H7 = np.uint64(0b0000000000000001000000000000000000000000000000000000000000000000)


    r8 = np.uint64(0b0111111000000000000000000000000000000000000000000000000000000000)
    C8 = np.uint64(0b0010000000000000000000000000000000000000000000000000000000000000)
    F8 = np.uint64(0b0000010000000000000000000000000000000000000000000000000000000000)

    r23 = r2 | r3
    r45 = r4 | r5
    r67 = r6 | r7

    min_eval = -1000
    max_eval = 1000

    # weights 

     

    # Helper Function for eval
    numpyone = np.uint64(1) 
    @staticmethod
    def count_figs(num):
        count = 0
        while num:
            num &= num - Board.numpyone 
            count += 1
        return count    
        
    @staticmethod
    def eval() -> int:
        """
        targeted -> attacked at least once
        protected -> protected at least once
        attacking -> attacks at least one figure
        """

        # pawn existence
        wp = 10

        # knight existence
        wk = 30

        # temp 
        w = 0
        b = 0 

        blue_p_movable = Board.blue_p & ~(Board.blue_k | Board.red_k)
        red_p_movable = Board.red_p & ~(Board.blue_k | Board.red_k)

        # Hits
        # Blue hits
        blue_k_hits = (Board.blue_k & Board.blue_k_forward_left << Board.bkfl) | (Board.blue_k & Board.blue_k_forward_right << Board.bkfr) | (Board.blue_k & Board.blue_k_left << Board.bkl) | (Board.blue_k & Board.blue_k_right << Board.bkr) if Board.blue_k else np.uint64(0)
        blue_p_hits = (blue_p_movable & Board.blue_p_hit_left << Board.bphl) | (blue_p_movable & Board.blue_p_hit_right << Board.bphr)
        blue_no_hits = ~(blue_k_hits | blue_p_hits)

        # Red hits
        red_k_hits = (Board.red_k & Board.red_k_forward_left >> Board.rkfl) | (Board.red_k & Board.red_k_forward_right >> Board.rkfr) | (Board.red_k & Board.red_k_left >> Board.rkl) | (Board.red_k & Board.red_k_right >> Board.rkr) if Board.red_k else np.uint64(0)
        red_p_hits = (red_p_movable & Board.red_p_hit_left >> Board.rphl) | (red_p_movable & Board.red_p_hit_right >> Board.rphr)
        red_no_hits = ~(red_k_hits | red_p_hits)

        # Potential Knights
        # Blue knights
        blue_pot_k = Board.blue_p & ((Board.blue_p & Board.blue_p_forward << Board.bpf) | (Board.blue_p & Board.blue_p_left << Board.bpl) | (Board.blue_p & Board.blue_p_right >> Board.bpr) | (Board.blue_p_hits & Board.red_k))
        blue_k_untargeted = Board.blue_k & red_no_hits

        # Blue Pawns
        blue_pot_p = Board.blue_k & Board.blue_p
        blue_p_untargeted = blue_p_movable & red_no_hits


        # Red knights
        red_pot_k = Board.red_p & ((Board.red_p & Board.red_p_forward >> Board.rpf) | (Board.red_p & Board.red_p_left << Board.rpl) | (Board.red_p & Board.red_p_right >> Board.rpr) | (Board.red_p_hits & Board.blue_k))
        red_k_untargeted = Board.red_k & blue_no_hits

        # Red Pawns
        red_p_untargeted = Board.red_p & blue_no_hits

        if Board.blue_turn:
            # Won
            if Board.blue & Board.r8:
                return Board.max_eval
            
            # Lost -> Red can force Win cause red moves next
            if Board.red_k & Board.r23:
                return Board.min_eval
            
            # Force Win in next knight move (knigth on r67)
            if (red_k_untargeted & Board.r67):
                return Board.max_eval - 1
            
            # Force Win in next pawn move (no hits, on r7))
            if ((blue_p_untargeted & Board.r7mid) << Board.bpf) & ~Board.red:
                return Board.max_eval - 1
            
            # Force Win in next pawn hit Knight left
            if ((blue_p_untargeted & Board.r7r) << Board.bphl) & Board.red_k:
                return Board.max_eval - 1
            
            # Force Win in next pawn hit Knight left
            if ((blue_p_untargeted & Board.r7l) << Board.bphr) & Board.red_k:
                return Board.max_eval - 1
        
        else:
           pass
            
        ##############################################################
        # Figure independent # Blue (Mostly Cause Partial dependent on red)
        ##############################################################

        # Material Advantage
        eval = wp*(len(Board.l_blue_p) - len(Board.l_red_p)) + wk*(len(Board.l_blue_k) - len(Board.l_red_k))

 
        
        # Blue untargeted Knights Attacking Pawns
        red_p_attacked_by_k = blue_k_hits & red_p_movable
        if red_p_attacked_by_k:
            blue_k_attacking_p = ((red_p_attacked_by_k >> Board.bkfl) | (red_p_attacked_by_k >> Board.bkfr) | (red_p_attacked_by_k >> Board.bkl) | (red_p_attacked_by_k >> Board.bkr)) & Board.blue_k
            eval += w*Board.count_figs(blue_k_attacking_p)

        # Blue untargeted Pawns Attacking Knights
        red_k_attacked_by_p = blue_p_hits & Board.red_k
        if red_k_attacked_by_p:
            blue_p_attacking_k = ((red_k_attacked_by_p >> Board.bphl) | (red_k_attacked_by_p >> Board.bphr)) & blue_p_movable
            eval += w*Board.count_figs(blue_p_attacking_k)

        ####################### Red #################################
        # Red untargeted Knights Attacking Pawns
        blue_p_attacked_by_k = red_k_hits & blue_p_movable
        if blue_p_attacked_by_k:
            red_k_attacking_p = ((blue_p_attacked_by_k << Board.rkfl) | (blue_p_attacked_by_k << Board.rkfr) | (blue_p_attacked_by_k << Board.rkl) | (blue_p_attacked_by_k << Board.rkr)) & Board.red_k
            eval -= w*Board.count_figs(red_k_attacking_p)

        # Red untargeted Pawns Attacking Knights
        blue_k_attacked_by_p = red_p_hits & Board.blue_k
        if blue_k_attacked_by_p:
            red_p_attacking_k = ((blue_k_attacked_by_p << Board.rphl) | (blue_k_attacked_by_p << Board.rphr)) & red_p_movable
            eval -= w*Board.count_figs(red_p_attacking_k)
        ##############################################################

        # Blue Pawns attacked by unprotected knights that can counterattack without being hit or with being hit and counterhit
        squares = (blue_p_attacked_by_k << Board.bpf | blue_p_attacked_by_k << Board.bpl | blue_p_attacked_by_k >> Board.bpr) & ~(Board.red | Board.blue_k) & (red_no_hits | ~blue_no_hits)
        if (squares << Board.bphr | squares << Board.bphl) & red_k_untargeted:
            eval += w*Board.count_figs(squares)
        
        """
        ##############################################################
        # For each Figure # Blue
        ##############################################################
        ########################## Pawns #############################
        for fig in Board.l_blue_p:
            # attacking Pawns
            if((fig & Board.blue_p_hit_right << Board.bphr) | (fig & Board.blue_p_hit_left << Board.bphl)) & Board.red:
                # untargeted
                if fig & ~Board.red_hits:
                    eval += b
                # targeted & protected
                elif fig & Board.blue_hits:
                    eval += b
                # targeted
                else:
                    eval += b

            # non-attacking Pawns
            else:
                # targeted
                if fig & Board.red_hits:
                    # protected
                    if fig & Board.blue_hits:
                        eval += b
                    
                    # unprotected
                    else:
                        eval += b
                # untargeted & non-attacking
                else:
                    eval += b
        
            ##############################################################
            # Certain Pawn Areas # Blue
            ##############################################################
            
            # Targeted
            if fig & ~Board.red_hits:
                # Valueble Pawn H7 untargeted
                if fig & Board.H7:
                    eval += b
                    # no Red Pawn on C8
                    if ~(Board.C8 & Board.red_p):
                        eval += b

                # Valueble Pawn H2 untargeted
                if blue_p_untarget & Board.H2:
                    eval += b
                    # no Red Pawn on F8          
                    if ~(Board.F8 & Board.red_p):
                        eval += b
                

            
        # TODO: Knights
        ########################## Knights #############################
        for fig in Board.l_blue_k: 
            # non-targeted
            if fig & ~Board.red_hits:

            ##############################################################
            # Certain Knight Areas # Blue
            ##############################################################

                # Possible Knight on r5 untargeted
                if fig & Board.r5:
                    eval += b

                # Knight on r5 untargeted or at least one possible takeback
                if fig & Board.r4:
                    eval += b
        """
                
        return eval


    ############################ TESTING ############################
    @staticmethod
    def state(message="",s=False,d=False) -> None:
        def board_to_string(board:np.uint64)->str:
            return np.binary_repr(board,width=64)
        def print_board(board:np.uint64):
            string = np.binary_repr(board,width=64)
            #str = 'X' + str[1:7]+'X'+str[8:56]+'X'+str[57:63]+'X'
            print('\n'.join(string[i:i+8] for i in range(0, len(string), 8)))
            print()
        if message:
            print(f"------------- {message}  --------------------------")
        else:
            print("-----------------------------------------------------");print()

        def print_move(s=False,d=False):
            if s | d:
                print("Source")
                print_board(s)
                print("Dest")
                print_board(d)

        red_p,blue_p,red_k ,blue_k = np.uint64(0),np.uint64(0),np.uint64(0),np.uint64(0)
        for p in Board.l_blue_p:
            if p & blue_p:
                print_move(s,d)
                Board.bitboard_states()
                raise Exception("Double Blue Pawn")
            blue_p = blue_p ^ p
        for k in Board.l_blue_k:
            if k & blue_k:
                print_move(s,d)
                Board.bitboard_states()
                raise Exception("Double Blue Knight")
            blue_k = blue_k ^ k
        for p in Board.l_red_p: 
            if p & red_p:
                print_move(s,d)
                Board.bitboard_states()
                raise Exception("Double Red Pawn")
            red_p = red_p ^ p
        for k in Board.l_red_k: 
            if k & red_k:
                print_move(s,d)
                Board.bitboard_states()
                raise Exception("Double Red Knight")
            red_k = red_k ^ k

        if blue_p==Board.blue_p:
            if blue_k==Board.blue_k:
                if blue_p | blue_k!=Board.blue:
                    print_move(s,d)
                    Board.bitboard_states()
                    raise Exception("blue != board.blue")

            else:
                print_move(s,d)
                Board.bitboard_states()
                raise Exception("blues knights != l_blues_knights")
        else:
            print_move(s,d)
            Board.bitboard_states()
            raise Exception("blues pawns != l_blues_pawns")

        if red_p==Board.red_p: 
            if red_k==Board.red_k:
                if red_p | red_k!=Board.red:
                    print_move(s,d)
                    Board.bitboard_states()
                    raise Exception("red != board.red")		
            else:
                print_move(s,d)
                Board.bitboard_states()
                raise Exception("red knights != l_red_knights")
        else:
            print_move(s,d)
            Board.bitboard_states()
            raise Exception("red pawns != l_red_pawns")
        
        s=""
        BLUE = "\033[34m"
        RED = "\033[31m"
        RESET = "\033[0m"

        for rp,bp,rk,bk in zip(board_to_string(red_p).replace('1','r'),board_to_string(blue_p ).replace('1','b'),board_to_string(red_k ).replace('1','R'),board_to_string(blue_k).replace('1','B')):
            if rk!="0":
                s+="R"
            elif bk!="0":
                s+="B"
            elif rp!="0":
                s+="r"
            elif bp!="0":
                s+="b"
            else:
                s+="0"
        s='\n'.join(s[i:i+8] for i in range(0, len(s), 8))
        print(s.replace("R",RED+"K"+RESET).replace("B",BLUE+"K"+RESET).replace("r",RED+"P"+RESET).replace("b",BLUE+"P"+RESET))
        # print_board(blue_p)
        # print_board(blue_k)
        # print_board(red_p)
        # print_board(red_k)
        print(f"Blue Turn?: {Board.blue_turn}")
        print(f"Stack: {Board.stack}")

    @staticmethod
    def play(FEN_board=False, blue_turn=True):

        if FEN_board:
            Board.initBoard(*GameState.createBitBoardFrom(Gui.fenToMatrix(FEN_board),True),blue_turn)
        else:
            Board.initBoard(np.uint64(0b0111111001111110000000000000000000000000000000000000000000000000), np.uint64(0),np.uint64(0b0111111001111110), np.uint64(0),blue_turn)
        Board.state("Startpos")
        if input("Move? -> Enter, State? -> s") == "s":
            Board.bitboard_states()

        def rand_move_execution(moves):
            fig = random.choice(moves)
            move = random.choice(fig[1])
            Board.exec_move(fig[0],move)
            return fig[0],move
        
        def takeback():
            inp = input("Takeback? -> 't', State? -> 's': ")
            
            if inp =="t":
                s,d  = Board.takeback()
                Board.state("Takeback",s,d)    
                takeback()
            elif inp == "s":
                Board.bitboard_states()
                takeback()
            

        while Board.isOver() == "":
            moves = Board.generate_moves()
            print(f"moves: {moves}")
            rand_move_execution(moves)

            Board.state()

            takeback()

        
            
        print(Board.isOver())

    @staticmethod
    def bitboard_states():
        def print_board(board:np.uint64):
            string = np.binary_repr(board,width=64)
            #str = 'X' + str[1:7]+'X'+str[8:56]+'X'+str[57:63]+'X'
            print('\n'.join(string[i:i+8] for i in range(0, len(string), 8)))
            print()

        red_p,blue_p ,red_k ,blue_k = np.uint64(0),np.uint64(0),np.uint64(0),np.uint64(0)
        for p in Board.l_blue_p:
            blue_p = blue_p ^ p
        for k in Board.l_blue_k:
            blue_k = blue_k ^ k
        for p in Board.l_red_p: 
            red_p = red_p ^ p
        for k in Board.l_red_k: 
            red_k = red_k ^ k

        print("Blue Pawns")
        print_board(Board.blue_p)
        print("Blue L_pawns (maybe double)")
        print_board(blue_p)
        print("Blue Knights")
        print_board(Board.blue_k)
        print("Blue L_knights (maybe double)")
        print_board(blue_k)
        # print("Blue")
        # print_board(Board.blue)

        # print("Red Pawns")
        # print_board(Board.red_p)
        # print("Red L_pawns (maybe double)")
        # print_board(red_p)
        # print("Red Knights")
        # print_board(Board.red_k)
        # print("Red L_knights (maybe double)")
        # print_board(red_k)
        # print("Red")
        # print_board(Board.red)

if __name__ == "__main__":
    # simple figure
    #test = "6/b07/8/8/8/8/8/6 b"

	# Blue Pawns
    # test = "1b04/8/8/8/8/8/8/6 b"
    # test = "8/r0b0r05/8/8/8/8/8/6 b"
    # test = "6/8/8/8/8/b0r06/8/6 b"
    # test = "6/8/8/8/8/6r0b0/8/6 b"
    # test = "6/8/8/8/8/7b0/7r0/6 b"
	# test = "6/8/8/8/8/8/7b0/6 b"
    # test = "8/rr0b0rr05/8/8/8/8/8/6 b"
    # test = "8/br0b0br05/8/8/8/8/8/6 b"
    
    # test = "6/8/8/8/8/8/6b0b0/6 b"

	# blue hits
	# hit pawn
    # test = "6/8/8/8/8/r0b0r05/r0r0r05/6 b"
	# hit double red knight
    # test = "6/8/8/8/8/rr0b0rr05/rr0rr0rr05/6 b"
	# hit red blue knight
    # test = "6/8/8/8/8/rr0b0rr05/br0rr0br05/6 b"

	# Blue knights
    # test = "6/2bb05/8/8/8/8/8/6 b"
    # test = "6/2bb05/rr07/1r01b0/8/8/8/6 b"

	# on r pawn?
	# test = "6/bb07/8/1r06/8/8/8/6 b"

	# on b pawn?
	#test = "6/bb07/8/1b06/8/8/8/6 b"

	# on rr knigth?
	# test = "6/bb07/8/1rr06/8/8/8/6 b"

	# on br knight?
    # test = "6/bb07/8/1br06/8/8/8/6 b"

	# on bb knigth?
    # test = "6/bb07/8/1bb06/8/8/8/6 b"

	############################################
	# Red Pawns
	# test = "8/8/8/8/8/8/b0r0b05/6 r"
	# test = "6/7b0/7r0/8/8/8/8/6 r"
	# test = "6/7r0/8/8/8/8/8/6 r"
	# test = "8/rb0r0rb05/8/8/8/8/8/6 r"
	# test = "8/bb0r0bb05/8/8/8/8/8/6 r"

	# test = "6/6r0r0/8/8/8/8/8/6 r"

	# Red hits
	# hit pawn
    # test = "6/b0b0b05/b0r0b05/8/8/8/8/6 r"
	# hit double red knight
    # test = "6/bb0bb0bb05/bb0r0bb05/8/8/8/8/6 r"
	# hit red blue knight
    # test = "6/rb0rb0bb05/rb0r0rb05/8/8/8/8/6 r"


	# Red knights
    # test = "6/8/8/8/8/8/2rr05/6 r"

	# on b pawn?
    # test = "6/8/8/8/1b06/8/rr07/6 r"

	# on r pawn?
    # test = "6/8/8/8/1r06/8/rr07/6 r"

	# on bb knigth
    # test = "6/8/8/8/1bb06/8/rr07/6 r"

	# on rb knight?
    # test = "6/8/8/8/1rb06/8/rr07/6 r"

	# on rr knigth?


    # Multiple takebacks
    # hitcombis
    test = "6/87/bb07/8/8/8/rr07/6 r"
    # test = "6/8/8/b07/1rr06/8/rr07/6 r"

    #test = "6/8/8/8/1bb06/07r/8/6 r"




    b, player = test.split(" ")
    game = {"board": b,
			"player": player,
			"player1": True,
			"player2": False,
	}
    # For Blue
    FEN_board = game["board"]
    Board.initBoard(*GameState.createBitBoardFrom(Gui.fenToMatrix(FEN_board),True),True)
    Board.state("Startpos")
    print(Board.isOpening())
    # For Red
    # Board.play()
    