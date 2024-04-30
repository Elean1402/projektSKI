FEN = "2rr3/5r02/1rr1rr2r0r0/2rb3b01/2r0b04/5b0bb1/2bb2b02/3b02"
import numpy as np

NO_FIELD = {(8,1),(1,8),(1,1),(8,8)}

def checkFen(fen: str):
    """
    checks if the FEN string is correct

    Args:
        fen (str): a FEN string

    Returns:
        boolean: if correct true
    """
    return True

def fenToMatrix(fen:str):
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
    if not checkFen(fen):
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
                print("zeichen:",value)
                if (zeile == 0 or zeile == 7) and spalte ==0: spalte += value if value != 0 else 1
                else:
                    #mögliche Fälle im FEN String:
                    # x{r,b}0 | {r,b}0y | {r,b}{r,b} |  
                    if value != 0 and spalte == 0: spalte += value
                    elif value != 0 and spalte > 0 and spalte < 7: spalte+=value;  
                    elif value == 0 and counter ==1 : counter=0;spalte+=1
            except ValueError:
                figure = mapColorToValue(tmpRow[i])
                print("figure",figure)
                if figure == 0:
                    raise Exception("FEN String contains unknown character!")
                if counter ==2 :spalte +=1; counter=1
                elif counter ==1 or counter ==0: counter +=1
                
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

#def setValueInMatrix(matrix: np.ndarray,zeile:int,spalte:int,figure:int,FigureOnTop:bool):