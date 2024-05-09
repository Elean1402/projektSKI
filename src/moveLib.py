import numpy as np
from src.gamestate import GameState


class MoveLib:
    _coldict = {"A":1, "B":2, "C":3, "D":4,"E":5,"F":6, "G":7, "H":8 }
    
    @classmethod
    def move(self,start, target, mode = 1):
        """
        defines a move from position xy to zv

        Args:
            start (str or uint64): start Position e.g. "A4"
            target (str or uint64): target Position e.g. "A5"
            mode (int, optional):  
                0: str -> tupel(str,str), 
                1: str -> tupel(uint64,uint64)
                3: uint64 -> str 

        Returns:
            mode=0: (str,str): string tupel of start and target (for Tests & internal usage)
            mode=1: (uint64,uint64): Bitboard tupel of start and target
            mode=3: str: for communication with game server
        """
        if mode == 0:
            if(type(start)==str and type(target)==str):
                return start,target
            else:
                raise ValueError("start and target are not of type str")
        if mode == 1:
            if(type(start)==str and type(target)==str):
                #TODO convert string to bits
                return self.extractValueFromString(start) | GameState.BITBOARD, self.extractValueFromString(target) | GameState.BITBOARD
            else:
                raise ValueError("start and target are not of type str")
        if mode == 3:
            if(type(start)==np.uint64 and type(target) == np.uint64):
                #TODO convert uint64 position to str value
                return self.BitsToPosition(start) + "-" + self.BitsToPosition(start)
            else:
                raise ValueError("start and target are not of type np.uint64")
    @classmethod
    def extractValueFromString(self,pos: str):
        """
        This function is used to convert a string to a bit value.
        Assuming msb bit order -> Position A0: last "row" in bit order

        Args:
            pos (str): A Position from the Board

        Returns:
            np.uint64: on failure 0, on success bit value
        """
        #todo
        emptyFields = {"A1", "H1" , "A8" , "H8"}
        if pos in emptyFields:
            return np.uint64(0)
        
        powValue = self.mapRowToPowValue(pos[1])
        addX = self.mapLetterToNumber(pos[0])
        
        if powValue == None or addX == None:
            return np.uint64(0)
        
        rowValue = 0
        
        if pos[1] == "1":
            rowValue = 8-int(addX)
        else: 
            rowValue = 8-int(addX)+1
        # runtime of Pow is garbage
        #completeValue = pow(2, powValue+ rowValue)
        completeValue = 1 << (powValue+rowValue)
        return np.uint64(completeValue) 
        
    def mapRowToPowValue(rowNumber: str):
        """
        Abstraction of the Bitboard and containing only exponent values.
            3 | .. .. .. .. ... ... 
        e.g. 2 |15 14 13 12 11 10 9 8 
            1 | 7  6  5  4  3  2 1 0
            | ____________________
                A  B  C  D  E  F G H
        
        computation goal: "A2" has the value 2**15, so A2 =  7   + (8-1)+1 = 15 
                                                            "2"     "A"        
        Args:
            rowNumber (str): rowNumber of a Position

        Returns:
            int: value for a row, which needs to be added to compute the complete exponent. e.g. "2" -> 7
        """
        match rowNumber:
            case "1": return 0
            case "2": return 7
            case "3": return 15
            case "4": return 23
            case "5": return 31
            case "6": return 39
            case "7": return 47
            case "8": return 55
            case _: return None
    @classmethod
    def mapLetterToNumber(self,letter:str):
        """
        map the letters to column numbers

        Args:
            letter (str): from A to H

        Returns:
            int: column number
        """
        retVal = 0
        try:
            retVal = self.__coldict[letter]
        except Exception as error:
            print("Error: ", type(error).__name__)
            return None
        
        # match letter:
        #     case "A": return 1
        #     case "B": return 2
        #     case "C": return 3
        #     case "D": return 4
        #     case "E": return 5
        #     case "F": return 6
        #     case "G": return 7
        #     case "H": return 8
        #     case _: return None 
        return retVal
    @classmethod         
    def BitsToPosition(self,value:np.uint64):
        row = 0
        col = 0
        tmp = value
        while(tmp >= 1):
            tmp = tmp >> np.uint64(1)
            if(col == 7):
               col = 0
               row +=1 
            col+=1
            
        colToLetter = dict(map(reversed, self._coldict.items()))
        retCol = ""
        try:
            retCol =colToLetter[col]
        except:
            print("Error at BitsToPosition")
        return retCol + str(row)