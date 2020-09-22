import tkinter as tk
import json
from functools import partial
from tkinter import ttk

with open('settings.json') as json_file:
    settings = json.load(json_file)

with open('widgets_data.json') as json_file:
    widgets_data = json.load(json_file)

# def save_summary(p_row, p_column, p_data, p_color):

def load_summary(p_buttons):
    for x in widgets_data['summary_data']:
        coord = x.split(',')
        row = int(coord[0])
        column = int(coord[1])
        data = widgets_data['summary_data'][x]
        color = widgets_data['summary_color'][x]
        data_text = data + '\n' + str(widgets_data['data'][data])
        p_buttons[row][column]['text'] = data_text
        p_buttons[row][column]['bg'] = color


def change_button(p_row, p_column, p_summary, p_combo_data, p_combo_color):
    data = p_combo_data.get()
    color = p_combo_color.get()
    data_text = data + '\n' + str(widgets_data['data'][data])
    p_summary.buttons[p_row][p_column]['text'] = data_text
    p_summary.buttons[p_row][p_column]['bg'] = color
    print(widgets_data['data'][data])


def choose_data(p_parent, p_row, p_column, p_summary):
    # Window handle
    login_window = tk.Toplevel(p_parent.frame)
    login_window.resizable(False, False)
    # login_window_width = settings['dimensions']['window_login_width']
    # login_window_height = settings['dimensions']['window_login_height']
    login_window_width = 500
    login_window_height = 220
    screen_width = p_parent.frame.winfo_screenwidth()
    screen_height = p_parent.frame.winfo_screenheight()
    x_cord = int((screen_width / 2) - (login_window_width / 2))
    y_cord = int((screen_height / 2) - (login_window_height / 2))
    login_window.geometry("{}x{}+{}+{}".format(login_window_width, login_window_height, x_cord, y_cord))
    login_window.columnconfigure((0, 1), weight=1)

    # Title of the login window
    bg_identification = settings['colors']['bg_identification']
    label_login_title = tk.Label(login_window, text="Ajouter une donnée", bg=bg_identification, fg="white")
    label_login_title.grid(row=0, columnspan=2, sticky='new', pady=(0, 0))
    font_login_title = settings['font']['font_login_title']
    font_size_login_title = settings['font_size']['font_size_login_title']
    label_login_title.config(font=(font_login_title, font_size_login_title))

    # Label - Choose data to draw
    label_data = tk.Label(login_window, text="Choisir la donnée \n à afficher")
    label_data.grid(row=1, column=0, pady=20, sticky='n')
    font_add_label_data = settings['font']['font_login_username']
    font_size_add_label_data = settings['font_size']['font_size_login_username']
    label_data.config(font=(font_add_label_data, font_size_add_label_data))

    # Combobox - Choose data to draw
    list_data = []
    for x in widgets_data['data']:
        list_data.append(x)
    # list_data = ["Laptop", "Imprimante", "Tablette", "SmartPhone"]
    combo_data = ttk.Combobox(login_window, values=list_data)
    combo_data.current(0)
    combo_data.grid(row=2, column=0)

    # Label - Choose color
    label_color = tk.Label(login_window, text="Choisir la couleur \n associée")
    label_color.grid(row=1, column=1, pady=20, sticky='n')
    font_add_label_color = settings['font']['font_login_password']
    font_size_add_label_color = settings['font_size']['font_size_login_password']
    label_color.config(font=(font_add_label_color, font_size_add_label_color))

    # Combobox - Choose data to draw
    list_color = ["red", "orange", "blue", "green"]
    combo_color = ttk.Combobox(login_window, values=list_color)
    combo_color.current(0)
    combo_color.grid(row=2, column=1)

    button_validate = tk.Button(login_window, text="Valider", width=30)
    button_validate.grid(row=3, columnspan=2, pady=(30, 0))
    button_validate['command'] = partial(change_button, p_row, p_column, p_summary, combo_data, combo_color)






class Summary:
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

        self.title = tk.Label(frame,text="Summary", bg="#333333",fg="white", compound="c", borderwidth=1, relief="raised")
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
                self.buttons[i][j]['command'] = partial(choose_data, p_parent, i, j, self)

        load_summary(self.buttons)