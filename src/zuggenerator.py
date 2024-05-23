import numpy as np
import random
from src.moveLib import MoveLib




######################################################################################################
# Initialisation
######################################################################################################



# Alpha pawns
alpha_p = np.uint64(0b0111111001111110) #panws start position
l_alpha_p = []

# Alpha knights
alpha_k =np.uint64(0) #knights start position
l_alpha_k = []

# Alpha
alpha = alpha_p | alpha_k


# Beta pawns
beta_p = np.uint64(0b0111111001111110000000000000000000000000000000000000000000000000) #pawns start position
l_beta_p = []

#Beta knights
beta_k =np.uint64(0) #knights start position
l_beta_k = []

# Beta
beta = beta_p | beta_k


def init_position(beta_pawns, beta_knights, alpha_pawns, alpha_knights):
	global alpha_p, alpha_k, alpha, beta_p, beta_k, beta
	alpha_p = alpha_pawns
	alpha_k = alpha_knights
	alpha = alpha_p | alpha_k

	beta_p = beta_pawns
	beta_k = beta_knights
	beta = beta_p | beta_knights

	def extract_figs():
		for board, figure_list in zip((alpha_p, alpha_k, beta_p, beta_k),(l_alpha_p,l_alpha_k,l_beta_p,l_beta_k)):
			# Create an array to store the new uint8 values
			# Iterate over each bit position in the uint8 value
			for bit in range(64):
				if board & (np.uint64(1 << bit)):
					figure_list.append(np.uint64(1 << bit))
					


	
	extract_figs()

	return alpha_p, l_alpha_p, alpha_k, l_alpha_k, alpha, beta_p, l_beta_p, beta_k,l_beta_k, beta

######################################################################################################
# Other
######################################################################################################


alpha_on_ground_row = np.uint64(0b0111111000000000000000000000000000000000000000000000000000000000)
beta_on_ground_row = np.uint64(0b0000000000000000000000000000000000000000000000000000000001111110)

def isOver():
	if alpha & alpha_on_ground_row:
		return "rw"	# alpha won
	elif beta & beta_on_ground_row:
		return "bw" # beta won
	return "continue"



def moves_to_string(moves):
	return [MoveLib.move(source,dest,mode=3) for index,source,dests in moves for dest in dests]

	

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
ampf, ampl, ampr, amphl, amphr = np.uint8(8), np.uint8(1), np.uint8(1), np.uint8(9), np.uint8(7)

#Knights
# left, forward left, right, forward right
amkl, amkfl, amkr, amkfr = np.uint8(10), np.uint8(17), np.uint8(6), np.uint8(15)

def alpha_p_move_generation(source:np.uint64): # after pre-validation wheather source can move (being below knight)
	dests = []
    # Pwans
	# Movable Pawns (not under a knight)
	# p_movable = alpha_p & ~(alpha_k & beta_k) this in pre validation

	# Pawns unmovable squares
	blocked_p_squares = beta | alpha_k

	# forward
	if (source & alpha_p_forward) << ampf & ~blocked_p_squares:
		dests.append(source << ampf) 

	# left
	if (source & alpha_p_left) << ampl & ~blocked_p_squares:
		dests.append(source << ampl) 

	# right
	if (source & alpha_p_right) >> ampr & ~blocked_p_squares:
		dests.append(source >> ampr) 

	# hit left
	if (source & alpha_p_hit_left) << amphl & beta:
		dests.append(source << amphl) 

	# hit right
	if (source & alpha_p_hit_right) << amphr & beta:
		dests.append(source << amphr) 
	
	return dests
	
def alpha_k_move_generation(source:np.uint64): # no pre-validation needed
	dests = []

	# left
	if (source & alpha_k_left) << amkl & ~alpha_k:
		dests.append(source << amkl) 

	# forward_left
	if (source & alpha_k_forward_left) << amkfl & ~alpha_k:
		dests.append(source << amkfl) 

	# right
	if (source & alpha_k_right) << amkr& ~alpha_k:
		dests.append(source << amkr) 

	# forward_right
	if (source & alpha_k_forward_right) << amkfr & ~alpha_k:
		dests.append(source << amkfr) 

	return dests

