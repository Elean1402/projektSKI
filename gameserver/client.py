import pygame
import json
import os
import sys
import random
from network import Network


pygame.font.init()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from alpha_beta_search import *



def main():
	run = True
	clock = pygame.time.Clock()
	n = Network()
	game_instance = Game(1)
	player = int(n.getP())
	print("You are player", player)
	last_action_time = pygame.time.get_ticks()

	while run:
		clock.tick(60)
		try:
			# try to send get as a json to server over network, rest is error handling
			game = n.send(json.dumps("get"))
			if game is None:
				raise ValueError("Game data is None")
		except:
			run = False
			print("Couldn't get game")
			break

		# response is also a json, json.loads transforms into a python dictionary
		# dictionary consists of board string, a variable player1 which is true, when player 1 (or better 0),
		# variable player2 with the same concept and bothConnected, also a boolean
		game = json.loads(game)

		# allow input just when both players are in
		if game["bothConnected"]:
			# allow to only give input, when it is your turn
			if player == 0 and game["player1"] or player == 1 and game["player2"]:
				print("New Board: " + game["board"])
				a = AlphaBetaSearch(game)
				response = a.search()
				data = json.dumps(response)
				n.send(data)
				last_action_time = pygame.time.get_ticks()  # Reset the timer after taking an action

		# Check if 3 seconds have passed without any action
		if pygame.time.get_ticks() - last_action_time > 10000:  # 3000 milliseconds = 3 seconds
			print("Timeout: No action for 3 seconds")
			sys.exit(0)


while True:
	main()
