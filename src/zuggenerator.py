import numpy as np

# Red/Alpha pawns
alpha_p = np.uint64(0b0111111001111110) #panws start position
l_alpha_p = []

# Red/Alpha knights
alpha_k =np.uint64(0) #knights start position
l_alpha_k = []

# Alpha
alpha = alpha_p & alpha_k

# Red/Alpha pawns move
alpha_p_forward = np.uint64(0b0000000001111110111111111111111111111111111111111111111111111111)
alpha_p_right = np.uint64(0b0000000011111110111111101111111011111110111111101111111011111100)
alpha_p_left = np.uint64(0b0000000001111111011111110111111101111111011111110111111100111111)

# Red/Alpha pawns hit
alpha_p_hit_right = np.uint64(0b0000000011111100111111101111111011111110111111101111111011111110)
alpha_p_hit_left = np.uint64(0b0000000000111111011111110111111101111111011111110111111101111111)



# Red/Alpha knights move/hit
alpha_k_forward_right = np.uint64(0b0000000000000000111111001111111011111110111111101111111011111110)
alpha_k_right = np.uint64(0b0000000011111000111111001111110011111100111111001111110011111100)
alpha_k_forward_left = np.uint64(0b0000000000000000001111110111111101111111011111110111111101111111)
alpha_k_left = np.uint64(0b0000000000011111001111110011111100111111001111110011111100111111)



# Blue/Beta pawns
beta_p = np.uint64(0b0111111001111110000000000000000000000000000000000000000000000000) #pawns start position
l_beta_p = []

#Beta knights
beta_k =np.uint64(0) #knights start position
l_beta_k = []

# Beta
beta = beta_p & beta_k

# Blue/Beta pawns move
beta_p_forward = np.uint64(0b1111111111111111111111111111111111111111111111110111111000000000)
beta_p_left = np.uint64(0b0011111101111111011111110111111101111111011111110111111100000000)
beta_p_right = np.uint64(0b1111110011111110111111101111111011111110111111101111111000000000)

# Blue/Beta pawns hit
beta_p_hit_right = np.uint64(0b1111111111111110111111101111111011111110111111101111110000000000)
beta_p_hit_left = np.uint64(0b1111111101111111011111110111111101111111011111110011111100000000)

# Blue/Beta knights
beta_k_forward_right = np.uint64(0b1111111011111110111111101111111011111110111111000000000000000000)
beta_k_right = np.uint64(0b1111110011111100111111001111110011111100111111001111100000000000)
beta_k_forward_left = np.uint64(0b0111111101111111011111110111111101111111001111110000000000000000)
beta_k_left = np.uint64(0b0011111100111111001111110011111100111111001111110001111100000000)


#testboard  = np.uint64(0b0010)

def print_board(board:np.uint64):
	str = np.binary_repr(board,width=64)
	#str = 'X' + str[1:7]+'X'+str[8:56]+'X'+str[57:63]+'X'
	print('\n'.join(str[i:i+8] for i in range(0, len(str), 8)))


def alpha_p_move_execution(index, source, dest):
	# delete source Position (bitboard)
	alpha_p = alpha_p ^ source
	
	# on alpha_p -> knight
	if dest & alpha_p:
		alpha_k = alpha_k & dest
		del l_alpha_p[index]
		l_alpha_k.append(dest)
	
	# on beta_k -> hit & knight
	elif dest & beta_k:
		beta_k = beta_k ^ dest
		alpha_k = alpha_k & dest
		l_beta_k.remove(dest)
		l_alpha_k.append(dest)
		beta = beta_p & beta_k


	# on beta_p -> hit
	elif dest & beta_p:
		beta_p = beta_p ^ dest
		alpha_p = alpha_p & dest
		l_beta_p.remove(dest)
		l_alpha_p[index] = dest
		beta = beta_p & beta_k


	# simple move
	else: 
		alpha_p = alpha_p & dest
		l_alpha_p[index] = dest
	
	alpha = alpha_p & alpha_k

