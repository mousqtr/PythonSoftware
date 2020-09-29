import tkinter as tk
import json
import pandas as pd
from csv import writer

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
        frame = tk.Frame(p_parent.frame, bg="white", width=frame_width, height=frame_height, highlightthickness=1)
        frame.grid_propagate(False)
        frame.config(highlightbackground="grey")
        frame.grid(row=self.row, column=0, pady=(5, 5))
        frame.update_idletasks()  # to display good dimensions with .winfo_width()
        frame.columnconfigure((0, 1, 2, 3), weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure((1, 2), weight=4)

        # Title of the page
        title = tk.Label(frame, text="Modificateurs", bg="#333333", fg="white", compound="c", borderwidth=1, relief="raised")
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
                self.buttons[i][j] = tk.Button(frame, width=self.button_width, height=self.button_height, text=" ")
                self.buttons[i][j].grid(row=i+1, column=j, padx=(10, 10), pady=(10, 10))
                self.buttons[i][j].config(font=("Calibri bold", 10))

        self.buttons[0][0].config(text="Ajouter un \n utilisateur")
        self.buttons[0][0]['command'] = self.add_line
        self.buttons[0][1].config(text="Supprimer un \n utilisateur")
        self.buttons[0][1]['command'] = self.delete_line
        self.buttons[0][2].config(text="Modifier")
        self.buttons[0][2]['command'] = self.modify_line

    def add_line(self):
        list_elt = ["Koulibaly", "Ali", "25", "41", "casque", "Grenoble"]
        with open(filename, 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow(list_elt)

        self.df = pd.read_csv(filename)

        self.widget_group.update_widgets()

        print(self.df)

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

        self.widget_group.update_widgets()

    def modify_line(self):
        print("Modify line")

    def update(self):
        print("Update Modifiers")
