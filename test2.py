from board import Board
import board
import items
import players
import subprocess
import os
import test

def display():
    subprocess.run("cls", shell=True)
    game = Board("board.txt")
    game.Board_map()
    #print(game)
    #print("N for New board, Q for exit: ")
    return game

d = display()
#print(Board.Element_location(d,"SF"))

print(type())




