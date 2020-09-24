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







class Research:
    def __init__(self, p_parent, p_row):
        frame_height = 200
        frame_width = 780
        frame = tk.Frame(p_parent.frame, bg="white", width=frame_width, height=frame_height, highlightthickness=1)
        frame.grid_propagate(False)
        frame.config(highlightbackground="grey")
        frame.grid(row=p_row, column=0, pady=(5, 5))
        frame.update_idletasks()  # to display good dimensions with .winfo_width()
        frame.columnconfigure((0, 1, 2, 3), weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure((1, 2), weight=4)

        self.title = tk.Label(frame,text="Paramètres", bg="#333333",fg="white", compound="c", borderwidth=1, relief="raised")
        self.title.grid(row=0, column=0, columnspan=5, sticky="nwe", ipadx=10, ipady=5)
        self.title.config(font=("Calibri bold", 12))

        self.nb_column = 4
        self.nb_row = 2
        self.buttons = [[tk.Button() for j in range(0, self.nb_column)] for i in range(0, self.nb_row)]
        self.button_width = int(frame_width/self.nb_column)
        self.button_height = int((frame_height/self.nb_row)/16)
        for i in range(0, self.nb_row):
            for j in range(0, self.nb_column):
                self.buttons[i][j] = tk.Button(frame, width=self.button_width, height=self.button_height, text=" ", fg="white")
                self.buttons[i][j].grid(row=i+1, column=j, padx=(10, 10), pady=(10, 10))
                self.buttons[i][j].config(font=("Calibri bold", 10))
                # self.buttons[i][j]['command'] = partial(choose_data, p_parent, i, j, self)


