from board import Board
import board
import items
import players

import os, random, subprocess

def pressed_enter():
    #print(text)
    if os.name == "nt":
        import msvcrt
        option = msvcrt.getwch()
        return option
    else:
        terminal = sys.stdin.fileno()
        original_settings = termios.tcgetattr(terminal)

        try:
            tty.setcbreak(terminal)
            option = sys.stdin.read(1)
        finally:
            termios.tcsetattr(terminal, termios.TCSADRAIN, original_settings)
    return option


def display(number_of_moves, number_of_steps):

    subprocess.run("cls", shell=True)
    game = Board("board.txt")
    game.Board_map()
    print("N for New board, Q for exit, W A S D Keys to move")
    print("Press 1 for 1 step, 2 for 2 steps and 3 for 3 steps")
    print("Points: 0")
    print(game)
    print("N for New board, Q for exit: ")
    print("Number of moves:",number_of_moves)
    if number_of_moves > 100:
        print("Out of moves. Game over!")
        return None
    return game

def show(game):
    print(game)

counter = 0 
number_of_moves = 0
number_of_steps = 1
option = ""
NPCs = []
while True:
    while counter < 1:
        game = display(number_of_moves, number_of_steps)
        player = game.objects[0][0]
        counter+=1

    while True:
        move = pressed_enter().upper()

        if move.isdigit():
            if 1 <= int(move) <= 3:
                number_of_steps = int(move)
                print("Selected steps:", number_of_steps)

        elif move in ["W", "A", "S", "D", "U", "C", "L", "R", "Q", "N"]:
            option = move
            break

    if option == "Q":
        break

    elif option == "N":
        game = display(number_of_moves, number_of_steps)
        player = game.objects[0][0]
        NPCs = players.NPC_Locations(game)
        continue

    number_of_moves += 1
        
    for moves in range(number_of_steps):        
        if option.upper() in ["S", "C"]:
            player.Move(game.objects, "down", game, number_of_moves, number_of_steps)
        if option.upper() in ["A", "L"]:
            player.Move(game.objects, "left", game, number_of_moves, number_of_steps)

        if option.upper() in["W", "U"]:
            player.Move(game.objects, "up", game, number_of_moves, number_of_steps)

        if option.upper() in["D", "R"]:
            player.Move(game.objects, "right", game, number_of_moves, number_of_steps)

    for npc in players.NPC_Locations(game):
        npc_distant = random.randint(1,3)
        npc_directtion = random.choice(["down","left","up","right"])

        for distance in range(npc_distant):
            npc.Move(game.objects, npc_directtion, game, number_of_moves, number_of_steps)

    for ipc in players.IPC_Locations(game):   
        ipc_distant = random.randint(1,3)
        for distance in range(ipc_distant):
            ipc.intelligent_move(game.objects, game, player, number_of_moves, number_of_steps)

    if option.upper() not in ["N", "Q"]:
        continue