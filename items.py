class BoardItem:
    def __init__(self, x: int, y: int, symbol: str):
        self.x = x
        self.y = y
        self.symbol = symbol



class Forest(BoardItem):
    def __init__(self,  x: int, y: int, type: str):
        super().__init__(x,y, symbol=type)

class Lake(BoardItem):
    def __init__(self,  x: int, y: int, type: str):
        super().__init__(x,y, symbol=type)

class Mountain(BoardItem):
    def __init__(self,  x: int, y: int, type: str):
        super().__init__(x,y, symbol=type)


class RepairStation(BoardItem):
    def __init__(self,  x: int, y: int, symbol: str):
        super().__init__(x,y, symbol)
            

    def pickUpItem(self):
        self.obtained = True

    def __str__(self):
        return f"Holding item?: {str(self.obtained)}"
    
    def itemStatus(self):
        print(f"Holding item?: {str(self.obtained)}")
    

        


class RepairMaterials(BoardItem):
    def __init__(self, x: int, y: int, symbol: str):
        super().__init__(x,y, symbol)

    def __str__(self):
        return f"Used Item?: {str(self.used)}"

    def itemStatus(self):
        print(f"Used Item?: {str(self.used)}")

    def useItem(self):
        self.used = True