import numpy as np
import random
from src.moveLib import MoveLib
from src.gamestate import GameState
from src.gui import Gui
from src.benchmark import benchmark



######################################################################################################
# Initialisation
######################################################################################################

alpha_turn = True


# Alpha pawns
alpha_p = np.uint64(0b0111111001111110) #panws start position

# Alpha knights
alpha_k = np.uint64(0) #knights start position

# Alpha
alpha = alpha_p | alpha_k


# Beta pawns
beta_p = np.uint64(0b0111111001111110000000000000000000000000000000000000000000000000) #pawns start position

#Beta knights
beta_k = np.uint64(0) #knights start position

# Beta
beta = beta_p | beta_k

l_alpha_k, l_alpha_p, l_beta_k, l_beta_p = [],[],[],[]



def init_position(beta_pawns, beta_knights, alpha_pawns, alpha_knights):
	global alpha_p, alpha_k, alpha, beta_p, beta_k, beta, l_alpha_k, l_alpha_p, l_beta_k, l_beta_p,list_alpha_p,list_alpha_k,list_beta_p,list_beta_k
	l_alpha_k, l_alpha_p, l_beta_k, l_beta_p =  [],[],[],[]
	alpha_p = alpha_pawns
	alpha_k = alpha_knights
	alpha = alpha_p | alpha_k

	beta_p = beta_pawns
	beta_k = beta_knights
	beta = beta_p | beta_knights

	for board, figure_list in zip((alpha_p, alpha_k, beta_p, beta_k),(l_alpha_p,l_alpha_k,l_beta_p,l_beta_k)):
		for bit in range(64):
			if board & (np.uint64(1 << bit)):
				figure_list.append(np.uint64(1 << bit))
				



	#return alpha_p, l_alpha_p, alpha_k, l_alpha_k, alpha, beta_p, l_beta_p, beta_k,l_beta_k, beta

######################################################################################################
# Other
######################################################################################################


alpha_on_ground_row = np.uint64(0b0111111000000000000000000000000000000000000000000000000000000000)
beta_on_ground_row = np.uint64(0b0000000000000000000000000000000000000000000000000000000001111110)

def isOver():
	if alpha & alpha_on_ground_row:
		# print_board(alpha)
		# print_board(alpha_on_ground_row)
		# print_board(alpha & alpha_on_ground_row)
		return "Alpha Won"	# alpha won
	elif beta & beta_on_ground_row:
		return "Beta Won" # beta won
	return "c"	# continue

def moves_to_string(moves):
	return [MoveLib.move(source,dest,mode=3) for source,dests in moves for dest in dests]
	
def play(FEN_board=False):
	global alpha_turn
	if FEN_board:
		init_position(GameState.createBitBoardFrom(Gui.fenToMatrix(FEN_board)))
	else:
		init_position(beta_p, beta_k, alpha_p, alpha_k)
	game = []
	print_state("Startpos")
	input()
	while isOver() == "c":
		if alpha_turn:
			source, dest = alpha_random_move_execution(alpha_generation())
		else:
			source, dest = beta_random_move_execution(beta_generation())
		game.append(MoveLib.move(source,dest,mode=3))
		if alpha_turn:
			print_state("Alpha")
		else:
			print_state("Beta")
		alpha_turn = not alpha_turn
		input()
	print(isOver())

######################################################################################################
# ALPHA
######################################################################################################

# Alpha pawn move bitboards
alpha_p_forward = np.uint64(0b0000000001111110111111111111111111111111111111111111111111111111)
alpha_p_right = np.uint64(0b0000000011111110111111101111111011111110111111101111111011111100)
alpha_p_left = np.uint64(0b0000000001111111011111110111111101111111011111110111111100111111)

# Alpha pawn hit bitboards
alpha_p_hit_right = np.uint64(0b0000000011111100111111101111111011111110111111101111111011111110)
alpha_p_hit_left = np.uint64(0b0000000000111111011111110111111101111111011111110111111101111111)

# Alpha knights move/hit bitboards
alpha_k_forward_right = np.uint64(0b0000000000000000111111001111111011111110111111101111111011111110)
alpha_k_right = np.uint64(0b0000000011111000111111001111110011111100111111001111110011111100)
alpha_k_forward_left = np.uint64(0b0000000000000000001111110111111101111111011111110111111101111111)
alpha_k_left = np.uint64(0b0000000000011111001111110011111100111111001111110011111100111111)

