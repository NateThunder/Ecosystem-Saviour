from items import BoardItem

class Player(BoardItem):
    def __init__(self, x: int, y: int, symbol: str):
        super().__init__(x,y,symbol)

class NPC(BoardItem):
    def __init__(self, x: int, y: int, symbol: str):
        super().__init__(x,y,symbol)

class Inteligent_NPC(NPC):
    def __init__(self, x: int, y: int, symbol: str):
        super().__init__(x,y,symbol)