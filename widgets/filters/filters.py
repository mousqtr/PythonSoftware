import tkinter as tk
import json
from functools import partial
from tkinter import ttk
import pandas as pd
import warnings

# Ignore the FutureWarning message
warnings.simplefilter(action='ignore', category=FutureWarning)

# Open the settings file
with open('settings.json') as json_file:
    settings = json.load(json_file)

# Open the filters data file
with open('widgets/filters/filters_data.json') as json_file:
    filters_data = json.load(json_file)

# Open the table data file
with open('widgets/table/table_data.json') as json_file:
    table_data = json.load(json_file)

# Open the csv file
df = pd.read_csv('csv/csv_test.csv')
nb_row_df = df.shape[0]

class Filters:
    """ Widget where the user use and custom filters """

    def __init__(self, p_parent, p_widget_group, p_row):
        """
        Initialization of the summary widget that shows some label and data

        :param p_parent: Page that will contain this summary widget
        :param p_row: Row of the page where the widget will be placed
        :param p_widget_group: Group containing this widget
        """

        # Saving the parameters to use them in each function
        self.parent = p_parent
        self.row = p_row
        self.widget_group = p_widget_group

        # Add this widget to p_parent widgets
        self.widget_group.widgets.append(self)
        self.type = "Filters"

        # Rows to draw after research
        self.row_to_draw = [i for i in range(0, nb_row_df)]

        # Properties of the widget
        frame_height = 200
        frame_width = 780
        self.frame = tk.Frame(self.parent.frame, bg="white", width=frame_width, height=frame_height, highlightthickness=1)
        self.frame.grid_propagate(False)
        self.frame.config(highlightbackground="grey")
        self.frame.grid(row=self.row, column=0, pady=(5, 5))
        self.frame.update_idletasks()  # to display good dimensions with .winfo_width()
        self.frame.columnconfigure((0, 1, 2, 3), weight=1)

        # Title of the page
        self.title = tk.Label(self.frame,text="Filtres", bg="#333333",fg="white", compound="c", borderwidth=1, relief="raised")
        self.title.grid(row=0, column=0, columnspan=4, sticky="nwe", ipadx=10, ipady=1, pady=(0, 0))
        self.title.config(font=("Calibri bold", 12))

        # Construction of the filters
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

        # Load the saving filters
        self.load()

        # Buttons under the filters
        frame_buttons = tk.Frame(self.frame, height=30, bg="white")
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
        button_validate['command'] = self.research

    def research(self):
        """
        Functions called when the user clicks on research button
        """

        # Transform the dataframe in string and lowercase
        str_df_lowercase = df.applymap(lambda s:s.lower() if type(s) == str else s)
        str_df = str_df_lowercase.applymap(str)

        # Rows list that contains research results
        rows_found = []
        rows_found_numbers = []
        row_research = []
        self.row_to_draw = []

        # Find all possibilities
        index = 0
        for i in range(0, 2):
            for j in range(0, 4):
                column_name = self.labels_settings[i][j]['text']
                text_entry = self.entry_settings[i][j].get()
                text_entry_lowercase = text_entry.lower()

                if (column_name != " ") and (text_entry_lowercase != " ") and (text_entry_lowercase != ""):
                    for elt in str_df[column_name].tolist():
                        if text_entry_lowercase in elt:
                            row_research.append(index)
                        index += 1

                    if row_research != []:
                        rows_found.append(row_research)

        # Creation of a possibility list
        for list_row in rows_found:
            for number in list_row:
                rows_found_numbers.append(number)

        # Correlation of each possibility list (we keep only the numbers present in all list)
        presence = 0
        for number in rows_found_numbers:
            for list_row in rows_found:
                if number in list_row:
                    presence += 1
            if presence == len(rows_found):
                self.row_to_draw.append(number)
            presence = 0

        # Transform the research list into a list with unique values
        self.row_to_draw = list(set(self.row_to_draw))

        # Case of an empty list
        if self.row_to_draw == []:
            self.row_to_draw = [i for i in range(0, nb_row_df)]

        # # Update the content of the table
        # num_id = self.widget_group.id
        # key = "row_to_draw_" + num_id
        # value_data = {key: self.row_to_draw}
        # table_data['rows_to_draw'].update(value_data)
        # with open('widgets/table/table_data.json', 'w') as outfile:
        #     json.dump(table_data, outfile, indent=4)

        # Updating
        self.widget_group.update_widgets()



    def settings_window(self):
        """
        Functions called when the user clicks on settings button
        """

        # Window handle
        window_settings = tk.Toplevel(self.frame)
        window_settings.resizable(False, False)
        window_settings.title("Paramètres")
        window_icon = tk.PhotoImage(file="img/settings.png")
        window_settings.iconphoto(False, window_icon)
        # login_window_width = settings['dimensions']['window_login_width']
        # login_window_height = settings['dimensions']['window_login_height']
        window_settings_width = 700
        window_settings_height = 270
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
        frames = [tk.Frame() for j in range(0, 2)]
        frames[0] = tk.Frame(window_settings, height=100, width=window_settings_width/2)
        frames[0].grid(row=2, column=0, sticky="n")
        frames[0].grid_propagate(False)
        frames[1] = tk.Frame(window_settings, height=100, width=window_settings_width/2)
        frames[1].grid(row=2, column=1, sticky="n")
        frames[1].grid_propagate(False)
        labels_column_choice = [[tk.Label() for j in range(0, self.nb_column)] for i in range(0, self.nb_row)]
        combo_column_choice = [[ttk.Combobox() for j in range(0, self.nb_column)] for i in range(0, self.nb_row)]
        list_headers = list(df.head())
        list_headers.insert(0, " ")
        num_filter = 1
        for i in range(0, 2):
            for j in range(0, 4):
                label_text = "Filtre " + str(num_filter)
                labels_column_choice[i][j] = tk.Label(frames[i], text=label_text)
                labels_column_choice[i][j].grid(row=j, column=0, sticky='nw', padx=(70, 0), pady=1)
                labels_column_choice[i][j].config(font=("Calibri bold", 10))
                combo_column_choice[i][j] = ttk.Combobox(frames[i], values=list_headers, state="readonly")
                combo_column_choice[i][j].grid(row=j, column=1, sticky='nw', padx=(5, 0), pady=1)
                combo_column_choice[i][j].config(font=("Calibri bold", 10))
                combo_column_choice[i][j].current(0)
                num_filter += 1

        # Button - Validation
        button_validate = tk.Button(window_settings, width=30, height=1, text="Appliquer")
        button_validate.config(font=("Calibri", 10))
        button_validate.grid(row=6, column=0, columnspan=2, sticky="nw", padx=(250,0), pady=(30, 0))
        button_validate['command'] = partial(self.change_filters, combo_column_choice)

    def change_filters(self, p_combo):
        """
        Functions called when the user clicks on validate button

        :param p_combo: Combobox that contains filter choices
        """
        for i in range(0, 2):
            for j in range(0, 4):
                text = p_combo[i][j].get()
                self.labels_settings[i][j]['text'] = text
                self.save(i, j, text)

    def save(self, p_row, p_column, p_data):
        """
        Functions that saves the filters properties

        :param p_row: Row of the filter
        :param p_column: Column of the filter
        :param p_data: Name of the data
        """
        # Build the texts that will be add to the saving file
        key = str(p_row) + ',' + str(p_column)
        value_data = {key: p_data}

        # Update the saving file (.json) with these data
        filters_data['filters_label'].update(value_data)
        with open('widgets/filters/filters_data.json', 'w') as outfile:
            json.dump(filters_data, outfile, indent=4)

    def load(self):
        """
        Function that loads the content of each filter
        """

        # Get all the data contain in the "filters_label" of the saving file
        for x in filters_data['filters_label']:
            coord = x.split(',')
            row = int(coord[0])
            column = int(coord[1])
            text = filters_data['filters_label'][x]
            self.labels_settings[row][column]['text'] = text

    def update(self):
        print("Update Filters")