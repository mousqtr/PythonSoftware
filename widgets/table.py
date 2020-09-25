import tkinter as tk
import pandas as pd
from functools import partial
import json
from tkinter import ttk


with open('settings.json') as json_file:
    settings = json.load(json_file)

def display_data():
    df = pd.read_csv('csv/csv_test.csv')
    print(df)
    # df.at[0, 'Prenom'] = 'Edouard'
    # print(df)
    # df.to_csv('csv/laptop.csv', index=False)

df = pd.read_csv('csv/csv_test.csv')
nb_row_df = df.shape[0]
nb_column_df = df.shape[1]
nb_column_to_show = 6
column_width = 15
nb_column_max = 6
list_width = [98, 48, 32, 23, 18, 15]
initial_list_columns = [0, 1, 2, 3, 4, 5]
# nb_column = df.shape[1]










class Table:
    def __init__(self, p_parent, p_row):
        frame_height = 400
        frame_width = 780
        self.frame = tk.Frame(p_parent.frame, bg="white", width=frame_width, height=frame_height, highlightthickness=1)
        self.frame.grid_propagate(False)
        self.frame.config(highlightbackground="grey")
        self.frame.grid(row=p_row, column=0, pady=(5, 5))
        self.frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.title = tk.Label(self.frame, text="Table", bg="#333333", fg="white", compound="c", borderwidth=1, relief="raised", height=1)
        self.title.grid(row=0, column=0, columnspan=6, sticky="nwe", ipadx=10, ipady=1)
        self.title.config(font=("Calibri bold", 12))



        self.frame_headers = tk.Frame(self.frame, bg="white")
        self.frame_headers.grid(row=1, padx=40, pady=(10,0))

        # Create a frame for the canvas with non-zero row&column weights
        self.frame_canvas = tk.Frame(self.frame)
        self.frame_canvas.grid(row=2, column=0, padx=(40, 0), pady=(0, 0), sticky='nw')
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)

        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        self.frame_canvas.grid_propagate(False)

        # Add a canvas in that frame
        self.canvas = tk.Canvas(self.frame_canvas, bg="grey")
        self.canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        self.vsb = tk.Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # Create a frame to contain the buttons
        self.frame_buttons = tk.Frame(self.canvas, bg="grey")
        self.canvas.create_window((0, 0), window=self.frame_buttons, anchor='nw')

        self.buttons_header = [tk.Button() for j in range(nb_column_to_show)]
        self.buttons_table = [[tk.Button() for j in range(nb_column_to_show)] for i in range(nb_row_df)]

        self.create_table(nb_column_to_show, column_width, initial_list_columns)

        # Buttons
        frame_buttons = tk.Frame(self.frame, height=40, bg="white")
        frame_buttons.grid(row=3, column=0, columnspan=6, sticky="nwe", pady=(10,0))
        frame_buttons.grid_propagate(False)

        button_settings = tk.Button(frame_buttons, width=20, height=1, text="Paramètres")
        button_settings.config(font=("Calibri", 10))
        button_settings.grid(row=0, column=0, sticky="nw", padx=(40, 0))
        button_settings['command'] = self.settings_window

        button_export = tk.Button(frame_buttons, width=20, height=1, text="Exporter")
        button_export.config(font=("Calibri", 10))
        button_export.grid(row=0, column=1,  sticky="nw", padx=(10, 0))



    def create_table(self, p_nb_column, p_width_column, p_list_col):

        headers_width = p_width_column
        self.buttons_header = [tk.Button() for j in range(p_nb_column)]
        current_col0 = -1
        for j in p_list_col:
            current_col0 += 1
            self.buttons_header[current_col0] = tk.Button(self.frame_headers, width=headers_width, text=list(df)[j-1],
                                          font=("Consolas bold", 10))
            self.buttons_header[current_col0].config(bg="green", fg="white")
            self.buttons_header[current_col0].grid(row=0, column=current_col0)
            self.buttons_header[current_col0].config(borderwidth=2, relief="ridge")

        button_width = p_width_column
        self.buttons_table = [[tk.Button() for j in range(p_nb_column)] for i in range(nb_row_df)]
        current_col = -1
        for j in p_list_col:
            current_col += 1
            for i in range(0, nb_row_df):
                self.buttons_table[i][current_col] = tk.Button(self.frame_buttons, width=button_width, text=(df.iloc[i][j-1]))
                self.buttons_table[i][current_col].config(bg="white")
                self.buttons_table[i][current_col]['command'] = partial(self.color_line, i, p_nb_column)
                self.buttons_table[i][current_col].grid(row=i, column=current_col)
                self.buttons_table[i][current_col].config(borderwidth=2, relief="groove")

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.frame_buttons.update_idletasks()

        # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        first5columns_width = sum([self.buttons_table[0][j].winfo_width() for j in range(0, p_nb_column)])
        first5rows_height = sum([self.buttons_table[i][0].winfo_height() for i in range(0, 11)])
        self.frame_canvas.config(width=first5columns_width + self.vsb.winfo_width(),
                            height=first5rows_height)

        # Set the canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def color_line(self, p_row, p_nb_column):
        """
        Function that colors a line
        :param p_row: A line of the table
        :return: None
        """
        for i in range(0, nb_row_df):
            for j in range(0, p_nb_column):
                if i == p_row:
                    self.buttons_table[i][j].config(bg="beige")
                else:
                    self.buttons_table[i][j].config(bg="white")

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
        window_settings_height = 260
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
        label_login_title = tk.Label(window_settings, text="Choix des colonnes")
        label_login_title.grid(row=1, sticky='nw', padx=10, pady=(0, 10))
        label_login_title.config(font=("Calibri bold", 12))

        # Column choice label

        labels_column_choice = [tk.Label() for j in range(nb_column_max)]
        combo_column_choice = [ttk.Combobox() for j in range(nb_column_max)]
        list_headers = list(df.head())
        list_headers.insert(0, " ")
        for j in range(nb_column_max):
            label_text = "Column " + str(j + 1)
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
        button_validate.grid(row=nb_column_max + 2, column=1, sticky="ne", padx=10, pady=(10, 0))
        button_validate['command'] = partial(self.change_column, combo_column_choice)

    def change_column(self, p_combo):
        list_columns = []                   # List of column number non empty
        for j in range(nb_column_max):
            col = p_combo[j].current()
            if (col != 0) and (col not in list_columns):
                list_columns.append(col)

        # offset
        for x in list_columns:
            x -= 1

        list_columns.sort()

        number_col = len(list_columns)
        width_col = list_width[number_col-1]
        if number_col != 0:
            self.delete_buttons()
            self.create_table(number_col, width_col, list_columns)

    def delete_buttons(self):

        for widget in self.frame_headers.winfo_children():
            widget.destroy()

        for widget in self.frame_buttons.winfo_children():
            widget.destroy()

