"""Edit these values before running controller.py. No extra packages needed."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
# Choose the starting board here, even when the in-game selector is hidden.
BOARD = "Board 1"
BOARD_SELECTOR_ENABLED = True
BOARDS = {
    "Board 1": "board1.txt",
    "Board 2": "board2.txt",
    "Board 3": "board3.txt",
    "Board 4": "board4.txt",
}
# Number of columns (X) and rows (Y), not the last coordinate.
# Smaller sizes crop the map; larger sizes add empty squares.
BOARD_SIZE_X = 8
BOARD_SIZE_Y = 8
DIFFICULTY = "easy"
DIFFICULTIES = {
    "easy": {"move_limit": 150, "npc_count": 1, "ipc_count": 0, "enemy_steps": (1, 2)},
    "normal": {"move_limit": 100, "npc_count": 2, "ipc_count": 1, "enemy_steps": (1, 3)},
    "hard": {"move_limit": 60, "npc_count": 3, "ipc_count": 2, "enemy_steps": (2, 3)},
    "standard":{"move_limit": 20, "npc_count": 2, "ipc_count": 1, "enemy_steps": (1, 3)},

}

# Add another entry to offer another playable character. Keep the board symbol P.
CHARACTER = "Ranger"
CHARACTERS = {
    "Ranger": {"sprite": "Forest Ranger Standing.png", "starts_with_kit": False},
    "Medic": {"sprite": "Forest Ranger Standing.png", "starts_with_kit": True},
}
STEP_OPTIONS = (1, 2, 3)  # Single-digit keyboard shortcuts, from 1 to 9.
HEAL_POINTS = 1
WIN_BONUS = 2
# Set to True to show the menu bar.
SETTINGS_BAR_ENABLED = False
# Set to True to show the leaderboard and save completed scores.
LEADERBOARD_ENABLED = False
LEADERBOARD_FILE = BASE_DIR / "leaderboard.txt"
LEADERBOARD_LIMIT = 10
PLAYER_NAME = "Player"


def difficulty():
    return DIFFICULTIES[DIFFICULTY]


def board_file():
    return BASE_DIR / BOARDS[BOARD]
