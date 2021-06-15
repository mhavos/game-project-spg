import os
from game import Game
import tkinter
import pickle

def menu():
    menu_window = tkinter.Tk()
    menu_window.title("Menu")

    def start(load):
        menu_window.destroy()
        if not load:
            game1 = Game()
            game1.init()
            game1.start()
        else:
            game2 = load_game()
            game2.init_drawer()
            game2.start()

    def open_rules():
        os.system("rules.md")

    menu_canvas = tkinter.Canvas(menu_window, width=300, height=300, bg="#008000")
    menu_canvas.pack()

    menu_canvas.create_text(150, 70, text="Solitaire", font=("Courier", 30, 'bold'))

    if "gamesave.bin" in os.listdir():
        button0 = tkinter.Button(menu_window, text="Load Game", width=15, command=lambda: start(True))
        button0.place(x=95, y=130)
    button1 = tkinter.Button(menu_window, text="New Game", width=15, command=lambda: start(False))
    button1.place(x=95, y=160)
    button2 = tkinter.Button(menu_window, width=15, text="Rules", command=lambda: os.system("rules.md"))
    button2.place(x=95, y=190)
    button3 = tkinter.Button(menu_window, width= 15, text="Close", command=lambda: menu_window.destroy())
    button3.place(x=95, y=220)
    menu_window.mainloop()

def save_game(saved):
    with open("gamesave.bin", "wb") as file:
        saved_dict = saved.get_dict().copy()
        saved_dict["_drawer"] = None
        pickle.dump(saved_dict, file)
    menu()

def load_game():
    with open("gamesave.bin", "rb") as file:
        saved = pickle.load(file)
    game3 = Game()
    for key in saved:
        if key == "_drawer":
            continue
        game3.get_dict()[key] = saved[key]
    return game3