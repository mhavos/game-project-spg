import os
from game import Game
import tkinter

menu_window = tkinter.Tk()
menu_window.title("Menu")

def start():
    game1 = Game()

def open_rules():
    os.system("rules.txt")

menu_canvas = tkinter.Canvas(menu_window, width=300, height=300, bg="#008000")
menu_canvas.pack()

menu_canvas.create_text(150, 70, text="Solitaire", font=("Courier", 30, 'bold'))
button1 = tkinter.Button(menu_window, text="New Game", width=15, command=lambda: start())
button1.place(x=95, y=130)
button2 = tkinter.Button(menu_window, width=15, text="Rules", command=lambda: os.system("rules.txt"))
button2.place(x=95, y=160)

menu_window.mainloop()
