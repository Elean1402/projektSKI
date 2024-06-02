import numpy as np
import random
from moveLib import MoveLib
from gamestate import GameState
from gui import Gui
from benchmark import benchmark



######################################################################################################
# Initialisation
######################################################################################################

blue_turn = True


# blue pawns
blue_p = np.uint64(0b0111111001111110) #panws start position

# blue knights
blue_k = np.uint64(0) #knights start position

# blue
blue = blue_p | blue_k


# red pawns
red_p = np.uint64(0b0111111001111110000000000000000000000000000000000000000000000000) #pawns start position

#red knights
red_k = np.uint64(0) #knights start position

# red
red = red_p | red_k

l_blue_k, l_blue_p, l_red_k, l_red_p = [],[],[],[]



def init_position(red_pawns, red_knights, blue_pawns, blue_knights):
	global blue_p, blue_k, blue, red_p, red_k, red, l_blue_k, l_blue_p, l_red_k, l_red_p,list_blue_p,list_blue_k,list_red_p,list_red_k
	l_blue_k, l_blue_p, l_red_k, l_red_p =  [],[],[],[]
	blue_p = blue_pawns
	blue_k = blue_knights
	blue = blue_p | blue_k

	red_p = red_pawns
	red_k = red_knights
	red = red_p | red_knights

	for board, figure_list in zip((blue_p, blue_k, red_p, red_k),(l_blue_p,l_blue_k,l_red_p,l_red_k)):
		for bit in range(64):
			if board & (np.uint64(1 << bit)):
				figure_list.append(np.uint64(1 << bit))
				



	#return blue_p, l_blue_p, blue_k, l_blue_k, blue, red_p, l_red_p, red_k,l_red_k, red

######################################################################################################
# Other
######################################################################################################

# Rows
R1 = np.uint64(0b0000000000000000000000000000000000000000000000000000000011111111)
R2 = np.uint64(0b0000000000000000000000000000000000000000000000001111111100000000)
R3 = np.uint64(0b0000000000000000000000000000000000000000111111110000000000000000)
R4 = np.uint64(0b0000000000000000000000000000000011111111000000000000000000000000)
R5 = np.uint64(0b0000000000000000000000001111111100000000000000000000000000000000)
R6 = np.uint64(0b0000000000000000111111110000000000000000000000000000000000000000)
R7 = np.uint64(0b0000000011111111000000000000000000000000000000000000000000000000)
R8 = np.uint64(0b1111111100000000000000000000000000000000000000000000000000000000)
def rating(player = 1):
	rating = 0
	for p in l_blue_p:
		if p & R1: rating +=1
		elif p & R2: rating +=2
		elif p & R3: rating +=3
		elif p & R4: rating +=4
		elif p & R5: rating +=5
		elif p & R6: rating +=6
		elif p & R7: rating +=7
		elif p & R8: rating +=10000

	for p in l_red_p:
		if p & R1: rating -=10000
		elif p & R2: rating -=7
		elif p & R3: rating -=6
		elif p & R4: rating -=5
		elif p & R5: rating -=4
		elif p & R6: rating -=3
		elif p & R7: rating -=2
		elif p & R8: rating -=1

	for k in l_blue_k:
		if k & R1: rating +=1
		elif k & R2: rating +=2
		elif k & R3: rating +=3
		elif k & R4: rating +=4
		elif k & R5: rating +=5
		elif k & R6: rating +=6
		elif k & R7: rating +=7
		elif k & R8: rating +=10000

	for k in l_red_k:
		if k & R1: rating -=10000
		elif k & R2: rating -=7
		elif k & R3: rating -=6
		elif k & R4: rating -=5
		elif k & R5: rating -=4
		elif k & R6: rating -=3
		elif k & R7: rating -=2
		elif k & R8: rating -=1

	return rating


blue_on_ground_row = np.uint64(0b0111111000000000000000000000000000000000000000000000000000000000)
red_on_ground_row = np.uint64(0b0000000000000000000000000000000000000000000000000000000001111110)

def isOver():
	if blue & blue_on_ground_row:
		# print_board(blue)
		# print_board(blue_on_ground_row)
		# print_board(blue & blue_on_ground_row)
		return "blue Won"	# blue won
	elif red & red_on_ground_row:
		return "red Won" # red won
	return "c"	# continue

