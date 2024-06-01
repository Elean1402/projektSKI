import numpy as np
from src.game import print_state

"""
for import use:
from board import blue_generation, blue_move_execution, blue_takeback, red_generation, red_move_execution, red_takeback

l_ --> List
_p --> pawn
_k --> knight
blue --> start player
red --> second player
"""
# Game Repr
stack = []

# Board Repr
# Blue
blue_p, blue_k = np.uint64(0b0111111001111110), np.uint64(0) 
blue = blue_p | blue_k
l_blue_k, l_blue_p = [],[]

# Red pawns
red_p, red_k = np.uint64(0b0111111001111110000000000000000000000000000000000000000000000000), np.uint64(0) 
red = red_p | red_k
l_red_k, l_red_p = [],[]




# Blue Move Execution
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

def blue_p_move_generation(source:np.uint64) :  
	dests = []
	blocked_squares = ~(red | blue_k) # Pawns unmovable squares
	# forward
	if (source & blue_p_forward) << bpf & blocked_squares: dests.append(source << bpf) 
	# left
	if (source & blue_p_left) << bpl & blocked_squares: dests.append(source << bpl) 
	# hit left
	if (source & blue_p_hit_left) << bphl & red: dests.append(source << bphl) 
	# hit right
	if (source & blue_p_hit_right) << bphr & red: dests.append(source << bphr) 
	# right
	if (source & blue_p_right) >> bpr & blocked_squares: dests.append(source >> bpr) 
	return dests

def blue_k_move_generation(source:np.uint64): 
	dests = []
	# left
	if (source & blue_k_left) << bkl & ~blue_k: dests.append(source << bkl) 
	# forward_left
	if (source & blue_k_forward_left) << bkfl & ~blue_k: dests.append(source << bkfl) 
	# right
	if (source & blue_k_right) << bkr & ~blue_k: dests.append(source << bkr) 
	# forward_right
	if (source & blue_k_forward_right) << bkfr & ~blue_k: dests.append(source << bkfr) 
	return dests

def blue_p_move_execution(source:np.uint64, dest:np.uint64):
	global blue_p, blue_k, blue, red_p, red_k, red
	# print_board(dest)
	# print_board(red_k)
	# print_board(red_k & dest)

	# delete source Position 
	l_blue_p.remove(source)
	blue_p = blue_p ^ source

	# on red_k -> hit & knight
	if dest & red_k:
		# remove red knight
		
		red_k = red_k ^ dest
		l_red_k.remove(dest)

		# add blue knigth
		blue_k = blue_k | dest
		l_blue_k.append(dest)

		# new red
		red = red_p | red_k
		stack.append((source, dest, True))

	# on blue_p -> knight
	elif dest & blue_p:
		# add blue knight
		blue_k = blue_k | dest
		l_blue_k.append(dest)
		stack.append((source, dest))


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
		stack.append((source, dest, True))

	# simple move
	else: 
		# move blue pawn
		blue_p = blue_p | dest
		l_blue_p.append(dest)
		stack.append((source, dest))
	
	# new blue
	blue = blue_p | blue_k
	
def blue_k_move_execution(source:np.uint64, dest:np.uint64):
	global blue_p, blue_k, blue, red_p, red_k, red
	# delete source Position 
	blue_k = blue_k ^ source
	l_blue_k.remove(source)

	
	
	# on red_k -> hit & knight
	if dest & red_k:
		# remove red knight
		red_k = red_k ^ dest
		l_red_k.remove(dest)

		# add blue knight
		blue_k = blue_k | dest
		l_blue_k.append(dest)

		# new red
		red = red_p | red_k
		stack.append((source, dest, True))

	# on blue_p -> knight
	elif dest & blue_p:
		# add blue knight
		blue_k = blue_k ^ dest
		l_blue_k.append(dest)
		stack.append((source, dest))



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
		stack.append((source, dest, True))


	# simple move -> pawn
	else: 
		# add blue pawn
		blue_p = blue_p | dest
		l_blue_p.append(dest)
		stack.append((source, dest))
	
	# new blue
	blue = blue_p | blue_k
	
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

def blue_move_execution(source:np.uint64, dest:np.uint64):
	if source & blue_k:
		blue_k_move_execution(source, dest)
	else:
		blue_p_move_execution(source, dest)

def blue_takeback(source, dest, hit=False):
	global blue_p, blue_k, blue, red_p, red_k, red

	# hit (add red)
	if hit:
		if blue_k & dest:
			l_red_k.append(dest)
			red_k = red_k | dest
		else:
			l_red_p.append(dest)
			red_p = red_p | dest
		red = red_p | red_k

	# delete dest
	if blue_k & dest:
		del l_blue_k[-1]
		blue_k = blue_k ^ dest
	else:
		del l_blue_p[-1]
		blue_p = blue_p ^ dest

	# add source
	if (blue_p | red_p) & source:
		l_blue_k.append(source)
		blue_k = blue_k | source
	else:
		l_blue_p.append(source)
		blue_p = blue_p | source
	
		

	blue = blue_p | blue_k
	

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


