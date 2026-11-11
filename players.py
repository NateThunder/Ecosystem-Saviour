from items import BoardItem
from scoring import Score
import board
import items
import subprocess, os, sys, random



class Player(BoardItem):
    def __init__(self, x: int, y: int, symbol: str):
        super().__init__(x,y,symbol)
        self.repair_kit = False

    def __str__(self):
        return self.symbol

    def Move(self, objects, direction, game, number_of_moves, number_of_steps):
        #clears current block
        

        objects[self.y][self.x] = None
        replace_forest(self, game, objects, self.x, self.y)
        repair_station_location(self, game, objects, self.x, self.y) #replace repair location once player moves of it
        
        
        # Move left  self.x > 0 represent limit
        if direction == "left" and self.x > 0 and (
                        objects[self.y][self.x - 1] is None or 
                        objects[self.y][self.x - 1].symbol not in ["L", "M"]):

            # program ends if platyer encounters NPC. change later to return True and if statement in controller in order not to end full programm
            encounters_npc(self, objects, direction)

            #No moves past the wall
            

            self.x -= 1
            has_repair_kit(self, objects)
            use_repair_kit(self, objects, game) 
        
        #if self.x - 1 < 0:
        #    number_of_moves -= 1

        # Move Right
        elif direction == "right" and self.x < 7 and (
                        objects[self.y][self.x + 1] is None or 
                        objects[self.y][self.x + 1].symbol not in ["L", "M"]):
            
            # encounter NPC
            encounters_npc(self, objects, direction)

            #No moves past the wall
            if self.x >= 7:
                number_of_moves -= 1

            self.x += 1
            
            has_repair_kit(self, objects)
            use_repair_kit(self, objects, game) 
         

        # Move up and limit     
        elif direction == "up" and self.y > 0 and (
                        objects[self.y - 1][self.x] is None or 
                        objects[self.y - 1][self.x].symbol not in ["L", "M"]):
            
            # Encounter NPC
            encounters_npc(self, objects, direction)

            #No moves past the wall
            if self.y <= 0:
                number_of_moves += 1

            self.y -= 1
            has_repair_kit(self, objects)
            use_repair_kit(self, objects, game) 

        # Move Down
        elif direction == "down" and self.y < 7 and (
                        objects[self.y + 1][self.x] is None or 
                        objects[self.y + 1][self.x ].symbol not in ["L", "M"]):
            #  Encounter NPC
            encounters_npc(self, objects, direction)

            #No moves past the wall
            if self.y >= 7:
                number_of_moves -= 1

            self.y += 1 
            #pased_over_symbol(self, object, prev_block_x, prev_block_y)
            has_repair_kit(self, objects)
            use_repair_kit(self, objects, game)  


        
        #==== Re-render board ====================
        sick_forest_location(self, game, objects, self.x, self.y)
        re_render(self, game, objects, number_of_moves, number_of_steps)
        you_win(self, game)




class NPC(BoardItem):
    def __init__(self, x: int, y: int, symbol: str):
        super().__init__(x,y,symbol)

    def __str__(self):
        return self.symbol

    def Move(self, objects, direction, game, number_of_moves, number_of_steps):
        objects[self.y][self.x] = None
        replace_sick_forest(self, game, objects, self.x, self.y)
        if direction == "left" and self.x > 0 and (
                        objects[self.y][self.x - 1] is None or 
                        objects[self.y][self.x - 1].symbol not in ["L", "M","NPC","IPC","R"]):
            encounters_player(self, objects, direction)
            #No moves past the wall
            self.x -= 1

        elif direction == "right" and self.x < 7 and (
                        objects[self.y][self.x + 1] is None or 
                        objects[self.y][self.x + 1].symbol not in ["L", "M","NPC","IPC","R"]):
            encounters_player(self, objects, direction)
            #No moves past the wall
            if self.x >= 7:
                number_of_moves -= 1
            self.x += 1   

        elif direction == "up" and self.y > 0 and (
                        objects[self.y - 1][self.x] is None or 
                        objects[self.y - 1][self.x].symbol not in ["L", "M","NPC","IPC","R"]):
            encounters_player(self, objects, direction)
            #No moves past the wall
            if self.y <= 0:
                number_of_moves += 1
            self.y -= 1

        # Move Down
        elif direction == "down" and self.y < 7 and (
                        objects[self.y + 1][self.x] is None or 
                        objects[self.y + 1][self.x ].symbol not in ["L", "M","NPC","IPC","R"]):
            encounters_player(self, objects, direction)
            #No moves past the wall
            if self.y >= 7:
                number_of_moves -= 1
            self.y += 1 

        objects[self.y][self.x] = self
        healthy_forest_location(self, game, objects, self.x, self.y)
        re_render_npc(self, game, objects, number_of_moves, number_of_steps)


class Inteligent_NPC(NPC):
    def __init__(self, x: int, y: int, symbol: str):
        super().__init__(x,y,symbol)

    def closest_target(self, game, player):
        target_x = player.x
        target_y = player.y

        closest_distance = abs(player.x - self.x) + abs(player.y - self.y)

        for x, y in game.Element_location("HF"):
            forest_distance = abs(x - self.x) + abs(y - self.y)

            if forest_distance < closest_distance:
                closest_distance = forest_distance
                target_x = x
                target_y = y

        return target_x, target_y

    def IPC_Direction(self,target_x, target_y):
        if target_x < self.x:
            direction = "left"
        elif target_x > self.x:
            direction = "right"
        elif target_y < self.y:
            direction = "up"
        elif target_y > self.y:
            direction = "down"
        else:
            return None
        return direction
    

    def intelligent_move(self, objects, game, player, number_of_moves, number_of_steps):
        target_x, target_y = self.closest_target(game, player)
        direction = self.IPC_Direction(target_x, target_y)


        if direction is not None:
            self.Move(objects, direction, game, number_of_moves, number_of_steps)

 