def moves_to_string(moves):
	return [MoveLib.move(source,dest,mode=3) for source,dests in moves for dest in dests]
	
def play(FEN_board=False):
	global blue_turn
	if FEN_board:
		init_position(GameState.createBitBoardFrom(Gui.fenToMatrix(FEN_board)))
	else:
		init_position(red_p, red_k, blue_p, blue_k)
	game = []
	print_state("Startpos")
	input()
	while isOver() == "c":
		if blue_turn:
			source, dest = blue_random_move_execution(blue_generation())
		else:
			source, dest = red_random_move_execution(red_generation())
		game.append(MoveLib.move(source,dest,mode=3))
		if blue_turn:
			print_state("blue")
		else:
			print_state("red")
		blue_turn = not blue_turn
		input()
	print(isOver())

######################################################################################################
# blue
######################################################################################################

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
apf, apl, apr, aphl, aphr = np.uint8(8), np.uint8(1), np.uint8(1), np.uint8(9), np.uint8(7)

#Knights
# left, forward left, right, forward right
akl, akfl, akr, akfr = np.uint8(10), np.uint8(17), np.uint8(6), np.uint8(15)



def blue_p_move_generation(source:np.uint64): # after pre-validation wheather source can move (being below knight)
	dests = []

	# Pawns unmovable squares
	blocked_squares = ~(red | blue_k)

	# forward
	if (source & blue_p_forward) << apf & blocked_squares:
		dests.append(source << apf) 

	# left
	if (source & blue_p_left) << apl & blocked_squares:
		dests.append(source << apl) 
	
	# hit left
	if (source & blue_p_hit_left) << aphl & red:
		dests.append(source << aphl) 

	# hit right
	if (source & blue_p_hit_right) << aphr & red:
		dests.append(source << aphr) 

	# right
	if (source & blue_p_right) >> apr & blocked_squares:
		dests.append(source >> apr) 
	
	return dests
	
def blue_k_move_generation(source:np.uint64): # no pre-validation needed
	dests = []

	# left
	if (source & blue_k_left) << akl & ~blue_k:
		dests.append(source << akl) 

	# forward_left
	if (source & blue_k_forward_left) << akfl & ~blue_k:
		dests.append(source << akfl) 

	# right
	if (source & blue_k_right) << akr & ~blue_k:
		dests.append(source << akr) 

	# forward_right
	if (source & blue_k_forward_right) << akfr & ~blue_k:
		dests.append(source << akfr) 

	return dests

def blue_p_move_execution(source:np.uint64, dest:np.uint64):
	global blue_p, blue_k, blue, red_p, red_k, red

	# delete source Position 
	blue_p = blue_p ^ source
	l_blue_p.remove(source)
	
	# on blue_p -> knight
	if dest & blue_p:
		# add blue knight
		blue_k = blue_k | dest
		l_blue_k.append(dest)

	# on red_p -> hit
	elif dest & red_p:
		# remove red pawn
		red_p = red_p ^ dest
		l_red_p.remove(dest)

		# move blue pawn
		blue_p = blue_p | dest
		l_blue_p.append(dest)
		
		# new red
		red = red_p | red_k

	# on red_k -> hit & knight
	elif dest & red_k:
		# remove red knight
		red_k = red_k ^ dest
		l_red_k.remove(dest)

		# add blue knigth
		blue_k = blue_k | dest
		l_blue_k.append(dest)

		# new red
		red = red_p | red_k

	# simple move
	else: 
		# move blue pawn
		blue_p = blue_p | dest
		l_blue_p.append(dest)
	
	#new blue
	blue = blue_p | blue_k

def blue_k_move_execution(source:np.uint64, dest:np.uint64):
	global blue_p, blue_k, blue, red_p, red_k, red
	# delete source Position 
	blue_k = blue_k ^ source
	l_blue_k.remove(source)

	# on blue_p -> knight
	if dest & blue_p:
		# add blue knight
		blue_k = blue_k ^ dest
		l_blue_k.append(dest)
	
	# on red_k -> hit & knight
	elif dest & red_k:
		# remove red knight
		red_k = red_k ^ dest
		l_red_k.remove(dest)

		# add blue knight
		blue_k = blue_k | dest
		l_blue_k.append(dest)

		# new red
		red = red_p | red_k


	# on red_p -> hit & pawn
	elif dest & red_p:
		# remove red pawn
		red_p = red_p ^ dest
		l_red_p.remove(dest)
		
		# add blue pawn
		blue_p = blue_p | dest
		l_blue_p.append(dest)
		
		# new red
		red = red_p | red_k

	# simple move -> pawn
	else: 
		# add blue pawn
		blue_p = blue_p | dest
		l_blue_p.append(dest)
	
	# new blue
	blue = blue_p | blue_k



