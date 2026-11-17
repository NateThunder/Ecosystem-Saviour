import tkinter as tk
import settings
from pathlib import Path

def load_sprite(canvas, path, width, height, keep_aspect=False, crop=None):
    source = tk.PhotoImage(master=canvas, file=str(path))
    if crop is not None:
        left, top, right, bottom = crop
        frame = tk.PhotoImage(master=canvas, width=right - left, height=bottom - top)
        frame.tk.call(str(frame), "copy", str(source), "-from", left, top, right, bottom)
        source = frame
    if keep_aspect:
        scale = min(width / source.width(), height / source.height())
        width = max(1, round(source.width() * scale))
        height = max(1, round(source.height() * scale))
    image = tk.PhotoImage(master=canvas, width=width, height=height)
    # Sample the original pixels using Tkinter, preserving transparent areas.
    for y in range(height):
        source_y = min(source.height() - 1, int((y + 0.5) * source.height() / height))
        for x in range(width):
            source_x = min(source.width() - 1, int((x + 0.5) * source.width() / width))
            if not source.transparency_get(source_x, source_y):
                red, green, blue = source.get(source_x, source_y)
                image.put(f"#{red:02x}{green:02x}{blue:02x}", (x, y))
    return image


def load_tile_images(canvas, square_size):
    sprite_directory = Path(__file__).resolve().parent / "sprites"
    filenames = {
        None: "Pixel-Art Grass.png",
        "HF": "Pixel-Art Forest Clearing.png",
        "SF": "Diseased Gnarled Forest Clearing.png",
        "L": "Pixel-Art Lake with Grassy Shore.png",
        "M": "Pixel-Art Mountain Tile.png",
        "R": "Pixel-Art Tree Care Workshop Stall.png",
    }
    images = {}
    for symbol, filename in filenames.items():
        images[symbol] = load_sprite(canvas, sprite_directory / filename,
                                     square_size, square_size)
    return images


def create_window(on_board=None):
    window = tk.Tk()
    window.title("Ecosystem Saviour")
    window.config(bg="#203e48")

    # This canvas scrolls the whole interface. The game has its own canvas below.
    scroll_area = tk.Frame(window, bg="#203e48")
    scroll_area.pack(fill="both", expand=True)
    scroll_area.rowconfigure(0, weight=1)
    scroll_area.columnconfigure(0, weight=1)

    window.scroll_canvas = tk.Canvas(scroll_area, bg="#203e48",
                                     highlightthickness=0)
    window.scroll_canvas.grid(row=0, column=0, sticky="nsew")

    vertical = tk.Scrollbar(scroll_area, orient="vertical",
                            command=window.scroll_canvas.yview)
    vertical.grid(row=0, column=1, sticky="ns")
    horizontal = tk.Scrollbar(scroll_area, orient="horizontal",
                              command=window.scroll_canvas.xview)
    horizontal.grid(row=1, column=0, sticky="ew")
    window.scroll_canvas.config(yscrollcommand=vertical.set,
                                xscrollcommand=horizontal.set)

    content = tk.Frame(window.scroll_canvas, bg="#203e48")
    window.scroll_canvas.create_window(0, 0, window=content, anchor="nw")
    content.bind("<Configure>", lambda event: update_scroll_area(window))
    window.bind("<MouseWheel>", lambda event: scroll_window(event, window))

    if settings.BOARD_SELECTOR_ENABLED and on_board is not None:
        create_board_selector(window, content, on_board)

    create_controls(content)

    window.score_status = tk.Label(content, bg="#203e48", fg="white",
                                    font=("Arial", 12, "bold"))
    window.score_status.pack(pady=(2, 4))

    canvas = tk.Canvas(content, width=480, height=480,
                       borderwidth=0, relief="flat",
                       highlightthickness=0)
    canvas.pack(padx=20, pady=(4, 0))

    create_bottom_panel(window, content)

    # Start at the full interface size, or smaller when the screen cannot fit it.
    window.update_idletasks()
    width = min(content.winfo_reqwidth() + vertical.winfo_reqwidth(),
                max(200, window.winfo_screenwidth() - 80))
    height = min(content.winfo_reqheight() + horizontal.winfo_reqheight(),
                 max(200, window.winfo_screenheight() - 120))
    window.geometry(f"{width}x{height}")

    return window, canvas, window.score_status


def update_scroll_area(window):
    window.scroll_canvas.config(scrollregion=window.scroll_canvas.bbox("all"))


def scroll_window(event, window):
    # Do not scroll when the full interface already fits in the window.
    top, bottom = window.scroll_canvas.yview()
    if top == 0 and bottom == 1:
        return

    if event.delta > 0:
        window.scroll_canvas.yview_scroll(-1, "units")
    elif event.delta < 0:
        window.scroll_canvas.yview_scroll(1, "units")


