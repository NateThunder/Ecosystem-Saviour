# Changing Ecosystem Saviour in a practical test

Run `python controller.py`. The Settings menu changes difficulty or character and starts a new game. Edit settings.py for permanent defaults; menu selections last only for the current run.

## Quick changes

| Request | Where to change it |
| --- | --- |
| Change the move limit, enemy count or speed | settings.py: DIFFICULTIES |
| Add a difficulty | Add a dictionary entry to DIFFICULTIES; the menu adds it automatically |
| Add a selectable character | Add an entry to CHARACTERS with sprite filename and starts_with_kit; menu adds it automatically |
| Give a character different movement or powers | Add attributes/behaviour in players.py; a settings entry alone cannot create a new ability |
| Change points | HEAL_POINTS and WIN_BONUS |
| Disable leaderboard | LEADERBOARD_ENABLED = False |
| Change leaderboard size or player name | LEADERBOARD_LIMIT or PLAYER_NAME |
| Change board width and height | BOARD_SIZE_X (columns) and BOARD_SIZE_Y (rows); smaller sizes crop, larger sizes add empty squares |
| Change the map | BOARD and BOARDS, using a rectangular comma-separated map |
| Change step choices | STEP_OPTIONS, using single digits 1 to 9 |

Normal preserves the original 100 moves, two random enemies and one intelligent enemy. Medic uses the existing ranger sprite and begins with a repair kit. Add a PNG in sprites and set its filename to give a character a different appearance. Keep the player symbol P because collisions use it.

The leaderboard records completed wins and losses, not abandoned games. It saves in leaderboard.txt using one game per line and tabs between values, read with open() and split(), ranks score descending then moves ascending, and records difficulty, character, outcome and date. Scores from different difficulties share the same list.

## Possible test tasks based on your notes

These are practice suggestions inferred from your notes, not a prediction of the assessment.

1. **Inheritance and super()** (Class vs Superclass; Week 3 and Week 4): create a new NPC subclass that moves differently. Connect spawning in Board_map and turn handling in controller.py. For a new enemy symbol, update collisions and drawing too.
2. **Object attributes and references** (User-Defined Data Types; Week 3 Objects): add health, lives or repair-kit capacity to Player; explain how changing an object affects the reference stored in the board.
3. **File reading and validation** (Reading files in Python): load another map; reject uneven rows and unknown symbols; test empty and malformed files. Rectangular sizing is now supported, but the map must have an empty top-left player start and enough empty enemy squares.
4. **Sorting lists** (Sorting lists in Python): change leaderboard ordering, show only one difficulty, or keep each player's best score. Start in leaderboard.py.
5. **Dates and times** (Python datetime): display the saved date or add elapsed time and a time bonus.
6. **Loops and enumerate()** (Enumerate): count forests, find all repair stations, or display ranked results starting at 1.
7. **Tkinter widgets and callbacks** (Week 5 GUI 1 and GUI 2): add a player-name Entry, pause button, difficulty dropdown or instructions window. Put widgets in ui.py and game actions in controller.py.
8. **Functions and conditions** (Week 1 lectures/tutorials): alter the win condition, award a bonus for remaining moves, or prevent blocked moves from consuming a turn.
9. **Testing** (Week 7 Testing): write unittest cases for a board edge, collision, healing with/without a kit, the exact move limit and leaderboard ties. Use temporary files and deterministic enemy placement where needed.
10. **Special methods** (Week 4 Python Objects): improve __str__ or add __repr__ to help inspect board items.

## A repeatable approach

Find the rule, change one place, run a normal example, then check its boundaries. Settings hold values; players.py holds movement and interactions; board.py builds the world; ui.py draws it; controller.py connects inputs to actions. New mechanics still need Python behaviour, even when their values live in settings.py.

Existing movement code uses SystemExit to signal a win/loss, caught by the GUI controller. Replacing that with a custom exception is another useful refactoring exercise. The old test.py and test2.py are interactive prototypes, not an automated test suite.

Choose the default map with BOARD (for example "Board 2"). BOARD_SELECTOR_ENABLED controls the independent in-game board dropdown. Add another filename to BOARDS to offer another map.