def blue_random_move_execution(moves): #  (index, source,[dest,dest,dest])
	fig = random.choice(moves)
	move = random.choice(fig[1])
	if fig[0] & blue_k:
		blue_k_move_execution(fig[0],move)
	else:
		blue_p_move_execution(fig[0],move)
	return fig[0], move

def blue_hits():
	return (blue_k >> akl) | (blue_k >> akfl) | (blue_k >> akr) | (blue_k >> akfr) | (blue_p >> aphl) | (blue_p >> aphr)

def blue_generation():
	moves = []
	precon = ~(blue_k | red_k)
	for source in l_blue_p:	
		if source & precon:   #pre-validation (pawn under knight)
			fig_moves = blue_p_move_generation(source)
			if len(fig_moves):
				moves.append((source, fig_moves))
	
	for source in l_blue_k:
		fig_moves = blue_k_move_generation(source)
		if len(fig_moves):
			moves.append((source, fig_moves))
	return moves

######################################################################################################
# red
######################################################################################################

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
bpf, bpl, bpr, bphl, bphr = np.uint8(8), np.uint8(1), np.uint8(1), np.uint8(7), np.uint8(9)

#Knights
# left, forward left, right, forward right
bkl, bkfl, bkr, bkfr = np.uint8(6), np.uint8(15), np.uint8(10), np.uint8(17)


def red_p_move_generation(source:np.uint64):	# after pre-validation wheather source can move (being below knight
	dests = []
	# Pawns unmovable squares
	blocked_squares = ~(blue | red_k)

	# forward
	if (source & red_p_forward) >> bpf & blocked_squares:
		dests.append(source >> bpf) 

	# left
	if (source & red_p_left) << bpl & blocked_squares:
		dests.append(source << bpl) 

	# right
	if (source & red_p_right) >> bpr & blocked_squares:
		dests.append(source >> bpr) 

	# hit left
	if (source & red_p_hit_left) >> bphl & blue:
		dests.append(source >> bphl) 

	# hit right
	if (source & blue_p_hit_right) >> bphr & blue:
		dests.append(source >> bphr) 
	
	return dests

def red_k_move_generation(source:np.uint64): # no pre-validation needed

	dests = []

	# left
	if (source & red_k_left) >> bkl & ~red_k:
		dests.append(source >> bkl) 

	# forward_left
	if (source & red_k_forward_left) >> bkfl & ~red_k:
		dests.append(source >> bkfl) 

	# right
	if (source & red_k_right) >> bkr & ~red_k:
		dests.append(source >> bkr) 

	# forward_left
	if (source & red_k_forward_right) >> bkfr & ~red_k:
		dests.append(source >> bkfr) 

	return dests

def red_p_move_execution(source:np.uint64, dest:np.uint64):
	global blue_p, blue_k, blue, red_p, red_k, red

	# delete source Position 
	red_p = red_p ^ source
	l_red_p.remove(source)
	
	# on red_p -> knight
	if dest & red_p:
		# add blue knight
		red_k = red_k | dest
		l_red_k.append(dest)

	# on blue_p -> hit
	elif dest & blue_p:
		# remove blue pawn
		blue_p = blue_p ^ dest
		l_blue_p.remove(dest)

		# move red pawn 
		red_p = red_p | dest
		l_red_p.append(dest)

		# new blue
		blue = blue_p | blue_k
	
	# on blue_k -> hit & knight
	elif dest & blue_k:
		# remove blue knight
		blue_k = blue_k ^ dest
		l_blue_k.remove(dest)

		# add red knight
		red_k = red_k | dest
		l_red_k.append(dest)
		
		# new blue
		blue = blue_p | blue_k

	# simple move
	else: 
		red_p = red_p | dest
		l_red_p.append(dest)
	
	# new red
	red = red_p | red_k

