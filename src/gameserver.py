from alpha_beta_search import *

test = "6/2r0b0r03/3r0r03/8/8/8/8/6 b"

game = {"board": test,
		"player1": True,
		"player2": False,
		}


def main() -> None:
	alpha_beta_max(10000, -10000, 1, game)


if __name__ == '__main__':
	main()
