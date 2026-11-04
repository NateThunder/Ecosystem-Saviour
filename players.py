from items import BoardItem
import board

class Player(BoardItem):
    def __init__(self, x: int, y: int, symbol: str):
        super().__init__(x,y,symbol)

    def __str__(self):
        return self.symbol

class NPC(BoardItem):
    def __init__(self, x: int, y: int, symbol: str):
        super().__init__(x,y,symbol)

    def __str__(self):
        return self.symbol

class Inteligent_NPC(NPC):
    def __init__(self, x: int, y: int, symbol: str):
        super().__init__(x,y,symbol)

    def __str__(self):
        return self.symbol