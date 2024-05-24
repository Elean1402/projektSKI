from zuggenerator import *
from alpha_beta_search import *
import sys
import os
import socket
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'gameserver')))
import network


def init():
	global game
	run = True
	n = network.Network()



	def receive_message():
		return client.recv(4096).decode('utf-8')

	player_number = receive_message()

	if player_number == "0":
		print("Connected as Player 1")
	elif player_number == "1":
		print("Connected as Player 2")
	else:
		print("Unexpected response from server")

	# Spiel-Schleife
	while run:
		# Nachrichten vom Server empfangen
		message = receive_message()
		print("Received from server:", message)
		if message.startswith("New Board:"):
			try:
				# try to send get as a json to server over network, rest is error handling
				game = n.send(json.dumps("get"))
				if game is None:
					raise ValueError("Game data is None")
			except:
				run = False
				print("Couldn't get game")
				break
		# Wenn eine Nachricht vom Server empfangen wird, dass das Spiel vorbei ist, die Schleife beenden
		if "Game finished" in message:
			break
		if player_number == "Player 1" and game["player1"] or player_number == "Player 2" and game["player2"]:
			response = generate_moves(game)
			data = json.dumps(response)
			n.send(data)


	# Hier kannst du den Spielstatus überprüfen und entsprechend reagieren
	# Zum Beispiel:
	# - Den Spielstatus analysieren und entsprechend reagieren
	# - Benutzereingaben lesen und an den Server senden
	# - usw.

	client.close()


def main() -> None:
	init()


if __name__ == '__main__':
	main()
