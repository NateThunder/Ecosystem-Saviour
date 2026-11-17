from board import Board
import players
import ui
import settings
import leaderboard
from tkinter import messagebox

import random


def display(number_of_moves, number_of_steps):
    game = Board(settings.board_file())
    game.Board_map()
    return game


def show(game):
    ui.show_board(canvas, game, number_of_steps)
    status.config(text=f"Points: {game.score.total}    Moves left: {settings.difficulty()["move_limit"] - number_of_moves}    "
                       f"Steps: {number_of_steps}    Repair kit: {'Yes' if player.repair_kit else 'No'}")


def pressed_enter(event):
    global game, player, number_of_moves, number_of_steps, game_over

    option = event.char.upper()

    if option == "Q":
        window.destroy()
        return

    elif option == "N":
        new_game()
        return

    if game_over:
        return

    if option in [str(step) for step in settings.STEP_OPTIONS]:
        number_of_steps = int(option)
        show(game)
        return

    if option not in ["W", "A", "S", "D", "U", "C", "L", "R"]:
        return

    try:
        move_player(option)
    except SystemExit as message:
        game_over = True
        end_message = str(message)
        if settings.LEADERBOARD_ENABLED:
            try:
                leaderboard.record(settings.PLAYER_NAME, game.score.total, number_of_moves, end_message)
            except (OSError, ValueError) as error:
                messagebox.showerror("Leaderboard", str(error), parent=window)

    show(game)
    if game_over:
        ui.show_game_over(canvas, end_message, game.score.total)


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
        npc_distant = random.randint(*settings.difficulty()["enemy_steps"])
        npc_directtion = random.choice(["down","left","up","right"])

        for distance in range(npc_distant):
            npc.Move(game.objects, npc_directtion, game, number_of_moves, number_of_steps)

    for ipc in players.IPC_Locations(game):   
        ipc_distant = random.randint(*settings.difficulty()["enemy_steps"])
        target_x, target_y = ipc.closest_target(game, player)
        ipc_direction = ipc.IPC_Direction(target_x, target_y)

        if ipc_direction is not None:
            for distance in range(ipc_distant):
                ipc.Move(game.objects, ipc_direction, game, number_of_moves, number_of_steps)


def new_game():
    global game, player, number_of_moves, number_of_steps, game_over
    number_of_moves = 0
    number_of_steps = settings.STEP_OPTIONS[0]
    game_over = False
    game = display(number_of_moves, number_of_steps)
    player = game.objects[0][0]
    show(game)


def change_board(value):
    settings.BOARD = value
    new_game()
    window.focus_set()


def change_difficulty(value):
    settings.DIFFICULTY = value
    new_game()


def change_character(value):
    settings.CHARACTER = value
    if hasattr(canvas, "player_image"):
        del canvas.player_image
    new_game()


def show_leaderboard():
    try:
        rows = leaderboard.load()
        text = "\n".join(f"{rank}. {row['name']} - {row['score']} points ({row['difficulty']}, {row['moves']} moves)"
                         for rank, row in enumerate(rows, 1))
        messagebox.showinfo("Leaderboard", text or "No completed games yet.", parent=window)
    except (OSError, ValueError) as error:
        messagebox.showerror("Leaderboard", str(error), parent=window)


def main():
    global window, canvas, status
    window, canvas, status = ui.create_window(change_board)
    if settings.SETTINGS_BAR_ENABLED:
        ui.create_settings_menu(window, change_difficulty, change_character, show_leaderboard)
    new_game()
    window.bind("<Key>", pressed_enter)
    window.mainloop()


if __name__ == "__main__":
    main()
