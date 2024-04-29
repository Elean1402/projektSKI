import numpy as np

# Red/Alpha pawns
alpha_p = np.uint64(0b0111111001111110) #panws start position

# Red/Alpha knights
alpha_k =np.uint64(0) #knights start position

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
beta_p = np.uint64(0b0111111001111110000000000000000000000000000000000000000000000000) #panws start position

#Beta knights
beta_k =np.uint64(0) #knights start position

# Alpha
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




def alpha_moves():
	
    # Pwans
	# forward
	moves = (alpha_p & alpha_p_forward) << 8
	p_forward = moves & (moves ^ (beta & alpha_k))

	# left
	moves = (alpha_p & alpha_p_left) << 1
	p_left = moves & (moves ^ (beta & alpha_k))

	# right
	moves = (alpha_p & alpha_p_right) >> 1
	p_right = moves & (moves ^ (beta & alpha_k))

	# hit left
	moves = (alpha_p & alpha_p_hit_left) >> 1
	p_hit_left = moves & beta

	# hit right
	moves = (alpha_p & alpha_p_hit_right) >> 1
	p_hit_right = moves & beta
	
    #Knights
	#forward left

	
def beta_moves():
	# forward
	moves = (beta_p & beta_p_forward) << 8
	forward = moves & (moves ^ (alpha & beta_k))

	# left
	moves = (beta_p & beta_p_left) << 1
	left = moves & (moves ^ (alpha & beta_k))

	# right
	moves = (beta_p & beta_p_right) >> 1
	right = moves & (moves ^ (alpha & beta_k))

	# hit left
	moves = (beta_p & beta_p_hit_left) >> 1
	hit_left = moves & beta

	# hit right
	moves = (beta_p & beta_p_hit_right) >> 1
	hit_right = moves & beta
	
#print_board(testboard)

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