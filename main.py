import tkinter as tk
import json
from functools import partial
import sqlite3
import pandas as pd
from product import Product

from gui import FrameContent, ButtonLeftText, ButtonTopText
from login import Login
from widgets import Summary



with open('settings.json') as json_file:
    settings = json.load(json_file)

# Custom settings
window_width = settings['dimensions']['window_width']
window_height = settings['dimensions']['window_height']
top_menu_height = settings['dimensions']['top_menu_height']
left_menu_width = settings['dimensions']['left_menu_width']

company_name = settings['company_name']
bg_company_name = settings['colors']['bg_company_name']
bg_top_menu = settings['colors']['bg_top_menu']
bg_left_menu = settings['colors']['bg_left_menu']
bg_connect = settings['colors']['bg_connect']

font_company_name = settings['font']['font_company_name']
font_size_company_name = settings['font_size']['font_size_company_name']

# Root initialization
root = tk.Tk()
root.title("Gestionnaire d'inventaire")
root.resizable(False, False)
root.minsize(700, 700)
window_icon = tk.PhotoImage(file="img/inventory.png")
root.iconphoto(False, window_icon)

# Window size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

# Left menu
frame_left = tk.Frame(root, bg=bg_left_menu, width=left_menu_width)
frame_left.grid_propagate(False)
frame_left.grid(row=0, column=0, sticky='ns')
frame_left.columnconfigure(0, weight=1)

# Company title
label_company_title = tk.Label(frame_left, text=company_name, bg=bg_company_name, fg="white", height=2)
label_company_title.grid(row=0, sticky='new', pady=(0, 20))
label_company_title.config(font=(font_company_name, font_size_company_name))

# Right frame (right part of the window)
frame_right_width = window_width - left_menu_width
frame_right = tk.Frame(root, bg="black", width=frame_right_width, height=window_height)
frame_right.grid_propagate(False)
frame_right.grid(row=0, column=1, sticky='n')
frame_right.columnconfigure(0, weight=1)

# Top menu (include in right_frame)
top_menu_width = window_width - left_menu_width
frame_top_menu = tk.Frame(frame_right, bg=bg_top_menu, width=top_menu_width, height=top_menu_height)
frame_top_menu.grid_propagate(False)
frame_top_menu.grid(row=0, column=0, sticky='n')
frame_top_menu.columnconfigure(0, weight=1)

# Initialization of right sub frames (include in right_frame)
Frame_dashboard = FrameContent(frame_right, "Dashboard", "#e8e8e8")
Frame_research = FrameContent(frame_right, "Recherche", "red")
Frame_settings = FrameContent(frame_right, "Paramètres", "#e8e8e8")
Frame_attribution = FrameContent(frame_right, "Attribution", "green")
Frame_help = FrameContent(frame_right, "Aide", "purple")
Frame_dashboard.frame.lift()

# Initialization of the left menu buttons (include in left_frame)
Button_dashboard = ButtonLeftText("Dashboard", 1, frame_left, bg_left_menu, (0, 10), Frame_dashboard.frame.lift)
Button_research = ButtonLeftText("Recherche", 2, frame_left, bg_left_menu, (0, 10), Frame_research.frame.lift)
Button_attribution = ButtonLeftText("Attribution", 3, frame_left, bg_left_menu, (0, 10), Frame_attribution.frame.lift)
Button_help = ButtonLeftText("Aide", 4, frame_left, bg_left_menu, (380, 10), Frame_help.frame.lift)
Button_settings = ButtonLeftText("Paramètres", 5, frame_left, bg_left_menu, (0, 0), Frame_settings.frame.lift)

# Initialization of the top menu buttons (include in frame_top_menu)
Window_login = Login(root)
Button_login = ButtonTopText("Se connecter", 2, frame_top_menu, bg_connect, Window_login.create_login_window)






# First frame
frame_first_width = 780
frame_first = tk.Frame(Frame_dashboard.frame, bg="white", width=frame_first_width, height=200, highlightthickness=1)
frame_first.grid_propagate(False)
frame_first.config(highlightbackground="grey")
frame_first.grid(row=1, sticky='new', padx=10, pady=(5, 10))
frame_first.columnconfigure(0, weight=1)

# Second frame
frame_second = tk.Frame(Frame_dashboard.frame, bg="white", height=395, highlightthickness=1)
frame_second.config(highlightbackground="grey")
frame_second.grid(row=2, sticky='new', padx=(10, 10), pady=(5, 10))
frame_second.columnconfigure(0, weight=1)



Widget_summary = Summary(Frame_settings, 1)



# # Detect the window resize
# def window_resize(event):
#     Frame_dashboard.frame["width"] = 800 + (root.winfo_width() - window_width)
#     Frame_settings.frame["width"] = 800 + (root.winfo_width() - window_width)
#     Frame_actions.frame["width"] = 800 + (root.winfo_width() - window_width)
#
#
# root.bind("<Configure>", window_resize)



# Launch the GUI
root.mainloop()