def create_controls(window):
    controls = tk.Frame(window, bg="#203e48", padx=10, pady=4)
    controls.pack()
    groups = [
        (["N"], "New board"),
        (["Q"], "Quit"),
        *[([str(step)], f"{step} steps") for step in settings.STEP_OPTIONS],
        (["W", "A", "S", "D"], "Move"),
    ]
    for keys, description in groups:
        group = tk.Frame(controls, bg="#203e48")
        group.pack(side="left", padx=4)
        for key in keys:
            tk.Label(group, text=key, bg="#d8e7df", fg="#203e38",
                     font=("Arial", 8, "bold"), width=2,
                     relief="solid", borderwidth=1).pack(side="left", padx=1)
        tk.Label(group, text=description, bg="#203e48", fg="white",
                 font=("Arial", 8)).pack(side="left", padx=(3, 0))


def create_bottom_panel(window, content):
    background = "#203e48"
    panel_colour = "#d8e7df"
    text_colour = "#203e38"

    panel = tk.Frame(content, bg=background, padx=10, pady=4)
    panel.pack()

    legend = tk.Frame(panel, bg=panel_colour, padx=8, pady=6,
                      highlightbackground="black", highlightthickness=3)
    tk.Label(legend, text="TILES & ENTITIES", bg=panel_colour,
             fg=text_colour, font=("Arial", 9, "bold"), anchor="w").grid(
                 row=0, column=0, columnspan=6, sticky="w", pady=(0, 4))

    sprite_directory = Path(__file__).resolve().parent / "sprites"
    entries = [
        ("P  Eco warrior", "Forest Ranger Standing.png", 1, 0),
        ("IPC  Intelligent NPC", "IPC Standing.png", 2, 0),
        ("NPC  Polluter", "Polluter Standing.png", 3, 0),
        ("HF  Healthy forest", "Pixel-Art Forest Clearing.png", 1, 2),
        ("SF  Sick forest", "Diseased Gnarled Forest Clearing.png", 2, 2),
        ("M  Mountain", "Pixel-Art Mountain Tile.png", 3, 2),
        ("L  Lake", "Pixel-Art Lake with Grassy Shore.png", 1, 4),
        ("R  Repair station", "Pixel-Art Tree Care Workshop Stall.png", 2, 4),
    ]
    for text, filename, row, column in entries:
        image = load_sprite(legend, sprite_directory / filename, 22, 22,
                            keep_aspect=True)
        icon = tk.Label(legend, image=image, bg=panel_colour)
        icon.image = image
        icon.grid(row=row, column=column, padx=(0, 4), pady=1)
        description = tk.Frame(legend, bg=panel_colour)
        description.grid(row=row, column=column + 1, sticky="w", padx=(0, 6))
        symbol, name = text.split("  ", 1)
        colours = {"P": "royalblue", "NPC": "firebrick", "IPC": "purple"}
        box = tk.Canvas(description, width=30, height=18,
                        bg=panel_colour, highlightthickness=0)
        box.pack(side="left", padx=(0, 4))
        box.create_rectangle(1, 1, 29, 17,
                             fill=colours.get(symbol, "white"),
                             outline="black")
        box.create_text(15, 9, text=symbol,
                        fill="white" if symbol in colours else "black",
                        font=("Arial", 8, "bold"))
        tk.Label(description, text=name, bg=panel_colour, fg=text_colour,
                 font=("Arial", 8), anchor="w").pack(side="left")

    restart_border = tk.Frame(panel, bg="black", padx=3, pady=3)
    restart = tk.Button(restart_border, text="Restart", bg="firebrick", fg="white",
                        activebackground="#8b1a1a", activeforeground="white",
                        relief="flat", borderwidth=0, font=("Arial", 10, "bold"),
                        cursor="hand2", takefocus=False,
                        command=lambda: restart_game(window))
    restart.pack(ipadx=28, ipady=3)
    restart_border.grid(row=0, column=0, pady=(0, 4))
    legend.grid(row=1, column=0)


def restart_game(window):
    window.focus_set()
    window.event_generate("<KeyPress-n>")


def show_game_over(canvas, message, score):
    canvas.create_rectangle(30, 170, 450, 310, fill="#203e48",
                            outline="black", width=3)
    canvas.create_text(240, 215, text=message, width=380,
                       fill="white", font=("Arial", 16, "bold"),
                       justify="center")
    canvas.create_text(240, 270, text=f"Final score: {score}",
                       fill="white", font=("Arial", 13))


