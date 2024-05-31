import json


class JSONHandler:
	"""
	A class used to handle JSON files.

	...

	Attributes
	----------
	filename : str
		a formatted string to print out the filename

	Methods
	-------
	create_json(fen: list[str], moves: list[str])
		Creates a JSON file from the given fen and moves lists.
	read_json()
		Reads the JSON file and returns the data.
	"""

	def __init__(self, filename: str):
		"""
		Constructs all the necessary attributes for the JSONHandler object.

		Parameters
		----------
			filename : str
				filename to be used for reading and writing JSON data
		"""


		self.filename = filename


	def create_from_fen(self, fen_var, fen_list, moves_list):
		# Read the existing data from the file
		try:
			with open(self.filename, 'r') as file:
				data = json.load(file)
		except FileNotFoundError:
			data = []

		# Add the new data to the existing data
		for fen, moves in zip(fen_list, moves_list):
			board, player = fen.split(' ')
			data.append({
				'type': fen_var.replace('FEN_', ''),  # Remove the 'FEN_' prefix
				'board': board,
				'player': player,
				'moves': moves,
				'bitboards': ''
			})

		# Write the updated data back to the file
		with open(self.filename, 'w') as file:
			json.dump(data, file, indent=2)

	def read_json(self):
		"""
		Reads the JSON file and returns the data.

		Returns
		-------
		data : dict
			data from the JSON file
		"""
		try:
			with open(self.filename, 'r') as f:
				data = json.load(f)
			return data
		except FileNotFoundError:
			print(f"File {self.filename} not found.")
			return None
		except IOError:
			print(f"Error reading from file {self.filename}")
			return None
		

def main():
	handler = JSONHandler("test.json")
	
	# Get the global variables from the current module
	global_vars = {var: globals()[var] for var in globals() if isinstance(globals()[var], list)}
	
	# Separate the FEN and poss lists
	fen_vars = [var for var in sorted(global_vars.keys()) if var.startswith("FEN")]
	poss_vars = [var for var in sorted(global_vars.keys()) if var.startswith("poss")]

	# Ensure there's an equal number of FEN and poss lists
	#assert len(fen_vars) == len(poss_vars), "Uneven number of FEN and poss lists"
	
	# Pair the FEN and poss lists
	for fen_var, moves_var in zip(fen_vars, poss_vars):
		fen_list = global_vars[fen_var]
		moves_list = global_vars[moves_var]
		handler.create_from_fen(fen_var, fen_list, moves_list)

if __name__ == "__main__":
	main()