#====== Player Actions =======================================

def has_repair_kit(self, objects):
    if objects[self.y][self.x] is not None and objects[self.y][self.x].symbol == "R":
        self.repair_kit = True

def use_repair_kit(self, objects, game):
    if (objects[self.y][self.x] is not None and 
        objects[self.y][self.x].symbol == "SF" and
        self.repair_kit == True):

        self.repair_kit = False
        objects[self.y][self.x].symbol = "HF"
        objects[self.y][self.x].health = True
        game.content[self.y][self.x] = "HF"
        game.score.total_points(1)
    else:
        return self.repair_kit

def encounters_player(self, objects, direction):
    lateral_movement = 0
    vertical_movement = 0

    if direction == "left":
        lateral_movement = -1
    elif direction == "right":
        lateral_movement = 1
    elif direction == "up":
        vertical_movement = -1
    elif direction == "down":
        vertical_movement = 1

    if (objects[self.y + vertical_movement][self.x + lateral_movement] is not None and 
        objects[self.y + vertical_movement][self.x + lateral_movement].symbol in ["P"]):
        print("Game Over, NPC Killed You")
        return sys.exit(1)

def encounters_npc(self, objects, direction):
    lateral_movement = 0
    vertical_movement = 0

    if direction == "left":
        lateral_movement = -1
    elif direction == "right":
        lateral_movement = 1
    elif direction == "up":
        vertical_movement = -1
    elif direction == "down":
        vertical_movement = 1

    if (objects[self.y + vertical_movement][self.x + lateral_movement] is not None and 
        objects[self.y + vertical_movement][self.x + lateral_movement].symbol in ["NPC", "IPC"]):
        print("Game Over, NPC Killed You")
        return sys.exit(1)
    

def re_render(self, game, objects, number_of_moves, number_of_steps):
    objects[self.y][self.x] = self # Store the player in this grid square
    subprocess.run("cls", shell=True)

    print("N for New board, Q for exit, W A S D Keys to move")
    print("Press 1 for 1 step, 2 for 2 steps and 3 for 3 steps")    
    print(game)
    print("Points:", game.score.total)
    #print(number_of_steps,"steps")
    move_limit = 100
    print("Number of Moves left:", move_limit - number_of_moves)
    if number_of_moves >= move_limit:
        print("Out of moves. Game over!")
        sys.exit(1)

    if self.repair_kit == True:
        print("Holding repair kit") 

    print(f"X={self.x}\nY={self.y}")   

def re_render_npc(self, game, objects, number_of_moves, number_of_steps):
    objects[self.y][self.x] = self # Store the player in this grid square
    subprocess.run("cls", shell=True)
    print("N for New board, Q for exit, W A S D Keys to move")
    print("Press 1 for 1 step, 2 for 2 steps and 3 for 3 steps")
    print("Points:", game.score.total)
    print(game)
    print(number_of_steps,"steps")
    move_limit = 100
    print("Number of Moves left:", move_limit - number_of_moves)
    if number_of_moves >= move_limit:
        print("Out of moves. Game over!")
        sys.exit(1)

    print(f"X={self.x}\nY={self.y}")


def repair_station_location(self, game, objects, x, y):
    for locations in game.Element_location("R"):
        if (x,y) == locations:
            objects[self.y][self.x] = items.Repair_station(x, y, "R")
            game.content[self.y][self.x] = "R"
            return

def sick_forest_location(self, game, objects, x, y):
    
    locations = []
    for location in game.Element_location("SF"):
        locations.append(location)

    if (x,y) in locations and self.repair_kit == True:
        objects[self.y][self.x] = items.Forest(x, y, "HF", True)
        game.content[self.y][self.x] = "HF"
        locations.append(location)     
    elif (x,y) in locations and self.repair_kit == False:
        print("sick forest without repair kit game over!")
        sys.exit(1)
    return

def replace_forest(self, game, objects, x, y):
    for locations in game.Element_location("HF"):
        if (x,y) == locations:
            objects[self.y][self.x] = items.Forest(x, y, "HF", True)
            game.content[self.y][self.x] = "HF"
            return

def replace_sick_forest(self, game, objects, x, y):
    for locations in game.Element_location("SF"):
        if (x,y) == locations:
            objects[self.y][self.x] = items.Forest(x, y, "SF", False)
            game.content[self.y][self.x] = "SF"
            return


def healthy_forest_location(self, game, objects, x, y):
    locations = []
    for location in game.Element_location("HF"):
        locations.append(location)

    if (x,y) in locations:
        objects[self.y][self.x] = items.Forest(x, y, "SF", False)
        game.content[self.y][self.x] = "SF"
        locations.append(location)        
    return




def you_win(self, game):
    locations = []
    for location in game.Element_location("SF"):
        locations.append(location)

    if len(locations) == 0:
        game.score.total_points(2)
        print("You Win!! All forests healed, You are the Ecosystem Savior!!!")
        print("Final score:", game.score.total)
        sys.exit(1)

def NPC_Locations(game):
    npcs = []
    for row in game.objects:
        for item in row:
            if item is not None and item.symbol in ["NPC"]:
                npcs.append(item)
    return npcs

def IPC_Locations(game):
    ipcs = []
    for row in game.objects:
        for item in row:
            if item is not None and item.symbol in ["IPC"]:
                ipcs.append(item)
    return ipcs

def game_over(self):
    pass