# Shifts for moves
# Pawns
# Forward, left, right, hit left, hit right
apf, apl, apr, aphl, aphr = np.uint8(8), np.uint8(1), np.uint8(1), np.uint8(9), np.uint8(7)

#Knights
# left, forward left, right, forward right
akl, akfl, akr, akfr = np.uint8(10), np.uint8(17), np.uint8(6), np.uint8(15)



def alpha_p_move_generation(source:np.uint64): # after pre-validation wheather source can move (being below knight)
	dests = []

	# Pawns unmovable squares
	blocked_squares = ~(beta | alpha_k)

	# forward
	if (source & alpha_p_forward) << apf & blocked_squares:
		dests.append(source << apf) 

	# left
	if (source & alpha_p_left) << apl & blocked_squares:
		dests.append(source << apl) 
	
	# hit left
	if (source & alpha_p_hit_left) << aphl & beta:
		dests.append(source << aphl) 

	# hit right
	if (source & alpha_p_hit_right) << aphr & beta:
		dests.append(source << aphr) 

	# right
	if (source & alpha_p_right) >> apr & blocked_squares:
		dests.append(source >> apr) 
	
	return dests
	
def alpha_k_move_generation(source:np.uint64): # no pre-validation needed
	dests = []

	# left
	if (source & alpha_k_left) << akl & ~alpha_k:
		dests.append(source << akl) 

	# forward_left
	if (source & alpha_k_forward_left) << akfl & ~alpha_k:
		dests.append(source << akfl) 

	# right
	if (source & alpha_k_right) << akr & ~alpha_k:
		dests.append(source << akr) 

	# forward_right
	if (source & alpha_k_forward_right) << akfr & ~alpha_k:
		dests.append(source << akfr) 

	return dests

def alpha_p_move_execution(source:np.uint64, dest:np.uint64):
	global alpha_p, alpha_k, alpha, beta_p, beta_k, beta

	# delete source Position 
	alpha_p = alpha_p ^ source
	l_alpha_p.remove(source)
	
	# on alpha_p -> knight
	if dest & alpha_p:
		# add alpha knight
		alpha_k = alpha_k | dest
		l_alpha_k.append(dest)

	# on beta_p -> hit
	elif dest & beta_p:
		# remove beta pawn
		beta_p = beta_p ^ dest
		l_beta_p.remove(dest)

		# move alpha pawn
		alpha_p = alpha_p | dest
		l_alpha_p.append(dest)
		
		# new beta
		beta = beta_p | beta_k

	# on beta_k -> hit & knight
	elif dest & beta_k:
		# remove beta knight
		beta_k = beta_k ^ dest
		l_beta_k.remove(dest)

		# add alpha knigth
		alpha_k = alpha_k | dest
		l_alpha_k.append(dest)

		# new beta
		beta = beta_p | beta_k

	# simple move
	else: 
		# move alpha pawn
		alpha_p = alpha_p | dest
		l_alpha_p.append(dest)
	
	#new alpha
	alpha = alpha_p | alpha_k

def alpha_k_move_execution(source:np.uint64, dest:np.uint64):
	global alpha_p, alpha_k, alpha, beta_p, beta_k, beta
	# delete source Position 
	alpha_k = alpha_k ^ source
	l_alpha_k.remove(source)

	# on alpha_p -> knight
	if dest & alpha_p:
		# add alpha knight
		alpha_k = alpha_k ^ dest
		l_alpha_k.append(dest)
	
	# on beta_k -> hit & knight
	elif dest & beta_k:
		# remove beta knight
		beta_k = beta_k ^ dest
		l_beta_k.remove(dest)

		# add alpha knight
		alpha_k = alpha_k | dest
		l_alpha_k.append(dest)

		# new beta
		beta = beta_p | beta_k


	# on beta_p -> hit & pawn
	elif dest & beta_p:
		# remove beta pawn
		beta_p = beta_p ^ dest
		l_beta_p.remove(dest)
		
		# add alpha pawn
		alpha_p = alpha_p | dest
		l_alpha_p.append(dest)
		
		# new beta
		beta = beta_p | beta_k

	# simple move -> pawn
	else: 
		# add alpha pawn
		alpha_p = alpha_p | dest
		l_alpha_p.append(dest)
	
	# new alpha
	alpha = alpha_p | alpha_k

