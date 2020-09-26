import tkinter as tk
import json
from functools import partial
from tkinter import ttk

# Open the settings file
with open('settings.json') as json_file:
    settings = json.load(json_file)

# Open the data file
with open('widgets/summary/summary_data.json') as json_file:
    widgets_data = json.load(json_file)


class Summary:
    """ Widget that shows some label and data """

    def __init__(self, p_parent, p_row, p_id):
        """
        Initialization of the summary widget that shows some label and data

        :param p_parent: Page that will contain this summary widget
        :param p_row: Row of the page where the widget will be placed
        :param p_id: Identifier of the widget (each widget is unique)
        """

        # Saving the parameters to use them in each function
        self.parent = p_parent
        self.row = p_row
        self.id = p_id

        # Properties of the widget-
        frame_height = 200
        frame_width = 780
        frame = tk.Frame(p_parent.frame, bg="white", width=frame_width, height=frame_height, highlightthickness=1)
        frame.grid_propagate(False)
        frame.config(highlightbackground="grey")
        frame.grid(row=self.row, column=0, pady=(5, 5))
        frame.update_idletasks()  # to display good dimensions with .winfo_width()
        frame.columnconfigure((0, 1, 2, 3), weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure((1, 2), weight=4)

        # Title of the page
        title = tk.Label(frame,text="Summary", bg="#333333", fg="white", compound="c", borderwidth=1, relief="raised")
        title.grid(row=0, column=0, columnspan=5, sticky="nwe", ipadx=10, ipady=5)
        title.config(font=("Calibri bold", 12))

        # Creation of the buttons that display data
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
                self.buttons[i][j]['command'] = partial(self.choose_data, i, j)

        # Loading and changing the content of the buttons
        self.load()

    def choose_data(self, p_i, p_j):
        """
        Function that opens a window where the user can choose which data will be displayed

        :param p_i: Row of the button
        :param p_j: Column of the button
        """

        # Window handle
        login_window = tk.Toplevel(self.parent.frame)
        login_window.resizable(False, False)
        # login_window_width = settings['dimensions']['window_login_width']
        # login_window_height = settings['dimensions']['window_login_height']
        login_window_width = 500
        login_window_height = 220
        screen_width = self.parent.frame.winfo_screenwidth()
        screen_height = self.parent.frame.winfo_screenheight()
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
        list_color = [" ", "red", "orange", "blue", "green", "white"]
        combo_color = ttk.Combobox(login_window, values=list_color)
        combo_color.current(0)
        combo_color.grid(row=2, column=1)

        # Button - Validation
        button_validate = tk.Button(login_window, text="Valider", width=30)
        button_validate.grid(row=3, columnspan=2, pady=(30, 0))
        button_validate['command'] = partial(self.change_button, p_i, p_j, combo_data, combo_color)

    def change_button(self, p_row, p_column, p_combo_data, p_combo_color):
        """
        Function that update the button in (p_row,p_column) with the content p_combo and p_combo_color

        :param p_row: Row of the button
        :param p_column: Column of the button
        :param p_combo_data: Name of the data
        :param p_combo_color: Data that will be displayed
        """

        # Get the content of comboboxes
        data = p_combo_data.get()
        color = p_combo_color.get()
        if data == ' ':
            data_text = data
            color = "SystemButtonFace"
        else:
            data_text = data + '\n' + str(widgets_data['data'][data])

        # Replace the buttons text with the comboboxes content
        self.buttons[p_row][p_column]['text'] = data_text
        self.buttons[p_row][p_column]['bg'] = color

        # Save the data
        self.save(p_row, p_column, data, color)

    def save(self, p_row, p_column, p_data, p_color):
        """
        Function that saves the content of each button

        :param p_row: Row of the button
        :param p_column: Column of the button
        :param p_data: Name of the data
        :param p_color: Color of the data
        """

        # Build the texts that will be add to the saving file
        key = str(p_row) + ',' + str(p_column)
        value_data = {key: p_data}
        value_color = {key: p_color}

        # Update the saving file (.json) with these data
        widgets_data['summary_data'].update(value_data)
        widgets_data['summary_color'].update(value_color)
        with open('widgets/summary/summary_data.json', 'w') as outfile:
            json.dump(widgets_data, outfile, indent=4)

    def load(self):
        """
        Function that loads the content of each button
        """

        # Get all the data contain in the "summary section" of the saving file
        for x in widgets_data['summary_data']:
            coord = x.split(',')
            row = int(coord[0])
            column = int(coord[1])
            data = widgets_data['summary_data'][x]
            color = widgets_data['summary_color'][x]
            if data == ' ':
                data_text = data
            else:
                data_text = data + '\n' + str(widgets_data['data'][data])
            self.buttons[row][column]['text'] = data_text
            self.buttons[row][column]['bg'] = color



