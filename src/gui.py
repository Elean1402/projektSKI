import numpy as np
import pygame

"""
Beispielaufruf:
gui = GUI("FENSTRING")
gui.start()
gui.updateGUI("FENSTRING2")
"""

class GUI:
  WEISS = (255, 255, 255)
  SCHWARZ = (50, 50, 50 )
  ROT = (255,0,0)
  DARKRED= (127,0,0)
  BLAU = (0, 102, 255)
  DARKBLUE = (0,0,255)
  BACKGROUND = (0,0,0)

  def checkFen(fen: str):
      """
      checks if the FEN string is correct

      Args:
          fen (str): a FEN string

      Returns:
          boolean: if correct true
      """
      #TODO
      return True
  @classmethod
  def fenToMatrix(self,fen:str):
      """Reads FEN and maps it into a 8x8 Matrix
        1 = red, 4 = blue
        2 = rr, 3 = br, 5= rb, 8= bb
        first color is top

      Args:
          fen (str): _description_
      Returns:
          numpy.ndarray: Matrix which contains the game state
      """
      board = np.zeros((8,8))
      if not self.checkFen(fen):
          return None
      
      fenArray = fen.split("/")[::-1]
      zeile = 0
      while zeile < 8:
          tmpRow = fenArray.pop()
          spalte = 0
          figure = 0
          counter = 0
          for i in range(len(tmpRow)):
              try:
                  value = int(tmpRow[i])
                  if (zeile == 0 or zeile == 7) and spalte ==0: spalte += value+1 if value != 0 else 1
                  else:
                      #mögliche Fälle im FEN String:
                      # x{r,b}0 | {r,b}0y | {r,b}{r,b} |  
                      if value != 0 and spalte == 0: spalte += value
                      elif value != 0 and spalte > 0 and spalte < 7: spalte+=value;  
                      elif value == 0 and counter ==1 : counter=0;spalte+=1
              except ValueError:
                  figure = self.mapColorToValue(tmpRow[i])
                  if figure == 0:
                      raise Exception("FEN String contains unknown character!")
                  if counter ==2 :spalte +=1; counter=1
                  elif counter ==1 or counter ==0: counter +=1
                  
                  if (zeile == 0 or zeile == 7) and spalte ==0: spalte += 1
                  # mögliche Fälle: rr=2, rb=5, br=3, bb=8
                  tmpVal = board[zeile][spalte]
                  match tmpVal:
                      case 0: board[zeile][spalte] = figure
                      case 1: board[zeile][spalte] += figure
                      case 4: board[zeile][spalte] += figure if figure == 4 else -1
                  
          zeile +=1
      return board       

  def mapColorToValue(c:str):
      """
      helper function: maps r or b to a  specific value
      Args:
          c (str):

      Returns:
          int: encoded value for r or b else 0
      """
      match c:
          case "r": return 1
          case "b": return 4
          case _: return 0


  def mapValueToColor(self,value: int):
      """Helper function for GUI
      

      Args:
          value (int): _description_

      Returns:
          RGB COLOR 3-Tuple: (x,y,z)
      """
      match value:
          case 1: return [self.ROT]
          case 2: return [self.ROT,self.DARKRED]
          case 3: return [self.ROT,self.BLAU]
          case 4: return [self.BLAU]
          case 5: return [self.BLAU,self.ROT]
          case 8: return [self.BLAU,self.DARKBLUE]
          case _: return []
  
    
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
      pygame.display.set_caption("GUI: Jumps Sturdy by shin-young")
      
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
              farbe = self.WEISS if (x + y) % 2 == 0 else self.SCHWARZ
              pos = (x,y)
              if pos in no_field:
                self.zeichne_feld(x,y,self.BACKGROUND)
              else:
                self.zeichne_feld(x, y, farbe)
          
          # Spaltenbeschriftungen zeichnen
          for x in range(0,self.FELDER):
            self.zeichne_text(chr(x + 65), x * self.BREITE / self.FELDER + self.BREITE / self.FELDER / 2, self.HÖHE + 20, self.SCHWARZ)
          
          self.zeichne_text("Zum Aktualisieren oder Beenden Enter drücken", 200, self.HÖHE + 80, self.DARKRED)
          # Zeilenbeschriftungen zeichnen
          for y in range(1, self.FELDER + 1):
            self.zeichne_text(str(9-y), -10, (y-1) * self.HÖHE / self.FELDER + self.HÖHE / self.FELDER / 2, self.SCHWARZ)
          GameStateMatrix = self.fenToMatrix(self.fen)
          for x in range(GameStateMatrix.shape[1]):
            for y in range(GameStateMatrix.shape[0]):
              ColorArray = self.mapValueToColor(GameStateMatrix[x][y])
              shift = 0
              while len(ColorArray)>0:
                self.zeichneFigur(y+1,x+1,ColorArray.pop(),shift)
                shift -=15
          
          
          # Aktualisieren des Bildschirms
          pygame.display.flip()
          
          # Taktrate begrenzen
          pygame.time.Clock().tick(60)