import time
import zuggenerator as gen
from moveLib import *
from evalFunction import *
import random
from scoreConfig_evalFunc import ScoreConfig

class MinimaxABAgent:
	"""
		Minimax agent
	"""

	def __init__(self, max_depth, player_color):
		"""
		Initiation
		Parameters
		----------
		max_depth : int
			The max depth of the tree
		player_color : int
			The player's index as MAX in minimax algorithm
		"""
		self.max_depth = max_depth
		self.player_color = player_color
		self.node_expanded = 0

	def generate_moves(self):
		if self.player_color == "r":
			return gen.beta_generation()
		if self.player_color == "b":
			return gen.alpha_generation()
		else:
			raise Exception("Invalid player color")

	def choose_action(self, state):
		"""
		Predict the move using minimax algorithm
		Parameters
		----------
		state : State
		Returns
		-------
		float, str:
			The evaluation or utility and the action key name
		"""
		self.node_expanded = 0

		start_time = time.time()

		print("MINIMAX AB : Wait AI is choosing")
		list_action = gen.moves_to_string(self.generate_moves())
		eval_score, selected_key_action = self._minimax(0, state, True, float('-inf'), float('inf'))
		print("MINIMAX : Done, eval = %d, expanded %d" % (eval_score, self.node_expanded))
		print("--- %s seconds ---" % (time.time() - start_time))

		return selected_key_action, list_action[selected_key_action]

	def _minimax(self, current_depth, state, is_max_turn, alpha, beta):
		if self.player_color == "r":
			ef = EvalFunction(ScoreConfig.Version1(), Player.Red)
		else:
			ef = EvalFunction(ScoreConfig.Version1(), Player.Blue)
		m = MoveLib()
		if current_depth == self.max_depth or state.is_terminal():
			return

		self.node_expanded += 1

		possible_action = self.generate_moves()
		key_of_actions = list(possible_action.keys())

		random.shuffle(key_of_actions)  # randomness
		best_value = float('-inf') if is_max_turn else float('inf')
		action_target = ""
		for action_key in key_of_actions:
			new_state = gen.alpha_p_move_execution(*m.move(source, dest, mode=1))  #alpha_p_move_execution(*m.move(source, dest, mode=1))

			eval_child, action_child = self._minimax(current_depth + 1, new_state, not is_max_turn, alpha, beta)

			if is_max_turn and best_value < eval_child:
				best_value = eval_child
				action_target = action_key
				alpha = max(alpha, best_value)
				if beta <= alpha:
					break

			elif (not is_max_turn) and best_value > eval_child:
				best_value = eval_child
				action_target = action_key
				beta = min(beta, best_value)
				if beta <= alpha:
					break

		return best_value, action_target
