import logging
import curses
from time import sleep
from random import shuffle
from copy import deepcopy

class Puzzle:
    def __init__(self):
        self.generate()
        # self.thin_out(difficulty)

    # Returns a value for success and a completed puzzle if success == True
    def solve(self):
        current = [0, 0]
        puzzle = deepcopy(self.puzzle)
        success = True

        while True:
            if current[1] > 8:
                break
            cell = puzzle[current[1]][current[0]]

            # Reset the cell and move current to previous cell
            if not cell.findNewValue():
                if cell.x == 0 and cell.y == 0:
                    success = False
                    puzzle = None
                    break
                # If touching left
                if current[0] == 0:
                    current[1] -= 1
                    current[0] = 8
                else:
                    current[0] -= 1

            # Move to the next cell
            else:
                if current[0] == 8:
                    current[0] = 0
                    current[1] += 1
                else:
                    current[0] += 1

            returnObject = {
                "success": success,
                "puzzle": puzzle
            }

        return returnObject

    def generate(self):
        self.puzzle = []
        for y in range(9):
            self.puzzle.append([])
            for x in range(9):
                self.puzzle[y].append(Cell(self, x, y))
        self.puzzle = self.solve()["puzzle"]
    
    def thin_out(self, difficulty):
        levels = {
            "easy": 35,
            "medium": 45,
            "hard": 50
        }
        self.level = levels[difficulty.casefold()]

        removed = 0


    def genASCII(self):
        output = ""
        for row in self.puzzle:
            for cell in row:
                output += str(cell.value) + ' '
            output += '\n'
        return output


class Cell:
    def __init__(self, puzzle, x, y):
        self.puzzle = puzzle
        self.x = x
        self.y = y
        
        self.untested = list(range(1, 10))
        shuffle(self.untested)
        self.block = []
        # Find which block cell belongs to
        for i in [x, y]:
            if(i > 5):
                self.block.append(3)
            elif(i > 2):
                self.block.append(2)
            else:
                self.block.append(1)
        self.value = 0

    # Attempts to find a valid untested number
        # if none is found return false
    def findNewValue(self):
        for integer in self.untested:
            if(
                self.alreadyInRow(integer) or
                self.alreadyInColumn(integer) or
                self.alreadyInBlock(integer)
            ):
                pass
            else:
                self.value = integer
                self.untested.remove(integer)
                return True
        logging.debug("Failed to find new value for cell")
        self.resetUntested()
        self.value = 0
        return False

    def resetUntested(self):
        self.untested = list(range(1, 10))
        shuffle(self.untested)

    def alreadyInRow(self, integer):
        for cell in self.puzzle.puzzle[self.y]:
            if cell.value == integer:
                return True
        return False

    def alreadyInColumn(self, integer):
        for y in range(9):
            if(integer == self.puzzle.puzzle[y][self.x].value):
                return True
        return False

    def alreadyInBlock(self, integer):
        for row in self.puzzle.puzzle:
            for cell in row:
                if cell.block == self.block and cell.value == integer:
                    return True
        return False

puzzle = Puzzle()
print(puzzle.genASCII())

