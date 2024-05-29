class Node:
	def __init__(self, value, children=[], move=None):
		self.value = value
		self.children = children
		self.move = move

class AlphaBetaSearch:
	def __init__(self, root):
		self.root = root
		self.alpha = -float('inf')
		self.beta = float('inf')

	def search(self):
		self.alpha_beta_max(self.root, self.alpha, self.beta)
		return self.root.move  # Return the move stored in the root node

	def alpha_beta_max(self, node, alpha, beta):
		if not node.children:  # If node is a leaf
			return node.value

		max_value = -float('inf')
		for child in node.children:
			value = self.alpha_beta_min(child, alpha, beta)
			if value > max_value:
				max_value = value
				if node == self.root:  # If the node is the root node
					self.root.move = child.move  # Store the move in the root node
			alpha = max(alpha, max_value)
			if beta <= alpha:
				break  # Beta cut-off
		return max_value

	def alpha_beta_min(self, node, alpha, beta):
		if not node.children:  # If node is a leaf
			return node.value

		min_value = float('inf')
		for child in node.children:
			value = self.alpha_beta_max(child, alpha, beta)
			if value < min_value:
				min_value = value
			beta = min(beta, min_value)
			if beta <= alpha:
				break  # Alpha cut-off
		return min_value

if __name__ == '__main__':
	# Create a deeper binary tree structure
	root = Node(0, [
		Node(0, [
			Node(3, [
				Node(1, move=7),
				Node(2, move=8)
			], move=1), 
			Node(1, [
				Node(3, move=9),
				Node(4, move=10)
			], move=2)
		], move=3),
		Node(0, [
			Node(2, [
				Node(5, move=11),
				Node(6, move=12)
			], move=4), 
			Node(4, [
				Node(7, move=13),
				Node(8, move=14)
			], move=5)
		], move=6)
	])


	abs = AlphaBetaSearch(root)
	print(abs.search())  # This will print the first move that leads to the highest value