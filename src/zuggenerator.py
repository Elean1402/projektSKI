import numpy as np

# Red/Alpha pawns
alpha_pawns = np.uint64(0b0111111001111110) #panws start position

# Red/Alpha knights
alpha_knights =np.uint64(0) #knights start position

# Alpha
alpha = alpha_pawns & alpha_knights

# Red/Alpha pawns move
alpha_pawns_forward = np.uint64(0b0000000001111110111111111111111111111111111111111111111111111111)
alpha_pawns_right = np.uint64(0b0000000011111110111111101111111011111110111111101111111011111100)
alpha_pawns_left = np.uint64(0b0000000001111111011111110111111101111111011111110111111100111111)

# Red/Alpha pawns hit
alpha_pawns_hit_right = np.uint64(0b0000000011111100111111101111111011111110111111101111111011111110)
alpha_pawns_hit_left = np.uint64(0b0000000000111111011111110111111101111111011111110111111101111111)



# Red/Alpha knights move/hit
alpha_knights_forward_right = np.uint64(0b0000000000000000111111001111111011111110111111101111111011111110)
alpha_knights_right = np.uint64(0b0000000011111000111111001111110011111100111111001111110011111100)
alpha_knights_forward_left = np.uint64(0b0000000000000000001111110111111101111111011111110111111101111111)
alpha_knights_left = np.uint64(0b0000000000011111001111110011111100111111001111110011111100111111)



# Blue/Beta pawns
beta_pawns = np.uint64(0b0111111001111110000000000000000000000000000000000000000000000000) #panws start position

#Beta knights
beta_knights =np.uint64(0) #knights start position

# Alpha
beta = beta_pawns & beta_knights

# Blue/Beta pawns move
beta_pawns_forward = np.uint64(0b1111111111111111111111111111111111111111111111110111111000000000)
beta_pawns_left = np.uint64(0b0011111101111111011111110111111101111111011111110111111100000000)
beta_pawns_right = np.uint64(0b1111110011111110111111101111111011111110111111101111111000000000)

# Blue/Beta pawns hit
beta_pawns_hit_right = np.uint64(0b1111111111111110111111101111111011111110111111101111110000000000)
beta_pawns_hit_left = np.uint64(0b1111111101111111011111110111111101111111011111110011111100000000)

# Blue/Beta knights
beta_knights_forward_right = np.uint64(0b1111111011111110111111101111111011111110111111000000000000000000)
beta_knights_right = np.uint64(0b1111110011111100111111001111110011111100111111001111100000000000)
beta_knights_forward_left = np.uint64(0b0111111101111111011111110111111101111111001111110000000000000000)
beta_knights_left = np.uint64(0b0011111100111111001111110011111100111111001111110001111100000000)


#testboard  = np.uint64(0b0010)

def print_board(board:np.uint64):
	str = np.binary_repr(board,width=64)
	#str = 'X' + str[1:7]+'X'+str[8:56]+'X'+str[57:63]+'X'
	print('\n'.join(str[i:i+8] for i in range(0, len(str), 8)))




def alpha_moves():
	# forward
	moves = (alpha_pawns & alpha_pawns_forward) << 8
	forward = moves & (moves ^ (beta_pawns & alpha_knights))

	# left
	moves = (alpha_pawns & alpha_pawns_left) << 1
	left = moves & (moves ^ (beta_pawns & alpha_knights))

	# right
	moves = (alpha_pawns & alpha_pawns_right) >> 1
	right = moves & (moves ^ (beta_pawns & alpha_knights))

	# hit left
	#moves = (alpha_pawns & alpha_pawns_hit_left) >> 1
	#hit_left = moves & 


	# hit right
	np.bitwise_and(alpha_pawns, alpha_pawns_hit_right)
	
#print_board(testboard)

#alphaboardtests
'''#Pawns
print("alpha_pawns_forward")
print_board(alpha_pawns_forward)

print("alpha_pawns_right")
print_board(alpha_pawns_right)

print("alpha_pawns_hit_right")
print_board(alpha_pawns_hit_right)

print("alpha_pawns_left")
print_board(alpha_pawns_left)

print("alpha_pawns_hit_left")
print_board(alpha_pawns_hit_left)'''

#Knights
print("alpha_knights_forwar_right")
print_board(alpha_knights_forward_right)

print("alpha_knights_right")
print_board(alpha_knights_right)

print("alpha_knights_forward_left")
print_board(alpha_knights_forward_left)

print("alpha_knights_left")
print_board(alpha_knights_left)

'''#betatest
#Pawns
print("beta_pawns_forward")
print_board(beta_pawns_forward)

print("beta_pawns_right")
print_board(beta_pawns_right)

print("beta_pawns_hit_right")
print_board(beta_pawns_hit_right)

print("beta_pawns_left")
print_board(beta_pawns_left)

print("beta_pawns_hit_left")
print_board(beta_pawns_hit_left)'''


#Knights
print("beta_knights_forwar_right")
print_board(beta_knights_forward_right)

print("beta_knights_right")
print_board(beta_knights_right)

print("beta_knights_forward_left")
print_board(beta_knights_forward_left)

print("beta_knights_left")
print_board(beta_knights_left)