def alpha_generation():
	moves = []
	precon = ~(alpha_k | beta_k)
	for source in l_alpha_p:	
		if source & precon:   #pre-validation (pawn under knight)
			fig_moves = alpha_p_move_generation(source)
			if len(fig_moves):
				moves.append((source, fig_moves))
	
	for source in l_alpha_k:
		fig_moves = alpha_k_move_generation(source)
		if len(fig_moves):
			moves.append((source, fig_moves))
	return moves

def alpha_random_move_execution(moves): #  (index, source,[dest,dest,dest])
	fig = random.choice(moves)
	move = random.choice(fig[1])
	if fig[0] & alpha_k:
		alpha_k_move_execution(fig[0],move)
	else:
		alpha_p_move_execution(fig[0],move)
	return fig[0], move

def alpha_hits():
	return (alpha_k >> akl) | (alpha_k >> akfl) | (alpha_k >> akr) | (alpha_k >> akfr) | (alpha_p >> aphl) | (alpha_p >> aphr)


######################################################################################################
# BETA
######################################################################################################

# Beta pawn move bitboards
beta_p_forward = np.uint64(0b1111111111111111111111111111111111111111111111110111111000000000)
beta_p_left = np.uint64(0b0011111101111111011111110111111101111111011111110111111100000000)
beta_p_right = np.uint64(0b1111110011111110111111101111111011111110111111101111111000000000)

# Beta pawn hit bitboards
beta_p_hit_right = np.uint64(0b1111111111111110111111101111111011111110111111101111110000000000)
beta_p_hit_left = np.uint64(0b1111111101111111011111110111111101111111011111110011111100000000)

# Beta knights move/hit bitboards
beta_k_forward_right = np.uint64(0b1111111011111110111111101111111011111110111111000000000000000000)
beta_k_right = np.uint64(0b1111110011111100111111001111110011111100111111001111100000000000)
beta_k_forward_left = np.uint64(0b0111111101111111011111110111111101111111001111110000000000000000)
beta_k_left = np.uint64(0b0011111100111111001111110011111100111111001111110001111100000000)


# Shifts for moves

# Pawns
# Forward, left, right, hit left, hit right
bpf, bpl, bpr, bphl, bphr = np.uint8(8), np.uint8(1), np.uint8(1), np.uint8(7), np.uint8(9)

#Knights
# left, forward left, right, forward right
bkl, bkfl, bkr, bkfr = np.uint8(6), np.uint8(15), np.uint8(10), np.uint8(17)


def beta_p_move_generation(source:np.uint64):	# after pre-validation wheather source can move (being below knight
	dests = []
	# Pawns unmovable squares
	blocked_squares = ~(alpha | beta_k)

	# forward
	if (source & beta_p_forward) >> bpf & blocked_squares:
		dests.append(source >> bpf) 

	# left
	if (source & beta_p_left) << bpl & blocked_squares:
		dests.append(source << bpl) 

	# right
	if (source & beta_p_right) >> bpr & blocked_squares:
		dests.append(source >> bpr) 

	# hit left
	if (source & beta_p_hit_left) >> bphl & alpha:
		dests.append(source >> bphl) 

	# hit right
	if (source & alpha_p_hit_right) >> bphr & alpha:
		dests.append(source >> bphr) 
	
	return dests

def beta_k_move_generation(source:np.uint64): # no pre-validation needed

	dests = []

	# left
	if (source & beta_k_left) >> bkl & ~beta_k:
		dests.append(source >> bkl) 

	# forward_left
	if (source & beta_k_forward_left) >> bkfl & ~beta_k:
		dests.append(source >> bkfl) 

	# right
	if (source & beta_k_right) >> bkr & ~beta_k:
		dests.append(source >> bkr) 

	# forward_left
	if (source & beta_k_forward_right) >> bkfr & ~beta_k:
		dests.append(source >> bkfr) 

	return dests

