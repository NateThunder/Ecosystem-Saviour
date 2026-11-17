import items
import players
import random
import settings
from scoring import Score

class Board:
    def __init__(self,file):
        self.content = []
        self.score = Score()

        with open(file, 'r') as f:
            for line in f:
                lines = line.strip().split(',')
                row = []

                for value in lines:
                    if value == '-':
                        row.append(None)
                    else:
                        row.append(value)

                self.content.append(row)
        if not self.content or not self.content[0] or any(len(row) != len(self.content[0]) for row in self.content):
            raise ValueError("Board must be a non-empty rectangle")
        if (type(settings.BOARD_SIZE_X) is not int or
            type(settings.BOARD_SIZE_Y) is not int or
            settings.BOARD_SIZE_X < 1 or settings.BOARD_SIZE_Y < 1):
            raise ValueError("Board X and Y sizes must be positive whole numbers")

        # Keep the top-left part of the map and fill extra squares with None.
        content = []
        for y in range(settings.BOARD_SIZE_Y):
            row = []
            for x in range(settings.BOARD_SIZE_X):
                if y < len(self.content) and x < len(self.content[0]):
                    row.append(self.content[y][x])
                else:
                    row.append(None)
            content.append(row)
        self.content = content
        self.objects = [[None for value in row] for row in self.content]




# Showing locations of all elements on the board
    def Board_map(self):
        self.locations = []
        for y, line in enumerate(self.content):
            for x, symbol in enumerate(line):
                if symbol == "M":
                    #print(f"{symbol}[{x}][{y}]")
                    self.objects[y][x] = items.Mountain(x, y, symbol)
                if symbol == "SF":
                    #print(f"{symbol}[{x}][{y}]")
                    self.objects[y][x] = items.Forest(x, y, symbol, False)
                if symbol == "HF":
                    #print(f"{symbol}[{x}][{y}]")
                    self.objects[y][x] = items.Forest(x, y, symbol, True)
                if symbol == "R":
                    #print(f"{symbol}[{x}][{y}]")
                    self.objects[y][x] = items.Repair_station(x, y, symbol)                
                if symbol == "L":
                    #print(f"{symbol}[{x}][{y}]")
                    self.objects[y][x] = items.Lake(x, y, symbol)

        self.objects[0][0] = players.Player(0, 0, "P")

        free_square = []
        # npc setup
        for y, line in enumerate(self.objects):
            for x, item in enumerate(line):
                if item  == None:
                    free_square.append((x, y))


        # mapping NPC and inteligent NPC ==================================
        enemy_types = ([players.NPC] * settings.difficulty()["npc_count"] +
                       [players.Inteligent_NPC] * settings.difficulty()["ipc_count"])
        if len(enemy_types) > len(free_square):
            raise ValueError("Not enough empty squares for the configured enemies")
        for enemy_type, (x, y) in zip(enemy_types, random.sample(free_square, len(enemy_types))):
            symbol = "IPC" if enemy_type is players.Inteligent_NPC else "NPC"
            self.objects[y][x] = enemy_type(x, y, symbol)



# Showing location of spceific element on the board
    def Element_location(self, element):
        locations = []
        
        for y, line in enumerate(self.content):
            for x, symbol in enumerate(line):
                if symbol == element.upper():
                    
                    locations.append((x,y))
        return locations



    def game_state(self, game_over: bool):
        self.game_over = game_over
        

#======= print each line one by one ========================== 
    def __str__(self):
        grid = ""
        for line in self.objects:
            for item in line:
                if item is None:
                    grid += "-" + "   "
                else:
                    grid += item.symbol + " "*(4 - len(str(item)))
            grid += "\n"
        return grid



    def printBoard(self):
        for i in self.content:
            print(i)