# Ecosystem Saviour progress

This checklist reflects the current code. Update it as you build and check each feature.

## To do
### A — Finish board setup

- [x] Create an 8×8 setup file in `board.txt`.
- [x] Read comma-separated board rows from a file.
- [x] Store the file values in `Board.content`, using `None` for empty squares.
- [x] Create an 8×8 `Board.objects` grid.
- [x] Define `BoardItem` with position and symbol attributes.
- [x] Define mountain, lake, forest, and repair-station classes using inheritance.
- [x] Store healthy/sick state on forest objects.
- [x] Create board-item objects through `Board_map()` and store them at `[y][x]`.
- [x] Find and print coordinates for a chosen board-item code.
- [x] Add basic textual display methods for the board rows.
- [x] Define player, ordinary NPC, and intelligent NPC classes.
- [x] Write a small manual test script for board creation and forest locations.
- [x] Create the player at `(0, 0)` and store the player object in `Board.objects[0][0]`.
- [x] Create two ordinary NPCs and one intelligent NPC on random valid free squares, avoiding the player and each other.
- [x] Check `board.txt` is 8 rows of 8 values and contains 4 mountains, 4 lakes, 5 healthy forests, 3 sick forests, and 3 repair stations.

### B — Textual board display

- [x] Display the object grid through `__str__()` and `print(game1)`, showing board-item symbols and `-` for empty squares.
- [x] Include the player (`P`), two ordinary NPCs (`NPC`), and intelligent NPC (`IPC`) in the display.
- [ ] Make sure the display reflects changes to the game objects.

`Board_map()` creates and places the objects; `__str__()` reads `Board.objects` to build the display. `printBoard()` still prints `Board.content`, the original file values. Changes to object symbols will appear through `__str__()`; movement and forest-state changes still need checking once implemented. Changing a forest's `health` alone does not currently update its symbol.

### C — Player movement

- [ ] Add movement behaviour to the model, preferably `Player.move()`.
- [ ] Handle `u`, `d`, `l`, and `r` with a distance of at most 3 in the text controller.
- [ ] Allow `q` to quit.
- [ ] Move one square at a time, stopping at edges, mountains, and lakes.

### D — Ordinary NPC movement

- [ ] Choose a random direction and distance from 1 to 3 for each ordinary NPC.
- [ ] Move NPCs one square at a time, respecting edges and fixed obstacles.

### E — Materials and forest interactions

- [ ] Decide where to store whether the player is carrying materials.
- [ ] Initialise any material-status attributes before reading them.
- [ ] Collect materials when entering a repair station; keep one bag if already carrying it.
- [ ] Repair a sick forest when carrying materials, consume the materials, and add 1 point.
- [ ] Preserve materials when entering a healthy forest.
- [ ] Award the 2-point bonus for repairing all sick forests.
- [ ] Make a polluter turn a healthy forest sick when entering its square.

### F — Turns and game over

- [ ] Start with 20 turns and track the turns remaining.
- [ ] End immediately when either the player or an NPC moves onto the other.
- [ ] End immediately when the player enters a sick forest without materials.
- [ ] End at the turn limit and report the score.

### G — Intelligent NPC

- [ ] Add movement towards healthy forests or the player using the NPC subclass.

### H — Organisation and checking

- [ ] Keep game state and rules in the Model, display in the View, and input handling in the Controller.
- [ ] Review names, comments, and unused variables as the code develops.
- [ ] Check movement at edges, obstacles, and intermediate squares.
- [ ] Check materials, forest changes, scoring, and each game-over condition.
- [ ] Practise explaining what each class and method does.
- [ ] Use only Python Standard Library modules.

### I and J — Tkinter GUI, after the textual game works

- [ ] Draw the board using images.
- [ ] Add mouse or keyboard movement input.
- [ ] Connect GUI input and display to the existing game model.

## Latest check — 4 November 2026

- Ran `python test.py` successfully: `print(game1)` displays `P` at the top-left, two `NPC` symbols and one `IPC`, followed by the three sick-forest coordinates.
- `Board_map()` collects empty-square coordinates and chooses three different entries for the NPCs. The player is placed first, so its square is excluded.
- The intelligent NPC inherits from `NPC`; its distinct movement behaviour is still to be added.
- Phase A setup is implemented for the current board file. Repeated calls to `Board_map()` have not been checked; use it once for initial setup for now.
- Movement, interactions, scoring, turns, and game-over rules remain unimplemented.

## Current focus

- [ ] Begin Phase C: decide how `Player.move()` will change the player's position and keep `Board.objects` consistent, then work on one-square movement before longer moves.
