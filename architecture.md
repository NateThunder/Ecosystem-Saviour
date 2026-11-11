# How your game connects

## Quick map: files -> classes -> methods and functions

A **method** is a function defined inside a class. A **standalone function** is defined outside a class. Indentation in this tree shows which class each method belongs to.

```text
Ecosystem-Saviour/
|
+-- board.py [mostly Model; display methods are View]
|   +-- class Board
|       +-- __init__(self, file)       Read file; create content and objects lists
|       +-- Board_map(self)            Create terrain, player and NPC objects
|       +-- Element_location(self, element)  Print matching starting positions
|       +-- __str__(self)              Return current board as text [View]
|       +-- printBoard(self)           Print starting content [View]
|
+-- items.py [Model]
|   +-- class BoardItem
|   |   +-- __init__(self, x, y, symbol)  Store x, y and symbol
|   +-- class Mountain(BoardItem)
|   |   +-- __init__(self, x, y, symbol)
|   |   +-- __str__(self)              Return symbol
|   +-- class Lake(BoardItem)
|   |   +-- __init__(self, x, y, type)
|   |   +-- __str__(self)              Return symbol
|   +-- class Forest(BoardItem)
|   |   +-- __init__(self, x, y, symbol, health)  Also store health
|   |   +-- __str__(self)              Return symbol
|   +-- class Repair_station(BoardItem)
|   |   +-- __init__(self, x, y, symbol)
|   |   +-- pickUpItem(self)           Set obtained to True
|   |   +-- __str__(self)              Return symbol
|   |   +-- itemStatus(self)           Print obtained
|   +-- class RepairMaterials(BoardItem)
|       +-- __init__(self, x, y, symbol)
|       +-- __str__(self)              Return text containing used
|       +-- itemStatus(self)           Print used
|       +-- useItem(self)              Set used to True
|
+-- players.py [mostly Model; re_render also handles View]
|   +-- class Player(BoardItem)
|   |   +-- __init__(self, x, y, symbol)  Also set repair_kit to False
|   |   +-- __str__(self)              Return symbol
|   |   +-- Move(self, objects, direction, game)
|   +-- class NPC(BoardItem)
|   |   +-- __init__(self, x, y, symbol)
|   |   +-- __str__(self)              Return symbol
|   +-- class Inteligent_NPC(NPC)
|   |   +-- __init__(self, x, y, symbol)
|   |   +-- __str__(self)              Return symbol
|   |
|   +-- standalone functions (outside all classes)
|       +-- has_repair_kit(self, objects)       Collect materials on R
|       +-- use_repair_kit(self, objects)       Repair SF with materials
|       +-- encounters_npc(self, objects, direction)  Exit on collision
|       +-- re_render(self, game, objects)     Store player and refresh display
|
+-- test.py [Controller and some View]
|   +-- standalone functions (no classes in this file)
|   |   +-- no_enter()                Read a key
|   |   +-- display()                 Create and display a new board
|   |   +-- show(game)                Print a board
|   |   +-- find_object()             Empty placeholder: pass
|   +-- main while loop               Call functions and Player.Move
|
+-- board.txt                         Starting terrain data; no classes/functions
```

`__init__` sets up a newly created object. `__str__` supplies text when Python uses `str(object)` or `print(object)`.

## Each object's class chain

Read these arrows as **is a kind of**, not as function calls. `object` is Python's built-in base class.

```text
Mountain object       -> Mountain       -> BoardItem -> object
Lake object           -> Lake           -> BoardItem -> object
Healthy forest object -> Forest         -> BoardItem -> object
Sick forest object    -> Forest         -> BoardItem -> object
Repair station object -> Repair_station -> BoardItem -> object
Repair materials      -> RepairMaterials -> BoardItem -> object
Player object         -> Player         -> BoardItem -> object
Ordinary NPC object   -> NPC            -> BoardItem -> object
Intelligent NPC object -> Inteligent_NPC -> NPC -> BoardItem -> object
Board object (game)   -> Board          -> object
```

Healthy and sick forests use the **same class**, with different attribute values. `Board_map` currently creates two ordinary NPC objects from the same `NPC` class. It does not currently create any `RepairMaterials` objects; materials are tracked using `Player.repair_kit` instead.

For an intelligent NPC, the setup calls follow this chain:

```text
Inteligent_NPC.__init__
    -> super().__init__ calls NPC.__init__
        -> super().__init__ calls BoardItem.__init__
            -> stores x, y and symbol on that same intelligent NPC object
```

This creates **one object**, not a separate object for each parent class.

## Function call chains: who calls whom?

These arrows mean **calls**, unlike the inheritance arrows above. Branches show possible calls; they are not all performed on every key press.

```text
test.py: main while loop
|
+-- display()                         At startup or when restarting
|   +-- Board("board.txt")            Runs Board.__init__
|   +-- game.Board_map()
|   |   +-- Mountain(...)             Runs Mountain.__init__ -> BoardItem.__init__
|   |   +-- Lake(...)                 Runs Lake.__init__ -> BoardItem.__init__
|   |   +-- Forest(...)               Runs Forest.__init__ -> BoardItem.__init__
|   |   +-- Repair_station(...)       Runs its __init__ -> BoardItem.__init__
|   |   +-- Player(...)               Runs Player.__init__ -> BoardItem.__init__
|   |   +-- NPC(...) twice            Each runs NPC.__init__ -> BoardItem.__init__
|   |   +-- Inteligent_NPC(...)       Runs its __init__ -> NPC -> BoardItem setup
|   +-- print(game)
|       +-- Board.__str__()
|           +-- str(item)             Calls each occupied square's __str__
|
+-- no_enter()                        Read input
|
+-- player.Move(...)                  On a movement key
    +-- encounters_npc(...)           If movement is allowed
    |   +-- sys.exit(1)               Only if destination contains an NPC
    +-- has_repair_kit(...)           After changing position
    +-- use_repair_kit(...)           After changing position
    +-- re_render(...)               Also called when movement is blocked
        +-- print(game)
            +-- Board.__str__()
                +-- str(item)
```

Methods/functions not called by the current game loop or its functions: `Board.Element_location`, `Board.printBoard`, `show`, `find_object`, `Repair_station.pickUpItem`, `Repair_station.itemStatus`, and the `RepairMaterials` methods.

The player currently collects materials through the standalone `has_repair_kit` function, **not** through `Repair_station.pickUpItem`. Also, `obtained` and `used` are only created when their setter methods run; reading them before then would cause an attribute error.

This is a map of your **current code**, using your existing names. It does not change your Python files. Notes labelled **to decide** describe things that still need thought, rather than code that already exists.

## 1. Start here: the files

```text
test.py                          Starts and controls the game
   |
   | creates Board("board.txt")
   v
board.py                         Reads the layout and stores the board
   |                     |
   | reads               | creates objects using classes from
   v                     v
board.txt              items.py and players.py
                       Terrain     Player and NPCs
```

Despite its name, `test.py` currently runs the game; it is not an automated test file.

| File | What it currently does |
| --- | --- |
| `board.txt` | Stores the starting terrain as comma-separated symbols. |
| `items.py` | Defines `BoardItem`, mountains, lakes, forests, repair stations and repair materials. |
| `players.py` | Defines the player and NPC classes, plus functions for player interactions and refreshing the screen. |
| `board.py` | Defines `Board`, reads the file, creates and stores objects, and builds text for display. |
| `test.py` | Creates the board, reads keys, asks the player to move, and handles restarting or quitting. |

## 2. Which class inherits from which?

Inheritance means **is a kind of**. It does not mean that one object stores another object.

```text
BoardItem                         items.py: x, y, symbol
   |
   +-- Mountain                   items.py
   +-- Lake                       items.py
   +-- Forest                     items.py: also has health
   +-- Repair_station             items.py
   +-- RepairMaterials            items.py
   +-- Player                     players.py: also has repair_kit
   +-- NPC                        players.py
        +-- Inteligent_NPC        players.py
```

For example, `Player` inherits the setup for `x`, `y` and `symbol` through `super().__init__(...)`. Each player object then stores its own values for those attributes.

`Board` is separate from this tree. It **stores board items**; it is not a kind of board item.

## 3. Where the objects are stored

```text
game --------------------> one Board object
                              |
                              +-- content: starting symbols / None
                              |
                              +-- objects: rows of actual objects / None
                                      |
                                      +-- objects[y][x]
                                               |
                                               v
                                      one object, such as a Player

player ------------------------------> that same Player object
```

