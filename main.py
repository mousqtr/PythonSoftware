import tkinter as tk
from functools import partial
import sqlite3
import pandas as pd
from product import Product


# Custom settings
color_title = "#602320"
color_window = "#979aaa"
color_headers = "#eb8c00"
color_left_menu = "#333333"
window_width = 1000
window_height = 700
title_font = ("Calibri bold", 16)
menu_font = ("Calibri bold", 14)


# Root initialization
root = tk.Tk()
root.title("Gestionnaire d'inventaire")
root.resizable(False, False)
root.config(bg=color_window)
window_icon = tk.PhotoImage(file="inventory.png")
root.iconphoto(False, window_icon)

# Window size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

# Window grid
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Left menu
frame_left_width = window_width/5
frame_left = tk.Frame(root, bg=color_left_menu, width=frame_left_width)
frame_left.grid(column=0, sticky='news')
frame_left.columnconfigure(0, weight=1)

# Main frame
frame_main_width = 4*(window_width/5)
frame_main = tk.Frame(root, bg=color_window, width=frame_main_width)
frame_main.grid(column=1, sticky='news')
frame_main.grid_rowconfigure(0, weight=1)
frame_main.columnconfigure(0, weight=1)

# Left title
label_title = tk.Label(frame_left, text="Nom entreprise", bg="#DCDCDC", fg="black")
label_title.grid(row=0, sticky='new', pady=(0,20))
label_title.config(font=title_font)


class Button_menu():
    def __init__(self, text, num_row):
        self.button = tk.Button(frame_left, text=text, bg=color_left_menu, fg="white", activebackground="red", borderwidth=0)
        self.button.grid(row=num_row, sticky='new', pady=(0, 10))
        self.button.config(font=menu_font)
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.button['background'] = 'green'

    def on_leave(self, e):
        self.button['background'] = color_left_menu


Button_1 = Button_menu("Tableau de bord", 1)
Button_2 = Button_menu("Produits", 2)
Button_3 = Button_menu("Historiques", 3)





# # Main title
# label_title = tk.Label(frame_main, text="Gestion de stock", bg=color_title, fg="white")
# label_title.grid(row=0, sticky='new')
# label_title.config(font=("Consolas", 30))
#
# # Research section
# frame_research = tk.Frame(frame_main, bg=color_window)
# frame_research.grid(row=1, sticky='new', pady=20, padx=10)
#
# label_reference = tk.Label(frame_research, text="Référence", fg="white", bg=color_window)
# label_reference.grid(row=0, column=0, padx=(200,5))
# label_reference.config(font=("Consolas", 15))
#
# entry_var = tk.StringVar(value='')
# entry_research = tk.Entry(frame_research, bg="white", width=30, textvariable=entry_var, font=("Consolas", 15))
# entry_research.grid(row=0, column=1, padx=(5, 15))
#
#
# label_research = tk.Button(frame_research, text="Rechercher", fg="black", width=30)
# label_research.grid(row=0, column=2, padx=(10, 5))
# label_research.config(font=("Consolas", 12))



# Launch the GUI
root.mainloop()
