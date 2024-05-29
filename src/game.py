import src.board as board
from src.moveLib import MoveLib
from src.gamestate import GameState
from src.gui import Gui
import random
import numpy as np


def init_board(red_pawns, red_knights,blue_pawns, blue_knights):
    board.blue_p = blue_pawns
    board.blue_k = blue_knights
    board.blue = blue_pawns | blue_knights
    board.red_p = red_pawns
    board.red_k = red_knights
    board.red = red_pawns | red_knights
    board.l_blue_p=[]
    board.l_blue_k=[]
    board.l_red_p=[]
    board.l_red_k=[]


    for bit_board, figure_list in zip((board.blue_p, board.blue_k, board.red_p, board.red_k),(board.l_blue_p,board.l_blue_k,board.l_red_p,board.l_red_k)):
        for bit in range(64):
            if bit_board & (np.uint64(1 << bit)):
                figure_list.append(np.uint64(1 << bit))


alpha_on_ground_row = np.uint64(0b0111111000000000000000000000000000000000000000000000000000000000)
beta_on_ground_row = np.uint64(0b0000000000000000000000000000000000000000000000000000000001111110)

def isOver():
	if board.blue & alpha_on_ground_row:
		# print_board(alpha)
		# print_board(alpha_on_ground_row)
		# print_board(alpha & alpha_on_ground_row)
		return "Blue Won"	# alpha won
	elif board.red & beta_on_ground_row:
		return "Red Won" # beta won
	return "c"	# continue

def red_random_move_execution(moves):
	fig = random.choice(moves)
	move = random.choice(fig[1])
	if fig[0] & board.red_k:
		board.red_k_move_execution(fig[0],move)
	else:
		board.red_p_move_execution(fig[0],move)
	return fig[0], move


def blue_random_move_execution(moves): #  (index, source,[dest,dest,dest])
	fig = random.choice(moves)
	move = random.choice(fig[1])
	if fig[0] & board.blue_k:
		board.blue_k_move_execution(fig[0],move)
	else:
		board.blue_p_move_execution(fig[0],move)
	return fig[0], move

def play(FEN_board=False, blue_turn=True):
	if FEN_board:
		init_board(GameState.createBitBoardFrom(Gui.fenToMatrix(FEN_board)))
	else:
		init_board(np.uint64(0b0111111001111110000000000000000000000000000000000000000000000000), np.uint64(0),np.uint64(0b0111111001111110), np.uint64(0))
	print_state("Startpos")

	#input()
	while isOver() == "c":
		if blue_turn:
			source, dest = blue_random_move_execution(board.blue_generation())
		else:
			source, dest = red_random_move_execution(board.red_generation())

		if blue_turn:
			print_state("blue")
		else:
			print_state("red")
		inp = input("Takeback? -> Enter 't': ")
		if inp=="t" and blue_turn:
			board.blue_takeback(*board.stack.pop())
			print_state("blue")
		elif inp=="t" and not blue_turn:
			board.red_takeback(*board.stack.pop())
			print_state("red")
		else :
			blue_turn = not blue_turn
		
	print(isOver())
	
def print_board(board:np.uint64):
	string = np.binary_repr(board,width=64)
	#str = 'X' + str[1:7]+'X'+str[8:56]+'X'+str[57:63]+'X'
	print('\n'.join(string[i:i+8] for i in range(0, len(string), 8)))
	print()

def board_to_string(board:np.uint64)->str:
	return np.binary_repr(board,width=64)


def print_state(Color=""):
	if Color:
		print(f"------------- {Color} Moves: -----------------------")
	else:
		print("-----------------------------------------------------");print()
	
	red_p,blue_p ,red_k ,blue_k = np.uint64(0),np.uint64(0),np.uint64(0),np.uint64(0)

	for p in board.l_blue_p: blue_p = blue_p ^ p
	for k in board.l_blue_k: blue_k = blue_k ^ k
	for p in board.l_red_p: red_p = red_p ^ p
	for k in board.l_red_k: red_k = red_k ^ k

	if blue_p==board.blue_p:
		if blue_k==board.blue_k:
			if blue_p | blue_k!=board.blue:
				print("blue")
				print_board(blue_p | blue_k)
				print("board.blue")
				print_board(board.blue)
				raise Exception("blue != board.blue")

		else:
			print("blue_k")
			print_board(board.blue_k)
			print("l_blue_k")
			print_board(blue_k)
			raise Exception("blues knights != l_blues_knights")
	else:
		print("blue_p")
		print_board(board.blue_p)
		print("l_blue_p")
		print_board(blue_p)
		raise Exception("blues pawns != l_blues_pawns")
	


	if red_p==board.red_p: 
		if red_k==board.red_k:
			if blue_p | blue_k!=board.blue:
				print("red")
				print_board(red_p | red_k)
				print("board.red")
				print_board(board.blue)
				raise Exception("red != board.red")		
		else:
			print("red_k")
			print_board(board.red_k)
			print("l_red_k")
			print_board(red_k)
			raise Exception("red knights != l_red_knights")
	else:
		print("red_p")
		print_board(board.red_p)
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
	print()


		

	

	
		
def moves_to_string(moves):
	return [MoveLib.move(source,dest,mode=3) for source,dests in moves for dest in dests]
	
	

if __name__ == "__main__":
	#init_board(board.blue_p, board.blue_k, board.red_p, board.red_k)
	#print_state()
	while(True):
		play()
		
	#print(moves_to_string(board.red_generation()))