def beta_p_move_execution(source:np.uint64, dest:np.uint64):
	global alpha_p, alpha_k, alpha, beta_p, beta_k, beta

	# delete source Position 
	beta_p = beta_p ^ source
	l_beta_p.remove(source)
	
	# on beta_p -> knight
	if dest & beta_p:
		# add alpha knight
		beta_k = beta_k | dest
		l_beta_k.append(dest)

	# on alpha_p -> hit
	elif dest & alpha_p:
		# remove alpha pawn
		alpha_p = alpha_p ^ dest
		l_alpha_p.remove(dest)

		# move beta pawn 
		beta_p = beta_p | dest
		l_beta_p.append(dest)

		# new alpha
		alpha = alpha_p | alpha_k
	
	# on alpha_k -> hit & knight
	elif dest & alpha_k:
		# remove alpha knight
		alpha_k = alpha_k ^ dest
		l_alpha_k.remove(dest)

		# add beta knight
		beta_k = beta_k | dest
		l_beta_k.append(dest)
		
		# new alpha
		alpha = alpha_p | alpha_k

	# simple move
	else: 
		beta_p = beta_p | dest
		l_beta_p.append(dest)
	
	# new beta
	beta = beta_p | beta_k

def beta_k_move_execution(source:np.uint64, dest:np.uint64):
	global alpha_p, alpha_k, alpha, beta_p, beta_k, beta
	# delete source Position 
	beta_k = beta_k ^ source
	l_beta_k.remove(source)
	
	# on beta_p -> knight
	if dest & beta_p:
		# add beta knight
		beta_k = beta_k ^ dest
		l_beta_k.append(dest)
	
	# on alpha_k -> hit & knight
	elif dest & alpha_k:
		# remove alpha knight
		alpha_k = alpha_k ^ dest
		l_alpha_k.remove(dest)

		# add beta knight
		beta_k = beta_k | dest
		l_beta_k.append(dest)

		# new alpha
		alpha = alpha_p | alpha_k


	# on alpha_p -> hit & pawn
	elif dest & alpha_p:
		# remove alpha pawn
		alpha_p = alpha_p ^ dest
		l_alpha_p.remove(dest)
		
		# add beta pawn
		beta_p = beta_p | dest
		l_beta_p.append(dest)
		
		# new alpha
		alpha = alpha_p | alpha_k


	# simple move -> pawn
	else: 
		# add beta pawn
		beta_p = beta_p | dest
		l_beta_p.append(dest)
	
	# new beta
	beta = beta_p | beta_k

def beta_generation():
	moves = []
	precon = ~(alpha_k | beta_k)
	for source in l_beta_p:	
		if source & precon:   #pre-validation (pawn under knight)
			fig_moves = beta_p_move_generation(source)
			if len(fig_moves):
				moves.append((source, fig_moves))
	
	for source in l_beta_k:
		fig_moves = beta_k_move_generation(source)
		if len(fig_moves):
			moves.append((source, fig_moves))
	return moves

def beta_random_move_execution(moves):
	fig = random.choice(moves)
	move = random.choice(fig[1])
	if fig[0] & beta_k:
		beta_k_move_execution(fig[0],move)
	else:
		beta_p_move_execution(fig[0],move)
	return fig[0], move
	
def beta_move_execution(source:np.uint64, dest:np.uint64): # not used
	global alpha, beta
	if dest not in [tup[2] for tup in beta_p_move_generation(source)+beta_k_move_generation(source)]:
		print("invalid move")
	if source & beta_k:
		#if source beta_k_move_generation
		# delete source Position (bitboard)
		beta_k = beta_k ^ source
		
		# on beta_p -> knight
		if dest & beta_p:
			beta_k = beta_k & dest
			l_beta_k[l_beta_k.index(source)] = dest
		
		# on alpha_k -> hit & knight
		elif dest & alpha_k:
			alpha_k = alpha_k ^ dest
			beta_k = beta_k & dest
			l_alpha_k.remove(dest)
			l_beta_k[l_beta_k.index(source)] = dest
			alpha = alpha_p & alpha_k


		# on alpha_p -> hit & pawn
		elif dest & alpha_p:
			alpha_p = alpha_p ^ dest
			beta_p = beta_p & dest
			l_alpha_p.remove(dest)
			l_beta_k.remove(source)
			l_beta_p.append(dest)
			alpha = alpha_p & alpha_k


		# simple move -> pawn
		else: 
			beta_p = beta_p & dest
			l_beta_k.remove(source)
			l_beta_p.append(dest)
		
		beta = beta_p & beta_k
	elif source & beta_p:
		# delete source Position (bitboard)
		beta_p = beta_p ^ source
		
		# on beta_p -> knight
		if dest & beta_p:
			beta_k = beta_k & dest
			l_beta_p.remove(source)
			l_beta_k.append(dest)
		
		# on alpha_k -> hit & knight
		elif dest & beta_k:
			alpha_k = alpha_k ^ dest
			beta_k = beta_k & dest
			l_alpha_k.remove(dest)
			l_beta_p.remove(source)
			l_beta_k.append(dest)
			alpha = alpha_p & alpha_k


		# on alpha_p -> hit 
		elif dest & beta_p:
			alpha_p = alpha_p ^ dest
			beta_p = beta_p & dest
			l_alpha_p.remove(dest)
			l_beta_p[l_beta_p.index(source)] = dest
			alpha = alpha_p & alpha_k


		# simple move
		else: 
			beta_p = beta_p & dest
			l_beta_p[l_beta_p.index(source)] = dest
		
		beta = beta_p & beta_k
	else:
		print("no figure on source position")