def red_k_move_execution(source:np.uint64, dest:np.uint64):
	global blue_p, blue_k, blue, red_p, red_k, red
	# delete source Position 
	red_k = red_k ^ source
	l_red_k.remove(source)
	
	# on red_p -> knight
	if dest & red_p:
		# add red knight
		red_k = red_k ^ dest
		l_red_k.append(dest)
	
	# on blue_k -> hit & knight
	elif dest & blue_k:
		# remove blue knight
		blue_k = blue_k ^ dest
		l_blue_k.remove(dest)

		# add red knight
		red_k = red_k | dest
		l_red_k.append(dest)

		# new blue
		blue = blue_p | blue_k


	# on blue_p -> hit & pawn
	elif dest & blue_p:
		# remove blue pawn
		blue_p = blue_p ^ dest
		l_blue_p.remove(dest)
		
		# add red pawn
		red_p = red_p | dest
		l_red_p.append(dest)
		
		# new blue
		blue = blue_p | blue_k


	# simple move -> pawn
	else: 
		# add red pawn
		red_p = red_p | dest
		l_red_p.append(dest)
	
	# new red
	red = red_p | red_k

def red_generation():
	moves = []
	precon = ~(blue_k | red_k)
	for source in l_red_p:	
		if source & precon:   #pre-validation (pawn under knight)
			fig_moves = red_p_move_generation(source)
			if len(fig_moves):
				moves.append((source, fig_moves))
	
	for source in l_red_k:
		fig_moves = red_k_move_generation(source)
		if len(fig_moves):
			moves.append((source, fig_moves))
	return moves

def red_random_move_execution(moves):
	fig = random.choice(moves)
	move = random.choice(fig[1])
	if fig[0] & red_k:
		red_k_move_execution(fig[0],move)
	else:
		red_p_move_execution(fig[0],move)
	return fig[0], move
	
def red_hits():
	return (red_k >> bkl) | (red_k >> bkfl) | (red_k >> bkr) | (red_k >> bkfr) | (red_p >> bphl) | (red_p >> bphr)

#########################################################################################################
# Tests
#########################################################################################################



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

	for p in l_blue_p: red_p = red_p ^ p
	for k in l_blue_k: red_k = red_k ^ k
	for p in l_red_p: blue_p = blue_p ^ p
	for k in l_red_k: blue_k = blue_k ^ k

	print("blue")
	print_board(red_p | red_k)
	print()
	print("red")
	print_board(blue_p | blue_k)

	#print(f"Number of blue Pawns: {len(l_blue_p)}");print_board(blue_p)
	#print("l_blue_p")
	#for p in l_blue_p:print_board(p);print()

	#print(f"Number of blue Knights: {len(l_blue_k)}");print_board(blue_k)
	#for k in l_blue_k:print_board(k);print()

	#print(f"Number of red Pawns: {len(l_red_p)}");print_board(red_p)
	#print("l_red_p")
	#for p in l_red_p:print_board(p);print()

	#print(f"Number of red Knights {len(l_red_k)}");print_board(red_k)
	# for k in l_red_k:print_board(k);print()



#red_random_move_execution(red_generation())
#blue_random_move_execution(blue_generation())
#print_state()
#init_position(red_p, red_k, blue_p, blue_k)
#print(moves_to_string(blue_generation()))


# import time
if __name__ == "__main__":
	#init_position(red_p, red_k, blue_p, blue_k)
	# print_bitboards()
	# for p in l_red_p:
	# 	print_board(p)
	play()
	#init_position(red_p, red_k, blue_p, blue_k)
	#benchmark(blue_left)
	#benchmark(blue_right)
	#benchmark(blue_generation)
	# benchmark(blue_generation_list1)




	# start_time = time.time()
	# for _ in range(1000000):
	# 	l_blue_p = l_blue_p << apf
	# vectorized_time = time.time() - start_time



	# start_time = time.time()
	# for _ in range(1000000):
	# 	for i,v in enumerate(l_blue_p):
	# 		l_blue_p[i] = v << apf
	# iterative_time = time.time() - start_time

	# print("Vectorized operation time:", vectorized_time)
	# print("Iterative operation time:", iterative_time)
