# Ecosystem Saviour progress

This checklist reflects the current code. Update it as you build and check each feature.

## To do

### A — Finish board setup

- [X]  Create an 8×8 setup file in `board.txt`.
- [X]  Read comma-separated board rows from a file.
- [X]  Store the file values in `Board.content`, using `None` for empty squares.
- [X]  Create an 8×8 `Board.objects` grid.
- [X]  Define `BoardItem` with position and symbol attributes.
- [X]  Define mountain, lake, forest, and repair-station classes using inheritance.
- [X]  Store healthy/sick state on forest objects.
- [X]  Create board-item objects through `Board_map()` and store them at `[y][x]`.
- [X]  Find and print coordinates for a chosen board-item code.
- [X]  Add basic textual display methods for the board rows.
- [X]  Define player, ordinary NPC, and intelligent NPC classes.
- [X]  Write a small manual test script for board creation and forest locations.
- [X]  Create the player at `(0, 0)` and store the player object in `Board.objects[0][0]`.
- [X]  Create two ordinary NPCs and one intelligent NPC on random valid free squares, avoiding the player and each other.
- [X]  Check `board.txt` is 8 rows of 8 values and contains 4 mountains, 4 lakes, 5 healthy forests, 3 sick forests, and 3 repair stations.

### B — Textual board display

- [X]  Display the object grid through `__str__()` and `print(game1)`, showing board-item symbols and `-` for empty squares.
- [X]  Include the player (`P`), two ordinary NPCs (`NPC`), and intelligent NPC (`IPC`) in the display.
- [X]  Make sure the display reflects changes to the game objects.

`Board_map()` creates and places the objects; `__str__()` reads `Board.objects` to build the display. `printBoard()` reads `Board.content`, which now also records forest repairs. Repair logic updates the forest symbol and health together. Full movement/display checking remains open; the previous `you_win` argument mismatch has been corrected.

### C — Player movement

- [X]  Add one-square movement behaviour to `Player.Move()` in `players.py` (code reviewed; interactive behaviour not tested).
- [X]  Handle WASD movement with a selected distance of 1-3 in the text controller (code reviewed; interactive checking remains). The student reports that the lecturer accepts WASD instead of the brief's example controls.
- [X]  Allow `q` to quit (code reviewed; interactive behaviour not tested).
- [X]  Prototype one-square movement with W/A/S/D in `test.py`, updating player coordinates and the object grid.
- [X]  Add board-edge checks to the movement prototype (code reviewed; interactive behaviour not tested).
- [X]  Stop one-square movement before mountains and lakes (code reviewed; interactive behaviour not tested).
- [X]  Add restoration helpers for repair stations and healthy forests, including repaired forests (previous helper checks passed; complete movement still needs checking).

### D — Ordinary NPC movement

- [X]  Choose a random direction and distance from 1 to 3 for each ordinary NPC (code reviewed; full interactive checking remains).
- [X]  Move ordinary NPCs one square at a time with edge and mountain/lake checks (code reviewed). Terrain preservation and NPC overlap still need checking.

### E — Materials and forest interactions

- [X]  Store whether the player carries materials in `Player.repair_kit`.
- [X]  Initialise `self.repair_kit = False` in `Player.__init__()`.
- [X]  Add collection logic that sets `repair_kit` to `True` on entering R, keeping one bag if already carrying it (code reviewed; not interactively tested).
- [ ]  Repair a sick forest when carrying materials, consume the materials, and add 1 point.
- [X]  Preserve materials when entering a healthy forest (code reviewed; not interactively tested).
- [ ]  Award the 2-point bonus for repairing all sick forests.
- [ ]  Make a polluter turn a healthy forest sick when entering its square.

### F — Turns and game over

- [X]  Add a movement-command counter and display 20 minus the count (code reviewed; turn-limit behaviour still needs checking).
- [ ]  Complete collision handling for both NPC types and for either actor moving onto the other. Player movement onto either `NPC` or `IPC` exits the program. Ordinary NPC movement now checks for `P` before each step in all four directions and exits on collision. IPC movement is not yet implemented; deterministic collision checking remains.
- [X]  Add immediate exit when entering a sick forest without materials (helper checked; full game integration still needs checking).
- [ ]  End at the turn limit and report the score.

### G — Intelligent NPC

