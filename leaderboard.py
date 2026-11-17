import settings
from datetime import datetime


# Highest score first. If scores are equal, fewest moves first.
def score_order(row):
    return (-row["score"], row["moves"])


def load():
    rows = []

    try:
        with open(settings.LEADERBOARD_FILE, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip() == "":
                    continue

                values = line.strip().split("\t")
                if len(values) != 7:
                    raise ValueError("Each leaderboard line must have seven values")

                row = {
                    "name": values[0],
                    "score": int(values[1]),
                    "moves": int(values[2]),
                    "difficulty": values[3],
                    "character": values[4],
                    "result": values[5],
                    "date": values[6]
                }
                rows.append(row)
    except FileNotFoundError:
        return rows

    rows.sort(key=score_order)
    return rows[:settings.LEADERBOARD_LIMIT]


def record(name, score, moves, result):
    if settings.LEADERBOARD_ENABLED == False:
        return

    rows = load()
    row = {
        "name": name,
        "score": score,
        "moves": moves,
        "difficulty": settings.DIFFICULTY,
        "character": settings.CHARACTER,
        "result": result,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    rows.append(row)
    rows.sort(key=score_order)

    with open(settings.LEADERBOARD_FILE, "w", encoding="utf-8") as file:
        for row in rows[:settings.LEADERBOARD_LIMIT]:
            values = []
            for key in ["name", "score", "moves", "difficulty", "character", "result", "date"]:
                # Keep each game on one line, with tabs separating the values.
                value = str(row[key])
                value = value.replace("\t", " ").replace("\n", " ").replace("\r", " ")
                values.append(value)
            file.write("\t".join(values) + "\n")
