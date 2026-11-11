import tkinter as tk


def create_window():
    window = tk.Tk()
    window.title("Ecosystem Saviour")

    instructions = tk.Label(window, text="N for New board, Q for exit, W A S D Keys to move\n"
                                        "Press 1 for 1 step, 2 for 2 steps and 3 for 3 steps")
    instructions.pack()

    canvas = tk.Canvas(window, width=480, height=480, highlightthickness=0)
    canvas.pack(padx=20, pady=20)

    legend = tk.Label(window, text="Blue: Player    Red: NPC    Purple: Intelligent NPC\n"
                                  "HF: Healthy forest    SF: Sick forest    M: Mountain    L: Lake    R: Repair station")
    legend.pack()

    status = tk.Label(window)
    status.pack(pady=10)

    return window, canvas, status


def show_board(canvas, game):
    canvas.delete("all")
    square_size = 60
    terrain_colours = {"HF": "darkgreen", "SF": "saddlebrown", "M": "dimgray",
                       "L": "blue", "R": "darkorange"}
    player_colours = {"P": "royalblue", "NPC": "firebrick", "IPC": "purple"}

    for y, row in enumerate(game.objects):
        for x, item in enumerate(row):
            left = x * square_size
            top = y * square_size

            if (x + y) % 2 == 0:
                colour = "#f0d9b5"
            else:
                colour = "#b58863"

            canvas.create_rectangle(left, top, left + square_size, top + square_size,
                                    fill=colour, outline=colour)

            symbol = game.content[y][x]
            if symbol in terrain_colours:
                canvas.create_text(left + 30, top + 12, text=symbol,
                                   fill=terrain_colours[symbol], font=("Arial", 11, "bold"))

            if item is not None and item.symbol in player_colours:
                canvas.create_oval(left + 12, top + 20, left + 48, top + 56,
                                   fill=player_colours[item.symbol], outline="white", width=2)
                canvas.create_text(left + 30, top + 38, text=item.symbol,
                                   fill="white", font=("Arial", 10, "bold"))
