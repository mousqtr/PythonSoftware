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


class ButtonLeftText():
    """ Text buttons located in the left of the window """

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


# Initialization of the left buttons
Button_1 = ButtonLeftText("Dashboard", 1)
Button_2 = ButtonLeftText("Produits", 2)
Button_3 = ButtonLeftText("Historique", 3)


# Top menu
frame_top_menu = tk.Frame(frame_right, bg="#13547a", width=frame_right_width, height=32)
frame_top_menu.grid(row=0, sticky='new')
frame_top_menu.columnconfigure(0, weight=1)


class ButtonTopIcon:
    """ Icon buttons located in the top of the window """

    def __init__(self, num_col, p_color_enter, p_color_leave):
        self.button = tk.Button(frame_top_menu, image=settings_icon_blue, height=31, width=31, borderwidth=0)
        self.button.grid(row=0, column=num_col, sticky="e", padx=(0, 0), pady=(0, 0))
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)
        self.color_enter = p_color_enter
        self.color_leave = p_color_leave

    def on_enter(self, e):
        self.button['image'] = self.color_enter

    def on_leave(self, e):
        self.button['image'] = self.color_leave


class ButtonTopText:
    """ Text buttons located in the top of the window """

    def __init__(self, num_col):
        self.button = tk.Button(frame_top_menu, text="Se connecter", bg="#13547a", fg="white", borderwidth=0, command=create_login_window)
        self.button.grid(row=0, column=num_col, sticky="e", padx=(10, 5))
        self.button.config(font=low_font)
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.button['bg'] = '#FFA500'
        self.button['fg'] = 'white'

    def on_leave(self, e):
        self.button['bg'] = "#13547a"
        self.button['fg'] = 'white'


def create_login_window():
    """ Creation of the login window """

    # Window handle
    login_window = tk.Toplevel(root)
    login_window_width = 500
    login_window_height = 250
    x_cord = int((screen_width / 2) - (login_window_width / 2))
    y_cord = int((screen_height / 2) - (login_window_height / 2))
    login_window.geometry("{}x{}+{}+{}".format(login_window_width, login_window_height, x_cord, y_cord))
    login_window.columnconfigure(0, weight=1)

    # Title of the login window
    label_login_title = tk.Label(login_window, text="Identification", bg="#13547a", fg="white")
    label_login_title.grid(row=0, sticky='new', pady=(0, 20))
    label_login_title.config(font=menu_font)

    # Username label
    label_username = tk.Label(login_window, text="Username")
    label_username.grid(row=1, sticky='new', pady=(0, 10))
    label_username.config(font=username_font)

    # Username entry
    var_username = tk.StringVar(value='')
    entry_username = tk.Entry(login_window, bg="white", width=30, textvariable=var_username, font=("Consolas", 15))
    entry_username.grid(row=2,  pady=(0, 20))

    # Password label
    label_password = tk.Label(login_window, text="Password")
    label_password.grid(row=3, sticky='new', pady=(0, 10))
    label_password.config(font=username_font)

    # Password entry
    var_password = tk.StringVar(value='')
    entry_password = tk.Entry(login_window, bg="white", width=30, textvariable=var_password, font=("Consolas", 15))
    entry_password.grid(row=4,  pady=(0, 20))


# Initialization of the top buttons
settings_icon_blue = tk.PhotoImage(file="settings_blue.png")
settings_icon_orange = tk.PhotoImage(file="settings_orange.png")
Button_settings = ButtonTopIcon(0, settings_icon_orange, settings_icon_blue)
Button_login = ButtonTopText(1)

# Main frame
frame_main = tk.Frame(frame_right, bg="#e8e8e8", width=frame_right_width, height=window_height-34)
frame_main.grid(row=2, sticky='new')





# Launch the GUI
root.mainloop()