def alpha_p_move_execution(index, source:np.uint64, dest:np.uint64):
	global alpha_p, alpha_k, alpha, beta_p, beta_k, beta

	# delete source Position (bitboard)
	alpha_p = alpha_p ^ source
	
	# on alpha_p -> knight
	if dest & alpha_p:
		alpha_k = alpha_k ^ dest
		del l_alpha_p[index]
		l_alpha_k.append(dest)
	
	# on beta_k -> hit & knight
	elif dest & beta_k:
		beta_k = beta_k ^ dest
		alpha_k = alpha_k ^ dest
		l_beta_k.remove(dest)
		del l_alpha_p[index]
		l_alpha_k.append(dest)
		beta = beta_p ^ beta_k


	# on beta_p -> hit
	elif dest & beta_p:
		beta_p = beta_p ^ dest
		alpha_p = alpha_p ^ dest
		l_beta_p.remove(dest)
		l_alpha_p[index] = dest
		beta = beta_p ^ beta_k


	# simple move
	else: 
		alpha_p = alpha_p ^ dest
		l_alpha_p[index] = dest
	
	alpha = alpha_p ^ alpha_k

def alpha_k_move_execution(index, source:np.uint64, dest:np.uint64):
	global alpha_p, alpha_k, alpha, beta_p, beta_k, beta
	# delete source Position (bitboard)
	alpha_k = alpha_k ^ source
	
	# on alpha_p -> knight
	if dest & alpha_p:
		alpha_k = alpha_k ^ dest
		l_alpha_k[index] = dest
	
	# on beta_k -> hit & knight
	elif dest & beta_k:
		beta_k = beta_k ^ dest
		alpha_k = alpha_k ^ dest
		l_beta_k.remove(dest)
		l_alpha_k[index] = dest
		beta = beta_p ^ beta_k


	# on beta_p -> hit & pawn
	elif dest & beta_p:
		beta_p = beta_p ^ dest
		alpha_p = alpha_p ^ dest
		l_beta_p.remove(dest)
		del l_alpha_k[index] 
		l_alpha_p.append(dest)
		beta = beta_p ^ beta_k


	# simple move -> pawn
	else: 
		alpha_p = alpha_p ^ dest
		del l_alpha_k[index]
		l_alpha_p.append(dest)
	
	alpha = alpha_p ^ alpha_k

def alpha_generation():
	moves = []
	knights =  alpha_k & beta_k
	for index,source in enumerate(filter(lambda x: x & ~knights, l_alpha_p)):	#pre-validation (pawn under knight)
		moves.append((index, source, alpha_p_move_generation(source)))
	
	for index,source in enumerate(l_alpha_k):
		moves.append((index, source, alpha_k_move_generation(source)))
	return moves

def alpha_random_move_execution(moves):
	fig = random.choice(moves)
	move = random.choice(fig[2])
	if fig[1] & alpha_k:
		alpha_k_move_execution(fig[0],fig[1],move)
	else:
		alpha_p_move_execution(fig[0],fig[1],move)




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
bmpf, bmpl, bmpr, bmphl, bmphr = np.uint8(8), np.uint8(1), np.uint8(1), np.uint8(7), np.uint8(9)

#Knights
# left, forward left, right, forward right
bmkl, bmkfl, bmkr, bmkfr = np.uint8(6), np.uint8(15), np.uint8(10), np.uint8(17)


def beta_p_move_generation(source:np.uint64):	# after pre-validation wheather source can move (being below knight)
	dests = []
    # Pwans
	# Movable Pawns (not under a knight)
	#p_movable = beta_p & ~(alpha_k & beta_k)

	# Pawns unmovable squares
	blocked_p_squares = alpha | beta_k

	# forward
	if (source & beta_p_forward) >> bmpf & ~blocked_p_squares:
		dests.append(source >> bmpf) 

	# left
	if (source & beta_p_left) << bmpl & ~blocked_p_squares:
		dests.append(source << bmpl) 

	# right
	if (source & beta_p_right) >> bmpr & ~blocked_p_squares:
		dests.append(source >> bmpr) 

	# hit left
	if (source & beta_p_hit_left) >> bmphl & beta:
		dests.append(source >> bmphl) 

	# hit right
	if (source & alpha_p_hit_right) >> bmphr & beta:
		dests.append(source >> bmphr) 
	
	return dests

