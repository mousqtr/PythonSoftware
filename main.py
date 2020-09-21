import tkinter as tk
from functools import partial
import sqlite3
import pandas as pd
from product import Product
from tools import FrameRight, ButtonLeftText, ButtonTopText
import json

with open('settings.json') as json_file:
    settings = json.load(json_file)
    # print(json.dumps(data, indent = 4, sort_keys=True))
    # print(settings['colors']['title'])


# Custom settings
window_width = settings['dimensions']['window_width']
window_height = settings['dimensions']['window_height']
top_menu_height = settings['dimensions']['top_menu_height']

company_name = settings['company_name']
bg_company_name = settings['colors']['bg_company_name']
bg_top_menu = settings['colors']['bg_top_menu']
bg_left_menu = settings['colors']['bg_left_menu']
bg_connect = settings['colors']['bg_connect']
bg_identification = settings['colors']['bg_identification']

font_company_name = settings['font']['font_company_name']
font_menu = settings['font']['font_menu']


font_size_company_name = settings['font_size']['font_size_company_name']
font_size_menu = settings['font_size']['font_size_menu']


# Root initialization
root = tk.Tk()
root.title("Gestionnaire d'inventaire")
root.resizable(False, False)
root.minsize(700, 700)
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
frame_left_width = 200
frame_left = tk.Frame(root, bg=bg_left_menu, width=frame_left_width)
frame_left.grid(row=0, column=0, sticky='news')
frame_left.columnconfigure(0, weight=1)

# Company title
label_company_title = tk.Label(frame_left, text=company_name, bg=bg_company_name, fg="white", height=2)
label_company_title.grid(row=0, sticky='new', pady=(0, 20))
label_company_title.config(font=(font_company_name,font_size_company_name))









# Right frame
frame_right_width = 4*(window_width/5)
frame_right = tk.Frame(root, bg="#e8e8e8", width=frame_right_width)
frame_right.grid(row=0, column=1, sticky='news')
frame_right.columnconfigure(0, weight=1)

frame_top_right_width = 4 * (window_width / 5)
frame_top_right = tk.Frame(frame_right, bg=bg_top_menu, width=frame_top_right_width, height=top_menu_height)
frame_top_right.grid(row=0, column=0, sticky='new')
frame_top_right.columnconfigure(0, weight=1)



# Initialization of the left buttons
DashboardFrame = FrameRight(frame_right, "Dashboard", "#e8e8e8")
Button_dashboard = ButtonLeftText("Dashboard", 1, frame_left, bg_left_menu, (0, 10), DashboardFrame.frame.lift)
Button_user = ButtonLeftText("Utilisateurs", 2, frame_left, bg_left_menu, (0, 10), None)
Button_action = ButtonLeftText("Actions", 3, frame_left, bg_left_menu, (0, 10), None)
Button_help = ButtonLeftText("Aide", 4,frame_left, bg_left_menu, (380, 10), None)


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
    label_login_title = tk.Label(login_window, text="Identification", bg=bg_identification, fg="white")
    label_login_title.grid(row=0, sticky='new', pady=(0, 20))
    font_login_title = settings['font']['font_login_title']
    font_size_login_title = settings['font_size']['font_size_login_title']
    label_login_title.config(font=(font_login_title, font_size_login_title))

    # Username label
    label_username = tk.Label(login_window, text="Username")
    label_username.grid(row=1, sticky='new', pady=(0, 10))
    font_login_username = settings['font']['font_login_username']
    font_size_login_username = settings['font_size']['font_size_login_username']
    label_username.config(font=(font_login_username, font_size_login_username))

    # Username entry
    var_username = tk.StringVar(value='')
    entry_username = tk.Entry(login_window, bg="white", width=30, textvariable=var_username, font=("Consolas", 15))
    entry_username.grid(row=2, pady=(0, 20))

    # Password label
    label_password = tk.Label(login_window, text="Password")
    label_password.grid(row=3, sticky='new', pady=(0, 10))
    font_login_password = settings['font']['font_login_password']
    font_size_login_password = settings['font_size']['font_size_login_password']
    label_password.config(font=(font_login_password, font_size_login_password))

    # Password entry
    var_password = tk.StringVar(value='')
    entry_password = tk.Entry(login_window, bg="white", width=30, textvariable=var_password, font=("Consolas", 15))
    entry_password.grid(row=4, pady=(0, 20))

Button_login = ButtonTopText("Se connecter", 2, frame_top_right, bg_connect, create_login_window)



# First frame
frame_first = tk.Frame(DashboardFrame.frame, bg="white", width=DashboardFrame.frame_width, height=200, highlightthickness=1)
frame_first.config(highlightbackground="grey")
frame_first.grid(row=1, sticky='new', padx=(10, 10), pady=(5, 10))
frame_first.columnconfigure(0, weight=1)

# Second frame
frame_second = tk.Frame(DashboardFrame.frame, bg="white", width=DashboardFrame.frame_width, height=200, highlightthickness=1)
frame_second.config(highlightbackground="grey")
frame_second.grid(row=2, sticky='new', padx=(10, 10), pady=(5, 10))
frame_second.columnconfigure(0, weight=1)


SettingsFrame = FrameRight(frame_right, "Paramètres", "orange")

DashboardFrame.frame.lift()
Button_settings = ButtonLeftText("Paramètres", 5, frame_left, bg_left_menu, (0, 0), SettingsFrame.frame.lift)



def window_resize(event):
    DashboardFrame.frame["width"] = 800 + (root.winfo_width() - window_width)
    SettingsFrame.frame["width"] = 800 + (root.winfo_width() - window_width)


root.bind("<Configure>", window_resize)

print(DashboardFrame.frame_height)
print(SettingsFrame.frame_height)

# Launch the GUI
root.mainloop()
