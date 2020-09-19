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
low_font = ("Calibri bold", 13)
username_font = ("Calibri", 13)


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
frame_left.grid(row=0, column=0, sticky='news')
frame_left.columnconfigure(0, weight=1)

# Right frame
frame_right_width = 4*(window_width/5)
frame_right = tk.Frame(root, bg="yellow", width=frame_right_width)
frame_right.grid(row=0, column=1, sticky='news')
frame_right.columnconfigure(0, weight=1)

# Left title
label_title = tk.Label(frame_left, text="Nom entreprise", bg="#13547a", fg="white")
label_title.grid(row=0, sticky='new', pady=(0, 20))
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


Button_1 = Button_menu("Dashboard", 1)
Button_2 = Button_menu("Produits", 2)
Button_3 = Button_menu("Historique", 3)


# Top menu
frame_top_menu = tk.Frame(frame_right, bg="#13547a", width=frame_right_width, height=32)
frame_top_menu.grid(row=0, sticky='new')
frame_top_menu.columnconfigure(0, weight=1)

# Top menu - right icon
settings_icon_blue = tk.PhotoImage(file="settings_blue.png")
settings_icon_orange = tk.PhotoImage(file="settings_orange.png")


def on_enter0(e):
    button_setting['image'] = settings_icon_orange


def on_leave0(e):
    button_setting['image'] = settings_icon_blue


settings_icon = tk.PhotoImage(file="settings_blue.png")
button_setting = tk.Button(frame_top_menu, image=settings_icon, height=31, width=31, borderwidth=0)
button_setting.grid(row=0, column=0, sticky="e", padx=(0, 0), pady=(0, 0))
button_setting.bind("<Enter>", on_enter0)
button_setting.bind("<Leave>", on_leave0)


# Top menu - right user name
def on_enter(e):
    button_login['bg'] = '#FFA500'
    button_login['fg'] = 'white'


def on_leave(e):
    button_login['bg'] = "#13547a"
    button_login['fg'] = 'white'




def create_window():
    login_window = tk.Toplevel(root)
    login_window_width = 500
    login_window_height = 250
    x_cord = int((screen_width / 2) - (login_window_width / 2))
    y_cord = int((screen_height / 2) - (login_window_height / 2))
    login_window.geometry("{}x{}+{}+{}".format(login_window_width, login_window_height, x_cord, y_cord))
    login_window.columnconfigure(0, weight=1)

    label_login_title = tk.Label(login_window, text="Identification", bg="#13547a", fg="white")
    label_login_title.grid(row=0, sticky='new', pady=(0, 20))
    label_login_title.config(font=menu_font)

    label_username = tk.Label(login_window, text="Username")
    label_username.grid(row=1, sticky='new', pady=(0, 10))
    label_username.config(font=username_font)

    var_username = tk.StringVar(value='')
    entry_username = tk.Entry(login_window, bg="white", width=30, textvariable=var_username, font=("Consolas", 15))
    entry_username.grid(row=2,  pady=(0, 20))

    label_password = tk.Label(login_window, text="Password")
    label_password.grid(row=3, sticky='new', pady=(0, 10))
    label_password.config(font=username_font)

    var_password = tk.StringVar(value='')
    entry_password = tk.Entry(login_window, bg="white", width=30, textvariable=var_password, font=("Consolas", 15))
    entry_password.grid(row=4,  pady=(0, 20))


button_login = tk.Button(frame_top_menu, text="Se connecter", bg="#13547a", fg="white", borderwidth=0, command=create_window)
button_login.grid(row=0, column=1, sticky="e", padx=(10,5))
button_login.config(font=low_font)
button_login.bind("<Enter>", on_enter)
button_login.bind("<Leave>", on_leave)





# Main frame
frame_main = tk.Frame(frame_right, bg="#e8e8e8", width=frame_right_width, height=window_height-34)
frame_main.grid(row=2, sticky='new')


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