- `game.content` is the layout read from the file. It is not updated when the player moves.
- `game.objects` is your current grid of objects. Movement changes this grid.
- `game.objects[y][x]` means **choose row y, then column x**.
- `player = game.objects[0][0]` gives another name to the existing player object. It does not create a second player.

### Creating, storing and changing are different

Your code in `Board.Board_map` does this:

```python
self.objects[0][0] = players.Player(0, 0, "P")
```

The right-hand side **creates** a player. The assignment **stores a reference to it** in the grid.

Later, inside `Player.Move`:

```python
self.x += 1
```

This **changes the player's x attribute**. By itself, it does not move the reference between grid squares. Your movement code also clears the old square and stores the player in the new square.

## 4. What happens when you run the game?

```text
test.py: main loop
   |
   +--> display()
   |      +--> Board("board.txt")       reads starting symbols
   |      +--> game.Board_map()         creates terrain, player and NPCs
   |      +--> print(game)              calls Board.__str__()
   |      +--> returns game
   |
   +--> player = game.objects[0][0]     remembers the player object
   |
   +--> no_enter()                     reads one key
   |
   +--> player.Move(...)
          +--> clears the player's current grid square
          +--> checks direction, edge and obstacles
          +--> encounters_npc(...)     checks the destination for an NPC
          +--> changes x or y
          +--> has_repair_kit(...)     collects materials on R
          +--> use_repair_kit(...)     changes SF to HF if carrying materials
          +--> re_render(...)
                 +--> stores the player in the destination square
                 +--> clears terminal and prints game
```

The action functions below the classes in `players.py` are **standalone functions**, not `Player` methods. Their parameter called `self` receives the player because `Move` explicitly passes it, for example `has_repair_kit(self, objects)`.

## 5. Model, View and Controller (MVC)

MVC describes responsibilities. You do not need to assume that each responsibility already has its own file.

```text
Controller                 Model                         View
reads the player's key --> checks rules and changes --> shows the current state
                           the game state
```

| Responsibility | What belongs here | Where it is now |
| --- | --- | --- |
| Model | Positions, terrain, materials, movement rules and interactions. Eventually also score, turns and game-over state. | Mostly `items.py`, `players.py` and the board storage/setup in `board.py`. |
| View | Turning the board into visible text and showing messages. | `Board.__str__`, `Board.printBoard`, printing in `test.py`, and `re_render` in `players.py`. |
| Controller | Reading input and asking the model to perform the requested action. | Mainly the loop and `no_enter` in `test.py`. |

**Current overlap:** `Player.Move` changes the model but also calls `re_render` to refresh the view. `encounters_npc` checks a game rule, prints a message and exits the program. Those responsibilities are currently mixed together.

`print(game)` uses `Board.__str__`, which reads `objects`. Your separate `printBoard()` method reads `content`, so it displays the starting layout instead of current actor positions.

## 6. Imports: which file depends on which?

An import lets a file use names from another file. This is different from inheritance or storing an object.

```text
test.py ------> board.py, items.py, players.py
board.py -----> items.py, players.py
players.py ---> items.py, board.py
items.py -----> no other project files
```

`board.py` and `players.py` currently import each other: this is called a **circular import**. The `import board` line in `players.py` is currently unused. Passing `game` into `Move` already gives that method access to the board object without that import.

## 7. The main storage question to understand next

**To decide:** how should a square remember its terrain while the player stands on it?

Currently each grid square holds only one object. When the player enters a forest or repair station, `re_render` replaces that square's reference with the player. When the player leaves, `Move` sets it to `None`. The underlying forest or station is therefore lost from `objects`.

`content` still has the starting symbol, but it does not record later repairs. Also, repairing a forest currently changes its `symbol` without changing its `health` attribute.

Before changing the design, trace this example: **player enters R, then leaves R. What should remain in that square, and where would your program remember it?**

## 8. What is not implemented yet?

These are remaining model/controller behaviours, not extra classes that this document requires you to create:

- NPC movement and forest pollution; the NPC classes currently only initialise and display themselves.
- Intelligent movement; `Inteligent_NPC` inherits from `NPC` but has no different movement behaviour yet.
- Score, repair bonus, turn limit and ending the game on an unrepairable sick forest.
- Distance input and movement of up to three squares, checking each square along the way. Your current controller requests one square per key press.

Keep working on the textual game before adding the GUI. The immediate architecture question is how to preserve terrain when actors move over it.
