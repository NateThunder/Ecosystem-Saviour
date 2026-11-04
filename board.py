import items
import players
import random

class Board:
    def __init__(self,file):
        self.content = []
        self.objects = [[None for x in range(8)] for y in range(8)]

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



# Showing locations of all elements on the board
    def Board_map(self):
        self.locations = []
        elements = ["HF","SF","M","R","L"]
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
        free_square_amount = len(free_square) -1

        npc1_location = random.randint(0, free_square_amount)
        npc1_location_x, npc1_location_y = free_square[npc1_location]
        self.objects[npc1_location_y][npc1_location_x] = players.NPC(npc1_location_x, npc1_location_y, "NPC")

        npc2_location = random.choice([n for n in range(0, free_square_amount + 1) if n != npc1_location])
        npc2_location_x, npc2_location_y = free_square[npc2_location]
        self.objects[npc2_location_y][npc2_location_x] = players.NPC(npc2_location_x, npc2_location_y, "NPC")

        Inteligent_NPC_location = random.choice([n for n in range(0, free_square_amount + 1) if n not in [npc1_location, npc2_location]])
        Inteligent_NPC_location_x, Inteligent_NPC_location_y = free_square[Inteligent_NPC_location]
        self.objects[Inteligent_NPC_location_y][Inteligent_NPC_location_x] = players.Inteligent_NPC(Inteligent_NPC_location_x, Inteligent_NPC_location_y, "IPC")        



# Showing location of spceific element on the board
    def Element_location(self, element):
        locations = []
        
        for y, line in enumerate(self.content):
            for x, symbol in enumerate(line):
                if symbol == element.upper():
                    
                    locations.append((x,y))
                    #print(f"{symbol}[{x}][{y}]")

        print(f"{element.upper()}: {locations}")





#======= print each line one by one ========================== 
    def __str__(self):
        grid = ""
        for line in self.objects:
            for item in line:
                if item is None:
                    grid += "-" + " "
                else:
                    grid += item.symbol + " "
            grid += "\n"

        return grid

    def printBoard(self):
        for i in self.content:
            print(i)