- [ ]  Add movement towards healthy forests or the player using the NPC subclass.

### H — Organisation and checking

- [ ]  Keep game state and rules in the Model, display in the View, and input handling in the Controller.
- [ ]  Review names, comments, and unused variables as the code develops.
- [ ]  Check movement at edges, obstacles, and intermediate squares.
- [ ]  Check materials, forest changes, scoring, and each game-over condition.
- [ ]  Practise explaining what each class and method does.
- [ ]  Use only Python Standard Library modules.

### I and J — Tkinter GUI, after the textual game works

- [ ]  Draw the board using images.
- [ ]  Add mouse or keyboard movement input.
- [ ]  Connect GUI input and display to the existing game model.

## Latest review - 10 November 2026

Reviewed `test.py`, `players.py`, `board.py`, and `items.py`. This update records code inspection, not a complete interactive test or a mark estimate.

### New progress

- `NPC_Locations(game)` scans `game.objects` and returns actual ordinary NPC objects rather than coordinates. Its standalone function signature is corrected.
- The controller loops over those objects, chooses one random direction and distance of 1-3 for each, and calls `npc.Move(...)` once per requested step.
- `NPC.Move()` clears its previous grid square, checks boundaries and fixed obstacles, changes coordinates, and stores the NPC in the resulting square.
- NPC movement calls `encounters_player()` before each permitted step in all four directions. The player symbol check now correctly uses uppercase `P`.
- Player movement still checks for both `NPC` and `IPC` before each step.
- `re_render_npc()` displays the board without accessing the player-only `repair_kit` attribute.
- Pollution now records `SF` in `game.content`; sick-forest restoration creates a forest with `health=False`. These changes were reviewed in code, not interactively tested.

### Current issues and remaining work

- Pollution now updates `game.content`, so newly polluted forest locations are recorded for restoration. In the saved file, `healthy_forest_location()` still creates `Forest(x, y, "SF", True)`; change the health argument to `False`. `replace_sick_forest()` already uses `False`. Check an NPC entering and leaving a healthy forest before marking pollution complete.
- NPC movement now blocks squares containing `NPC` or `IPC`, preventing direct overwriting of other NPCs (code reviewed; not interactively tested). The student has chosen to block repair stations (`R`) too. The brief does not explicitly settle NPC entry into repair stations; record this as a design choice, not a confirmed requirement or a required correction.
- Player repair updates symbol, health, and content and consumes materials, but complete repair routes still need checking. No repair points or completion bonus are implemented.
- `NPC_Locations()` currently includes only `NPC`, so IPC stays still. The intelligent subclass exists but has no targeting behaviour yet.
- The student reports that the lecturer accepts WASD instead of the brief's example controls. Keep the chosen WASD mapping; it is not an outstanding correction. Input currently selects distance before direction.
- Both movement loops keep attempting steps after a blocked step, rather than explicitly ending that movement request.
- Turn-limit checks run during redraw after each step. Turn 20 can therefore end a multi-step player command after its first step and before NPC movement.
- N creates a board without resetting turns or selected distance.
- `you_win()` exits when no sick forests remain; the required 2-point bonus is not implemented. Game-over messages do not report a score.
- The final NPC redraw shows NPC coordinates and clears the player's repair-kit message.
- Model and View are still mixed: movement methods call terminal redraw and game-over helpers exit the program directly. Input is handled in `test.py` as the Controller.
- The non-Windows input branch references `sys`, `termios`, and `tty` without importing them in `test.py`.
- No Tkinter GUI is implemented in the reviewed files.

## Current focus

- [ ]  Keep forest symbol, health, and `game.content` consistent when an NPC pollutes a forest.
- [ ]  Check an NPC entering and leaving healthy and sick forests. Check that repair stations remain blocked under the chosen design.
- [ ]  Check ordinary NPC movement onto the player from each direction and on an intermediate step.
- [ ]  Check that an NPC attempting to enter another NPC's square stops without either NPC disappearing; blocking checks are now present.
- [ ]  Check player repair routes, then add scoring and the completion bonus.
- [ ]  Finish blocked-step handling, complete-turn timing, and new-game reset. WASD controls are accepted according to the lecturer clarification reported by the student.
- [ ]  Add intelligent movement after ordinary NPC behaviour is understood and checked.
- [ ]  Continue the textual game before starting the GUI.
