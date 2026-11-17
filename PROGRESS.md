# Ecosystem Saviour progress

Last updated: 12 November 2026.

This checklist reflects the current code. Checked items mean implemented; full gameplay testing is still outstanding unless explicitly recorded below.

## A - Board setup and objects

- [X] Read comma-separated rows from board.txt, using None for empty squares.
- [X] Create Board.content and Board.objects, indexed using [y][x].
- [X] Define BoardItem and subclasses for mountains, lakes, forests and repair stations.
- [X] Define Player, NPC and Inteligent_NPC classes using inheritance.
- [X] Create the player at (0, 0).
- [X] Place configured enemy counts on distinct random empty squares.
- [X] Reject empty or uneven board rows and insufficient enemy spawn space.
- [X] Configure columns and rows with BOARD_SIZE_X and BOARD_SIZE_Y; crop or extend the map with empty squares, and use the resulting grid for movement boundaries.
- [X] Find terrain coordinates using Element_location() and display the board using __str__().
- [ ] Validate unknown map symbols and the player's starting square.

## B - Player and enemy movement

- [X] Handle WASD and existing U/C/L/R aliases in controller.py.
- [X] Select player movement distance using settings.STEP_OPTIONS, currently 1, 2 or 3.
- [X] Block mountains, lakes and movement beyond board edges.
- [X] Choose an ordinary NPC's random direction and movement distance each turn.
- [X] Use settings enemy_steps for both enemy types.
- [X] Block enemies from entering other enemy squares and repair stations.
- [X] Target the nearest healthy forest or player with the intelligent NPC.
- [X] Move the intelligent NPC towards that target in the GUI controller.
- [ ] Check edge, obstacle, intermediate-step and collision behaviour through complete gameplay.
- [ ] Review blocked-step handling: loops currently keep attempting remaining steps.
- [ ] Review intelligent movement: controller.py chooses a direction once per turn; the alternative intelligent_move() helper is not called there.

## C - Forests, materials and scoring

- [X] Track the player's repair kit and collect it at a repair station.
- [X] Set the starting kit from the selected character.
- [X] Implement healing, kit consumption and settings.HEAL_POINTS.
- [X] Implement settings.WIN_BONUS when no sick forests remain.
- [X] Record repaired and polluted forests in game.content.
- [X] Create polluted forests with health=False.
- [X] Restore forests and repair stations after actors leave their squares.
- [ ] Check complete repair and pollution routes, including terrain hidden under actors.
- [ ] Check kit consumption, points and the completion bonus in full gameplay.

## D - Turns and game over

- [X] Count movement commands and display remaining moves using the chosen difficulty.
- [X] Implement collision loss, sick-forest loss, move-limit loss and victory messages.
- [X] Catch SystemExit in the GUI controller and show the final score on the board.
- [X] Reset moves, step selection, score and game-over state on a new game.
- [X] Support N, the Restart button and Q.
- [ ] Check both actors moving into each other for both enemy types.
- [ ] Review final-turn timing: the move limit is checked during redraw after individual steps, so it can interrupt a multi-step command before enemies move.

## E - Tkinter interface

- [X] Draw terrain and characters using PNG sprites.
- [X] Connect keyboard input to movement and redraw the board after commands.
- [X] Display points, remaining moves, selected steps and repair-kit status.
- [X] Add a Restart button and tiles/entities legend.
- [X] Arrange the legend in three columns with 3, 3 and 2 items; Lake and Repair station are on the right.
- [X] Add vertical and horizontal scrollbars around the whole interface.
- [X] Add mouse-wheel scrolling and choose an initial window size based on the screen.
- [X] Add optional difficulty and character menu choices; selecting one starts a new game.

## F - Settings and leaderboard

- [X] Add settings.py for map path, difficulties, characters, step choices and scoring.
- [X] Configure move limit, random enemy count, intelligent enemy count and enemy movement range per difficulty.
- [X] Add Ranger and Medic choices; Medic starts with a repair kit and currently shares the Ranger sprite.
- [X] Generate menu choices from the difficulty and character dictionaries.
- [X] Add SETTINGS_BAR_ENABLED to show or hide the menu bar.
- [X] Add LEADERBOARD_ENABLED to control score recording and the leaderboard menu entry.
- [X] Save completed wins and losses in leaderboard.txt using open(), loops, split() and write(); the game no longer uses JSON.
- [X] Preserve the existing score when converting to the text format.
- [X] Rank by highest score, then fewest moves, and keep the configured number of entries.
- [X] Store name, score, moves, difficulty, character, result and date.
- [X] Add EXAM_PRACTICE.md with possible changes based on the course notes and the relevant files.

Current defaults: standard difficulty (20 moves, two ordinary NPCs, one intelligent NPC, enemy steps 1-3), Ranger, 1 point per healed forest and a 2-point win bonus. SETTINGS_BAR_ENABLED and LEADERBOARD_ENABLED are both False. Restart the program after editing settings.py. To show the leaderboard menu, enable both switches. Existing scores remain saved when disabled.

## G - Organisation and practical-test preparation

- [X] Use only Python Standard Library modules.
- [X] Keep new work close to the student's existing style, using straightforward functions and text files.
- [X] Guard controller startup with if __name__ == "__main__" so importing it does not launch the GUI.
- [ ] Separate remaining terminal display calls from movement logic in players.py.
- [ ] Consider replacing SystemExit game-over signals with a game-specific exception or return value.
- [ ] Review names, comments and unused imports/variables.
- [ ] Practise explaining and changing each class, method and setting.
- [ ] Add focused automated gameplay checks for boundaries, repairs, pollution and game-over rules.

## Checks completed during this session

- Python syntax parsing and importing controller without launching the game.
- Enemy spawn counts for Easy, Normal and Hard.
- Ranger and Medic starting repair-kit values.
- Rectangular map construction.
- Leaderboard text save/load, score ordering and ties; earlier leaderboard-disable check also passed.
- Existing score conversion from JSON to text.
- Tkinter window and settings-menu construction.
- Small-window scrolling, mouse wheel over the board, reaching the bottom, horizontal scrolling and the restart key.
- Window construction after the legend layout change.
- Import and settings checks after disabling the menu bar and leaderboard.

These were targeted checks, not a complete interactive playthrough or a complete automated test suite. test.py and test2.py remain older interactive prototypes.

## Current focus

- [ ] Play through repair, pollution, collision, victory and move-limit scenarios.
- [ ] Resolve final-turn timing and blocked-step behaviour if required by the brief.
- [ ] Check that terrain and actors remain consistent throughout movement.
- [ ] Practise the changes listed in EXAM_PRACTICE.md while keeping the code understandable and close to the student's style.

## Multiple boards - 12 November 2026

- [X] Add board1.txt through board4.txt; Board 1 copies the original map, which remains in board.txt.
- [X] Choose the default with BOARD in settings.py and list map files in BOARDS.
- [X] Use board_file() to resolve the selected map when starting a game.
- [X] Add an independent BOARD_SELECTOR_ENABLED switch for the in-game dropdown, currently True.
- [X] Start a new game when selecting another board; the selector works with SETTINGS_BAR_ENABLED=False.
- Board size settings still apply to every map. Menu selections last for the current run; edit BOARD for the permanent default.