def alpha_k_move_execution(index, source, dest):
	# delete source Position (bitboard)
	alpha_k = alpha_k ^ source
	
	# on alpha_p -> knight
	if dest & alpha_p:
		alpha_k = alpha_k & dest
		l_alpha_k[index] = dest
	
	# on beta_k -> hit & knight
	elif dest & beta_k:
		beta_k = beta_k ^ dest
		alpha_k = alpha_k & dest
		l_beta_k.remove(dest)
		l_alpha_k[index] = dest
		beta = beta_p & beta_k


	# on beta_p -> hit & pawn
	elif dest & beta_p:
		beta_p = beta_p ^ dest
		alpha_p = alpha_p & dest
		l_beta_p.remove(dest)
		del l_alpha_k[index] 
		l_alpha_p.append(dest)
		beta = beta_p & beta_k


	# simple move -> pawn
	else: 
		alpha_p = alpha_p & dest
		del l_alpha_k[index]
		l_alpha_p.append(dest)
	
	alpha = alpha_p & alpha_k

def beta_move_execution(source, dest): # not for alpha beta search but enemy move
	if source & beta_k:
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
			del l_beta_k[l_beta_k.index(source)] 
			l_beta_p.append(dest)
			alpha = alpha_p & alpha_k


		# simple move -> pawn
		else: 
			beta_p = beta_p & dest
			del l_beta_k[l_beta_k.index(source)]
			l_beta_p.append(dest)
		
		beta = beta_p & beta_k
	else:
		# delete source Position (bitboard)
		beta_p = beta_p ^ source
		
		# on beta_p -> knight
		if dest & beta_p:
			beta_k = beta_k & dest
			del l_beta_p[l_beta_p.index(source)]
			l_beta_k.append(dest)
		
		# on alpha_k -> hit & knight
		elif dest & beta_k:
			alpha_k = alpha_k ^ dest
			beta_k = beta_k & dest
			l_alpha_k.remove(dest)
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
	
def alpha_p_move_generation(source):	# after pre-validation wheather source can move (being below knight)
	dests = []
    # Pwans
	# Movable Pawns (not under a knight)
	p_movable = alpha_p & ~(alpha_k & beta_k)

	# Pawns unmovable squares
	blocked_p_squares = beta & alpha_k

	# forward
	if (source & alpha_p_forward) << 8 & ~blocked_p_squares:
		dests.append(source << 8) 

	# left
	if (p_movable & alpha_p_left) << 1 & ~blocked_p_squares:
		dests.append(source << 1) 

	# right
	if (p_movable & alpha_p_right) >> 1 & ~blocked_p_squares:
		dests.append(source >> 1) 

	# hit left
	if (p_movable & alpha_p_hit_left) << 9 & beta:
		dests.append(source << 9) 

	# hit right
	if (p_movable & alpha_p_hit_right) << 7 & beta:
		dests.append(source << 7) 
	
	return dests
	
def alpha_k_move_generation(source): # no pre-validation needed
	dests = []

	# left
	if (alpha_k & alpha_k_left) << 10 & ~alpha_k:
		dests.append(source << 10) 

	# forward_left
	if (alpha_k & alpha_k_forward_left) << 17 & ~alpha_k:
		dests.append(source << 17) 

	# right
	if (alpha_k & alpha_k_right) << 6 & ~alpha_k:
		dests.append(source << 6) 

	# forward_left
	if (alpha_k & alpha_k_forward_right) << 15 & ~alpha_k:
		dests.append(source << 15) 

	return dests


#alphaboardtests
'''#Pawns
print("alpha_p_forward")
print_board(alpha_p_forward)

print("alpha_p_right")
print_board(alpha_p_right)

print("alpha_p_hit_right")
print_board(alpha_p_hit_right)

print("alpha_p_left")
print_board(alpha_p_left)

print("alpha_p_hit_left")
print_board(alpha_p_hit_left)'''

#Knights
print("alpha_k_forwar_right")
print_board(alpha_k_forward_right)

print("alpha_k_right")
print_board(alpha_k_right)

print("alpha_k_forward_left")
print_board(alpha_k_forward_left)

print("alpha_k_left")
print_board(alpha_k_left)

'''#betatest
#Pawns
print("beta_p_forward")
print_board(beta_p_forward)

print("beta_p_right")
print_board(beta_p_right)

print("beta_p_hit_right")
print_board(beta_p_hit_right)

print("beta_p_left")
print_board(beta_p_left)

print("beta_p_hit_left")
print_board(beta_p_hit_left)'''


#Knights
print("beta_k_forwar_right")
print_board(beta_k_forward_right)

print("beta_k_right")
print_board(beta_k_right)

print("beta_k_forward_left")
print_board(beta_k_forward_left)

print("beta_k_left")
print_board(beta_k_left)