def beta_hits():
	return (beta_k >> bkl) | (beta_k >> bkfl) | (beta_k >> bkr) | (beta_k >> bkfr) | (beta_p >> bphl) | (beta_p >> bphr)

#########################################################################################################
# Tests
#########################################################################################################



def print_board(board:np.uint64):
	str = np.binary_repr(board,width=64)
	#str = 'X' + str[1:7]+'X'+str[8:56]+'X'+str[57:63]+'X'
	print('\n'.join(str[i:i+8] for i in range(0, len(str), 8)))
	print()

def print_bitboards():
	print("alpha_p");print_board(alpha_p)
	print("alpha_k");print_board(alpha_k)
	print("alpha");print_board(alpha)
	print("beta_p");print_board(beta_p)
	print("beta_k");print_board(beta_k)
	print("beta");print_board(beta)

def print_game():
	def split_string(string, chunk_size=8):
		temp =  [list(string[i:i+chunk_size]) for i in range(0, len(string), chunk_size)]

	red_pawns  = np.binary_repr(alpha_p,width=64)
	red_knights  = np.binary_repr(alpha_k,width=64)
	blue_pawns  = np.binary_repr(beta_p,width=64)
	blue_knights  = np.binary_repr(beta_k,width=64)


def print_state(Color=""):
	if Color:
		print(f"------------- {Color} Moves: -----------------------")
	else:
		print("-----------------------------------------------------");print()
	
	red_p,blue_p ,red_k ,blue_k = np.uint64(0),np.uint64(0),np.uint64(0),np.uint64(0)

	for p in l_alpha_p: red_p = red_p ^ p
	for k in l_alpha_k: red_k = red_k ^ k
	for p in l_beta_p: blue_p = blue_p ^ p
	for k in l_beta_k: blue_k = blue_k ^ k

	print("alpha")
	print_board(red_p | red_k)
	print()
	print("beta")
	print_board(blue_p | blue_k)

	#print(f"Number of alpha Pawns: {len(l_alpha_p)}");print_board(alpha_p)
	#print("l_alpha_p")
	#for p in l_alpha_p:print_board(p);print()

	#print(f"Number of alpha Knights: {len(l_alpha_k)}");print_board(alpha_k)
	#for k in l_alpha_k:print_board(k);print()

	#print(f"Number of beta Pawns: {len(l_beta_p)}");print_board(beta_p)
	#print("l_beta_p")
	#for p in l_beta_p:print_board(p);print()

	#print(f"Number of beta Knights {len(l_beta_k)}");print_board(beta_k)
	# for k in l_beta_k:print_board(k);print()



#beta_random_move_execution(beta_generation())
#alpha_random_move_execution(alpha_generation())
#print_state()
#init_position(beta_p, beta_k, alpha_p, alpha_k)
#print(moves_to_string(alpha_generation()))


# import time
if __name__ == "__main__":
	init_position(beta_p, beta_k, alpha_p, alpha_k)
	# print_bitboards()
	# for p in l_beta_p:
	# 	print_board(p)
	#play()
	#init_position(beta_p, beta_k, alpha_p, alpha_k)
	#benchmark(alpha_left)
	#benchmark(alpha_right)
	benchmark(alpha_generation)
	# benchmark(alpha_generation_list1)




	# start_time = time.time()
	# for _ in range(1000000):
	# 	l_alpha_p = l_alpha_p << apf
	# vectorized_time = time.time() - start_time



	# start_time = time.time()
	# for _ in range(1000000):
	# 	for i,v in enumerate(l_alpha_p):
	# 		l_alpha_p[i] = v << apf
	# iterative_time = time.time() - start_time

	# print("Vectorized operation time:", vectorized_time)
	# print("Iterative operation time:", iterative_time)
