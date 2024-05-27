# def alpha_beta_max(alpha, beta, depth_left: int, l) -> int:
# 	if depth_left == 0:
# 		return l
# 	ld=(1,2,3,4,5,6,7,8,9)
# 	for move in ld:
#
# 		score = alpha_beta_min(alpha, beta, depth_left - 1, l)
# 		l[move] = score
# 		# rework move
# 		if score >= beta:
# 			return beta  # fail hard beta-cutoff
# 		if score > alpha:
# 			alpha = score  # alpha acts like max in MiniMax
# 	return alpha
#
#
# def alpha_beta_min(alpha, beta, depth_left: int, l) -> int:
# 	if depth_left == 0:
# 		return l
# 	ld = (5, 3, 3, 4, 5, 6, 7, 8, 9)
# 	for move in ld:
# 		print(l)
# 		score = alpha_beta_max(alpha, beta, depth_left - 1, l)
# 		#rework move
# 		l[move] = score
# 		if score <= alpha:
# 			return alpha  # fail hard alpha-cutoff
# 		if score < beta:
# 			beta = score  # beta acts like min in MiniMax
# 	return beta
#
# def main() -> None:
# 	alpha = -float('inf')
# 	beta = float('inf')
# 	depth = 2
# 	l = dict()
# 	best_score = alpha_beta_max(alpha, beta, depth, l, )
# 	print(best_score)
#
#
# if __name__ == '__main__':
#     main()