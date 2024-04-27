import numpy as np



# Red pawns
red_pawns = np.uint64(0b0111111001111110) #panws start position
red_pawn_middle=np.uint64(0b0000000001111110011111100111111001111110011111100111111001111110) #middle red pawns


# Red knights
red_knight =np.uint64(0) #knights start position

# middle
red_knight_middle=np.uint64(0b0000000000000000001111000011110000111100001111000011110000111100) #knights middle position

#inner
red_knight_inner_left = np.uint64(0b0000000000000000010000000100000001000000010000000100000001000000) #knights left position
red_knight_inner_right = np.uint64(0b0000000000000000000000100000001000000010000000100000001000000010) #knights right position

#top
red_knight_left_top = np.uint64(0b0000000011000000000000000000000000000000000000000000000000000000) #knights left corner position
red_knight_right_top = np.uint64(0b00000000000000011000000000000000000000000000000000000000000000000) #knights right corner position
red_knight_middle_top=np.uint64(0b0000000000111100000000000000000000000000000000000000000000000000) #knights top position

# Outer
red_knight_outer_left = np.uint64(0b0000000000000000100000001000000010000000100000001000000000000000)
red_knight_outer_right = np.uint64(0b0000000000000000000000010000000100000001000000010000000100000000)



# Blue pawns
blue_pawns = np.uint64(0b0111111001111110000000000000000000000000000000000000000000000000) #panws start position
blues_pawn_middle=np.uint64(0b0111111001111110011111100111111001111110011111100111111000000000) #middle blue pawns

#Blue knights
blue_knight =np.uint64(0) #knights start position

#middle
blue_knight_middle=np.uint64(0b0011110000111100001111000011110000111100001111000000000000000000) #knights middle position

#inner
blue_knight_inner_left = np.uint64(0b0100000001000000010000000100000001000000010000000000000000000000) #knights left position
blue_knight_inner_right = np.uint64(0b0000001000000010000000100000001000000010000000100000000000000000) #knights right position


#top 
blue_knight_middle_top=np.uint64(0b0000000000000000000000000000000000000000000000000011110000000000) #knights top position
blue_knight_left_top = np.uint64(0b0000000000000000000000000000000000000000000000001100000000000000)
blue_knight_right_top = np.uint64(0b00000000000000000000000000000000000000000000000000000001100000000)

# outer
blue_knight_outer_left = np.uint64(0b0000000010000000100000001000000010000000100000000000000000000000)
blue_knight_outer_right = np.uint64(0b0000000000000001000000010000000100000001000000010000000000000000)





#Common Pawns
pawn_rightside = np.uint64(0b0000000000000001000000010000000100000001000000010000000100000000)
pawn_leftside = np.uint64(0b0000000010000000100000001000000010000000100000001000000000000000)

#testboard  = np.uint64(0b0010)

def print_board(board:np.uint64):
	str = np.binary_repr(board,width=64)
	str = 'X' + str[1:7]+'X'+str[8:56]+'X'+str[57:63]+'X'
	print('\n'.join(str[i:i+8] for i in range(0, len(str), 8)))




#print_board(testboard)
print('knight start position')
print_board(blue_knight)
print('knights middle position')
print_board(blue_knight_middle)
print('knights inner left position')
print_board(blue_knight_inner_left)
print('knights inner right position')
print_board(blue_knight_inner_right)
print('knights inner left single position')
print_board(blue_knight_left_top)
print('knights inner right single position')
print_board(blue_knight_right_top)
print('knights middle top position')
print_board(blue_knight_middle_top)
print('knights outer left position')
print_board(blue_knight_outer_left)
print('knights outer right position')
print_board(blue_knight_outer_right)
