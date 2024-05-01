import pygame
from fenStringLib import*

"""
Beispielaufruf:
gui = GUI("FENSTRING")
gui.start()
gui.updateGUI("FENSTRING2")
"""

class GUI:
    
    
    
    def __init__(self,fen):
        self.BREITE =800
        self.HÖHE = 800
        self.FELDER = 8
        self.fen = fen
        #starte pygame
        pygame.init()
        self.SCHRIFTART = pygame.font.Font(None, 32)
        
        # Spielfeld erstellen
        self.screen = pygame.display.set_mode((self.BREITE+200, self.HÖHE+200))
        pygame.display.set_caption("Projekt: Symbolische KI: Jumps Sturdy")
        
    def zeichne_feld(self,x, y, farbe):
        pygame.draw.rect(self.screen, farbe, (x * self.BREITE / self.FELDER, y * self.HÖHE / self.FELDER, self.BREITE / self.FELDER, self.HÖHE / self.FELDER))
    
    # Funktion zum Zeichnen von Text
    def zeichne_text(self,text, x, y, farbe):
        textobjekt = self.SCHRIFTART.render(text, True, farbe)
        textrect = textobjekt.get_rect(center=(x+100, y+100))
        self.screen.blit(textobjekt,textrect)
    
    # Zeichne Spielfigur
    def zeichneFigur(self,x,y,farbe, shift):
        pygame.draw.ellipse(self.screen, farbe,(x * self.BREITE / self.FELDER,y* self.HÖHE / self.FELDER+25+shift,self.BREITE / self.FELDER, self.HÖHE / (self.FELDER*2)))
    
    def updateGUI(self, FEN):
        self.fen = FEN
        #pygame.event.post(pygame.event.Event(pygame.USEREVENT, customdata={"fen":self.FEN}))
        #self.start()
    def start(self):
        running = True
        while running:
            # Ereignisse abrufen
            for event in pygame.event.get():
              if event.type == pygame.QUIT:
                pygame.quit()
                quit()
              if event.type== pygame.KEYDOWN:
                  if event.key == pygame.K_RETURN:
                    running = False
            # Schachbrett zeichnen
            no_field = {(1,1),(1,8),(8,8),(8,1)}
            for x in range(1,self.FELDER+1):
              for y in range(1,self.FELDER+1):
                farbe = WEISS if (x + y) % 2 == 0 else SCHWARZ
                pos = (x,y)
                if pos in no_field:
                  self.zeichne_feld(x,y,BACKGROUND)
                else:
                  self.zeichne_feld(x, y, farbe)
            
            # Spaltenbeschriftungen zeichnen
            for x in range(0,self.FELDER):
              self.zeichne_text(chr(x + 65), x * self.BREITE / self.FELDER + self.BREITE / self.FELDER / 2, self.HÖHE + 20, SCHWARZ)
            
            self.zeichne_text("Zum Aktualisieren oder Beenden Enter drücken", 200, self.HÖHE + 80, DARKRED)

            # Zeilenbeschriftungen zeichnen
            for y in range(1, self.FELDER + 1):
              self.zeichne_text(str(9-y), -10, (y-1) * self.HÖHE / self.FELDER + self.HÖHE / self.FELDER / 2, SCHWARZ)

            GameStateMatrix = fenToMatrix(self.fen)
            for x in range(GameStateMatrix.shape[1]):
              for y in range(GameStateMatrix.shape[0]):
                ColorArray = mapValueToColor(GameStateMatrix[x][y])
                shift = 0
                while len(ColorArray)>0:
                  self.zeichneFigur(y+1,x+1,ColorArray.pop(),shift)
                  shift -=15
            
            
            # Aktualisieren des Bildschirms
            pygame.display.flip()
            print(self.fen)
            # Taktrate begrenzen
            pygame.time.Clock().tick(60)