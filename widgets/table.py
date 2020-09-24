import tkinter as tk
import pandas as pd
from functools import partial

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

        button_export = tk.Button(frame_buttons, width=20, height=1, text="Exporter")
        button_export.config(font=("Calibri", 10))
        button_export.grid(row=4, column=1,  sticky="nw", padx=(10,0), pady=5)

        frame_headers = tk.Frame(frame, bg="white")
        frame_headers.grid(row=2, padx=40)
        frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)


        headers_width = 15
        headers_buttons = [tk.Button() for j in range(nb_column)]
        for j in range(0, nb_column):
            headers_buttons[j] = tk.Button(frame_headers, width=headers_width, text=list(df)[j],
                                           font=("Consolas bold", 10))
            headers_buttons[j].config(bg="green", fg="white")
            headers_buttons[j].grid(row=0, column=j)
            headers_buttons[j].config(borderwidth=2, relief="ridge")

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