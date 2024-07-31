import subprocess
import os


def main() -> None:
	# Pfad zum Verzeichnis, das das Skript enthält
	script_dir = ""

	# Der Name des Skripts
	script_name = "client.py"

	# Vollständiger Pfad zum Skript
	script_path = os.path.join(script_dir, script_name)

	# Den Befehl ausführen
	result = subprocess.run(["python", script_path])


if __name__ == '__main__':
	main()
