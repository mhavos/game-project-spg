import os
from game import Game
import tkinter

def menu(saved_game):
    menu_window = tkinter.Tk()
    menu_window.title("Menu")

    def start(load_game):
        menu_window.destroy()
        if not saved_game or not load_game:
            game1 = Game()
        else:
            game2 = saved_game
            game2.init_drawer()
            game2.start()
            print("saved")

    def open_rules():
        os.system("rules.txt")

    menu_canvas = tkinter.Canvas(menu_window, width=300, height=300, bg="#008000")
    menu_canvas.pack()

    menu_canvas.create_text(150, 70, text="Solitaire", font=("Courier", 30, 'bold'))
    if saved_game:
        button0 = tkinter.Button(menu_window, text="Load Game", width=15, command=lambda: start(True))
        button0.place(x=95, y=130)
    button1 = tkinter.Button(menu_window, text="New Game", width=15, command=lambda: start(False))
    button1.place(x=95, y=160)
    button2 = tkinter.Button(menu_window, width=15, text="Rules", command=lambda: os.system("rules.txt"))
    button2.place(x=95, y=190)
    button3 = tkinter.Button(menu_window, width= 15, text="Close", command=lambda: menu_window.destroy())
    button3.place(x=95, y=220)
    menu_window.mainloop()
menu(None)
