import tkinter as tk
import json
from functools import partial
from tkinter import ttk
import pandas as pd

# xlsx = pd.ExcelFile('excel/Gestion_Parc_Relyens.xlsx')
# df1 = pd.read_excel(xlsx, 'Laptop')
# df2 = pd.read_excel(xlsx, 'Desktop')
#
# def display_data():
#     print(df1.shape)
#     print(df1["Site"])
#     df1.at['C', 'x', ]







class Filter:
    def __init__(self, p_parent, p_row):
        frame_height = 200
        frame_width = 780
        frame = tk.Frame(p_parent.frame, bg="white", width=frame_width, height=frame_height, highlightthickness=1)
        frame.grid_propagate(False)
        frame.config(highlightbackground="grey")
        frame.grid(row=p_row, column=0, pady=(5, 5))
        frame.update_idletasks()  # to display good dimensions with .winfo_width()
        frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.title = tk.Label(frame,text="Filtres", bg="#333333",fg="white", compound="c", borderwidth=1, relief="raised")
        self.title.grid(row=0, column=0, columnspan=4, sticky="nwe", ipadx=10, ipady=1, pady=(0, 0))
        self.title.config(font=("Calibri bold", 12))

        self.nb_column = 4
        self.nb_row = 2
        self.frames_settings = [[tk.Frame() for j in range(0, self.nb_column)] for i in range(0, self.nb_row)]
        self.labels_settings = [[tk.Label() for j in range(0, self.nb_column)] for i in range(0, self.nb_row)]
        self.entry_settings = [[tk.Entry() for j in range(0, self.nb_column)] for i in range(0, self.nb_row)]
        self.var_username = [[tk.StringVar(value='') for j in range(0, self.nb_column)] for i in range(0, self.nb_row)]
        self.frame_entry_width = int(frame_width/self.nb_column)
        self.frame_entry_height = 60
        for i in range(0, self.nb_row):
            for j in range(0, self.nb_column):
                self.frames_settings[i][j] = tk.Frame(frame, width=self.frame_entry_width, height=self.frame_entry_height)
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

        button_validate = tk.Button(frame, width=30, height=1, text="Rechercher")
        button_validate.config(font=("Calibri", 10))
        button_validate.grid(row=4, column=0, columnspan=4, sticky="ne", padx=10)

    def configure_settings(self, p_row, p_column, p_text):
        self.labels_settings[p_row][p_column]['text'] = p_text