def red_p_move_generation(source:np.uint64):	# after pre-validation wheather source can move (being below knight
	dests = []
	# Pawns unmovable squares
	blocked_squares = ~(blue | red_k)

	# forward
	if (source & red_p_forward) >> rpf & blocked_squares:
		dests.append(source >> rpf) 

	# left
	if (source & red_p_left) << rpl & blocked_squares:
		dests.append(source << rpl) 

	# right
	if (source & red_p_right) >> rpr & blocked_squares:
		dests.append(source >> rpr) 

	# hit left
	if (source & red_p_hit_left) >> rphl & blue:
		dests.append(source >> rphl) 

	# hit right
	if (source & blue_p_hit_right) >> rphr & blue:
		dests.append(source >> rphr) 
	
	return dests

def red_k_move_generation(source:np.uint64): # no pre-validation needed

	dests = []

	# left
	if (source & red_k_left) >> rkl & ~red_k:
		dests.append(source >> rkl) 

	# forward_left
	if (source & red_k_forward_left) >> rkfl & ~red_k:
		dests.append(source >> rkfl) 

	# right
	if (source & red_k_right) >> rkr & ~red_k:
		dests.append(source >> rkr) 

	# forward_left
	if (source & red_k_forward_right) >> rkfr & ~red_k:
		dests.append(source >> rkfr) 

	return dests

def red_p_move_execution(source:np.uint64, dest:np.uint64):
	global blue_p, blue_k, blue, red_p, red_k, red

	# delete source Position 
	l_red_p.remove(source)
	red_p = red_p ^ source



	# on blue_k -> hit & knight
	if dest & blue_k:
		# remove blue knight
		blue_k = blue_k ^ dest
		l_blue_k.remove(dest)

		# add red knight
		red_k = red_k | dest
		l_red_k.append(dest)
		
		# new blue
		blue = blue_p | blue_k
		stack.append((source, dest, True))

	
		
	# on red_p -> knight
	elif dest & red_p:
		# add blue knight
		red_k = red_k | dest
		l_red_k.append(dest)
		stack.append((source, dest))

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
		stack.append((source, dest, True))


	# simple move
	else: 
		red_p = red_p | dest
		l_red_p.append(dest)
		stack.append((source, dest))

	
	# new red
	red = red_p | red_k

def red_k_move_execution(source:np.uint64, dest:np.uint64):
	global blue_p, blue_k, blue, red_p, red_k, red
	# delete source Position 
	red_k = red_k ^ source
	l_red_k.remove(source)
	
	
	# on blue_k -> hit & knight
	if dest & blue_k:
		# remove blue knight
		blue_k = blue_k ^ dest
		l_blue_k.remove(dest)

		# add red knight
		red_k = red_k | dest
		l_red_k.append(dest)

		# new blue
		blue = blue_p | blue_k
		stack.append((source, dest, True))

	# on red_p -> knight
	elif dest & red_p:
		# add red knight
		red_k = red_k ^ dest
		l_red_k.append(dest)
		stack.append((source, dest))



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
		stack.append((source, dest, True))



	# simple move -> pawn
	else: 
		# add red pawn
		red_p = red_p | dest
		l_red_p.append(dest)
		stack.append((source, dest))

	
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

def red_move_execution(source:np.uint64, dest:np.uint64):
	if source & red_k:
		red_k_move_execution(source, dest)
	else:
		red_p_move_execution(source, dest)
		
def red_takeback(source, dest, hit=False):
	global blue_p, blue_k, blue, red_p, red_k, red

	# hit (add blue)
	if hit:
		if red_k & dest:
			l_blue_k.append(dest)
			blue_k = blue_k | dest
		else:
			l_blue_p.append(dest)
			blue_p = blue_p | dest
		blue = blue_p | blue_k

	# delete dest
	if red_k & dest:
		del l_red_k[-1]
		red_k = red_k ^ dest
	else:
		del l_red_p[-1]
		red_p = red_p ^ dest

	# add source
	if (blue_p | red_p) & source:
		l_red_k.append(source)
		red_k = red_k | source
	else:
		l_red_p.append(source)
		red_p = red_p | source


	red = red_p | red_k



def print_board(board:np.uint64):
	str = np.binary_repr(board,width=64)
	#str = 'X' + str[1:7]+'X'+str[8:56]+'X'+str[57:63]+'X'
	print('\n'.join(str[i:i+8] for i in range(0, len(str), 8)))
	print()