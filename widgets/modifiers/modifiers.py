import tkinter as tk
import json
import pandas as pd
from csv import writer
from functools import partial

# Open the settings file
with open('settings.json') as json_file:
    settings = json.load(json_file)

# Open the data file
with open('widgets/filters/filters_data.json') as json_file:
    filters_data = json.load(json_file)

filename = 'csv/csv_test.csv'


class Modifiers:
    """ Widget where the user can modify a table """

    def __init__(self, p_parent, p_widget_group, p_row):
        """
        Initialization of the modifier widget that shows some label and data

        :param p_parent: Page that will contain this modifier widget
        :param p_row: Row of the page where the widget will be placed
        :param p_widget_group: Group containing this widget
        """
        # Open the csv file
        self.df = pd.read_csv(filename)
        self.nb_row_df = self.df.shape[1]

        # Saving the parameters to use them in each function
        self.parent = p_parent
        self.row = p_row
        self.widget_group = p_widget_group

        # Add this widget to p_parent widgets
        self.widget_group.widgets.append(self)
        self.type = "Modifiers"

        # Properties of the widget-
        frame_height = 200
        frame_width = 780
        self.frame = tk.Frame(p_parent.frame, bg="white", width=frame_width, height=frame_height, highlightthickness=1)
        self.frame.grid_propagate(False)
        self.frame.config(highlightbackground="grey")
        self.frame.grid(row=self.row, column=0, pady=(5, 5))
        self.frame.update_idletasks()  # to display good dimensions with .winfo_width()
        self.frame.columnconfigure((0, 1, 2, 3), weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure((1, 2), weight=4)

        # Title of the page
        title = tk.Label(self.frame, text="Modificateurs", bg="#333333", fg="white", compound="c", borderwidth=1, relief="raised")
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
                self.buttons[i][j] = tk.Button(self.frame, width=self.button_width, height=self.button_height, text=" ")
                self.buttons[i][j].grid(row=i+1, column=j, padx=(10, 10), pady=(10, 10))
                self.buttons[i][j].config(font=("Calibri bold", 10))

        self.buttons[0][0].config(text="Ajouter un \n utilisateur")
        self.buttons[0][0]['command'] = self.add_line_window
        self.buttons[0][1].config(text="Supprimer un \n utilisateur")
        self.buttons[0][1]['command'] = self.delete_line
        self.buttons[0][2].config(text="Modifier")
        self.buttons[0][2]['command'] = self.modify_line

    def add_line(self, p_list_elt):

        # self.add_line_window()

        # list_elt = ["Koulibaly", "Ali", "25", "41", "casque", "Grenoble"]
        list_elt = []
        for elt in p_list_elt:
            if len(elt.get()) == 0:
                list_elt.append("None")
            else:
                list_elt.append(elt.get())

        # Add the list_elt to the csv file
        with open(filename, 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow(list_elt)

        # Update the dataframe
        self.df = pd.read_csv(filename)

        # Update widgets of the same group
        self.widget_group.update_widgets()

    def add_line_window(self):
        """
        Functions called when the user clicks on details button
        """
        # Window handle
        window_settings = tk.Toplevel(self.frame)
        window_settings.resizable(False, False)
        window_settings.title("Ajouter une donnée")
        window_icon = tk.PhotoImage(file="img/add.png")
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
        label_login_title = tk.Label(window_settings, text="Ajouter une donnée", bg=bg_identification, fg="white")
        label_login_title.grid(row=0, columnspan=2, sticky='new', pady=(0, 10))
        font_login_title = settings['font']['font_login_title']
        font_size_login_title = settings['font_size']['font_size_login_title']
        label_login_title.config(font=(font_login_title, font_size_login_title))

        # Title - choice of the columns
        label_login_title = tk.Label(window_settings, text="Entrée les données")
        label_login_title.grid(row=1, sticky='nw', padx=10, pady=(0, 10))
        label_login_title.config(font=("Calibri bold", 12))

        # Column choice label
        labels_column_choice = [tk.Label() for j in range(self.nb_row_df)]
        entry_column_choice = [tk.Entry() for j in range(self.nb_row_df)]
        var_username = [tk.StringVar(value='') for j in range(self.nb_row_df)]
        list_headers = list(self.df.head())
        list_headers.insert(0, " ")
        for j in range(self.nb_row_df):
            label_text = list_headers[j+1]
            labels_column_choice[j] = tk.Label(window_settings, text=label_text)
            labels_column_choice[j].grid(row=j + 2, column=0, sticky='ne', padx=30, pady=1)
            labels_column_choice[j].config(font=("Calibri bold", 10))
            entry_column_choice[j] = tk.Entry(window_settings, bg="white", width=30, textvariable=var_username[j])
            entry_column_choice[j].grid(row=j + 2, column=1, sticky='nw', padx=10, pady=1)
            entry_column_choice[j].config(font=("Calibri bold", 10))

        # Button - Validation
        button_validate = tk.Button(window_settings, width=30, height=1, text="Appliquer")
        button_validate.config(font=("Calibri", 10))
        button_validate.grid(row=self.nb_row_df + 2, column=1, sticky="ne", padx=10, pady=(10, 0))
        button_validate['command'] = partial(self.add_line, var_username)


    def delete_line(self):

        # Find the table in the same page
        row = -1
        for w in self.widget_group.widgets:
            if w.type == "Table":
                row = w.selected_row

        if row != -1:
            self.df.drop(self.df.index[row], inplace=True)
            self.df.to_csv(filename, index=False)
            self.df = pd.read_csv(filename)

        # Update widgets of the same group
        self.widget_group.update_widgets()

    def modify_line(self):
        print("Modify line")

    def update(self):
        print("Update Modifiers")
