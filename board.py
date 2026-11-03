class Board:
    def __init__(self,file):
        self.content = []

        with open(file, 'r') as f:
            for line in f:
                lines = line.strip().split(',')
                row = []

                for value in lines:
                    if value == '-':
                        row.append(None)
                    else:
                        row.append(value)

                self.content.append(row)

#======= print each line one by one ========================== 
    def __str__(self):
        result  = ""
        for i in self.content:
            result += str(i) + "\n"
        return result

    def printBoard(self):
        for i in self.content:
            print(i)