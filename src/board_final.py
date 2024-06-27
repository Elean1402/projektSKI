import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from src.gamestate import GameState
from src.gui import Gui
import random

"""
Notes:
    Only static methods -> don't create instances e.g. just call self.func()
    To use:
        initBoard(*Bitboards, blue_turn) -> None   # new game
        generate_moves() -> [(source1, [dest1, dest2, ...]), ...] # generates all possible moves of the current player
        exec_move(source, dest) -> (blue_pawns, blue_knights, red_pawns, red_knights) # executes move of the current player
        takeback -> takeback last move
        isOver  -> checks if the game is over
        --> check isOver after initBoard and after exec_move

    In process (don't use yet):
        eval() -> int # evaluation of the current board
"""



class MoveGenerator:
    def __init__(self,red_pawns, red_knights,blue_pawns, blue_knights, blue_turn=True) -> None:
        """
        Sets up new game:
        Call like this: 
            self.initBoard(*GameState.createBitBoardFrom(Gui.fenToMatrix(FEN_board),True),blue_turn:bool)

        Imports needed for that:
            from src.gamestate import GameState
            from src.gui import Gui
        """
        self.blue_turn = blue_turn
        self.blue_p = blue_pawns
        self.blue_k = blue_knights
        self.blue = blue_pawns | blue_knights
        self.red_p = red_pawns
        self.red_k = red_knights
        self.red = red_pawns | red_knights
        self.l_blue_p=[]
        self.l_blue_k=[]
        self.l_red_p=[]
        self.l_red_k=[]
        for bit_board, figure_list in zip((self.blue_p, self.blue_k, self.red_p, self.red_k),(self.l_blue_p,self.l_blue_k,self.l_red_p,self.l_red_k)):
            for bit in range(64):
                if bit_board & (np.uint64(1 << bit)):
                    figure_list.append(np.uint64(1 << bit))


    def generate_moves(self) -> list:
        """
        Format of the returned list:
        [(source1, [dest1, dest2, ...]), (source2, [dest1, dest2, ...]), ...]
        """
        if self.blue_turn:
            return self.blue_generation()
        else:
            return self.red_generation()
    

    def exec_move(self,source:np.uint64, dest:np.uint64) -> tuple:
        """
        switches player automatically after execution
        Args: source, dest
        Returns: (blue_p, blue_k, red_p, red_k) # all bitboards for transition table
        """
        if self.blue_turn:
            if source & self.blue_k:
                self.blue_k_move_execution(source, dest)
            else:
                self.blue_p_move_execution(source, dest)
        else:
            if source & self.red_k:
                self.red_k_move_execution(source, dest)
            else:
                self.red_p_move_execution(source, dest)
        self.blue_turn = not self.blue_turn
        return self.blue_p, self.blue_k, self.red_p, self.red_k
         

    def takeback(self) -> None:
        """
        switches player automatically after execution
        
        """
        if self.blue_turn:
            self.red_takeback(*self.stack.pop())
        else:
            self.blue_takeback(*self.stack.pop())
        self.blue_turn = not self.blue_turn
    

    def isOver(self) -> str:
        """
        Returns: "blue" or "red" if one of the players has won, "" if not
        """
        if self.blue & self.blue_on_ground_row:
            return "blue"
        elif self.red & self.red_on_ground_row:
            return "red"
        else:
            return ""
        
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


    def blue_p_move_generation(self,source:np.uint64) -> list:  
        dests = []
        blocked_squares = ~(self.red | self.blue_k) # Pawns unmovable squares
        # forward
        if (source & self.blue_p_forward) << self.bpf & blocked_squares: dests.append(source << self.bpf) 
        # left
        if (source & self.blue_p_left) << self.bpl & blocked_squares: dests.append(source << self.bpl) 
        # hit left
        if (source & self.blue_p_hit_left) << self.bphl & self.red: dests.append(source << self.bphl) 
        # hit right
        if (source & self.blue_p_hit_right) << self.bphr & self.red: dests.append(source << self.bphr) 
        # right
        if (source & self.blue_p_right) >> self.bpr & blocked_squares: dests.append(source >> self.bpr) 
        return dests


    def blue_k_move_generation(self,source:np.uint64) -> list: 
        dests = []
        # left
        if (source & self.blue_k_left) << self.bkl & ~self.blue_k: dests.append(source << self.bkl) 
        # forward_left
        if (source & self.blue_k_forward_left) << self.bkfl & ~self.blue_k: dests.append(source << self.bkfl) 
        # right
        if (source & self.blue_k_right) << self.bkr & ~self.blue_k: dests.append(source << self.bkr) 
        # forward_right
        if (source & self.blue_k_forward_right) << self.bkfr & ~self.blue_k: dests.append(source << self.bkfr) 
        return dests


    def blue_p_move_execution(self,source:np.uint64, dest:np.uint64) -> None:
        # delete source Position 
        self.l_blue_p.remove(source)
        self.blue_p = self.blue_p ^ source

        # on red_k -> hit & knight
        if dest & self.red_k:
            # remove red knight
            
            self.red_k = self.red_k ^ dest
            self.l_red_k.remove(dest)

            # add blue knigth
            self.blue_k = self.blue_k | dest
            self.l_blue_k.append(dest)

            # new red
            self.red = self.red_p | self.red_k
            self.stack.append((source, dest, True))

        # on blue_p -> knight
        elif dest & self.blue_p:
            # add blue knight
            self.blue_k = self.blue_k | dest
            self.l_blue_k.append(dest)
            self.stack.append((source, dest))


        # on red_p -> hit
        elif dest & self.red_p:
            # remove red pawn
            self.red_p = self.red_p ^ dest
            self.l_red_p.remove(dest)

            # move blue pawn
            self.blue_p = self.blue_p | dest
            self.l_blue_p.append(dest)
            
            # new red
            self.red = self.red_p | self.red_k
            self.stack.append((source, dest, True))

        # simple move
        else: 
            # move blue pawn
            self.blue_p = self.blue_p | dest
            self.l_blue_p.append(dest)
            self.stack.append((source, dest))
        
        # new blue
        self.blue = self.blue_p | self.blue_k
    
    def blue_k_move_execution(self,source:np.uint64, dest:np.uint64) -> None:
        # delete source Position 
        self.blue_k = self.blue_k ^ source
        self.l_blue_k.remove(source)

        
        
        # on red_k -> hit & knight
        if dest & self.red_k:
            # remove red knight
            self.red_k = self.red_k ^ dest
            self.l_red_k.remove(dest)

            # add blue knight
            self.blue_k = self.blue_k | dest
            self.l_blue_k.append(dest)

            # new red
            self.red = self.red_p | self.red_k
            self.stack.append((source, dest, True))

        # on blue_p -> knight
        elif dest & self.blue_p:
            # add blue knight
            self.blue_k = self.blue_k ^ dest
            self.l_blue_k.append(dest)
            self.stack.append((source, dest))

        # on red_p -> hit & pawn
        elif dest & self.red_p:
            # remove red pawn
            self.red_p = self.red_p ^ dest
            self.l_red_p.remove(dest)
            
            # add blue pawn
            self.blue_p = self.blue_p | dest
            self.l_blue_p.append(dest)
            
            # new red
            self.red = self.red_p | self.red_k
            self.stack.append((source, dest, True))


        # simple move -> pawn
        else: 
            # add blue pawn
            self.blue_p = self.blue_p | dest
            self.l_blue_p.append(dest)
            self.stack.append((source, dest))
        
        # new blue
        self.blue = self.blue_p | self.blue_k
    
    def blue_generation(self):
        moves = []
        precon = ~(self.blue_k | self.red_k)
        for source in self.l_blue_p:	
            if source & precon:   #pre-validation (pawn under knight)
                fig_moves = self.blue_p_move_generation(source)
                if len(fig_moves):
                    moves.append((source, fig_moves))
        for source in self.l_blue_k:
            fig_moves = self.blue_k_move_generation(source)
            if len(fig_moves):
                moves.append((source, fig_moves))
        return moves

    def blue_takeback(self,source, dest, hit=False):
        # hit (add red)
        if hit:
            if self.blue_k & dest:
                self.l_red_k.append(dest)
                self.red_k = self.red_k | dest
            else:
                self.l_red_p.append(dest)
                self.red_p = self.red_p | dest
            self.red = self.red_p | self.red_k

        # delete dest
        if self.blue_k & dest:
            del self.l_blue_k[-1]
            self.blue_k = self.blue_k ^ dest
        else:
            del self.l_blue_p[-1]
            self.blue_p = self.blue_p ^ dest

        # add source
        if (self.blue_p | self.red_p) & source:
            self.l_blue_k.append(source)
            self.blue_k = self.blue_k | source
        else:
            self.l_blue_p.append(source)
            self.blue_p = self.blue_p | source
        
        self.blue = self.blue_p | self.blue_k

    ############ Red ##################

    def red_p_move_generation(self,source:np.uint64) -> list:	# after pre-validation wheather source can move (being below knight
        dests = []
        # Pawns unmovable squares
        blocked_squares = ~(self.blue | self.red_k)

        # forward
        if (source & self.red_p_forward) >> self.rpf & blocked_squares:
            dests.append(source >> self.rpf) 

        # left
        if (source & self.red_p_left) << self.rpl & blocked_squares:
            dests.append(source << self.rpl) 

        # right
        if (source & self.red_p_right) >> self.rpr & blocked_squares:
            dests.append(source >> self.rpr) 

        # hit left
        if (source & self.red_p_hit_left) >> self.rphl & self.blue:
            dests.append(source >> self.rphl) 

        # hit right
        if (source & self.blue_p_hit_right) >> self.rphr & self.blue:
            dests.append(source >> self.rphr) 
        
        return dests

    def red_k_move_generation(self,source:np.uint64) -> list: # no pre-validation needed
        dests = []
        # left
        if (source & self.red_k_left) >> self.rkl & ~self.red_k:
            dests.append(source >> self.rkl) 

        # forward_left
        if (source & self.red_k_forward_left) >> self.rkfl & ~self.red_k:
            dests.append(source >> self.rkfl) 

        # right
        if (source & self.red_k_right) >> self.rkr & ~self.red_k:
            dests.append(source >> self.rkr) 

        # forward_left
        if (source & self.red_k_forward_right) >> self.rkfr & ~self.red_k:
            dests.append(source >> self.rkfr) 

        return dests


    def red_p_move_execution(self,source:np.uint64, dest:np.uint64) -> None:
        # delete source Position 
        self.l_red_p.remove(source)
        self.red_p = self.red_p ^ source

        # on blue_k -> hit & knight
        if dest & self.blue_k:
            # remove blue knight
            self.blue_k = self.blue_k ^ dest
            self.l_blue_k.remove(dest)

            # add red knight
            self.red_k = self.red_k | dest
            self.l_red_k.append(dest)
            
            # new blue
            self.blue = self.blue_p | self.blue_k
            self.stack.append((source, dest, True))
            
        # on red_p -> knight
        elif dest & self.red_p:
            # add blue knight
            self.red_k = self.red_k | dest
            self.l_red_k.append(dest)
            self.stack.append((source, dest))

        # on blue_p -> hit
        elif dest & self.blue_p:
            # remove blue pawn
            self.blue_p = self.blue_p ^ dest
            self.l_blue_p.remove(dest)

            # move red pawn 
            self.red_p = self.red_p | dest
            self.l_red_p.append(dest)

            # new blue
            self.blue = self.blue_p | self.blue_k
            self.stack.append((source, dest, True))

        # simple move
        else: 
            self.red_p = self.red_p | dest
            self.l_red_p.append(dest)
            self.stack.append((source, dest))
        
        # new red
        self.red = self.red_p | self.red_k


    def red_k_move_execution(self,source:np.uint64, dest:np.uint64) -> None:
        # delete source Position 
        self.red_k = self.red_k ^ source
        self.l_red_k.remove(source)
        
        # on blue_k -> hit & knight
        if dest & self.blue_k:
            # remove blue knight
            self.blue_k = self.blue_k ^ dest
            self.l_blue_k.remove(dest)

            # add red knight
            self.red_k = self.red_k | dest
            self.l_red_k.append(dest)

            # new blue
            self.blue = self.blue_p | self.blue_k
            self.stack.append((source, dest, True))

        # on red_p -> knight
        elif dest & self.red_p:
            # add red knight
            self.red_k = self.red_k ^ dest
            self.l_red_k.append(dest)
            self.stack.append((source, dest))

        # on blue_p -> hit & pawn
        elif dest & self.blue_p:
            # remove blue pawn
            self.blue_p = self.blue_p ^ dest
            self.l_blue_p.remove(dest)
            
            # add red pawn
            self.red_p = self.red_p | dest
            self.l_red_p.append(dest)
            
            # new blue
            self.blue = self.blue_p | self.blue_k
            self.stack.append((source, dest, True))

        # simple move -> pawn
        else: 
            # add red pawn
            self.red_p = self.red_p | dest
            self.l_red_p.append(dest)
            self.stack.append((source, dest))

        # new red
        self.red = self.red_p | self.red_k


    def red_generation(self) -> list:
        moves = []
        precon = ~(self.blue_k | self.red_k)
        for source in self.l_red_p:	
            if source & precon:   #pre-validation (pawn under knight)
                fig_moves = self.red_p_move_generation(source)
                if len(fig_moves):
                    moves.append((source, fig_moves))
        
        for source in self.l_red_k:
            fig_moves = self.red_k_move_generation(source)
            if len(fig_moves):
                moves.append((source, fig_moves))
        return moves

    
    def red_takeback(self,source, dest, hit=False) -> None:
        # hit (add blue)
        if hit:
            if self.red_k & dest:
                self.l_blue_k.append(dest)
                self.blue_k = self.blue_k | dest
            else:
                self.l_blue_p.append(dest)
                self.blue_p = self.blue_p | dest
            self.blue = self.blue_p | self.blue_k

        # delete dest
        if self.red_k & dest:
            del self.l_red_k[-1]
            self.red_k = self.red_k ^ dest
        else:
            del self.l_red_p[-1]
            self.red_p = self.red_p ^ dest

        # add source
        if (self.blue_p | self.red_p) & source:
            self.l_red_k.append(source)
            self.red_k = self.red_k | source
        else:
            self.l_red_p.append(source)
            self.red_p = self.red_p | source

        self.red = self.red_p | self.red_k



    def eval(self) -> int:
        """
        Returns: evaluation of the current board
        """
        # Hits
        # Blue hits
        blue_k_hits = (self.blue_k & self.blue_k_forward_left << self.bkfl) | (self.blue_k & self.blue_k_forward_right << self.bkfr) | (self.blue_k & self.blue_k_left << self.bkl) | (self.blue_k & self.blue_k_right << self.bkr) if self.blue_k else np.uint64(0)
        blue_p_hits = (self.blue_p & self.blue_p_hit_left << self.bphl) | (self.blue_p & self.blue_p_hit_right << self.bphr)

        # Red hits
        red_k_hits = (self.red_k & self.red_k_forward_left >> self.rkfl) | (self.red_k & self.red_k_forward_right >> self.rkfr) | (self.red_k & self.red_k_left >> self.rkl) | (self.red_k & self.red_k_right >> self.rkr) if self.red_k else np.uint64(0)
        red_p_hits = (self.red_p & self.red_p_hit_left >> self.rphl) | (self.red_p & self.red_p_hit_right >> self.rphr)

        # Potential Knights
        # Blue knights
        blue_pot_k = self.blue_p & ((self.blue_p & self.blue_p_forward << self.bpf) | (self.blue_p & self.blue_p_left << self.bpl) | (self.blue_p & self.blue_p_right >> self.bpr) | (blue_p_hits & self.red_k))

        # Red knights
        red_pot_k = self.red_p & ((self.red_p & self.red_p_forward >> self.rpf) | (self.red_p & self.red_p_left << self.rpl) | (self.red_p & self.red_p_right >> self.rpr) | (red_p_hits & self.blue_k))
        return 0

    ############################ TESTING ############################

    def state(self, message="") -> None:
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
	
        red_p,blue_p ,red_k ,blue_k = np.uint64(0),np.uint64(0),np.uint64(0),np.uint64(0)
        for p in self.l_blue_p: blue_p = blue_p ^ p
        for k in self.l_blue_k: blue_k = blue_k ^ k
        for p in self.l_red_p: red_p = red_p ^ p
        for k in self.l_red_k: red_k = red_k ^ k

        if blue_p==self.blue_p:
            if blue_k==self.blue_k:
                if blue_p | blue_k!=self.blue:
                    print("blue")
                    print_board(blue_p | blue_k)
                    print("self.blue")
                    print_board(self.blue)
                    raise Exception("blue != self.blue")

            else:
                print("blue_k")
                print_board(self.blue_k)
                print("l_blue_k")
                print_board(blue_k)
                raise Exception("blues knights != l_blues_knights")
        else:
            print("blue_p")
            print_board(self.blue_p)
            print("l_blue_p")
            print_board(blue_p)
            raise Exception("blues pawns != l_blues_pawns")

        if red_p==self.red_p: 
            if red_k==self.red_k:
                if red_p | red_k!=self.red:
                    print("red")
                    print_board(red_p | red_k)
                    print("self.red")
                    print_board(self.red)
                    raise Exception("red != self.red")		
            else:
                print("red_k")
                print_board(self.red_k)
                print("l_red_k")
                print_board(red_k)
                raise Exception("red knights != l_red_knights")
        else:
            print("red_p")
            print_board(self.red_p)
            print("l_red_p")
            print_board(red_p)
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
        print(f"Blue Turn?: {self.blue_turn}")
        print(f"Stack: {self.stack}")


    def play(self, FEN_board=False, blue_turn=True):
        if FEN_board:
            self.initBoard(*GameState.createBitBoardFrom(Gui.fenToMatrix(FEN_board),True),blue_turn)
        else:
            self.initBoard(np.uint64(0b0111111001111110000000000000000000000000000000000000000000000000), np.uint64(0),np.uint64(0b0111111001111110), np.uint64(0),blue_turn)
        self.state("Startpos")

        def rand_move_execution(moves):
            fig = random.choice(moves)
            move = random.choice(fig[1])
            self.exec_move(fig[0],move)
            return fig[0],move

        while self.isOver() == "":
            moves = self.generate_moves()
            print(f"moves: {moves}")

            rand_move_execution(moves)

            self.state()
            inp = input("Takeback? -> Enter 't': ")
            
            if inp =="t":
                self.takeback()
                self.state("Takeback")
            
        print(self.isOver())

# if __name__ == "__main__":
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
    # test = "6/8/8/8/1rr06/8/rr07/6 r"

    # b, player = test.split(" ")
    # game = {"board": b,
	# 		"player": player,
	# 		"player1": True,
	# 		"player2": False,
	# }
    # # For Blue
    # # self.play(game["board"])

    # # For Red
    # Board = Board(game["board"])
