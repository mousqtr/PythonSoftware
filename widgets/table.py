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
nb_row = df.shape[0]
nb_column = df.shape[1]

def color_line(p_table, p_row):
    """
    Function that colors a line
    :param line: A line of the table
    :return: None
    """
    for i in range(0, nb_row):
        for j in range(0, nb_column):
            if i == p_row:
                p_table.buttons[i][j].config(bg="beige")
            else:
                p_table.buttons[i][j].config(bg="white")

def settings_window(p_parent):
    # Window handle
    window_settings = tk.Toplevel(p_parent)
    window_settings.resizable(False, False)
    window_settings.title("Paramètres")
    window_icon = tk.PhotoImage(file="img/settings.png")
    window_settings.iconphoto(False, window_icon)
    # login_window_width = settings['dimensions']['window_login_width']
    # login_window_height = settings['dimensions']['window_login_height']
    window_settings_width = 550
    window_settings_height = 260
    screen_width = p_parent.winfo_screenwidth()
    screen_height = p_parent.winfo_screenheight()
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
    nb_column_max = 6
    labels_column_choice = [tk.Label() for j in range(nb_column)]
    combo_column_choice= [ttk.Combobox() for j in range(nb_column)]
    list_headers = list(df.head())
    list_headers.insert(0, " ")
    for j in range(nb_column_max):
        label_text = "Column " + str(j+1)
        labels_column_choice[j] = tk.Label(window_settings, text=label_text)
        labels_column_choice[j].grid(row=j+2, column=0, sticky='ne', padx=30, pady=1)
        labels_column_choice[j].config(font=("Calibri bold", 10))
        combo_column_choice[j] = ttk.Combobox(window_settings, values=list_headers)
        combo_column_choice[j].grid(row=j+2, column=1, sticky='nw', padx=10, pady=1)
        combo_column_choice[j].config(font=("Calibri bold", 10))
        combo_column_choice[j].current(0)

    # Button - Validation
    button_validate = tk.Button(window_settings, width=30, height=1, text="Appliquer")
    button_validate.config(font=("Calibri", 10))
    button_validate.grid(row=nb_column_max+2, column=1, sticky="ne", padx=10, pady=(10,0))





class Table:
    def __init__(self, p_parent, p_row):
        frame_height = 400
        frame_width = 780
        frame = tk.Frame(p_parent.frame, bg="white", width=frame_width, height=frame_height, highlightthickness=1)
        frame.grid_propagate(False)
        frame.config(highlightbackground="grey")
        frame.grid(row=p_row, column=0, pady=(5, 5))

        self.title = tk.Label(frame, text="Table", bg="#333333",fg="white", compound="c", borderwidth=1, relief="raised", height=1)
        self.title.grid(row=0, column=0, columnspan=6, sticky="nwe", ipadx=10, ipady=1)
        self.title.config(font=("Calibri bold", 12))

        frame_buttons = tk.Frame(frame, height=40)
        frame_buttons.grid(row=1, column=0, columnspan=6, sticky="nwe")
        frame_buttons.grid_propagate(False)

        button_settings = tk.Button(frame_buttons, width=20, height=1, text="Paramètres")
        button_settings.config(font=("Calibri", 10))
        button_settings.grid(row=4, column=0, sticky="nw", padx=(40,0), pady=5)
        button_settings['command'] = partial(settings_window, frame)

        button_export = tk.Button(frame_buttons, width=20, height=1, text="Exporter")
        button_export.config(font=("Calibri", 10))
        button_export.grid(row=4, column=1,  sticky="nw", padx=(10,0), pady=5)

        frame_headers = tk.Frame(frame, bg="white")
        frame_headers.grid(row=2, padx=40)
        frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        headers_width = 15
        buttons_header = [tk.Button() for j in range(nb_column)]
        for j in range(0, nb_column):
            buttons_header[j] = tk.Button(frame_headers, width=headers_width, text=list(df)[j],
                                           font=("Consolas bold", 10))
            buttons_header[j].config(bg="green", fg="white")
            buttons_header[j].grid(row=0, column=j)
            buttons_header[j].config(borderwidth=2, relief="ridge")

        # Create a frame for the canvas with non-zero row&column weights
        frame_canvas = tk.Frame(frame)
        frame_canvas.grid(row=3, column=0, padx=(40, 0), pady=(0, 0), sticky='nw')
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)

        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        frame_canvas.grid_propagate(False)



        # Add a canvas in that frame
        canvas = tk.Canvas(frame_canvas, bg="grey")
        canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)

        # Create a frame to contain the buttons
        frame_buttons = tk.Frame(canvas, bg="grey")
        canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

        self.buttons = [[tk.Button() for j in range(nb_column)] for i in range(nb_row)]

        button_width = 15
        for i in range(0, nb_row):
            for j in range(0, nb_column):
                self.buttons[i][j] = tk.Button(frame_buttons, width=button_width, text=(df.iloc[i][j]))
                self.buttons[i][j].config(bg="white")
                self.buttons[i][j]['command'] = partial(color_line, self, i)
                self.buttons[i][j].grid(row=i, column=j)
                self.buttons[i][j].config(borderwidth=2, relief="groove")

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        frame_buttons.update_idletasks()

        # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        first5columns_width = sum([self.buttons[0][j].winfo_width() for j in range(0, nb_column)])
        first5rows_height = sum([self.buttons[i][0].winfo_height() for i in range(0, 11)])
        frame_canvas.config(width=first5columns_width + vsb.winfo_width(),
                            height=first5rows_height)

        # Set the canvas scrolling region
        canvas.config(scrollregion=canvas.bbox("all"))
