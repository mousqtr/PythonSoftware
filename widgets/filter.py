import tkinter as tk
import json
from functools import partial
from tkinter import ttk
import pandas as pd


with open('settings.json') as json_file:
    settings = json.load(json_file)

df = pd.read_csv('csv/csv_test.csv')


class Filter:
    def __init__(self, p_parent, p_row):
        frame_height = 200
        frame_width = 780
        self.frame = tk.Frame(p_parent.frame, bg="white", width=frame_width, height=frame_height, highlightthickness=1)
        self.frame.grid_propagate(False)
        self.frame.config(highlightbackground="grey")
        self.frame.grid(row=p_row, column=0, pady=(5, 5))
        self.frame.update_idletasks()  # to display good dimensions with .winfo_width()
        self.frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.title = tk.Label(self.frame,text="Filtres", bg="#333333",fg="white", compound="c", borderwidth=1, relief="raised")
        self.title.grid(row=0, column=0, columnspan=4, sticky="nwe", ipadx=10, ipady=1, pady=(0, 0))
        self.title.config(font=("Calibri bold", 12))

        self.nb_column = 4
        self.nb_row = 2
        self.nb_filtres = self.nb_column * self.nb_row
        self.frames_settings = [[tk.Frame() for j in range(0, self.nb_column)] for i in range(0, self.nb_row)]
        self.labels_settings = [[tk.Label() for j in range(0, self.nb_column)] for i in range(0, self.nb_row)]
        self.entry_settings = [[tk.Entry() for j in range(0, self.nb_column)] for i in range(0, self.nb_row)]
        self.var_username = [[tk.StringVar(value='') for j in range(0, self.nb_column)] for i in range(0, self.nb_row)]
        self.frame_entry_width = int(frame_width/self.nb_column)
        self.frame_entry_height = 60
        for i in range(0, self.nb_row):
            for j in range(0, self.nb_column):
                self.frames_settings[i][j] = tk.Frame(self.frame, width=self.frame_entry_width, height=self.frame_entry_height)
                self.frames_settings[i][j].grid(row=i+1, column=j, padx=(5, 5), pady=(5, 5))
                self.frames_settings[i][j].columnconfigure(0, weight=1)
                self.frames_settings[i][j].rowconfigure((0, 1), weight=1)
                self.frames_settings[i][j].grid_propagate(False)
                self.labels_settings[i][j] = tk.Label(self.frames_settings[i][j], text=" ", borderwidth=1, relief="flat")
                self.labels_settings[i][j].grid(row=0, column=0, sticky='nw')
                self.labels_settings[i][j].config(font=("Calibri bold", 10))
                self.entry_settings[i][j] = tk.Entry(self.frames_settings[i][j], bg="white", width=30, textvariable=self.var_username[i][j])
                self.entry_settings[i][j].grid(row=1, column=0, sticky='nw')
                self.entry_settings[i][j].config(font=("Calibri bold", 10))
                # self.buttons[i][j]['command'] = partial(choose_data, p_parent, i, j, self)

        frame_buttons = tk.Frame(self.frame, height=40, bg="white")
        frame_buttons.grid(row=4, column=0, columnspan=6, sticky="nwe")
        frame_buttons.grid_propagate(False)

        # Button - Settings
        button_settings = tk.Button(frame_buttons, width=20, height=1, text="Paramètres")
        button_settings.config(font=("Calibri", 10))
        button_settings.grid(row=0, column=0, sticky="nw", padx=(40, 300))
        button_settings['command'] = self.settings_window

        # Button - Research
        button_validate = tk.Button(frame_buttons, width=30, height=1, text="Rechercher")
        button_validate.config(font=("Calibri", 10))
        button_validate.grid(row=0, column=1, sticky="ne", padx=10)

    def configure_settings(self, p_row, p_column, p_text):
        self.labels_settings[p_row][p_column]['text'] = p_text

    def settings_window(self):
        # Window handle
        window_settings = tk.Toplevel(self.frame)
        window_settings.resizable(False, False)
        window_settings.title("Paramètres")
        window_icon = tk.PhotoImage(file="img/settings.png")
        window_settings.iconphoto(False, window_icon)
        # login_window_width = settings['dimensions']['window_login_width']
        # login_window_height = settings['dimensions']['window_login_height']
        window_settings_width = 550
        window_settings_height = 300
        screen_width = self.frame.winfo_screenwidth()
        screen_height = self.frame.winfo_screenheight()
        x_cord = int((screen_width / 2) - (window_settings_width / 2))
        y_cord = int((screen_height / 2) - (window_settings_height / 2))
        window_settings.geometry("{}x{}+{}+{}".format(window_settings_width, window_settings_height, x_cord, y_cord))
        window_settings.columnconfigure((0, 1), weight=1)

        # Title - Settings
        bg_identification = settings['colors']['bg_identification']
        label_login_title = tk.Label(window_settings, text="Paramètres", bg=bg_identification, fg="white")
        label_login_title.grid(row=0, columnspan=2, sticky='new', pady=(0, 10))
        font_login_title = settings['font']['font_login_title']
        font_size_login_title = settings['font_size']['font_size_login_title']
        label_login_title.config(font=(font_login_title, font_size_login_title))

        # Title - choice of the columns
        label_login_title = tk.Label(window_settings, text="Choix des filtres")
        label_login_title.grid(row=1, sticky='nw', padx=10, pady=(0, 10))
        label_login_title.config(font=("Calibri bold", 12))

        # Column choice label
        labels_column_choice = [tk.Label() for j in range(self.nb_filtres)]
        combo_column_choice = [ttk.Combobox() for j in range(self.nb_filtres)]
        list_headers = list(df.head())
        list_headers.insert(0, " ")
        for j in range(self.nb_filtres):
            label_text = "Filtre " + str(j + 1)
            labels_column_choice[j] = tk.Label(window_settings, text=label_text)
            labels_column_choice[j].grid(row=j + 2, column=0, sticky='ne', padx=30, pady=1)
            labels_column_choice[j].config(font=("Calibri bold", 10))
            combo_column_choice[j] = ttk.Combobox(window_settings, values=list_headers, state="readonly")
            combo_column_choice[j].grid(row=j + 2, column=1, sticky='nw', padx=10, pady=1)
            combo_column_choice[j].config(font=("Calibri bold", 10))
            combo_column_choice[j].current(0)

        # Button - Validation
        button_validate = tk.Button(window_settings, width=30, height=1, text="Appliquer")
        button_validate.config(font=("Calibri", 10))
        button_validate.grid(row=self.nb_filtres + 2, column=1, sticky="ne", padx=10, pady=(10, 0))
        # button_validate['command'] = partial(self.change_column, combo_column_choice)
