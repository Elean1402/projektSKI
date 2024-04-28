Um alle Tests im Ordner "test" auszuführen einfach im Projekt Root-Verzeichnis im Terminal

$ python -m unittest

ausführen.


Um eine farbliche Konsolenausgabe zu bekommen kann "pytest" installiert werden

$ pip install --user pytest



Anleitung für Testerstellung:

..nicht vergessen die zu testende Python-Datei zu importieren..

Präfix für den Dateinamen "test_"
Präfix für die Funktion "test_"

sonst führt unittest die tests nicht aus..