def beta_k_move_generation(source:np.uint64): # no pre-validation needed

	dests = []

	# left
	if (source & beta_k_left) >> bmkl & ~beta_k:
		dests.append(source >> bmkl) 

	# forward_left
	if (source & beta_k_forward_left) >> bmkfl & ~beta_k:
		dests.append(source >> bmkfl) 

	# right
	if (source & beta_k_right) >> bmkr & ~beta_k:
		dests.append(source >> bmkr) 

	# forward_left
	if (source & beta_k_forward_right) >> bmkfr & ~beta_k:
		dests.append(source >> bmkfr) 

	return dests

def beta_p_move_execution(index, source:np.uint64, dest:np.uint64):
	global alpha_p, alpha_k, alpha, beta_p, beta_k, beta


	# delete source Position (bitboard)
	beta_p = beta_p ^ source
	
	# on beta_p -> knight
	if dest & beta_p:
		beta_k = beta_k ^ dest
		del l_beta_p[index]
		l_beta_k.append(dest)
	
	# on alpha_k -> hit & knight
	elif dest & alpha_k:
		alpha_k = alpha_k ^ dest
		beta_k = beta_k ^ dest
		l_alpha_k.remove(dest)
		del l_beta_p[index]
		l_beta_k.append(dest)
		alpha = alpha_p ^ alpha_k


	# on alpha_p -> hit
	elif dest & alpha_p:
		alpha_p = alpha_p ^ dest
		beta_p = beta_p ^ dest
		l_alpha_p.remove(dest)
		l_beta_p[index] = dest
		alpha = alpha_p ^ alpha_k


	# simple move
	else: 
		beta_p = beta_p ^ dest
		l_beta_p[index] = dest
	
	beta = beta_p ^ beta_k

def beta_k_move_execution(index, source:np.uint64, dest:np.uint64):
	global alpha_p, alpha_k, alpha, beta_p, beta_k, beta

	# delete source Position (bitboard)
	beta_k = beta_k ^ source
	
	# on beta_p -> knight
	if dest & beta_p:
		beta_k = beta_k ^ dest
		l_beta_k[index] = dest
	
	# on alpha_k -> hit & knight
	elif dest & alpha_k:
		alpha_k = alpha_k ^ dest
		beta_k = beta_k ^ dest
		l_alpha_k.remove(dest)
		l_beta_k[index] = dest
		alpha = alpha_p ^ alpha_k


	# on alpha_p -> hit & pawn
	elif dest & alpha_p:
		alpha_p = alpha_p ^ dest
		beta_p = beta_p ^ dest
		l_alpha_p.remove(dest)
		del l_beta_k[index] 
		l_beta_p.append(dest)
		alpha = alpha_p ^ alpha_k


	# simple move -> pawn
	else: 
		beta_p = beta_p ^ dest
		del l_beta_k[index]
		l_beta_p.append(dest)
	
	beta = beta_p ^ beta_k

def beta_move_execution(source:np.uint64, dest:np.uint64): # not used
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

def beta_generation():
	moves = []
	knights =  alpha_k & beta_k
	for index,source in enumerate(filter(lambda x: x & ~knights, l_beta_p)):	#pre-validation (pawn under knight)
		moves.append((index, source, beta_p_move_generation(source)))
	
	for index,source in enumerate(l_beta_k):
		moves.append((index, source, beta_k_move_generation(source)))
	return moves

def beta_random_move_execution(moves):
	fig = random.choice(moves)
	move = random.choice(fig[2])
	if fig[1] & beta_k:
		beta_k_move_execution(fig[0],fig[1],move)
	else:
		beta_p_move_execution(fig[0],fig[1],move)





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

def print_state():
	print("Number of alpha Pawns");print(len(l_alpha_p));print();print("alpha_p");print_board(alpha_p);print()
	# for p in l_alpha_p:print_board(p);print()

	print("beta_p");print_board(beta_p);print();print("Number of beta Pawns");print(len(l_beta_p));print()
	# for p in l_beta_p:print_board(p);print()


	print("alpha_k");print_board(alpha_k);print();print("Number of alpha Knights");print(len(l_alpha_k));print()
	#for k in l_alpha_k:print_board(k);print()


	# print("beta_k");print_board(beta_k);print();print("Number of beta Knights");print(len(l_beta_k));print()
	# for k in l_beta_k:print_board(k);print()



#beta_random_move_execution(beta_generation())
#alpha_random_move_execution(alpha_generation())
#print_state()
#init_position(alpha_p, alpha_k, beta_p, beta_k)
#print(moves_to_string(alpha_generation()))