def show_board(canvas, game, number_of_steps):
    canvas.delete("all")
    square_size = 60
    canvas.config(width=len(game.objects[0]) * square_size, height=len(game.objects) * square_size)
    # Keep references on the canvas so Tk retains the images between redraws.
    if not hasattr(canvas, "tile_images"):
        canvas.tile_images = load_tile_images(canvas, square_size)
    if not hasattr(canvas, "player_image"):
        sprite_path = (Path(__file__).resolve().parent / "sprites" /
                       settings.CHARACTERS[settings.CHARACTER]["sprite"])
        canvas.player_image = load_sprite(canvas, sprite_path, 56, 54,
                                          keep_aspect=True)
    if not hasattr(canvas, "npc_image"):
        sprite_path = Path(__file__).resolve().parent / "sprites" / "Polluter Standing.png"
        canvas.npc_image = load_sprite(canvas, sprite_path, 56, 54, keep_aspect=True)
    if not hasattr(canvas, "ipc_image"):
        sprite_path = Path(__file__).resolve().parent / "sprites" / "IPC Standing.png"
        canvas.ipc_image = load_sprite(canvas, sprite_path, 56, 54, keep_aspect=True)
    terrain_symbols = {"HF", "SF", "M", "L", "R"}
    player_colours = {"P": "royalblue", "NPC": "firebrick", "IPC": "purple"}

    for y, row in enumerate(game.objects):
        for x, item in enumerate(row):
            left = x * square_size
            top = y * square_size

            symbol = game.content[y][x]
            canvas.create_image(left, top, anchor="nw",
                                image=canvas.tile_images.get(symbol, canvas.tile_images[None]))
            canvas.create_rectangle(left, top, left + square_size, top + square_size,
                                    outline="black", width=2)
            if symbol in terrain_symbols:
                canvas.create_rectangle(left + 17, top + 3, left + 43, top + 21,
                                        fill="white", outline="black")
                canvas.create_text(left + 30, top + 12, text=symbol,
                                   fill="black", font=("Arial", 11, "bold"))

            if item is not None and item.symbol == "P":
                canvas.create_image(left + 30, top + 58, anchor="s",
                                    image=canvas.player_image)
                canvas.create_rectangle(left + 3, top + 3, left + 17, top + 19,
                                        fill="royalblue", outline="white")
                canvas.create_text(left + 10, top + 11, text="P",
                                   fill="white", font=("Arial", 10, "bold"))
                canvas.create_rectangle(left + 3, top + 41, left + 17, top + 57,
                                        fill="white", outline="black")
                canvas.create_text(left + 10, top + 49, text=number_of_steps,
                                   fill="black", font=("Arial", 10, "bold"))
                if item.repair_kit:
                    canvas.create_rectangle(left + 43, top + 41, left + 57, top + 57,
                                            fill="orange", outline="black")
                    canvas.create_text(left + 50, top + 49, text="T",
                                       fill="black", font=("Arial", 10, "bold"))
            elif item is not None and item.symbol in {"NPC", "IPC"}:
                canvas.create_image(left + 30, top + 58, anchor="s",
                                    image=canvas.npc_image if item.symbol == "NPC" else canvas.ipc_image)
                canvas.create_rectangle(left + 3, top + 3, left + 29, top + 19,
                                        fill=player_colours[item.symbol], outline="white")
                canvas.create_text(left + 16, top + 11, text=item.symbol,
                                   fill="white", font=("Arial", 8, "bold"))
            elif item is not None and item.symbol in player_colours:
                canvas.create_oval(left + 12, top + 20, left + 48, top + 56,
                                   fill=player_colours[item.symbol], outline="white", width=2)
                canvas.create_text(left + 30, top + 38, text=item.symbol,
                                   fill="white", font=("Arial", 10, "bold"))


def create_settings_menu(window, on_difficulty, on_character, on_leaderboard):
    menu = tk.Menu(window)
    options = tk.Menu(menu, tearoff=False)
    difficulty = tk.StringVar(window, value=settings.DIFFICULTY)
    character = tk.StringVar(window, value=settings.CHARACTER)
    for name in settings.DIFFICULTIES:
        options.add_radiobutton(label=name.title(), variable=difficulty, value=name,
                               command=lambda value=name: on_difficulty(value))
    options.add_separator()
    for name in settings.CHARACTERS:
        options.add_radiobutton(label=name, variable=character, value=name,
                               command=lambda value=name: on_character(value))
    menu.add_cascade(label="Settings (starts a new game)", menu=options)
    if settings.LEADERBOARD_ENABLED:
        menu.add_command(label="Leaderboard", command=on_leaderboard)
    window.config(menu=menu)
    window.settings_variables = (difficulty, character)


def create_board_selector(window, content, on_board):
    panel = tk.Frame(content, bg="#203e48")
    panel.pack(pady=4)
    tk.Label(panel, text="Board (starts a new game):", bg="#203e48",
             fg="white").pack(side="left", padx=4)
    window.board_choice = tk.StringVar(window, value=settings.BOARD)
    selector = tk.OptionMenu(panel, window.board_choice, *settings.BOARDS,
                             command=on_board)
    selector.pack(side="left")
