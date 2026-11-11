from board import Board
import players
import ui

import random


def display(number_of_moves, number_of_steps):
    game = Board("board.txt")
    game.Board_map()
    return game


def show(game):
    ui.show_board(canvas, game)
    status.config(text=f"Points: {game.score.total}    Number of Moves left: {100 - number_of_moves}\n"
                       f"Selected steps: {number_of_steps}    Holding repair kit: {player.repair_kit}")


def pressed_enter(event):
    global game, player, number_of_moves, number_of_steps, game_over

    option = event.char.upper()

    if option == "Q":
        window.destroy()
        return

    elif option == "N":
        number_of_moves = 0
        number_of_steps = 1
        game_over = False
        game = display(number_of_moves, number_of_steps)
        player = game.objects[0][0]
        show(game)
        return

    if game_over:
        return

    if option in ["1", "2", "3"]:
        number_of_steps = int(option)
        show(game)
        return

    if option not in ["W", "A", "S", "D", "U", "C", "L", "R"]:
        return

    try:
        move_player(option)
    except SystemExit:
        game_over = True

    show(game)
    if game_over:
        if len(game.Element_location("SF")) == 0:
            status.config(text=f"You Win!! Final score: {game.score.total}\nN for New board, Q for exit")
        else:
            status.config(text=f"Game over! Final score: {game.score.total}\nN for New board, Q for exit")


def move_player(option):
    global number_of_moves

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


number_of_moves = 0
number_of_steps = 1
game_over = False

game = display(number_of_moves, number_of_steps)
player = game.objects[0][0]

window, canvas, status = ui.create_window()

restart = ui.tk.Button(window, text="Restart", command=lambda: window.event_generate("<KeyPress-n>"))
restart.pack(pady=5)

show(game)
window.bind("<Key>", pressed_enter)
window.mainloop()
