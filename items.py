class boardItems:
    def __init__(self, x: int, y: int, symbol: str):
        self.x = x
        self.y = y
        self.symbol = symbol



class obstacle(boardItems):
    def __init__(self, obst):
        self.obst = obst


    def isObstabcle(self, obj):
        if obj in ["M","L"]:
            return True

    def __str__(self):
        pass



class repairStation(boardItems):
    def __init__(self, obtained: bool):
            self.obtained = obtained

    def pickUpItem(self):
        self.obtained = True

    def __str__(self):
        return f"Holding item?: {str(self.obtained)}"
    
    def itemStatus(self):
        print(f"Holding item?: {str(self.obtained)}")
    

        


class repairMaterials(boardItems):
    def __init__(self, used: bool):
        self.used = used

    def __str__(self):
        return f"Used Item?: {str(self.used)}"

    def itemStatus(self):
        print(f"Used Item?: {str(self.used)}")

    def useItem(self):
        self.used = True