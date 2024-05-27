import src.board as board
from src.moveLib import MoveLib
from src.gamestate import GameState
from src.gui import Gui
import random
import numpy as np


def init_board(blue_pawns, blue_knights, red_pawns, red_knights):
    board.blue_p = blue_pawns
    board.blue_k = blue_knights
    board.blue = blue_pawns | blue_knights
    board.red_p = red_pawns
    board.red_k = red_knights
    board.red = red_pawns | red_knights

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

def play(FEN_board="6/2r0b0r03/3r0r03/8/8/8/8/6" , blue_turn=True):
	if FEN_board:
		init_board(*GameState.createBitBoardFrom(Gui.fenToMatrix(FEN_board), True))
	else:
		init_board(board.blue_p, board.blue_k, board.red_p, board.red_k)
	print_state("Startpos")
	moves = board.blue_generation()
	print(moves)

	input()
	while isOver() == "c":
		if blue_turn:
			source, dest = blue_random_move_execution(board.blue_generation())
		else:
			source, dest = red_random_move_execution(board.red_generation())

		if blue_turn:
			print_state("blue")
		else:
			print_state("red")
		inp = input()
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
	str = np.binary_repr(board,width=64)
	#str = 'X' + str[1:7]+'X'+str[8:56]+'X'+str[57:63]+'X'
	print('\n'.join(str[i:i+8] for i in range(0, len(str), 8)))
	print()

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


	print("red")
	print_board(board.red_p | board.red_k)
	print()
	print("blue")
	print_board(board.blue_p | board.blue_k)
	
def moves_to_string(moves):
	return [MoveLib.move(source,dest,mode=3) for source,dests in moves for dest in dests]
	
	

if __name__ == "__main__":
	#init_board(board.blue_p, board.blue_k, board.red_p, board.red_k)
	#print_state()
	play()
	#print(moves_to_string(board.red_generation()))